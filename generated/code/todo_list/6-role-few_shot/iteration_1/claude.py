from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid


class TaskManager:
    """
    A class for managing tasks in a to-do list application.
    
    Provides functionality to add, remove, search, and manage tasks
    with proper validation and error handling.
    """
    
    def __init__(self) -> None:
        """Initialize the TaskManager with an empty task store."""
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): A detailed description of the task.
            
        Returns:
            int: The unique ID assigned to the task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
        
        # Create a new task with a unique ID
        task_id = self._next_id
        self._next_id += 1
        
        # Store the task
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
            "created_at": datetime.now()
        }
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The unique identifier of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative or not an integer.
            KeyError: If the task with the given ID does not exist.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
        
        del self._tasks[task_id]
        return True
    
    def search(self, task_term: str) -> List[Dict[str, Any]]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task names or descriptions.
            
        Returns:
            list[dict]: A list of dictionaries containing matching tasks.
            
        Raises:
            ValueError: If task_term is empty or not a string.
        """
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
        
        term = task_term.lower()
        results = []
        
        for task in self._tasks.values():
            if (term in task["task_name"].lower() or 
                term in task["task_description"].lower()):
                results.append(self._format_task_output(task))
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique identifier of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative or not an integer.
            KeyError: If the task with the given ID does not exist.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
        
        # If the task is already finished, return False to indicate no change
        if self._tasks[task_id]["is_finished"]:
            return False
        
        self._tasks[task_id]["is_finished"] = True
        self._tasks[task_id]["completed_at"] = datetime.now()
        return True
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all tasks in the system.
        
        Returns:
            list[dict]: A list of dictionaries containing all tasks with their details.
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the system.
        
        Returns:
            bool: True if all tasks were successfully cleared, False otherwise.
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format task data for external consumption.
        
        Args:
            task (dict): The internal task representation.
            
        Returns:
            dict: A dictionary with the required task information.
        """
        return {
            "id": task["id"],
            "task_name": task["task_name"],
            "task_description": task["task_description"],
            "is_finished": task["is_finished"]
        }


# Example usage:
if __name__ == "__main__":
    task_manager = TaskManager()
    
    # Add some tasks
    task1_id = task_manager.add("Complete project", "Finish the Python to-do list project")
    task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
    task3_id = task_manager.add("Call mom", "Don't forget to call mom for her birthday")
    
    print(f"All tasks: {task_manager.get_all()}")
    
    # Mark a task as finished
    task_manager.finish(task1_id)
    print(f"After marking task {task1_id} as finished: {task_manager.get_all()}")
    
    # Search for tasks
    print(f"Search results for 'project': {task_manager.search('project')}")
    
    # Remove a task
    task_manager.remove(task2_id)
    print(f"After removing task {task2_id}: {task_manager.get_all()}")
    
    # Clear all tasks
    task_manager.clear_all()
    print(f"After clearing all tasks: {task_manager.get_all()}")
