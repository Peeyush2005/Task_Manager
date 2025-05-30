from task_manager import TaskManager
from user_interface import UserInterface
from datetime import datetime, timedelta
import sys

def main():
    print("=" * 50)
    print("    TASK MANAGER v2.0")
    print("    🏷️  Now with Categories!")
    print("=" * 50)
    print()

    task_manager = TaskManager()
    ui = UserInterface(task_manager)

    # Load tasks and categories if they exist, otherwise create default categories
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

    # Run the user interface loop
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Thanks for using Task Manager!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
    finally:
        # Attempt to save tasks on exit
        try:
            task_manager.save_tasks()
            print("Tasks saved successfully!")
        except Exception as e:
            print(f"Error saving tasks: {e}")

def search_tasks(tasks, keyword=None, status=None, priority=None):
    results = []
    for task in tasks:
        if keyword and keyword.lower() not in task['title'].lower():
            continue
        if status and task['status'].lower() != status.lower():
            continue
        if priority and task.get('priority', '').lower() != priority.lower():
            continue
        results.append(task)
    return results

def handle_recurring_tasks(tasks):
    new_tasks = []
    for task in tasks:
        if task.get('recurrence') != 'none' and task['status'] == 'completed':
            next_due = calculate_next_due_date(task['due_date'], task['recurrence'])
            new_task = task.copy()
            new_task['due_date'] = next_due
            new_task['status'] = 'pending'
            new_tasks.append(new_task)
    tasks.extend(new_tasks)
    return tasks

def calculate_next_due_date(due_date_str, recurrence):
    date_format = "%Y-%m-%d"
    due_date = datetime.strptime(due_date_str, date_format)
    if recurrence == 'daily':
        due_date += timedelta(days=1)
    elif recurrence == 'weekly':
        due_date += timedelta(weeks=1)
    elif recurrence == 'monthly':
        due_date += timedelta(days=30)
    return due_date.strftime(date_format)

if __name__ == "__main__":
    main()
