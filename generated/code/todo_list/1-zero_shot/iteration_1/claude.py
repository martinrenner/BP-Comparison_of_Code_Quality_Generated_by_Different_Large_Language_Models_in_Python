#!/usr/bin/env python3
"""
Todo List Application

A console-based todo list manager that allows users to add, remove, search,
complete, and manage tasks efficiently.

This implementation follows ISO/IEC 25010 quality standards with focus on:
- Functional suitability
- Performance efficiency
- Compatibility
- Usability
- Reliability
- Security
- Maintainability
- Portability
"""

from typing import List, Dict, Union, Any, Optional
from datetime import datetime
import uuid


class TaskManager:
    """
    Task Manager class that implements the todo list functionality.
    
    This class provides methods to add, remove, search, complete, and manage tasks.
    Tasks are stored in memory with efficient lookup capabilities.
    """

    def __init__(self):
        """Initialize the TaskManager with empty task storage and index structures."""
        # Main storage for tasks: Dictionary with task_id as key for O(1) lookup
        self._tasks: Dict[int, Dict[str, Any]] = {}
        # Index to track the next available ID
        self._next_id: int = 1
        
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): The name of the task (must not be empty)
            task_description (str): The description of the task
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If task_name is empty or not a string
            TypeError: If any argument is not of the correct type
        """
        # Validate input parameters
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
            
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        # Create a new task with a unique ID
        task_id = self._next_id
        self._next_id += 1
        
        # Store the task with all its details
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False,
            "created_at": datetime.now(),
            "completed_at": None
        }
        
        return task_id
        
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove
            
        Returns:
            bool: True if the task was removed, False if it doesn't exist
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Validate input parameter
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
            
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
        
        # Try to remove the task
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions
            
        Returns:
            list[dict]: A list of tasks matching the search term (empty if none found)
            
        Raises:
            TypeError: If task_term is not a string
        """
        # Validate input parameter
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
            
        search_term = task_term.strip().lower()
        
        # Return an empty list for empty search terms
        if not search_term:
            return []
        
        # Search for matching tasks
        results = []
        for task_id, task in self._tasks.items():
            if (search_term in task["task_name"].lower() or 
                search_term in task["task_description"].lower()):
                results.append(self._format_task_output(task))
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as completed
            
        Returns:
            bool: True if the task was marked as completed, False if it doesn't exist
                 or was already completed
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Validate input parameter
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
            
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
        
        # Try to mark the task as completed
        if task_id in self._tasks and not self._tasks[task_id]["is_finished"]:
            self._tasks[task_id]["is_finished"] = True
            self._tasks[task_id]["completed_at"] = datetime.now()
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
            bool: True if tasks were deleted, False if there were no tasks
        """
        if not self._tasks:
            return False
        
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output according to the specified format.
        
        Args:
            task (dict): The task to format
            
        Returns:
            dict: A dictionary with the required fields: id, task_name, 
                  task_description, is_finished
        """
        return {
            "id": task["id"],
            "task_name": task["task_name"],
            "task_description": task["task_description"],
            "is_finished": task["is_finished"]
        }


def main():
    """
    Entry point for the application with example usage.
    """
    # Create a task manager instance
    manager = TaskManager()
    
    # Example usage
    print("=== Todo List Application ===")
    
    # Add some tasks
    task1_id = manager.add("Complete project", "Finish the Python project by Friday")
    task2_id = manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
    task3_id = manager.add("Call mom", "Discuss weekend plans")
    
    print("\n=== All Tasks ===")
    for task in manager.get_all():
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
    
    # Complete a task
    manager.finish(task1_id)
    
    # Search for tasks
    print("\n=== Search Results for 'project' ===")
    for task in manager.search("project"):
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
    
    # Remove a task
    manager.remove(task2_id)
    
    print("\n=== Updated Task List ===")
    for task in manager.get_all():
        status = "✓" if task["is_finished"] else "□"
        print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
    
    # Clear all tasks
    manager.clear_all()
    print("\n=== After Clearing Tasks ===")
    print(f"Tasks remaining: {len(manager.get_all())}")


if __name__ == "__main__":
    main()
