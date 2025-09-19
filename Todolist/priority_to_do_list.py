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
            
            # Add due date input
            due_date_input = input("Due date (YYYY-MM-DD) or days from now (e.g., '3' for 3 days): ").strip()
            due_date = None
            
            if due_date_input:
                try:
                    # Try parsing as number of days
                    if due_date_input.isdigit():
                        days = int(due_date_input)
                        due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                    else:
                        # Try parsing as date
                        datetime.strptime(due_date_input, "%Y-%m-%d")
                        due_date = due_date_input
                except ValueError:
                    print("Invalid date format. Skipping due date.")
            
            task = {
                'id': len(self.tasks) + 1,
                'title': title,
                'description': description,
                'priority': priority,
                'category': category,
                'completed': False,
                'created': datetime.now().strftime("%Y-%m-%d"),
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
        
        # Sort tasks by priority and due date
        priority_order = {'High': 3, 'Medium': 2, 'Low': 1}
        filtered_tasks.sort(key=lambda x: (
            priority_order.get(x['priority'], 0),
            x.get('due_date') or '9999-12-31'
        ), reverse=True)
        
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
            print("9. Save & Exit")
            
            choice = input("\nChoice (1-9): ").strip()
            
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
