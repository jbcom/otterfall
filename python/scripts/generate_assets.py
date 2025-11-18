#!/usr/bin/env python3
"""Generate game assets using Meshy SDK"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.meshy import (
    AssetGenerator,
    otter_player_spec,
    otter_npc_male_spec,
    otter_npc_female_spec,
    fish_bass_spec,
    cattail_reeds_spec,
    wooden_dock_spec
)


def main():
    """Generate core game assets"""
    
    print("🎨 Generating Rivermarsh Game Assets")
    print("=" * 60)
    
    generator = AssetGenerator(output_root="client/public")
    
    # Define asset queue
    specs = [
        ("Player Otter", otter_player_spec()),
        ("NPC Male Otter", otter_npc_male_spec()),
        ("NPC Female Otter", otter_npc_female_spec()),
        ("Bass Fish", fish_bass_spec()),
        ("Cattail Reeds", cattail_reeds_spec()),
        ("Wooden Dock", wooden_dock_spec()),
    ]
    
    print(f"\nGenerating {len(specs)} assets...")
    print("This will take 2-5 minutes per asset.\n")
    
    manifests = []
    for name, spec in specs:
        print(f"🔨 Generating: {name}")
        print(f"   Prompt: {spec.description[:60]}...")
        
        try:
            manifest = generator.generate_model(spec, wait=True, poll_interval=5.0)
            manifests.append(manifest)
            
            print(f"   ✓ Model: {manifest.model_path}")
            if manifest.texture_paths:
                print(f"   ✓ Textures: {len(manifest.texture_paths)} maps")
            print()
            
        except Exception as e:
            print(f"   ✗ Error: {e}\n")
    
    print("=" * 60)
    print(f"✅ Generated {len(manifests)}/{len(specs)} assets")
    print(f"\nAssets saved to: client/public/models/")
    print("Manifests include GLB paths, textures, and metadata for ECS integration.")


if __name__ == "__main__":
    main()
