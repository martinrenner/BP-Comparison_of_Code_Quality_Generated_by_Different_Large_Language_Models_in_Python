class TaskManager:
    """
    TaskManager class for managing a to-do list with CRUD operations.
    
    This class implements a task management system adhering to ISO/IEC 25010 
    quality standards. It provides functionality to add, remove, search, 
    complete tasks, and more while maintaining data integrity and usability.
    """
    
    def __init__(self):
        """Initialize an empty task manager with a task counter for unique IDs."""
        self._tasks = {}  # Using dictionary for O(1) lookup by ID
        self._id_counter = 1  # Counter for generating unique IDs
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The name of the task (non-empty string)
            task_description: Description of the task (can be empty)
            
        Returns:
            int: The unique ID of the newly added task
            
        Raises:
            ValueError: If task_name is empty or not a string
            TypeError: If inputs are not strings
        """
        # Validate inputs
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
            
        # Create a new task with a unique ID
        task_id = self._id_counter
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        
        self._id_counter += 1
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
            
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> list[dict]:
        """
        Search for tasks containing the specified term in name or description.
        
        Args:
            task_term: The search term to look for
            
        Returns:
            list[dict]: List of tasks matching the search criteria
            
        Raises:
            TypeError: If task_term is not a string
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
            
        term = task_term.lower().strip()
        results = []
        
        for task in self._tasks.values():
            if (term in task['task_name'].lower() or 
                term in task['task_description'].lower()):
                results.append(task.copy())
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique identifier of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
            
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
            
        if task_id in self._tasks:
            self._tasks[task_id]['is_finished'] = True
            return True
            
        return False
    
    def get_all(self) -> list[dict]:
        """
        Get all tasks in the task manager.
        
        Returns:
            list[dict]: A list of all tasks with their details
        """
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if operation was successful
        """
        self._tasks.clear()
        # We don't reset the ID counter to maintain ID uniqueness over time
        return True


def main():
    """
    Main function to demonstrate the TaskManager functionality.
    
    This provides a simple command-line interface to interact with the TaskManager.
    """
    task_manager = TaskManager()
    
    print("=== To-Do List Application ===")
    
    while True:
        print("\nOptions:")
        print("1. Add a new task")
        print("2. Remove a task")
        print("3. Search for tasks")
        print("4. Mark a task as finished")
        print("5. View all tasks")
        print("6. Clear all tasks")
        print("7. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-7): "))
            
            if choice == 1:
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = task_manager.add(name, desc)
                print(f"Task added successfully with ID: {task_id}")
                
            elif choice == 2:
                task_id = int(input("Enter task ID to remove: "))
                if task_manager.remove(task_id):
                    print("Task removed successfully")
                else:
                    print("Task not found")
                    
            elif choice == 3:
                term = input("Enter search term: ")
                results = task_manager.search(term)
                if results:
                    print("\nSearch results:")
                    for task in results:
                        status = "✓" if task['is_finished'] else "☐"
                        print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
                else:
                    print("No matching tasks found")
                    
            elif choice == 4:
                task_id = int(input("Enter task ID to mark as finished: "))
                if task_manager.finish(task_id):
                    print("Task marked as finished")
                else:
                    print("Task not found")
                    
            elif choice == 5:
                tasks = task_manager.get_all()
                if tasks:
                    print("\nAll tasks:")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "☐"
                        print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
                else:
                    print("No tasks found")
                    
            elif choice == 6:
                confirm = input("Are you sure you want to clear all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    task_manager.clear_all()
                    print("All tasks cleared")
                    
            elif choice == 7:
                print("Thank you for using the To-Do List App. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number between a 1 and 7.")
                
        except ValueError as e:
            if str(e):  # Custom validation error from our methods
                print(f"Error: {e}")
            else:  # Input conversion error
                print("Invalid input. Please enter a valid number.")
                
        except TypeError as e:
            print(f"Error: {e}")
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
