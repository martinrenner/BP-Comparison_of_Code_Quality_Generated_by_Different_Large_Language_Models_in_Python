class TaskManager:
    """
    A task management system that allows for creating, searching, completing,
    and removing tasks.
    
    This implementation follows ISO/IEC 25010 quality standards with focus on
    functionality, performance, maintainability, and security.
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage and ID counter."""
        # Dictionary for O(1) lookups by ID
        self._tasks = {}
        # Counter for generating unique IDs
        self._id_counter = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The name of the task (must not be empty)
            task_description: The description of the task (can be empty)
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If task_name is empty or None
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty")
        
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string")
            
        # Create new task with generated ID
        task_id = self._id_counter
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        
        # Increment ID counter for next task
        self._id_counter += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the task manager.
        
        Args:
            task_id: The unique ID of the task to remove
            
        Returns:
            bool: True if the task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Validate input
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if task exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def search(self, task_term: str) -> list[dict]:
        """
        Search for tasks containing the specified term in name or description.
        
        Args:
            task_term: The search term (case-insensitive)
            
        Returns:
            list[dict]: A list of matching tasks
            
        Raises:
            ValueError: If task_term is None
        """
        # Validate input
        if task_term is None:
            raise ValueError("Search term cannot be None")
            
        if not isinstance(task_term, str):
            raise ValueError("Search term must be a string")
        
        # Convert to lowercase for case-insensitive search
        term_lower = task_term.lower()
        
        # Find matching tasks
        results = []
        for task in self._tasks.values():
            if (term_lower in task["task_name"].lower() or
                term_lower in task["task_description"].lower()):
                results.append(task.copy())
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique ID of the task to complete
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Validate input
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Update task if it exists
        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True
        return False
    
    def get_all(self) -> list[dict]:
        """
        Get all tasks in the task manager.
        
        Returns:
            list[dict]: A list of all tasks
        """
        # Return a copy of tasks to prevent external modification
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if the operation was successful
        """
        self._tasks.clear()
        # We don't reset the ID counter to ensure IDs remain unique throughout the lifetime
        return True

# Example usage
def main():
    """
    Example function demonstrating the usage of TaskManager.
    """
    task_manager = TaskManager()
    
    # Adding tasks
    task1_id = task_manager.add("Complete project", "Finish the Python project by Friday")
    task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
    task3_id = task_manager.add("Call mom", "Don't forget mom's birthday on Saturday")
    
    print("All tasks:")
    for task in task_manager.get_all():
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
    
    # Completing a task
    task_manager.finish(task2_id)
    
    # Searching tasks
    print("\nTasks containing 'project':")
    for task in task_manager.search("project"):
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
    
    # Removing a task
    task_manager.remove(task3_id)
    
    print("\nRemaining tasks:")
    for task in task_manager.get_all():
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
    
    # Clear all tasks
    task_manager.clear_all()
    print(f"\nAll tasks cleared. Task count: {len(task_manager.get_all())}")

if __name__ == "__main__":
    main()
