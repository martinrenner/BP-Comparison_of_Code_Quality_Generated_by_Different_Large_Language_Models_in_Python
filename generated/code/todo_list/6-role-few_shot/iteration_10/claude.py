from typing import List, Dict, Union, Optional
import re


class TaskManager:
    """
    A class that manages a to-do list with various operations like adding, removing,
    searching, and marking tasks as completed.
    
    Attributes:
        _tasks (dict): A dictionary to store tasks with their IDs as keys.
        _next_id (int): A counter to assign unique IDs to new tasks.
    """

    def __init__(self):
        """Initialize an empty task manager."""
        self._tasks = {}  # Using a dictionary for O(1) lookups by ID
        self._next_id = 1  # Start task IDs at 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            
        Returns:
            int: The unique ID assigned to the new task.
            
        Raises:
            ValueError: If the task name or description is empty.
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
        
        # Create and store the new task
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
        Remove a task from the task manager.
        
        Args:
            task_id (int): The unique ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If the task ID is negative or not an integer.
            KeyError: If the task ID does not exist.
        """
        # Validate input
        self._validate_task_id(task_id)
        
        # Check if task exists
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
        
        # Remove the task
        del self._tasks[task_id]
        return True
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task names or descriptions.
            
        Returns:
            list[dict]: A list of tasks matching the search term.
            
        Raises:
            ValueError: If the search term is empty or not a string.
        """
        # Validate input
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
        
        # Perform case-insensitive search
        result = []
        pattern = re.compile(re.escape(task_term), re.IGNORECASE)
        
        for task in self._tasks.values():
            if (pattern.search(task["task_name"]) or 
                pattern.search(task["task_description"])):
                result.append(task.copy())  # Return a copy to prevent modification
        
        return result
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If the task ID is negative or not an integer.
            KeyError: If the task ID does not exist.
        """
        # Validate input
        self._validate_task_id(task_id)
        
        # Check if task exists
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
        
        # If task is already finished, return False to indicate no change
        if self._tasks[task_id]["is_finished"]:
            return False
        
        # Mark task as finished
        self._tasks[task_id]["is_finished"] = True
        return True
    
    def get_all(self) -> List[Dict]:
        """
        Get all tasks in the task manager.
        
        Returns:
            list[dict]: A list of all tasks.
        """
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self._tasks.clear()
        return True
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate that a task ID is positive and an integer.
        
        Args:
            task_id (int): The task ID to validate.
            
        Raises:
            ValueError: If the task ID is not positive or not an integer.
        """
        if not isinstance(task_id, int):
            raise ValueError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be positive")


# Example usage
if __name__ == "__main__":
    # This block demonstrates how to use the TaskManager class
    # It will only execute when this file is run directly
    manager = TaskManager()
    
    # Add some tasks
    task1_id = manager.add("Buy groceries", "Get milk, eggs, and bread")
    task2_id = manager.add("Finish report", "Complete quarterly sales report")
    task3_id = manager.add("Call mom", "Wish her happy birthday")
    
    # Display all tasks
    print("All tasks:")
    for task in manager.get_all():
        status = "Completed" if task["is_finished"] else "Pending"
        print(f"ID: {task['id']}, Name: {task['task_name']}, Status: {status}")
    
    # Complete a task
    manager.finish(task1_id)
    
    # Search for tasks
    print("\nTasks containing 'report':")
    for task in manager.search("report"):
        status = "Completed" if task["is_finished"] else "Pending"
        print(f"ID: {task['id']}, Name: {task['task_name']}, Status: {status}")
    
    # Remove a task
    manager.remove(task2_id)
    
    # Display all tasks again
    print("\nRemaining tasks:")
    for task in manager.get_all():
        status = "Completed" if task["is_finished"] else "Pending"
        print(f"ID: {task['id']}, Name: {task['task_name']}, Status: {status}")
