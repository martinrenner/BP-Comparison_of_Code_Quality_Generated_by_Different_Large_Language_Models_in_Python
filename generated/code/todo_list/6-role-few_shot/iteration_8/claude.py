import uuid
from typing import Dict, List, Any, Optional, Union
from datetime import datetime


class TaskManager:
    """
    A class for managing a to-do list application with task tracking capabilities.
    
    This class provides methods for adding, removing, searching, and managing tasks
    with proper validation and efficient data storage.
    """
    
    def __init__(self) -> None:
        """Initialize the TaskManager with an empty tasks dictionary."""
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            
        Returns:
            int: The unique ID of the newly created task.
            
        Raises:
            ValueError: If task_name or task_description is empty or None.
        """
        # Validate input parameters
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
        
        # Create a new task with given parameters
        task_id = self._next_id
        self._next_id += 1
        
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
            task_id (int): The unique ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is not positive.
            KeyError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise KeyError(f"No task found with ID: {task_id}")
        
        del self._tasks[task_id]
        return True
    
    def search(self, task_term: str) -> List[Dict[str, Any]]:
        """
        Search tasks by name or description.
        
        Args:
            task_term (str): A search term to find in task names or descriptions.
            
        Returns:
            list[dict]: A list of dictionaries containing details of matching tasks.
            
        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
        
        task_term = task_term.lower()
        matching_tasks = []
        
        for task in self._tasks.values():
            if (task_term in task["task_name"].lower() or 
                task_term in task["task_description"].lower()):
                matching_tasks.append(self._format_task_output(task))
                
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is not positive.
            KeyError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise KeyError(f"No task found with ID: {task_id}")
        
        # If already finished, return True without modification
        if self._tasks[task_id]["is_finished"]:
            return True
        
        self._tasks[task_id]["is_finished"] = True
        self._tasks[task_id]["finished_at"] = datetime.now()
        return True
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            list[dict]: A list of dictionaries containing details of all tasks.
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if all tasks were successfully deleted.
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a task for output according to the required format.
        
        Args:
            task (dict): The task to format.
            
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
    # This block demonstrates how to use the TaskManager class
    task_manager = TaskManager()
    
    # Add some tasks
    task1_id = task_manager.add("Complete project", "Finish the Python project by Friday")
    task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
    
    # Display all tasks
    print("All tasks:")
    for task in task_manager.get_all():
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']} - {task['task_description']}")
    
    # Mark a task as complete
    task_manager.finish(task1_id)
    
    # Search for tasks
    print("\nSearch results for 'project':")
    for task in task_manager.search("project"):
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']} - {task['task_description']}")
    
    # Remove a task
    task_manager.remove(task2_id)
    
    # Show all tasks after modifications
    print("\nRemaining tasks:")
    for task in task_manager.get_all():
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']} - {task['task_description']}")
