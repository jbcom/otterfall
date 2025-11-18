"""Unit tests for TaskRepository"""
import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, mock_open
from mesh_toolkit.persistence.repository import TaskRepository
from mesh_toolkit.persistence.schemas import (
    SpeciesManifest,
    AssetManifest,
    TaskGraphEntry,
    ArtifactRecord,
    StatusHistoryEntry
)


class TestTaskRepository:
    """Test TaskRepository manifest operations"""
    
    @pytest.fixture
    def temp_repo(self):
        """Create temporary repository directory"""
        temp_dir = tempfile.mkdtemp()
        repo = TaskRepository(base_path=temp_dir)
        yield repo
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_initialization(self, temp_repo):
        """Test repository initialization creates base directory"""
        assert temp_repo.base_path.exists()
        assert temp_repo.base_path.is_dir()
    
    def test_manifest_path(self, temp_repo):
        """Test manifest path generation"""
        path = temp_repo._manifest_path("otter")
        assert path == temp_repo.base_path / "otter" / "manifest.json"
    
    def test_load_species_manifest_creates_new(self, temp_repo):
        """Test loading non-existent manifest creates empty one"""
        manifest = temp_repo.load_species_manifest("otter")
        
        # Verify empty manifest
        assert manifest.species == "otter"
        assert manifest.asset_specs == {}
        assert manifest.version == "1.0"
        
        # Verify manifest file was created
        manifest_path = temp_repo._manifest_path("otter")
        assert manifest_path.exists()
        
        # Verify file contents
        with open(manifest_path, 'r') as f:
            data = json.load(f)
            assert data["species"] == "otter"
            assert data["asset_specs"] == {}
    
    def test_load_species_manifest_existing(self, temp_repo):
        """Test loading existing manifest from disk"""
        # Create manifest first
        manifest = temp_repo.load_species_manifest("beaver")
        temp_repo.save_species_manifest(manifest)
        
        # Load it again
        loaded = temp_repo.load_species_manifest("beaver")
        
        assert loaded.species == "beaver"
        assert loaded.version == "1.0"
    
    def test_save_species_manifest_updates_timestamp(self, temp_repo):
        """Test save updates last_updated timestamp"""
        manifest = SpeciesManifest(species="otter")
        original_time = manifest.last_updated
        
        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.01)
        
        temp_repo.save_species_manifest(manifest)
        
        # Load and verify timestamp updated
        loaded = temp_repo.load_species_manifest("otter")
        assert loaded.last_updated > original_time
    
    def test_save_species_manifest_serializes_datetime(self, temp_repo):
        """Test datetime fields are properly serialized to ISO format"""
        manifest = SpeciesManifest(species="otter")
        temp_repo.save_species_manifest(manifest)
        
        manifest_path = temp_repo._manifest_path("otter")
        with open(manifest_path, 'r') as f:
            data = json.load(f)
            
        # Verify last_updated is ISO string
        assert isinstance(data["last_updated"], str)
        # Verify it can be parsed back to datetime
        datetime.fromisoformat(data["last_updated"])
    
    def test_get_asset_record_found(self, temp_repo):
        """Test get_asset_record returns existing asset"""
        # Create manifest with asset
        manifest = SpeciesManifest(species="otter")
        asset = AssetManifest(
            asset_spec_hash="hash123",
            spec_fingerprint='{"test": "data"}',
            species="otter",
            asset_intent="creature"
        )
        manifest.asset_specs["hash123"] = asset
        temp_repo.save_species_manifest(manifest)
        
        # Retrieve asset
        found = temp_repo.get_asset_record("otter", "hash123")
        
        assert found is not None
        assert found.asset_spec_hash == "hash123"
        assert found.species == "otter"
    
    def test_get_asset_record_not_found(self, temp_repo):
        """Test get_asset_record returns None for missing asset"""
        temp_repo.load_species_manifest("otter")
        
        found = temp_repo.get_asset_record("otter", "nonexistent_hash")
        
        assert found is None
    
    def test_upsert_asset_record_insert(self, temp_repo):
        """Test upsert creates new asset record"""
        asset = AssetManifest(
            asset_spec_hash="new_hash",
            spec_fingerprint='{"prompt": "otter"}',
            species="otter",
            asset_intent="creature"
        )
        
        temp_repo.upsert_asset_record("otter", asset)
        
        # Verify asset was saved
        found = temp_repo.get_asset_record("otter", "new_hash")
        assert found is not None
        assert found.asset_spec_hash == "new_hash"
    
    def test_upsert_asset_record_update(self, temp_repo):
        """Test upsert updates existing asset record"""
        # Create initial asset
        asset = AssetManifest(
            asset_spec_hash="update_hash",
            spec_fingerprint='{"v": 1}',
            species="otter",
            asset_intent="creature"
        )
        temp_repo.upsert_asset_record("otter", asset)
        
        # Update asset
        asset.spec_fingerprint = '{"v": 2}'
        temp_repo.upsert_asset_record("otter", asset)
        
        # Verify update
        found = temp_repo.get_asset_record("otter", "update_hash")
        assert found.spec_fingerprint == '{"v": 2}'
    
    def test_upsert_asset_record_updates_timestamp(self, temp_repo):
        """Test upsert updates the updated_at timestamp"""
        asset = AssetManifest(
            asset_spec_hash="time_hash",
            spec_fingerprint='{"test": "data"}',
            species="otter",
            asset_intent="creature"
        )
        original_time = asset.updated_at
        
        import time
        time.sleep(0.01)
        
        temp_repo.upsert_asset_record("otter", asset)
        
        found = temp_repo.get_asset_record("otter", "time_hash")
        assert found.updated_at > original_time
    
    def test_record_task_update_new_task(self, temp_repo):
        """Test recording new task in manifest"""
        # Create asset first
        asset = AssetManifest(
            asset_spec_hash="task_hash",
            spec_fingerprint='{"test": "data"}',
            species="otter",
            asset_intent="creature"
        )
        temp_repo.upsert_asset_record("otter", asset)
        
        # Record new task
        temp_repo.record_task_update(
            species="otter",
            spec_hash="task_hash",
            task_id="task_123",
            status="PENDING",
            service="text3d",
            payload={"prompt": "otter"},
            source="orchestrator"
        )
        
        # Verify task was added
        manifest = temp_repo.load_species_manifest("otter")
        asset_record = manifest.asset_specs["task_hash"]
        
        assert len(asset_record.task_graph) == 1
        task = asset_record.task_graph[0]
        assert task.task_id == "task_123"
        assert task.service == "text3d"
        assert task.status == "PENDING"
        assert task.payload == {"prompt": "otter"}
        
        # Verify history entry
        assert len(asset_record.history) == 1
        history = asset_record.history[0]
        assert history.old_status == ""
        assert history.new_status == "PENDING"
        assert history.source == "orchestrator"
        assert history.task_id == "task_123"
    
    def test_record_task_update_existing_task(self, temp_repo):
        """Test updating existing task status"""
        # Setup asset with task
        asset = AssetManifest(
            asset_spec_hash="update_task_hash",
            spec_fingerprint='{"test": "data"}',
            species="otter",
            asset_intent="creature"
        )
        task_entry = TaskGraphEntry(
            task_id="task_456",
            service="text3d",
            status="PENDING",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        )
        asset.task_graph.append(task_entry)
        temp_repo.upsert_asset_record("otter", asset)
        
        # Update task status
        temp_repo.record_task_update(
            species="otter",
            spec_hash="update_task_hash",
            task_id="task_456",
            status="SUCCEEDED",
            result_paths={"glb": "https://example.com/model.glb"},
            source="webhook"
        )
        
        # Verify update
        manifest = temp_repo.load_species_manifest("otter")
        asset_record = manifest.asset_specs["update_task_hash"]
        
        assert len(asset_record.task_graph) == 1
        task = asset_record.task_graph[0]
        assert task.status == "SUCCEEDED"
        assert task.result_paths["glb"] == "https://example.com/model.glb"
        
        # Verify history
        assert len(asset_record.history) == 1
        history = asset_record.history[0]
        assert history.old_status == "PENDING"
        assert history.new_status == "SUCCEEDED"
        assert history.source == "webhook"
    
    def test_record_task_update_with_error(self, temp_repo):
        """Test recording task failure with error message"""
        # Setup
        asset = AssetManifest(
            asset_spec_hash="error_hash",
            spec_fingerprint='{"test": "data"}',
            species="otter",
            asset_intent="creature"
        )
        task_entry = TaskGraphEntry(
            task_id="task_error",
            service="text3d",
            status="IN_PROGRESS",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        )
        asset.task_graph.append(task_entry)
        temp_repo.upsert_asset_record("otter", asset)
        
        # Record failure
        temp_repo.record_task_update(
            species="otter",
            spec_hash="error_hash",
            task_id="task_error",
            status="FAILED",
            error="Prompt contains inappropriate content"
        )
        
        # Verify error recorded
        manifest = temp_repo.load_species_manifest("otter")
        task = manifest.asset_specs["error_hash"].task_graph[0]
        assert task.status == "FAILED"
        assert task.error == "Prompt contains inappropriate content"
    
    def test_record_task_update_with_artifacts(self, temp_repo):
        """Test recording task with downloaded artifacts"""
        # Setup
        asset = AssetManifest(
            asset_spec_hash="artifact_hash",
            spec_fingerprint='{"test": "data"}',
            species="otter",
            asset_intent="creature"
        )
        temp_repo.upsert_asset_record("otter", asset)
        
        # Record task with artifacts
        artifacts = [
            ArtifactRecord(
                relative_path="otter_model.glb",
                sha256_hash="abc123",
                file_size_bytes=12345,
                downloaded_at=datetime.utcnow(),
                source_url="https://example.com/model.glb"
            )
        ]
        
        temp_repo.record_task_update(
            species="otter",
            spec_hash="artifact_hash",
            task_id="task_artifact",
            status="SUCCEEDED",
            service="text3d",
            artifacts=artifacts
        )
        
        # Verify artifacts recorded
        manifest = temp_repo.load_species_manifest("otter")
        asset_record = manifest.asset_specs["artifact_hash"]
        
        assert len(asset_record.artifacts) == 1
        artifact = asset_record.artifacts[0]
        assert artifact.relative_path == "otter_model.glb"
        assert artifact.sha256_hash == "abc123"
        assert artifact.file_size_bytes == 12345
    
    def test_record_task_update_asset_not_found_raises(self, temp_repo):
        """Test recording task for non-existent asset raises error"""
        temp_repo.load_species_manifest("otter")
        
        with pytest.raises(ValueError, match="Asset .* not found"):
            temp_repo.record_task_update(
                species="otter",
                spec_hash="nonexistent",
                task_id="task_123",
                status="PENDING"
            )
    
    def test_list_pending_assets(self, temp_repo):
        """Test listing assets with non-terminal tasks"""
        # Create assets with different states
        pending_asset = AssetManifest(
            asset_spec_hash="pending_hash",
            spec_fingerprint='{"test": 1}',
            species="otter",
            asset_intent="creature"
        )
        pending_asset.task_graph.append(TaskGraphEntry(
            task_id="task_pending",
            service="text3d",
            status="PENDING",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        ))
        
        completed_asset = AssetManifest(
            asset_spec_hash="completed_hash",
            spec_fingerprint='{"test": 2}',
            species="otter",
            asset_intent="creature"
        )
        completed_asset.task_graph.append(TaskGraphEntry(
            task_id="task_completed",
            service="text3d",
            status="SUCCEEDED",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        ))
        
        temp_repo.upsert_asset_record("otter", pending_asset)
        temp_repo.upsert_asset_record("otter", completed_asset)
        
        # List pending
        pending = temp_repo.list_pending_assets("otter")
        
        assert len(pending) == 1
        assert pending[0].asset_spec_hash == "pending_hash"
    
    def test_list_pending_assets_multiple_tasks(self, temp_repo):
        """Test asset is pending if any task is non-terminal"""
        asset = AssetManifest(
            asset_spec_hash="multi_hash",
            spec_fingerprint='{"test": 1}',
            species="otter",
            asset_intent="creature"
        )
        asset.task_graph.append(TaskGraphEntry(
            task_id="task_1",
            service="text3d",
            status="SUCCEEDED",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        ))
        asset.task_graph.append(TaskGraphEntry(
            task_id="task_2",
            service="rigging",
            status="IN_PROGRESS",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        ))
        
        temp_repo.upsert_asset_record("otter", asset)
        
        pending = temp_repo.list_pending_assets("otter")
        assert len(pending) == 1
    
    def test_find_task_by_id_found(self, temp_repo):
        """Test finding asset by task ID"""
        asset = AssetManifest(
            asset_spec_hash="find_hash",
            spec_fingerprint='{"test": 1}',
            species="otter",
            asset_intent="creature"
        )
        asset.task_graph.append(TaskGraphEntry(
            task_id="unique_task_999",
            service="text3d",
            status="PENDING",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        ))
        temp_repo.upsert_asset_record("otter", asset)
        
        # Find by task ID
        result = temp_repo.find_task_by_id("unique_task_999", species="otter")
        
        assert result is not None
        species, spec_hash, found_asset = result
        assert species == "otter"
        assert spec_hash == "find_hash"
        assert found_asset.asset_spec_hash == "find_hash"
    
    def test_find_task_by_id_not_found(self, temp_repo):
        """Test find_task_by_id returns None when not found"""
        temp_repo.load_species_manifest("otter")
        
        result = temp_repo.find_task_by_id("nonexistent_task", species="otter")
        
        assert result is None
    
    def test_find_task_by_id_searches_all_species(self, temp_repo):
        """Test find_task_by_id searches all species when not specified"""
        # Create assets in different species
        otter_asset = AssetManifest(
            asset_spec_hash="otter_hash",
            spec_fingerprint='{"test": 1}',
            species="otter",
            asset_intent="creature"
        )
        otter_asset.task_graph.append(TaskGraphEntry(
            task_id="otter_task_123",
            service="text3d",
            status="PENDING",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        ))
        temp_repo.upsert_asset_record("otter", otter_asset)
        
        beaver_asset = AssetManifest(
            asset_spec_hash="beaver_hash",
            spec_fingerprint='{"test": 2}',
            species="beaver",
            asset_intent="creature"
        )
        beaver_asset.task_graph.append(TaskGraphEntry(
            task_id="beaver_task_456",
            service="text3d",
            status="PENDING",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            payload={}
        ))
        temp_repo.upsert_asset_record("beaver", beaver_asset)
        
        # Find without species filter
        result = temp_repo.find_task_by_id("beaver_task_456")
        
        assert result is not None
        species, spec_hash, found_asset = result
        assert species == "beaver"
        assert spec_hash == "beaver_hash"
    
    def test_manifest_survives_corrupted_json(self, temp_repo):
        """Test handling of corrupted manifest JSON"""
        manifest_path = temp_repo._manifest_path("otter")
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write corrupted JSON
        with open(manifest_path, 'w') as f:
            f.write('{"species": "otter", invalid json')
        
        # Should raise JSONDecodeError
        with pytest.raises(json.JSONDecodeError):
            temp_repo.load_species_manifest("otter")
    
    def test_missing_directory_created(self, temp_repo):
        """Test missing species directory is created on save"""
        manifest = SpeciesManifest(species="new_species")
        
        # Directory shouldn't exist yet
        species_dir = temp_repo.base_path / "new_species"
        assert not species_dir.exists()
        
        # Save should create it
        temp_repo.save_species_manifest(manifest)
        
        assert species_dir.exists()
        assert (species_dir / "manifest.json").exists()
