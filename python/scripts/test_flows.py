
#!/usr/bin/env python3
"""Quick smoke test for all flows."""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent / "crew_agents" / "src"))

def test_flow_imports():
    """Test that all flows can be imported."""
    print("🧪 Testing flow imports...")
    
    try:
        from crew_agents.flows import (
            TDDPrototypeFlow,
            MeshyAssetFlow,
            PrototypeToProductionFlow,
            AssetIntegrationFlow,
            HITLReviewFlow,
            BatchGenerationFlow,
        )
        print("✅ All flows imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_flow_instantiation():
    """Test that flows can be instantiated."""
    print("\n🧪 Testing flow instantiation...")
    
    try:
        from crew_agents.flows import TDDPrototypeFlow
        flow = TDDPrototypeFlow()
        print(f"✅ TDDPrototypeFlow instantiated: {flow.name}")
        return True
    except Exception as e:
        print(f"❌ Instantiation failed: {e}")
        return False

if __name__ == "__main__":
    results = []
    results.append(test_flow_imports())
    results.append(test_flow_instantiation())
    
    print("\n" + "="*50)
    if all(results):
        print("✅ ALL SMOKE TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
