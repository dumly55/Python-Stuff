"""
Simple To-Do List Application
"""

import json
import os
from datetime import datetime

class SimpleTodoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        try:
            if os.path.exists("todo_data.json"):
                with open("todo_data.json", 'r') as f:
                    self.tasks = json.load(f).get('tasks', [])
        except:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open("todo_data.json", 'w') as f:
                json.dump({'tasks': self.tasks}, f, indent=2)
            print("Saved!")
        except:
            print("Error saving tasks.")
    
    def add_task(self):
        """Add a new task"""
        title = input("Task: ").strip()
        if title:
            task = {
                'id': len(self.tasks) + 1,
                'title': title,
                'completed': False,
                'created': datetime.now().strftime("%Y-%m-%d")
            }
            self.tasks.append(task)
            print(f"Added: {title}")
    
    def view_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("No tasks found.")
            return
        
        print(f"\n{'='*50}")
        print("TO-DO LIST")
        print(f"{'='*50}")
        
        for task in self.tasks:
            status = "✓" if task['completed'] else "○"
            print(f"{status} #{task['id']} {task['title']}")
        print(f"{'='*50}")
    
    def complete_task(self):
        """Mark a task as completed"""
        try:
            task_id = int(input("Task ID to complete: "))
            for task in self.tasks:
                if task['id'] == task_id:
                    task['completed'] = True
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
    
    def run(self):
        """Main application loop"""
        print("=== SIMPLE TO-DO LIST ===")
        
        while True:
            print("\n1. Add task")
            print("2. View tasks")
            print("3. Complete task")
            print("4. Delete task")
            print("5. Save & Exit")
            
            choice = input("\nChoice (1-5): ").strip()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.complete_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
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
