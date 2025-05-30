class TaskManager:
    """Task Manager class that handles todo list operations.
    
    This class implements the required interface for a todo list application,
    providing functionality to add, remove, search, finish, and retrieve tasks.
    """

    def __init__(self):
        """Initialize an empty TaskManager with a task dictionary and ID counter."""
        self._tasks = {}  # Dictionary to store tasks with ID as key
        self._next_id = 1  # Counter for generating unique task IDs
    
    def add(self, task_name: str, task_description: str) -> int:
        """Add a new task to the task manager.
        
        Args:
            task_name: Name of the task (non-empty string)
            task_description: Description of the task (can be empty)
            
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
            
        # Create task with a unique ID
        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False
        }
        
        # Increment ID counter for next task
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """Remove a task by its ID.
        
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
            
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> list[dict]:
        """Search for tasks by name or description.
        
        Args:
            task_term: The search term to look for in task names or descriptions
            
        Returns:
            list[dict]: List of matching tasks (empty if no matches)
            
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
            if (task_term in task["name"].lower() or 
                task_term in task["description"].lower()):
                results.append(task.copy())
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """Mark a task as completed by its ID.
        
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
            
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
            
        if task_id in self._tasks:
            # Only update if not already finished
            if not self._tasks[task_id]["is_finished"]:
                self._tasks[task_id]["is_finished"] = True
                return True
            return True  # Return true even if already finished
        
        return False
    
    def get_all(self) -> list[dict]:
        """Retrieve all tasks.
        
        Returns:
            list[dict]: List of all tasks (empty if no tasks exist)
        """
        # Return a copy of each task to prevent external modification
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """Delete all tasks.
        
        Returns:
            bool: True if tasks were cleared (also true if already empty)
        """
        self._tasks.clear()
        # We don't reset the ID counter to ensure previously used IDs aren't reused
        return True
