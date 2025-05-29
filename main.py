from task_manager import TaskManager
from user_interface import UserInterface
import sys

def main():
    """Main application entry point"""
    print("=" * 50)
    print("    WELCOME TO TASK MANAGER v1.0")
    print("=" * 50)
    print()
    
    # Initialize the task manager
    task_manager = TaskManager()
    ui = UserInterface(task_manager)
    
    # Load existing tasks
    try:
        task_manager.load_tasks()
        print(f"Loaded {len(task_manager.tasks)} existing tasks.")
    except FileNotFoundError:
        print("No existing tasks found. Starting fresh!")
    except Exception as e:
        print(f"Error loading tasks: {e}")
    
    print()
    
    # Main application loop
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Thanks for using Task Manager!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
    finally:
        # Save tasks before exiting
        try:
            task_manager.save_tasks()
            print("Tasks saved successfully!")
        except Exception as e:
            print(f"Error saving tasks: {e}")

if __name__ == "__main__":
    main()