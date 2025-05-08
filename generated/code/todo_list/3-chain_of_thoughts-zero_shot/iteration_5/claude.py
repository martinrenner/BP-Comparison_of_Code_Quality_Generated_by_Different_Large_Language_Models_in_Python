class TaskManager:
    """
    A Task Manager class that implements a todo list with comprehensive task management capabilities.
    This implementation follows ISO/IEC 25010 standards for software quality.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task storage and a task ID counter."""
        self._tasks = {}  # Dictionary for O(1) lookups by ID
        self._next_id = 1  # Auto-incrementing ID for tasks

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): Name of the task
            task_description (str): Detailed description of the task
            
        Returns:
            int: Unique ID of the newly created task
            
        Raises:
            ValueError: If task_name or task_description is empty
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
            
        # Create task
        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self._next_id += 1
        
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): Unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is negative or not an integer
            KeyError: If task_id does not exist
        """
        # Validate input
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
            
        # Remove task
        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> list:
        """
        Search tasks by name or description.
        
        Args:
            task_term (str): Search term to match against task names and descriptions
            
        Returns:
            list: List of task dictionaries that match the search term
            
        Raises:
            ValueError: If task_term is empty or not a string
        """
        # Validate input
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
            
        # Search for matching tasks
        results = []
        for task in self._tasks.values():
            if (task_term.lower() in task["task_name"].lower() or 
                task_term.lower() in task["task_description"].lower()):
                results.append(task.copy())
        
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): Unique identifier of the task to mark as completed
            
        Returns:
            bool: True if task was successfully marked as completed
            
        Raises:
            ValueError: If task_id is negative or not an integer
            KeyError: If task_id does not exist
        """
        # Validate input
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
            
        # Mark task as finished if it's not already finished
        if not self._tasks[task_id]["is_finished"]:
            self._tasks[task_id]["is_finished"] = True
            return True
        return False  # Task was already finished

    def get_all(self) -> list:
        """
        Retrieve all tasks.
        
        Returns:
            list: List of all task dictionaries
        """
        # Return a copy of all tasks to prevent external modification
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if tasks were successfully cleared
        """
        self._tasks.clear()
        return True


def display_tasks(tasks):
    """
    Helper function to display tasks in a formatted way.
    
    Args:
        tasks (list): List of task dictionaries to display
    """
    if not tasks:
        print("No tasks found.")
        return
        
    print("\n" + "=" * 80)
    print(f"{'ID':<5} {'Status':<10} {'Name':<20} {'Description':<45}")
    print("-" * 80)
    
    for task in tasks:
        status = "[DONE]" if task["is_finished"] else "[PENDING]"
        print(f"{task['id']:<5} {status:<10} {task['task_name'][:20]:<20} {task['task_description'][:45]:<45}")
    
    print("=" * 80 + "\n")


def main():
    """
    Main function to run the todo list application with a command-line interface.
    """
    task_manager = TaskManager()
    
    # Adding some example tasks
    try:
        task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
        task_manager.add("Call doctor", "Schedule annual checkup")
        task_manager.add("Pay bills", "Electricity and internet bills due this week")
        print("Example tasks added successfully.")
    except Exception as e:
        print(f"Error adding example tasks: {str(e)}")
    
    while True:
        print("\nTodo List Application")
        print("1. Add a new task")
        print("2. Remove a task")
        print("3. Search tasks")
        print("4. Mark task as completed")
        print("5. View all tasks")
        print("6. Clear all tasks")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-6): ")
        
        try:
            if choice == "1":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = task_manager.add(name, description)
                print(f"Task added with ID: {task_id}")
                
            elif choice == "2":
                task_id = int(input("Enter task ID to remove: "))
                if task_manager.remove(task_id):
                    print(f"Task {task_id} removed successfully.")
                
            elif choice == "3":
                term = input("Enter search term: ")
                results = task_manager.search(term)
                display_tasks(results)
                
            elif choice == "4":
                task_id = int(input("Enter task ID to mark as completed: "))
                if task_manager.finish(task_id):
                    print(f"Task {task_id} marked as completed.")
                else:
                    print(f"Task {task_id} was already completed.")
                
            elif choice == "5":
                tasks = task_manager.get_all()
                display_tasks(tasks)
                
            elif choice == "6":
                confirm = input("Are you sure you want to clear all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    if task_manager.clear_all():
                        print("All tasks cleared successfully.")
                
            elif choice == "0":
                print("Thank you for using the Todo List Application. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError as e:
            print(f"Invalid input: {str(e)}")
        except KeyError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
