"""
Simple To-Do List Application
"""

import json
import os
from datetime import datetime, timedelta

class SimpleTodoList:
    def __init__(self):
        self.tasks = []
        # Create data file path in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(script_dir, "todo_data.json")
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f).get('tasks', [])
        except:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump({'tasks': self.tasks}, f, indent=2)
            print("Saved!")
        except:
            print("Error saving tasks.")
    
    def add_task(self):
        """Add a new task"""
        title = input("Task: ").strip()
        if title:
            description = input("Description (optional): ").strip()
            
            print("Priority levels: High, Medium, Low")
            priority = input("Priority (default: Medium): ").strip() or "Medium"
            if priority not in ["High", "Medium", "Low"]:
                priority = "Medium"
            
            category = input("Category (default: General): ").strip() or "General"
            
            # Add due date input with better prompts
            print("\nDue date options:")
            print("  • Enter a specific date: YYYY-MM-DD (e.g., 2025-12-25)")
            print("  • Enter days from today: just a number (e.g., 7 for one week)")
            print("  • Press Enter to skip due date")
            due_date_input = input("When is this task due? ").strip()
            due_date = None
            
            if due_date_input:
                try:
                    # Try parsing as number of days
                    if due_date_input.isdigit():
                        days = int(due_date_input)
                        due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                        print(f"✓ Due date set to: {due_date} ({days} days from today)")
                    else:
                        # Try parsing as date
                        datetime.strptime(due_date_input, "%Y-%m-%d")
                        due_date = due_date_input
                        print(f"✓ Due date set to: {due_date}")
                except ValueError:
                    print("❌ Invalid date format. Task created without due date.")
            
            # Show creation confirmation
            creation_date = datetime.now().strftime("%Y-%m-%d")
            print(f"📅 Task will be created on: {creation_date}")
            
            # Generate unique ID by finding the maximum existing ID
            max_id = max([task['id'] for task in self.tasks], default=0)
            new_id = max_id + 1
            
            task = {
                'id': new_id,
                'title': title,
                'description': description,
                'priority': priority,
                'category': category,
                'completed': False,
                'created': creation_date,
                'due_date': due_date,
                'completed_date': None
            }
            self.tasks.append(task)
            print(f"Added: {title} (Priority: {priority}, Category: {category})")
    
    def view_tasks(self, filter_by=None, show_completed=True):
        """Display tasks with various filters"""
        if not self.tasks:
            print("No tasks found.")
            return
        
        # Filter tasks
        filtered_tasks = self.tasks.copy()
        
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task['completed']]
        
        if filter_by:
            if filter_by.lower() == 'high':
                filtered_tasks = [task for task in filtered_tasks if task['priority'] == 'High']
            elif filter_by.lower() == 'today':
                today = datetime.now().strftime("%Y-%m-%d")
                filtered_tasks = [task for task in filtered_tasks if task.get('due_date') == today]
            elif filter_by.lower() == 'overdue':
                today = datetime.now().strftime("%Y-%m-%d")
                filtered_tasks = [task for task in filtered_tasks 
                                if task.get('due_date') and task.get('due_date') < today and not task['completed']]
        
        if not filtered_tasks:
            print(f"\nNo tasks found with filter: {filter_by}")
            return
        
        # Sort tasks by due date (earliest first), then by priority, then by creation date
        def sort_key(task):
            # Handle due dates: None/empty dates go to the end
            due_date = task.get('due_date')
            if due_date:
                due_sort = due_date
            else:
                due_sort = '9999-12-31'  # Far future date for tasks without due dates
            
            # Priority order (High first)
            priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
            priority_sort = priority_order.get(task['priority'], 4)
            
            # Creation date for final sorting
            created_sort = task.get('created', '9999-12-31')
            
            return (due_sort, priority_sort, created_sort)
        
        filtered_tasks.sort(key=sort_key)
        
        print(f"\n{'='*60}")
        print(f"TO-DO LIST ({len(filtered_tasks)} tasks)")
        print(f"{'='*60}")
        
        for task in filtered_tasks:
            status = "✓" if task['completed'] else "○"
            priority_symbol = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task['priority'], "⚪")
            
            print(f"{status} #{task['id']} {priority_symbol} {task['title']}")
            
            if task.get('description'):
                print(f"   📝 {task['description']}")
            
            print(f"   📂 Category: {task['category']} | Priority: {task['priority']}")
            
            # Display creation date
            if task.get('created'):
                created_date = datetime.strptime(task['created'], "%Y-%m-%d")
                days_ago = (datetime.now() - created_date).days
                
                if days_ago == 0:
                    print(f"   📅 Created: {task['created']} (Today)")
                elif days_ago == 1:
                    print(f"   📅 Created: {task['created']} (Yesterday)")
                else:
                    print(f"   📅 Created: {task['created']} ({days_ago} days ago)")
            
            # Display due date information
            if task.get('due_date'):
                due_date = datetime.strptime(task['due_date'], "%Y-%m-%d")
                days_until = (due_date - datetime.now()).days
                
                if days_until < 0:
                    print(f"   ⏰ Due: {task['due_date']} (OVERDUE by {abs(days_until)} days)")
                elif days_until == 0:
                    print(f"   ⏰ Due: {task['due_date']} (TODAY)")
                elif days_until == 1:
                    print(f"   ⏰ Due: {task['due_date']} (Tomorrow)")
                else:
                    print(f"   ⏰ Due: {task['due_date']} (in {days_until} days)")
            
            if task['completed'] and task.get('completed_date'):
                print(f"   ✅ Completed: {task['completed_date']}")
            
            print()
        print(f"{'='*60}")
    
    def complete_task(self):
        """Mark a task as completed"""
        try:
            task_id = int(input("Task ID to complete: "))
            for task in self.tasks:
                if task['id'] == task_id:
                    if task['completed']:
                        print(f"Task #{task_id} is already completed.")
                    else:
                        task['completed'] = True
                        task['completed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Completed: {task['title']}")
                    return
            print("Task not found.")
        except ValueError:
            print("Invalid ID.")
    
    def delete_task(self):
        """Delete a task"""
        try:
            task_id = int(input("Task ID to delete: "))
            for i, task in enumerate(self.tasks):
                if task['id'] == task_id:
                    title = task['title']
                    del self.tasks[i]
                    print(f"Deleted: {title}")
                    return
            print("Task not found.")
        except ValueError:
            print("Invalid ID.")
    
    def search_tasks(self):
        """Search tasks by title, description, or category"""
        search_term = input("Enter search term: ").strip().lower()
        if not search_term:
            return
        
        matches = []
        for task in self.tasks:
            if (search_term in task['title'].lower() or 
                search_term in task.get('description', '').lower() or 
                search_term in task.get('category', '').lower()):
                matches.append(task)
        
        if matches:
            print(f"\nFound {len(matches)} tasks matching '{search_term}':")
            for task in matches:
                status = "✓" if task['completed'] else "○"
                priority_symbol = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task['priority'], "⚪")
                print(f"{status} #{task['id']} {priority_symbol} {task['title']} ({task.get('category', 'General')})")
        else:
            print(f"No tasks found matching '{search_term}'")

    def clear_completed_tasks(self):
        """Remove all completed tasks"""
        completed_tasks = [task for task in self.tasks if task['completed']]
        
        if not completed_tasks:
            print("No completed tasks to clear.")
            return
        
        print(f"\nFound {len(completed_tasks)} completed task(s):")
        for task in completed_tasks:
            print(f"✓ #{task['id']} {task['title']}")
        
        confirm = input(f"\nAre you sure you want to delete these {len(completed_tasks)} completed task(s)? (y/N): ").strip().lower()
        
        if confirm == 'y' or confirm == 'yes':
            self.tasks = [task for task in self.tasks if not task['completed']]
            print(f"Cleared {len(completed_tasks)} completed task(s).")
            # Reorganize IDs after clearing
            self.reorganize_ids()
        else:
            print("Clear operation cancelled.")

    def reorganize_ids(self):
        """Reorganize task IDs to be sequential (1, 2, 3, ...)"""
        for i, task in enumerate(self.tasks, 1):
            task['id'] = i
        print("Task IDs reorganized sequentially.")

    def edit_task(self):
        """Edit an existing task"""
        try:
            task_id = int(input("Task ID to edit: "))
            task_found = None
            
            for task in self.tasks:
                if task['id'] == task_id:
                    task_found = task
                    break
            
            if not task_found:
                print("Task not found.")
                return
            
            print(f"\nEditing task: {task_found['title']}")
            print("Leave blank to keep current value, or enter new value:")
            
            # Edit title
            new_title = input(f"Title [{task_found['title']}]: ").strip()
            if new_title:
                task_found['title'] = new_title
            
            # Edit description
            current_desc = task_found.get('description', '')
            new_description = input(f"Description [{current_desc}]: ").strip()
            if new_description or new_description == "":
                task_found['description'] = new_description
            
            # Edit priority
            print("Priority levels: High, Medium, Low")
            new_priority = input(f"Priority [{task_found['priority']}]: ").strip()
            if new_priority and new_priority in ["High", "Medium", "Low"]:
                task_found['priority'] = new_priority
            elif new_priority and new_priority not in ["High", "Medium", "Low"]:
                print("Invalid priority. Keeping current value.")
            
            # Edit category
            new_category = input(f"Category [{task_found['category']}]: ").strip()
            if new_category:
                task_found['category'] = new_category
            
            # Edit due date
            current_due = task_found.get('due_date', 'None')
            print(f"Current due date: {current_due}")
            due_date_input = input("Due date (YYYY-MM-DD, days from now, or 'clear' to remove): ").strip()
            
            if due_date_input.lower() == 'clear':
                task_found['due_date'] = None
                print("Due date cleared.")
            elif due_date_input:
                due_date = None
                try:
                    # Try parsing as number of days
                    if due_date_input.isdigit():
                        days = int(due_date_input)
                        due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                    else:
                        # Try parsing as date
                        datetime.strptime(due_date_input, "%Y-%m-%d")
                        due_date = due_date_input
                    
                    task_found['due_date'] = due_date
                    print(f"Due date updated to: {due_date}")
                except ValueError:
                    print("Invalid date format. Keeping current due date.")
            
            print(f"\nTask #{task_id} updated successfully!")
            
        except ValueError:
            print("Invalid ID.")
    
    def run(self):
        """Main application loop"""
        print("=== SIMPLE TO-DO LIST ===")
        
        while True:
            print("\n1. Add task")
            print("2. View all tasks")
            print("3. View high priority tasks")
            print("4. View today's tasks")
            print("5. View overdue tasks")
            print("6. Complete task")
            print("7. Delete task")
            print("8. Search tasks")
            print("9. Edit task")
            print("10. Clear completed tasks")
            print("11. Save & Exit")
            
            choice = input("\nChoice (1-11): ").strip()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.view_tasks(filter_by='high', show_completed=False)
            elif choice == '4':
                self.view_tasks(filter_by='today', show_completed=False)
            elif choice == '5':
                self.view_tasks(filter_by='overdue')
            elif choice == '6':
                self.complete_task()
            elif choice == '7':
                self.delete_task()
            elif choice == '8':
                self.search_tasks()
            elif choice == '9':
                self.edit_task()
            elif choice == '10':
                self.clear_completed_tasks()
            elif choice == '11':
                self.save_tasks()
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

def main():
    todo = SimpleTodoList()
    todo.run()

if __name__ == "__main__":
    main()
