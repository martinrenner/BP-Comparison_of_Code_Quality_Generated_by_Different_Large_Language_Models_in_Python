from typing import List, Dict, Union, Optional
from datetime import datetime


class TaskManager:
    """
    A class for managing a to-do list with full CRUD operations.
    
    This implementation uses efficient data structures for storage
    and provides robust error handling for all operations.
    """
    
    def __init__(self):
        """Initialize an empty task manager with a counter for unique IDs."""
        self._tasks = {}  # Dictionary for O(1) lookups by ID
        self._next_id = 1  # Auto-incrementing ID counter
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The name of the task (cannot be empty)
            task_description: The description of the task
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If task_name is empty
        """
        # Validate inputs
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        # Create task with metadata
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.now()
        }
        
        # Increment ID counter for next task
        self._next_id += 1
        
        return task_id
        
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The unique ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is negative
        """
        # Validate task ID
        if task_id < 1:
            raise ValueError("Task ID must be positive")
            
        # Remove task if it exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term: The search term to look for in task names and descriptions
            
        Returns:
            list[dict]: A list of tasks that match the search criteria
            
        Raises:
            ValueError: If search term is empty
        """
        # Validate search term
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
            
        task_term = task_term.lower().strip()
        results = []
        
        # Search through tasks
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                # Return a copy of the task data to prevent modification
                results.append(self._format_task_output(task))
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique ID of the task to mark as complete
            
        Returns:
            bool: True if task was marked complete, False if task doesn't exist
            
        Raises:
            ValueError: If task_id is negative
        """
        # Validate task ID
        if task_id < 1:
            raise ValueError("Task ID must be positive")
            
        # Mark task as finished if it exists
        if task_id in self._tasks:
            # Only update if not already finished
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                self._tasks[task_id]['completed_at'] = datetime.now()
            return True
            
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            list[dict]: A list of all tasks with their details
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if operation was successful
        """
        self._tasks = {}
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output according to the required format.
        
        Args:
            task: The task dictionary to format
            
        Returns:
            dict: A formatted task dictionary with only the required fields
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


# Example usage
if __name__ == "__main__":
    # This block demonstrates usage but won't run when imported as a module
    try:
        manager = TaskManager()
        
        # Add some tasks
        task1_id = manager.add("Complete project", "Finish the Python project by Friday")
        task2_id = manager.add("Buy groceries", "Milk, eggs, bread")
        
        # Mark a task as complete
        manager.finish(task1_id)
        
        # Search for tasks
        results = manager.search("project")
        
        # Get all tasks
        all_tasks = manager.get_all()
        
        # Output results
        print(f"Search results for 'project': {results}")
        print(f"All tasks: {all_tasks}")
        
        # Remove a task
        manager.remove(task2_id)
        
        # Verify removal
        all_tasks = manager.get_all()
        print(f"After removal: {all_tasks}")
        
    except ValueError as e:
        print(f"Error: {e}")
