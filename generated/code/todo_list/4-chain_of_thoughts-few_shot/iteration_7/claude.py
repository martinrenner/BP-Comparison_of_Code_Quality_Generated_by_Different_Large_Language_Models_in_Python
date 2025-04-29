#!/usr/bin/env python3
"""
Todo List Application

A console-based task management system that allows users to add, remove,
search, complete, and manage tasks efficiently.

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

from typing import Dict, List, Optional, Union
import time


class TaskManager:
    """
    Manages a collection of tasks with operations for adding, removing,
    searching, and completing tasks.
    
    Attributes:
        _tasks (Dict[int, Dict]): Dictionary storing tasks with task_id as key
        _next_id (int): Counter for generating unique task IDs
    """
    
    def __init__(self):
        """Initialize an empty task manager."""
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task
            task_description (str): The detailed description of the task
            
        Returns:
            int: The unique ID assigned to the new task
            
        Raises:
            ValueError: If task_name or task_description is empty
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
        
        # Create task object
        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
            "created_at": time.time()
        }
        
        # Increment the ID counter for next task
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if task exists and remove it
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks matching the given term in name or description.
        
        Args:
            task_term (str): The search term to look for
            
        Returns:
            List[Dict]: List of tasks matching the search term
            
        Raises:
            ValueError: If task_term is empty
        """
        # Validate search term
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
        
        # Perform case-insensitive search
        search_term = task_term.lower()
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
            task_id (int): The unique ID of the task to mark as completed
            
        Returns:
            bool: True if task was successfully marked as completed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if task exists and update its status
        if task_id in self._tasks:
            # Only update if not already finished
            if not self._tasks[task_id]["is_finished"]:
                self._tasks[task_id]["is_finished"] = True
                self._tasks[task_id]["completed_at"] = time.time()
                return True
            return True  # Task already finished
        
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            List[Dict]: List of all tasks with their details
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks.
        
        Returns:
            bool: True if all tasks were successfully cleared
        """
        self._tasks.clear()
        # Resetting next_id is optional, but makes testing easier
        self._next_id = 1
        return True
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """
        Retrieve a specific task by its ID.
        
        Args:
            task_id (int): The unique ID of the task to retrieve
            
        Returns:
            Optional[Dict]: The task if found, None otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Return the task if it exists
        if task_id in self._tasks:
            return self._format_task_output(self._tasks[task_id])
        
        return None
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for external representation.
        
        Args:
            task (Dict): The internal task representation
            
        Returns:
            Dict: The formatted task with only the public fields
        """
        return {
            "id": task["id"],
            "task_name": task["task_name"],
            "task_description": task["task_description"],
            "is_finished": task["is_finished"]
        }


def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    task_manager = TaskManager()
    
    # Example usage
    try:
        # Add some tasks
        task1_id = task_manager.add("Complete project", "Finish the Python project by Friday")
        task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
        task3_id = task_manager.add("Call mom", "Remember to call mom on her birthday")
        
        print("All tasks:")
        for task in task_manager.get_all():
            status = "Completed" if task["is_finished"] else "Pending"
            print(f"ID: {task['id']} | {task['task_name']} | {status}")
        
        # Mark a task as completed
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("\nSearch results for 'project':")
        for task in task_manager.search("project"):
            status = "Completed" if task["is_finished"] else "Pending"
            print(f"ID: {task['id']} | {task['task_name']} | {status}")
        
        # Remove a task
        task_manager.remove(task2_id)
        
        print("\nAll tasks after removal:")
        for task in task_manager.get_all():
            status = "Completed" if task["is_finished"] else "Pending"
            print(f"ID: {task['id']} | {task['task_name']} | {status}")
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
