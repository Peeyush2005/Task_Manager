from task_manager import TaskManager
from user_interface import UserInterface
import sys

def main():
    print("=" * 50)
    print("    TASK MANAGER v2.0")
    print("    🏷️  Now with Categories!")
    print("=" * 50)
    print()
    
    task_manager = TaskManager()
    ui = UserInterface(task_manager)
    
    try:
        task_manager.load_tasks()
        print(f"Loaded {len(task_manager.tasks)} existing tasks.")
        categories = task_manager.get_all_categories()
        if categories:
            print(f"Found {len(categories)} categories: {', '.join(categories)}")
    except FileNotFoundError:
        print("No existing tasks found. Starting fresh!")
        task_manager.create_default_categories()
        print("Created default categories: Work, Personal, Shopping, Health")
    except Exception as e:
        print(f"Error loading tasks: {e}")
    
    print()
    
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Thanks for using Task Manager!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
    finally:
        try:
            task_manager.save_tasks()
            print("Tasks saved successfully!")
        except Exception as e:
            print(f"Error saving tasks: {e}")

if __name__ == "__main__":
    main()