#!/usr/bin/env python3
"""
Todo List Application

A console-based task management system that allows users to create, track,
and manage tasks according to ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional, Any, Union
import datetime
import re


class TaskManager:
    """
    Manages a collection of tasks with operations for adding, removing,
    searching, completing, and retrieving tasks.
    
    This class implements task management with optimized data structures
    for efficient lookups, insertions and deletions.
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks = {}  # Dictionary for O(1) lookups by ID
        self._next_id = 1  # Auto-increment ID counter
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The name/title of the task
            task_description: A detailed description of the task
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If task_name or task_description is empty or invalid
        """
        # Input validation
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
        
        # Sanitize inputs (basic security measure)
        task_name = task_name.strip()
        task_description = task_description.strip()
        
        if not task_name:
            raise ValueError("Task name cannot be just whitespace")
            
        # Create task
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'is_finished': False,
            'created_at': datetime.datetime.now(),
            'completed_at': None
        }
        
        self._next_id += 1
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The unique identifier of the task to remove
            
        Returns:
            bool: True if the task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Input validation
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists
        if task_id not in self._tasks:
            return False
            
        # Remove task
        del self._tasks[task_id]
        return True
    
    def search(self, task_term: str) -> List[Dict[str, Any]]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term: The search term to match against task names and descriptions
            
        Returns:
            list: A list of dictionaries containing matching tasks
            
        Raises:
            ValueError: If task_term is empty or invalid
        """
        # Input validation
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
        
        # Sanitize input
        task_term = task_term.strip().lower()
        if not task_term:
            raise ValueError("Search term cannot be just whitespace")
        
        # Find matching tasks
        results = []
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                results.append(self._format_task_output(task))
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique identifier of the task to mark as completed
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Input validation
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists
        if task_id not in self._tasks:
            return False
            
        # Don't mark already finished tasks as finished again
        if self._tasks[task_id]['is_finished']:
            return True
            
        # Mark task as completed
        self._tasks[task_id]['is_finished'] = True
        self._tasks[task_id]['completed_at'] = datetime.datetime.now()
        return True
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks.
        
        Returns:
            list: A list of dictionaries containing all tasks
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks.
        
        Returns:
            bool: True if all tasks were successfully removed
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format task data for output.
        
        Args:
            task: The task dictionary to format
            
        Returns:
            dict: A dictionary with standardized task information
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


def main():
    """
    Main function to demonstrate task manager functionality.
    """
    task_manager = TaskManager()
    
    print("Todo List Application")
    print("---------------------")
    
    # Example operations
    try:
        # Adding tasks
        task1_id = task_manager.add("Complete project", "Finish the Python project by Friday")
        task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread")
        
        print("\nAdded tasks:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, " 
                  f"Finished: {task['is_finished']}")
        
        # Marking a task as finished
        task_manager.finish(task1_id)
        print("\nAfter marking first task as finished:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, " 
                  f"Finished: {task['is_finished']}")
        
        # Searching for tasks
        print("\nSearching for 'project':")
        for task in task_manager.search("project"):
            print(f"ID: {task['id']}, Name: {task['task_name']}, " 
                  f"Description: {task['task_description']}")
        
        # Removing a task
        task_manager.remove(task2_id)
        print("\nAfter removing second task:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}")
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
