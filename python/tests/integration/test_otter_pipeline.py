"""Integration test for complete otter model pipeline with webhook simulation

This test uses webhook simulation instead of polling:
1. Create task via API (VCR recorded)
2. Register task in repository
3. Simulate webhook callback with success payload
4. Verify state updated correctly

NO time.sleep() or polling loops - tests run quickly!
"""
import pytest
import json
from pathlib import Path
from mesh_toolkit.api.base_client import BaseHttpClient
from mesh_toolkit.services.text3d_service import Text3DService
from mesh_toolkit.services.rigging_service import RiggingService
from mesh_toolkit.services.animation_service import AnimationService
from mesh_toolkit.services.retexture_service import RetextureService
from mesh_toolkit.models import TaskStatus
from mesh_toolkit.persistence.schemas import AssetManifest, TaskGraphEntry
from mesh_toolkit.webhooks.handler import WebhookHandler
from mesh_toolkit.webhooks.schemas import MeshyWebhookPayload
from datetime import datetime


class TestOtterPipeline:
    """Test complete otter model generation pipeline using webhook simulation"""
    
    def test_1_text_to_3d_with_webhook(
        self,
        meshy_api_key,
        test_repository,
        webhook_payload_loader,
        glb_fixtures_dir
    ):
        """Create sculptured otter model via text-to-3D with webhook simulation"""
        client = BaseHttpClient(api_key=meshy_api_key)
        service = Text3DService(client)
        
        # Step 1: Create task (this will be VCR recorded if needed)
        # For testing, we'll use a mock task ID that matches our fixture
        task_id = "018a210d-8ba4-705c-b111-1f1776f7f578"
        species = "otter"
        spec_hash = "test_spec_hash_001"
        
        # Step 2: Register task in repository
        asset_manifest = AssetManifest(
            asset_spec_hash=spec_hash,
            spec_fingerprint="{}",
            species=species,
            asset_intent="creature",
            prompts={"text3d": "realistic river otter standing upright"},
            task_graph=[
                TaskGraphEntry(
                    task_id=task_id,
                    service="text3d",
                    status="PENDING",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    payload={
                        "prompt": "realistic river otter standing upright",
                        "art_style": "sculpture"
                    }
                )
            ]
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        # Step 3: Load webhook payload fixture
        webhook_payload = webhook_payload_loader("text3d_success.json")
        
        # Override the task ID to match our registered task
        webhook_payload.id = task_id
        
        # Step 4: Simulate webhook callback
        webhook_handler = WebhookHandler(
            repository=test_repository,
            client=client,
            download_artifacts=False  # Skip actual download for test
        )
        
        result = webhook_handler.handle_webhook(webhook_payload, species=species)
        
        # Step 5: Verify webhook was processed
        assert result["status"] == "success"
        assert result["task_id"] == task_id
        assert result["task_status"] == "SUCCEEDED"
        
        # Step 6: Verify repository state was updated
        updated_manifest = test_repository.get_asset_record(species, spec_hash)
        assert updated_manifest is not None
        
        # Find the task in the task graph
        task_entry = None
        for entry in updated_manifest.task_graph:
            if entry.task_id == task_id:
                task_entry = entry
                break
        
        assert task_entry is not None
        assert task_entry.status == "SUCCEEDED"
        assert "glb" in task_entry.result_paths
        
        print(f"\n✓ Text-to-3D webhook processed successfully")
        print(f"  Task ID: {task_id}")
        print(f"  Status: {task_entry.status}")
        print(f"  GLB URL: {task_entry.result_paths.get('glb')}")
    
    def test_2_rigging_with_webhook(
        self,
        meshy_api_key,
        test_repository,
        webhook_payload_loader
    ):
        """Auto-rig the otter model using webhook simulation"""
        client = BaseHttpClient(api_key=meshy_api_key)
        
        # Setup: Create asset with text3d task already completed
        task_id = "018b314a-a1b5-716d-c222-2f1776f7f579"
        species = "otter"
        spec_hash = "test_spec_hash_002"
        
        asset_manifest = AssetManifest(
            asset_spec_hash=spec_hash,
            spec_fingerprint="{}",
            species=species,
            asset_intent="creature",
            prompts={"rigging": "Auto-rig otter model"},
            task_graph=[
                TaskGraphEntry(
                    task_id=task_id,
                    service="rigging",
                    status="PENDING",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    payload={"model_id": "018a210d-8ba4-705c-b111-1f1776f7f578"}
                )
            ]
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        # Load and process webhook
        webhook_payload = webhook_payload_loader("rigging_success.json")
        webhook_payload.id = task_id
        
        webhook_handler = WebhookHandler(
            repository=test_repository,
            client=client,
            download_artifacts=False
        )
        
        result = webhook_handler.handle_webhook(webhook_payload, species=species)
        
        # Verify
        assert result["status"] == "success"
        assert result["task_status"] == "SUCCEEDED"
        
        updated_manifest = test_repository.get_asset_record(species, spec_hash)
        task_entry = next((e for e in updated_manifest.task_graph if e.task_id == task_id), None)
        
        assert task_entry is not None
        assert task_entry.status == "SUCCEEDED"
        assert "glb" in task_entry.result_paths
        
        print(f"\n✓ Rigging webhook processed successfully")
        print(f"  Task ID: {task_id}")
        print(f"  Status: {task_entry.status}")
    
    def test_3_animation_with_webhook(
        self,
        meshy_api_key,
        test_repository,
        webhook_payload_loader
    ):
        """Apply Attack animation using webhook simulation"""
        client = BaseHttpClient(api_key=meshy_api_key)
        
        task_id = "018c425b-b2c6-827e-d333-3f1776f7f580"
        species = "otter"
        spec_hash = "test_spec_hash_003"
        
        asset_manifest = AssetManifest(
            asset_spec_hash=spec_hash,
            spec_fingerprint="{}",
            species=species,
            asset_intent="creature",
            prompts={"animation": "Attack animation"},
            task_graph=[
                TaskGraphEntry(
                    task_id=task_id,
                    service="animation",
                    status="PENDING",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    payload={
                        "model_id": "018b314a-a1b5-716d-c222-2f1776f7f579",
                        "animation_id": "4"
                    }
                )
            ]
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        # Load and process webhook
        webhook_payload = webhook_payload_loader("animation_success.json")
        webhook_payload.id = task_id
        
        webhook_handler = WebhookHandler(
            repository=test_repository,
            client=client,
            download_artifacts=False
        )
        
        result = webhook_handler.handle_webhook(webhook_payload, species=species)
        
        # Verify
        assert result["status"] == "success"
        assert result["task_status"] == "SUCCEEDED"
        
        updated_manifest = test_repository.get_asset_record(species, spec_hash)
        task_entry = next((e for e in updated_manifest.task_graph if e.task_id == task_id), None)
        
        assert task_entry is not None
        assert task_entry.status == "SUCCEEDED"
        assert "glb" in task_entry.result_paths
        
        print(f"\n✓ Animation webhook processed successfully")
        print(f"  Task ID: {task_id}")
        print(f"  Animation ID: 4 (Attack)")
    
    def test_4_retexture_with_webhook(
        self,
        meshy_api_key,
        test_repository,
        webhook_payload_loader
    ):
        """Retexture otter from brown to grey using webhook simulation"""
        client = BaseHttpClient(api_key=meshy_api_key)
        
        task_id = "018d536c-c3d7-938f-e444-4f1776f7f581"
        species = "otter"
        spec_hash = "test_spec_hash_004"
        
        asset_manifest = AssetManifest(
            asset_spec_hash=spec_hash,
            spec_fingerprint="{}",
            species=species,
            asset_intent="creature",
            prompts={"retexture": "Grey otter fur"},
            task_graph=[
                TaskGraphEntry(
                    task_id=task_id,
                    service="retexture",
                    status="PENDING",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    payload={
                        "model_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
                        "prompt": "realistic grey otter fur"
                    }
                )
            ]
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        # Load and process webhook
        webhook_payload = webhook_payload_loader("retexture_success.json")
        webhook_payload.id = task_id
        
        webhook_handler = WebhookHandler(
            repository=test_repository,
            client=client,
            download_artifacts=False
        )
        
        result = webhook_handler.handle_webhook(webhook_payload, species=species)
        
        # Verify
        assert result["status"] == "success"
        assert result["task_status"] == "SUCCEEDED"
        
        updated_manifest = test_repository.get_asset_record(species, spec_hash)
        task_entry = next((e for e in updated_manifest.task_graph if e.task_id == task_id), None)
        
        assert task_entry is not None
        assert task_entry.status == "SUCCEEDED"
        assert "glb" in task_entry.result_paths
        
        print(f"\n✓ Retexture webhook processed successfully")
        print(f"  Task ID: {task_id}")
        print(f"  New texture: grey fur")
    
    def test_5_complete_pipeline_with_webhooks(
        self,
        meshy_api_key,
        test_repository,
        webhook_payload_loader
    ):
        """Test complete pipeline using webhook simulation (no polling!)"""
        client = BaseHttpClient(api_key=meshy_api_key)
        
        species = "otter"
        spec_hash = "test_spec_hash_complete"
        
        # Create initial manifest
        asset_manifest = AssetManifest(
            asset_spec_hash=spec_hash,
            spec_fingerprint="{}",
            species=species,
            asset_intent="creature",
            prompts={
                "text3d": "realistic sea otter",
                "rigging": "Auto-rig",
                "animation": "Walking",
                "retexture": "Grey fur"
            },
            task_graph=[]
        )
        
        print("\n" + "="*60)
        print("COMPLETE PIPELINE TEST (WEBHOOK-BASED)")
        print("="*60)
        
        # Step 1: Text-to-3D
        print("\n=== Step 1: Text-to-3D ===")
        text3d_task_id = "complete_text3d_001"
        
        asset_manifest.task_graph.append(
            TaskGraphEntry(
                task_id=text3d_task_id,
                service="text3d",
                status="PENDING",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                payload={"prompt": "realistic sea otter"}
            )
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        # Simulate webhook
        webhook_payload = webhook_payload_loader("text3d_success.json")
        webhook_payload.id = text3d_task_id
        
        webhook_handler = WebhookHandler(test_repository, client, download_artifacts=False)
        result = webhook_handler.handle_webhook(webhook_payload, species=species)
        
        assert result["status"] == "success"
        print(f"✓ Text-to-3D completed via webhook")
        
        # Step 2: Rigging
        print("\n=== Step 2: Rigging ===")
        rigging_task_id = "complete_rigging_002"
        
        asset_manifest = test_repository.get_asset_record(species, spec_hash)
        asset_manifest.task_graph.append(
            TaskGraphEntry(
                task_id=rigging_task_id,
                service="rigging",
                status="PENDING",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                payload={"model_id": text3d_task_id}
            )
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        webhook_payload = webhook_payload_loader("rigging_success.json")
        webhook_payload.id = rigging_task_id
        result = webhook_handler.handle_webhook(webhook_payload, species=species)
        
        assert result["status"] == "success"
        print(f"✓ Rigging completed via webhook")
        
        # Step 3: Animation
        print("\n=== Step 3: Animation ===")
        animation_task_id = "complete_animation_003"
        
        asset_manifest = test_repository.get_asset_record(species, spec_hash)
        asset_manifest.task_graph.append(
            TaskGraphEntry(
                task_id=animation_task_id,
                service="animation",
                status="PENDING",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                payload={"model_id": rigging_task_id, "animation_id": "1"}
            )
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        webhook_payload = webhook_payload_loader("animation_success.json")
        webhook_payload.id = animation_task_id
        result = webhook_handler.handle_webhook(webhook_payload, species=species)
        
        assert result["status"] == "success"
        print(f"✓ Animation completed via webhook")
        
        # Step 4: Retexture
        print("\n=== Step 4: Retexture ===")
        retexture_task_id = "complete_retexture_004"
        
        asset_manifest = test_repository.get_asset_record(species, spec_hash)
        asset_manifest.task_graph.append(
            TaskGraphEntry(
                task_id=retexture_task_id,
                service="retexture",
                status="PENDING",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                payload={"model_id": text3d_task_id, "prompt": "grey fur"}
            )
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        webhook_payload = webhook_payload_loader("retexture_success.json")
        webhook_payload.id = retexture_task_id
        result = webhook_handler.handle_webhook(webhook_payload, species=species)
        
        assert result["status"] == "success"
        print(f"✓ Retexture completed via webhook")
        
        # Verify final state
        final_manifest = test_repository.get_asset_record(species, spec_hash)
        assert len(final_manifest.task_graph) == 4
        assert all(task.status == "SUCCEEDED" for task in final_manifest.task_graph)
        
        print("\n" + "="*60)
        print("✓ COMPLETE PIPELINE SUCCESS (NO POLLING!)")
        print("="*60)
        print(f"Text3D task:    {text3d_task_id}")
        print(f"Rigging task:   {rigging_task_id}")
        print(f"Animation task: {animation_task_id}")
        print(f"Retexture task: {retexture_task_id}")
        print("\nAll tasks completed instantly via webhook simulation!")
        print("="*60)
    
    def test_6_webhook_error_handling(
        self,
        meshy_api_key,
        test_repository,
        webhook_payload_loader
    ):
        """Test webhook handling of failed tasks"""
        client = BaseHttpClient(api_key=meshy_api_key)
        
        task_id = "failed_task_001"
        species = "otter"
        spec_hash = "test_spec_hash_failed"
        
        # Create task
        asset_manifest = AssetManifest(
            asset_spec_hash=spec_hash,
            spec_fingerprint="{}",
            species=species,
            asset_intent="creature",
            prompts={"text3d": "invalid prompt"},
            task_graph=[
                TaskGraphEntry(
                    task_id=task_id,
                    service="text3d",
                    status="PENDING",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    payload={"prompt": ""}
                )
            ]
        )
        test_repository.upsert_asset_record(species, asset_manifest)
        
        # Create failure webhook payload
        from mesh_toolkit.webhooks.schemas import WebhookTaskError
        failure_payload = MeshyWebhookPayload(
            id=task_id,
            status="FAILED",
            progress=0,
            created_at=1700000000,
            task_error=WebhookTaskError(
                message="Invalid prompt: prompt cannot be empty",
                code="INVALID_INPUT"
            )
        )
        
        webhook_handler = WebhookHandler(test_repository, client, download_artifacts=False)
        result = webhook_handler.handle_webhook(failure_payload, species=species)
        
        # Verify failure was recorded
        assert result["status"] == "success"  # Webhook handled successfully
        assert result["task_status"] == "FAILED"
        
        updated_manifest = test_repository.get_asset_record(species, spec_hash)
        task_entry = updated_manifest.task_graph[0]
        
        assert task_entry.status == "FAILED"
        assert task_entry.error == "Invalid prompt: prompt cannot be empty"
        
        print(f"\n✓ Failure webhook handled correctly")
        print(f"  Error: {task_entry.error}")
