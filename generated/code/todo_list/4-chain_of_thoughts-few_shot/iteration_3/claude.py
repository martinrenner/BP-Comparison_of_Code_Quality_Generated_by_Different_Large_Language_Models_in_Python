class TaskManager:
    """
    A task management system that allows adding, removing, searching, and managing tasks.
    Implements ISO/IEC 25010 quality standards for maintainability and reliability.
    """

    def __init__(self):
        """
        Initialize the TaskManager with an empty task dictionary and ID counter.
        """
        self._tasks = {}  # Dictionary to store tasks with ID as key
        self._id_counter = 1  # Counter for generating unique IDs
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task with a name and description.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            
        Returns:
            int: The unique ID assigned to the new task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Validate input
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty.")
        
        # Create a new task
        task_id = self._id_counter
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        
        # Increment the ID counter for next task
        self._id_counter += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The unique identifier of the task.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        # Validate input
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        
        # Remove the task if it exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def search(self, task_term: str) -> list[dict]:
        """
        Search tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions.
            
        Returns:
            list[dict]: A list of tasks matching the search term.
            
        Raises:
            ValueError: If task_term is empty.
        """
        # Validate input
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        
        task_term = task_term.lower().strip()
        
        # Search for matching tasks
        matching_tasks = []
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                matching_tasks.append(task.copy())
        
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique identifier of the task.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        # Validate input
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        
        # Mark the task as finished if it exists
        if task_id in self._tasks:
            self._tasks[task_id]['is_finished'] = True
            return True
        return False
    
    def get_all(self) -> list[dict]:
        """
        Get all tasks.
        
        Returns:
            list[dict]: A list of all tasks.
        """
        return list(self._tasks.values())
    
    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if all tasks were successfully deleted.
        """
        self._tasks = {}
        return True


def display_menu():
    """Display the application menu options."""
    print("\n===== Todo List Application =====")
    print("1. Add a new task")
    print("2. Remove a task")
    print("3. Search tasks")
    print("4. Mark a task as completed")
    print("5. Show all tasks")
    print("6. Clear all tasks")
    print("7. Exit")
    print("================================")


def display_task(task):
    """Display a single task with formatted output."""
    status = "✓ Completed" if task['is_finished'] else "☐ Pending"
    print(f"\nID: {task['id']} [{status}]")
    print(f"Title: {task['task_name']}")
    print(f"Description: {task['task_description']}")


def main():
    """Main application function that handles user interaction with the TaskManager."""
    task_manager = TaskManager()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
                
            elif choice == '2':
                task_id = int(input("Enter task ID to remove: "))
                if task_manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
                    
            elif choice == '3':
                term = input("Enter search term: ")
                results = task_manager.search(term)
                if results:
                    print(f"Found {len(results)} matching task(s):")
                    for task in results:
                        display_task(task)
                else:
                    print("No matching tasks found.")
                    
            elif choice == '4':
                task_id = int(input("Enter task ID to mark as completed: "))
                if task_manager.finish(task_id):
                    print("Task marked as completed.")
                else:
                    print("Task not found.")
                    
            elif choice == '5':
                tasks = task_manager.get_all()
                if tasks:
                    print(f"Total tasks: {len(tasks)}")
                    for task in tasks:
                        display_task(task)
                else:
                    print("No tasks available.")
                    
            elif choice == '6':
                confirm = input("Are you sure you want to clear all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    task_manager.clear_all()
                    print("All tasks cleared.")
                    
            elif choice == '7':
                print("Thank you for using the Todo List Application. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
