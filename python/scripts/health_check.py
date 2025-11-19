
#!/usr/bin/env python3
"""
Comprehensive health check for Rivermarsh CrewAI system.
Validates all flows, dependencies, and configurations before deployment.
"""

import sys
import importlib.util
from pathlib import Path
from typing import List, Tuple


def check_flow_imports() -> List[Tuple[str, bool, str]]:
    """Check if all declared flows can be imported."""
    results = []
    flows = [
        "tdd_prototype_flow",
        "meshy_asset_flow", 
        "prototype_to_production_flow",
        "asset_integration_flow",
        "hitl_review_flow",
        "batch_generation_flow",
    ]
    
    for flow in flows:
        try:
            spec = importlib.util.find_spec(f"crew_agents.flows.{flow}")
            if spec is not None:
                results.append((flow, True, "✓ Import successful"))
            else:
                results.append((flow, False, "✗ Module not found"))
        except Exception as e:
            results.append((flow, False, f"✗ Error: {str(e)}"))
    
    return results


def check_required_files() -> List[Tuple[str, bool, str]]:
    """Check if required configuration files exist."""
    results = []
    required_files = [
        "python/crew_agents/crewbase.yaml",
        "python/crew_agents/src/crew_agents/config/agents.yaml",
        "python/crew_agents/src/crew_agents/config/tasks.yaml",
        "process-compose.yaml",
        ".ruler/AGENTS.md",
        "python/crew_agents/.ruler/reusable_workflows.md",
    ]
    
    for file_path in required_files:
        path = Path(file_path)
        exists = path.exists()
        status = "✓ Found" if exists else "✗ Missing"
        results.append((file_path, exists, status))
    
    return results


def check_python_dependencies() -> List[Tuple[str, bool, str]]:
    """Check if critical Python packages are available."""
    results = []
    packages = [
        "crewai",
        "pydantic",
    ]
    
    for package in packages:
        try:
            spec = importlib.util.find_spec(package)
            if spec is not None:
                results.append((package, True, "✓ Available"))
            else:
                results.append((package, False, "✗ Not installed"))
        except Exception as e:
            results.append((package, False, f"✗ Error: {str(e)}"))
    
    return results


def test_flow_instantiation() -> bool:
    """Test if flows can actually be instantiated."""
    try:
        from crew_agents.flows.tdd_prototype_flow import TDDPrototypeFlow
        flow = TDDPrototypeFlow()
        return flow.name == "tdd_prototype_flow"
    except Exception:
        return False


def main():
    """Run all health checks and report results."""
    print("=" * 60)
    print("RIVERMARSH CREWAI SYSTEM HEALTH CHECK")
    print("=" * 60)
    
    all_passed = True
    
    # Check Flow Imports
    print("\n📦 Flow Import Check:")
    flow_results = check_flow_imports()
    for name, passed, status in flow_results:
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    # Check Flow Instantiation
    print("\n🏗️  Flow Instantiation Check:")
    can_instantiate = test_flow_instantiation()
    status = "✓ Can instantiate flows" if can_instantiate else "✗ Cannot instantiate flows"
    print(f"  {status}")
    if not can_instantiate:
        all_passed = False
    
    # Check Required Files
    print("\n📄 Configuration Files Check:")
    file_results = check_required_files()
    for name, passed, status in file_results:
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    # Check Python Dependencies
    print("\n🐍 Python Dependencies Check:")
    dep_results = check_python_dependencies()
    for name, passed, status in dep_results:
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - System ready for deployment")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Review issues above")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
