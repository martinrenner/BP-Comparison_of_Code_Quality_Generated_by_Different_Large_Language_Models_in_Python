class TaskManager:
    """
    A task manager that implements a todo list with CRUD operations.
    
    This class provides methods to add, remove, search, finish tasks,
    as well as retrieve all tasks or clear the entire task list.
    """
    
    def __init__(self):
        """Initialize a new TaskManager with an empty task dictionary and a task counter."""
        self._tasks = {}  # Using a dictionary for O(1) lookups by ID
        self._task_counter = 0  # Counter for generating unique task IDs
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.
            
        Returns:
            int: The unique ID of the newly created task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty")
            
        self._task_counter += 1
        task_id = self._task_counter
        
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'is_finished': False
        }
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative or not an integer.
            KeyError: If no task with the given task_id exists.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id not in self._tasks:
            raise KeyError(f"No task found with ID {task_id}")
            
        del self._tasks[task_id]
        return True
    
    def search(self, task_term: str) -> list[dict]:
        """
        Search tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions.
            
        Returns:
            list[dict]: A list of tasks matching the search term.
            
        Raises:
            ValueError: If search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty")
            
        result = []
        term = task_term.lower()
        
        for task in self._tasks.values():
            if (term in task['task_name'].lower() or 
                term in task['task_description'].lower()):
                result.append(task.copy())  # Return copy to protect internal data
                
        return result
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative or not an integer.
            KeyError: If no task with the given task_id exists.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id not in self._tasks:
            raise KeyError(f"No task found with ID {task_id}")
            
        # If task is already finished, still return True
        self._tasks[task_id]['is_finished'] = True
        return True
    
    def get_all(self) -> list[dict]:
        """
        Retrieve all tasks.
        
        Returns:
            list[dict]: A list containing all tasks.
        """
        return list(task.copy() for task in self._tasks.values())
    
    def clear_all(self) -> bool:
        """
        Clear all tasks.
        
        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self._tasks.clear()
        return True


def main():
    """
    Main function to demonstrate the TaskManager's functionality.
    """
    task_manager = TaskManager()
    
    try:
        # Add some tasks
        task1_id = task_manager.add("Buy groceries", "Milk, eggs, bread")
        task2_id = task_manager.add("Finish report", "Complete the quarterly report")
        task3_id = task_manager.add("Call mom", "Don't forget to call mom on her birthday")
        
        print("\nAll tasks:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Description: {task['task_description']}, "
                  f"Completed: {task['is_finished']}")
        
        # Search for tasks
        print("\nSearching for 'report':")
        for task in task_manager.search("report"):
            print(f"ID: {task['id']}, Name: {task['task_name']}")
        
        # Mark a task as completed
        task_manager.finish(task1_id)
        print(f"\nMarked task {task1_id} as completed")
        
        # Remove a task
        task_manager.remove(task2_id)
        print(f"Removed task {task2_id}")
        
        # Get all tasks again
        print("\nRemaining tasks:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
        # Clear all tasks
        task_manager.clear_all()
        print("\nCleared all tasks")
        print(f"Tasks remaining: {len(task_manager.get_all())}")
        
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
