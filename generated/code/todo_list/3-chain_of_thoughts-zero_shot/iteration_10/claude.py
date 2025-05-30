class TaskManager:
    """
    A task manager that provides functionality to manage a todo list.
    This implementation adheres to ISO/IEC 25010 quality standards.
    """

    def __init__(self):
        """Initialize an empty task manager with a counter for task IDs."""
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
            TypeError: If inputs are not strings
        """
        # Validate inputs
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        # Create new task
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
            task_id: The unique ID of the task to remove
            
        Returns:
            bool: True if the task was removed, False otherwise
            
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
        Search for tasks containing the given term in name or description.
        
        Args:
            task_term: The search term to look for
            
        Returns:
            list[dict]: List of tasks (as dictionaries) that match the search term
            
        Raises:
            TypeError: If task_term is not a string
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        
        task_term = task_term.lower().strip()
        
        if not task_term:
            return []
        
        results = []
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                results.append(task.copy())
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished.
        
        Args:
            task_id: The unique ID of the task to mark as finished
            
        Returns:
            bool: True if the task was marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
        
        if task_id in self._tasks:
            # Check if task is already finished
            if self._tasks[task_id]['is_finished']:
                return False  # Task already finished
            
            self._tasks[task_id]['is_finished'] = True
            return True
            
        return False
    
    def get_all(self) -> list[dict]:
        """
        Get all tasks in the task manager.
        
        Returns:
            list[dict]: List of all tasks as dictionaries
        """
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if tasks were cleared, False if there were no tasks
        """
        if not self._tasks:
            return False
        
        self._tasks.clear()
        return True


# Example usage
def main():
    """Example usage of the TaskManager class."""
    tm = TaskManager()
    
    try:
        # Add tasks
        task1_id = tm.add("Complete project", "Finish the Python project by Friday")
        task2_id = tm.add("Buy groceries", "Milk, eggs, bread")
        task3_id = tm.add("Call mom", "Call mom on her birthday")
        
        print("All tasks:")
        for task in tm.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Finished: {task['is_finished']}")
        
        # Mark a task as finished
        tm.finish(task1_id)
        print(f"\nMarked task {task1_id} as finished")
        
        # Search for tasks
        print("\nSearch results for 'call':")
        for task in tm.search("call"):
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Description: {task['task_description']}")
        
        # Remove a task
        tm.remove(task2_id)
        print(f"\nRemoved task {task2_id}")
        
        print("\nRemaining tasks:")
        for task in tm.get_all():
            status = "✓" if task['is_finished'] else "✗"
            print(f"ID: {task['id']}, Name: {task['task_name']}, Status: {status}")
        
        # Clear all tasks
        tm.clear_all()
        print("\nCleared all tasks")
        print(f"Tasks remaining: {len(tm.get_all())}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
