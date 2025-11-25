"""
Main entry point for Rivermarsh CrewAI Game Builder.

Usage:
    uv run crew_agents build "Create a QuestComponent for tracking player quests"
    uv run crew_agents train 5
    uv run crew_agents list-knowledge
"""

import argparse
import sys
from pathlib import Path


def build_component(spec: str) -> None:
    """Build a game component from a specification."""
    from crew_agents.crews.game_builder import GameBuilderCrew

    print("=" * 60)
    print("🎮 RIVERMARSH GAME BUILDER")
    print("=" * 60)
    print()
    print(f"Building component: {spec[:100]}...")
    print()

    crew = GameBuilderCrew()
    result = crew.crew().kickoff(
        inputs={
            "component_spec": spec,
            "target_directory": "client/src/ecs/components",
        }
    )

    print()
    print("=" * 60)
    print("📄 RESULT")
    print("=" * 60)
    print(result.raw if hasattr(result, "raw") else str(result))


def train_crew(n_iterations: int, filename: str = "trained_agents_data.pkl") -> None:
    """Train the crew with human feedback."""
    from crew_agents.crews.game_builder import GameBuilderCrew

    print("=" * 60)
    print("🏋️ TRAINING GAME BUILDER CREW")
    print("=" * 60)
    print()
    print(f"Running {n_iterations} training iterations")
    print(f"Training data will be saved to: {filename}")
    print()
    print("You will be asked to provide feedback on each iteration.")
    print("This feedback helps the agents improve their code quality.")
    print()

    crew = GameBuilderCrew()

    # Training inputs - a representative task
    training_inputs = {
        "component_spec": """
        Create a SkillComponent for the player's skill system.
        
        Requirements:
        - Track skill levels (0-100)
        - Include skills: swimming, climbing, stealth, combat
        - Support experience gain towards next level
        - Include cooldowns for active skills
        """,
        "target_directory": "client/src/ecs/components",
    }

    try:
        crew.crew().train(
            n_iterations=n_iterations,
            inputs=training_inputs,
            filename=filename,
        )
        print()
        print("✅ Training complete!")
        print(f"Trained data saved to: {filename}")
        print()
        print("The crew will now use this training data to improve future code generation.")

    except Exception as e:
        print(f"❌ Training error: {e}")
        sys.exit(1)


def list_knowledge() -> None:
    """List available knowledge sources."""
    knowledge_path = Path(__file__).parent.parent.parent / "knowledge"

    print("=" * 60)
    print("📚 KNOWLEDGE SOURCES")
    print("=" * 60)
    print()

    if not knowledge_path.exists():
        print("No knowledge directory found")
        return

    for category in sorted(knowledge_path.iterdir()):
        if category.is_dir() and not category.name.startswith("."):
            print(f"📁 {category.name}/")
            for file in sorted(category.iterdir()):
                if file.suffix == ".md":
                    # Get first line as description
                    with open(file, "r") as f:
                        first_line = f.readline().strip().replace("#", "").strip()
                    print(f"   📄 {file.name}")
                    print(f"      {first_line[:60]}...")


def test_tools() -> None:
    """Test that the file tools work correctly."""
    from crew_agents.tools.file_tools import (
        DirectoryListTool,
        GameCodeReaderTool,
        get_workspace_root,
    )

    print("=" * 60)
    print("🔧 TESTING TOOLS")
    print("=" * 60)
    print()

    workspace = get_workspace_root()
    print(f"Workspace root: {workspace}")
    print()

    # Test directory listing
    dir_tool = DirectoryListTool()
    result = dir_tool._run("client/src/ecs/components")
    print("Directory listing:")
    print(result)
    print()

    # Test file reading
    read_tool = GameCodeReaderTool()
    result = read_tool._run("client/src/ecs/components.ts")
    print("File reading (first 500 chars):")
    print(result[:500] + "..." if len(result) > 500 else result)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Rivermarsh CrewAI Game Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Build a new ECS component
    uv run crew_agents build "Create a QuestComponent for tracking player quests"
    
    # Train the crew with human feedback (5 iterations)
    uv run crew_agents train 5
    
    # List available knowledge sources
    uv run crew_agents list-knowledge
    
    # Test that file tools work
    uv run crew_agents test-tools
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build a game component")
    build_parser.add_argument("spec", help="Component specification")

    # Train command
    train_parser = subparsers.add_parser("train", help="Train the crew with feedback")
    train_parser.add_argument("iterations", type=int, help="Number of training iterations")
    train_parser.add_argument(
        "-f", "--filename", default="trained_agents_data.pkl", help="Output filename"
    )

    # List knowledge command
    subparsers.add_parser("list-knowledge", help="List knowledge sources")

    # Test tools command
    subparsers.add_parser("test-tools", help="Test file tools")

    args = parser.parse_args()

    if args.command == "build":
        build_component(args.spec)
    elif args.command == "train":
        train_crew(args.iterations, args.filename)
    elif args.command == "list-knowledge":
        list_knowledge()
    elif args.command == "test-tools":
        test_tools()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
