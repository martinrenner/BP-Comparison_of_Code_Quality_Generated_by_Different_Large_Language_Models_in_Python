"""
To-Do List Application

A console-based application that manages tasks with functionality for adding,
removing, searching, and marking tasks as complete.

This module implements a TaskManager class that provides a clean interface
for task management operations.
"""
from typing import List, Dict, Optional, Any
from datetime import datetime


class TaskManager:
    """
    Manages a collection of tasks with operations for adding, removing,
    searching, and completing tasks.
    
    The TaskManager maintains tasks in memory with optimized data structures
    for efficient operations.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Sets up the internal data structures for task management.
        """
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
    
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
            TypeError: If arguments are not of the expected types
        """
        # Input validation
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        # Create task
        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
            "created_at": datetime.now(),
        }
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The unique ID of the task to remove
            
        Returns:
            bool: True if the task was removed, False if the task was not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
        
        # Remove task if it exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict[str, Any]]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term: The search term to look for in task names and descriptions
            
        Returns:
            list[dict]: A list of matching tasks with their details
            
        Raises:
            TypeError: If task_term is not a string
        """
        # Input validation
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        
        # Convert to lowercase for case-insensitive search
        search_term = task_term.lower()
        
        # Search in both task name and description
        results = []
        for task in self._tasks.values():
            if (search_term in task["task_name"].lower() or 
                search_term in task["task_description"].lower()):
                results.append(self._format_task_output(task))
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique ID of the task to mark as completed
            
        Returns:
            bool: True if the task was marked as completed, 
                  False if the task was not found
                  
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
        
        # Update task if it exists
        if task_id in self._tasks:
            # If already finished, we still return True as the operation succeeded
            self._tasks[task_id]["is_finished"] = True
            return True
        
        return False
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all tasks in the task manager.
        
        Returns:
            list[dict]: A list of all tasks with their details
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True indicating the operation was successful
        """
        self._tasks.clear()
        # We don't reset the ID counter to ensure unique IDs across the lifetime
        # of the TaskManager instance
        return True
    
    def _format_task_output(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a task for output, including only the required fields.
        
        Args:
            task: The task dictionary with all fields
            
        Returns:
            dict: A dictionary with only the required output fields
        """
        return {
            "id": task["id"],
            "task_name": task["task_name"],
            "task_description": task["task_description"],
            "is_finished": task["is_finished"]
        }


def main():
    """Example usage of the TaskManager class."""
    manager = TaskManager()
    
    # Add some sample tasks
    task1_id = manager.add("Complete project", "Finish the Python project by Friday")
    task2_id = manager.add("Buy groceries", "Milk, eggs, bread")
    
    print("All tasks:")
    for task in manager.get_all():
        print(f"ID: {task['id']}, Name: {task['task_name']}, " 
              f"Finished: {task['is_finished']}")
    
    # Mark a task as completed
    manager.finish(task1_id)
    print("\nAfter marking task 1 as completed:")
    for task in manager.get_all():
        print(f"ID: {task['id']}, Name: {task['task_name']}, " 
              f"Finished: {task['is_finished']}")
    
    # Search for tasks
    print("\nSearching for 'project':")
    for task in manager.search("project"):
        print(f"ID: {task['id']}, Name: {task['task_name']}, " 
              f"Description: {task['task_description']}")
    
    # Remove a task
    manager.remove(task2_id)
    print("\nAfter removing task 2:")
    for task in manager.get_all():
        print(f"ID: {task['id']}, Name: {task['task_name']}")
    
    # Clear all tasks
    manager.clear_all()
    print("\nAfter clearing all tasks:")
    print(f"Task count: {len(manager.get_all())}")


if __name__ == "__main__":
    main()
