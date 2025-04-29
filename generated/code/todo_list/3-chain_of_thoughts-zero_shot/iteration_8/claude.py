class TaskManager:
    """
    A task management system that allows users to create, manage, and track tasks.
    
    This implementation follows ISO/IEC 25010 standards, providing a reliable,
    efficient, and maintainable solution for task management.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with an empty task dictionary and a task ID counter.
        """
        self._tasks = {}  # Dictionary to store tasks with ID as key
        self._next_id = 1  # Counter for generating unique task IDs
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The name of the task (non-empty string)
            task_description: The description of the task (can be empty)
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If task_name is empty or not a string
            TypeError: If inputs are not of the expected types
        """
        # Input validation
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        # Create new task with unique ID
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The unique identifier of the task to remove
            
        Returns:
            bool: True if the task was successfully removed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
            
        if task_id < 1:
            raise ValueError("Task ID must be positive")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> list[dict]:
        """
        Search tasks by name or description.
        
        Args:
            task_term: The search term to look for in task names and descriptions
            
        Returns:
            list[dict]: A list of tasks (as dictionaries) that match the search term
            
        Raises:
            TypeError: If task_term is not a string
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
            
        task_term = task_term.lower().strip()
        results = []
        
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                results.append(task.copy())
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique identifier of the task to mark as completed
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
            
        if task_id < 1:
            raise ValueError("Task ID must be positive")
            
        if task_id in self._tasks:
            # Return False if the task is already finished, True otherwise
            if self._tasks[task_id]['is_finished']:
                return False
                
            self._tasks[task_id]['is_finished'] = True
            return True
            
        return False
    
    def get_all(self) -> list[dict]:
        """
        Get all tasks stored in the task manager.
        
        Returns:
            list[dict]: A list of all tasks with their details
        """
        # Return a copy of all tasks to prevent direct modification
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if the operation was successful
        """
        self._tasks.clear()
        return True


def display_task(task):
    """Helper function to format a task for display."""
    status = "[COMPLETED]" if task['is_finished'] else "[PENDING]"
    return (f"ID: {task['id']} {status}\n"
            f"Task: {task['task_name']}\n"
            f"Description: {task['task_description']}")


def main():
    """
    Main application function that provides a command-line interface for the TaskManager.
    """
    task_manager = TaskManager()
    
    print("Welcome to Task Manager!")
    
    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. Remove task")
        print("3. Search tasks")
        print("4. Mark task as completed")
        print("5. View all tasks")
        print("6. Clear all tasks")
        print("7. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-7): "))
            
            if choice == 1:
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                try:
                    task_id = task_manager.add(name, desc)
                    print(f"Task added successfully with ID: {task_id}")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
                    
            elif choice == 2:
                try:
                    task_id = int(input("Enter task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print(f"No task found with ID: {task_id}")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
                    
            elif choice == 3:
                term = input("Enter search term: ")
                try:
                    results = task_manager.search(term)
                    if results:
                        print(f"Found {len(results)} matching task(s):")
                        for task in results:
                            print("\n" + display_task(task))
                    else:
                        print("No matching tasks found")
                except TypeError as e:
                    print(f"Error: {e}")
                    
            elif choice == 4:
                try:
                    task_id = int(input("Enter task ID to mark as completed: "))
                    if task_manager.finish(task_id):
                        print("Task marked as completed")
                    else:
                        print(f"No task found with ID {task_id} or task already completed")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
                    
            elif choice == 5:
                tasks = task_manager.get_all()
                if tasks:
                    print(f"Total tasks: {len(tasks)}")
                    for task in tasks:
                        print("\n" + display_task(task))
                else:
                    print("No tasks found")
                    
            elif choice == 6:
                confirm = input("Are you sure you want to delete all tasks? (y/n): ").lower()
                if confirm == 'y':
                    task_manager.clear_all()
                    print("All tasks have been removed")
                    
            elif choice == 7:
                print("Thank you for using Task Manager. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                
        except ValueError:
            print("Please enter a valid number")
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
