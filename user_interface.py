import os
from typing import List
from task_manager import TaskManager, Task

class UserInterface:
    """Command-line user interface for the task manager"""
    
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 40)
        print("           TASK MANAGER MENU")
        print("=" * 40)
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Edit Task")
        print("8. Delete Task")
        print("9. View Statistics")
        print("10. Search Tasks")
        print("0. Exit")
        print("=" * 40)
    
    def get_user_input(self, prompt: str) -> str:
        """Get user input with prompt"""
        return input(f"{prompt}: ").strip()
    
    def get_user_choice(self) -> str:
        """Get user menu choice"""
        return self.get_user_input("Enter your choice")
    
    def display_tasks(self, tasks: List[Task], title: str = "Tasks"):
        """Display a list of tasks"""
        print(f"\n{title.upper()}")
        print("-" * len(title))
        
        if not tasks:
            print("No tasks found.")
            return
        
        # Sort tasks: incomplete first, then by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(tasks, key=lambda t: (t.completed, priority_order[t.priority]))
        
        for i, task in enumerate(sorted_tasks, 1):
            print(f"{i}. {task}")
            if task.description:
                print(f"   Description: {task.description}")
            print(f"   Created: {task.created_at}")
            if task.completed_at:
                print(f"   Completed: {task.completed_at}")
            print()
    
    def add_task(self):
        """Add a new task"""
        print("\n" + "=" * 30)
        print("        ADD NEW TASK")
        print("=" * 30)
        
        title = self.get_user_input("Task title")
        if not title:
            print("Error: Task title cannot be empty!")
            return
        
        description = self.get_user_input("Description (optional)")
        
        print("\nPriority levels: low, medium, high")
        priority = self.get_user_input("Priority (default: medium)")
        if not priority:
            priority = "medium"
        
        try:
            task = self.task_manager.add_task(title, description, priority)
            print(f"\nTask '{task.title}' added successfully!")
        except ValueError as e:
            print(f"Error: {e}")
    
    def mark_task_complete(self):
        """Mark a task as complete"""
        pending_tasks = self.task_manager.get_pending_tasks()
        if not pending_tasks:
            print("\nNo pending tasks to complete!")
            return
        
        self.display_tasks(pending_tasks, "Pending Tasks")
        
        task_id = self.select_task_by_number(pending_tasks)
        if task_id:
            task = self.task_manager.get_task(task_id)
            task.mark_complete()
            print(f"\nTask '{task.title}' marked as complete!")
    
    def mark_task_incomplete(self):
        """Mark a task as incomplete"""
        completed_tasks = self.task_manager.get_completed_tasks()
        if not completed_tasks:
            print("\nNo completed tasks to mark incomplete!")
            return
        
        self.display_tasks(completed_tasks, "Completed Tasks")
        
        task_id = self.select_task_by_number(completed_tasks)
        if task_id:
            task = self.task_manager.get_task(task_id)
            task.mark_incomplete()
            print(f"\nTask '{task.title}' marked as incomplete!")
    
    def edit_task(self):
        """Edit an existing task"""
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("\nNo tasks available to edit!")
            return
        
        self.display_tasks(tasks, "All Tasks")
        
        task_id = self.select_task_by_number(tasks)
        if not task_id:
            return
        
        task = self.task_manager.get_task(task_id)
        
        print(f"\nEditing task: {task.title}")
        print("Leave empty to keep current value")
        
        new_title = self.get_user_input(f"New title (current: {task.title})")
        new_description = self.get_user_input(f"New description (current: {task.description})")
        new_priority = self.get_user_input(f"New priority (current: {task.priority})")
        
        try:
            task.update(
                title=new_title if new_title else None,
                description=new_description if new_description else None,
                priority=new_priority if new_priority else None
            )
            print("\nTask updated successfully!")
        except Exception as e:
            print(f"Error updating task: {e}")
    
    def delete_task(self):
        """Delete a task"""
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("\nNo tasks available to delete!")
            return
        
        self.display_tasks(tasks, "All Tasks")
        
        task_id = self.select_task_by_number(tasks)
        if not task_id:
            return
        
        task = self.task_manager.get_task(task_id)
        confirm = self.get_user_input(f"Delete '{task.title}'? (y/N)")
        
        if confirm.lower() == 'y':
            if self.task_manager.delete_task(task_id):
                print("\nTask deleted successfully!")
            else:
                print("\nError deleting task!")
        else:
            print("\nTask deletion cancelled.")
    
    def select_task_by_number(self, tasks: List[Task]) -> str:
        """Select a task by its display number"""
        try:
            choice = int(self.get_user_input("Select task number"))
            if 1 <= choice <= len(tasks):
                return tasks[choice - 1].id
            else:
                print("Invalid task number!")
                return None
        except ValueError:
            print("Please enter a valid number!")
            return None
    
    def view_statistics(self):
        """Display task statistics"""
        stats = self.task_manager.get_stats()
        
        print("\n" + "=" * 30)
        print("       TASK STATISTICS")
        print("=" * 30)
        print(f"Total Tasks: {stats['total']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")
        print(f"Completion Rate: {stats['completion_rate']:.1f}%")
        print("\nPriority Breakdown:")
        print(f"  High: {stats['priority_counts']['high']}")
        print(f"  Medium: {stats['priority_counts']['medium']}")
        print(f"  Low: {stats['priority_counts']['low']}")
    
    def search_tasks(self):
        """Search for tasks"""
        query = self.get_user_input("Enter search term")
        if not query:
            print("Search term cannot be empty!")
            return
        
        all_tasks = self.task_manager.get_all_tasks()
        matching_tasks = []
        
        query_lower = query.lower()
        for task in all_tasks:
            if (query_lower in task.title.lower() or 
                query_lower in task.description.lower()):
                matching_tasks.append(task)
        
        if matching_tasks:
            self.display_tasks(matching_tasks, f"Search Results for '{query}'")
        else:
            print(f"No tasks found matching '{query}'")
    
    def run(self):
        """Main application loop"""
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.display_tasks(self.task_manager.get_all_tasks(), "All Tasks")
            elif choice == "3":
                self.display_tasks(self.task_manager.get_pending_tasks(), "Pending Tasks")
            elif choice == "4":
                self.display_tasks(self.task_manager.get_completed_tasks(), "Completed Tasks")
            elif choice == "5":
                self.mark_task_complete()
            elif choice == "6":
                self.mark_task_incomplete()
            elif choice == "7":
                self.edit_task()
            elif choice == "8":
                self.delete_task()
            elif choice == "9":
                self.view_statistics()
            elif choice == "10":
                self.search_tasks()
            elif choice == "0":
                self.running = False
                print("\nThank you for using Task Manager!")
            else:
                print("\nInvalid choice! Please try again.")
            
            if self.running:
                input("\nPress Enter to continue...")