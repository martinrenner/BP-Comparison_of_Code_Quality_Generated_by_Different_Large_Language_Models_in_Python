#!/usr/bin/env python3
"""
Todo List Application

A console-based task management application that allows users to create, manage, 
and track tasks following ISO/IEC 25010 quality standards.
"""
from typing import List, Dict, Any, Optional
import re
from datetime import datetime


class TaskManager:
    """
    Task management system that handles the creation, retrieval, modification,
    and removal of tasks.
    
    Attributes:
        _tasks (dict): In-memory storage for tasks
        _next_id (int): Counter for assigning unique IDs to tasks
    """
    
    def __init__(self):
        """Initialize TaskManager with empty task storage and ID counter."""
        self._tasks = {}  # Dictionary for O(1) lookups by ID
        self._next_id = 1  # Start task IDs at 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: Name of the task (non-empty string)
            task_description: Description of the task
            
        Returns:
            int: Unique ID assigned to the created task
            
        Raises:
            ValueError: If task_name is empty
        """
        # Validate inputs
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
            
        # Create task with unique ID
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        # Increment ID counter for next task
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: Unique identifier of the task
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is negative
            KeyError: If no task exists with the given ID
        """
        # Validate task_id
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists
        if task_id not in self._tasks:
            raise KeyError(f"No task found with ID {task_id}")
        
        # Remove the task
        del self._tasks[task_id]
        return True
    
    def search(self, task_term: str) -> List[Dict[str, Any]]:
        """
        Search tasks by name or description.
        
        Args:
            task_term: Search term to look for in task names and descriptions
            
        Returns:
            list: List of dictionaries containing matching tasks
            
        Raises:
            ValueError: If search term is empty
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
            
        task_term = task_term.strip().lower()
        matching_tasks = []
        
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                matching_tasks.append(self._format_task_output(task))
                
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: Unique identifier of the task
            
        Returns:
            bool: True if task was successfully marked as completed
            
        Raises:
            ValueError: If task_id is negative
            KeyError: If no task exists with the given ID
        """
        # Validate task_id
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
            
        # Check if task exists
        if task_id not in self._tasks:
            raise KeyError(f"No task found with ID {task_id}")
        
        # Mark task as completed if it's not already
        if not self._tasks[task_id]['is_finished']:
            self._tasks[task_id]['is_finished'] = True
            self._tasks[task_id]['updated_at'] = datetime.now()
            return True
            
        return False  # Task was already completed
        
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks.
        
        Returns:
            list: List of dictionaries containing all tasks
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks.
        
        Returns:
            bool: True if all tasks were successfully removed
        """
        self._tasks = {}
        return True
    
    def _format_task_output(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a task dictionary for output.
        
        Args:
            task: Dictionary containing task data
            
        Returns:
            dict: Dictionary with selected task fields
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


def main():
    """
    Main function to demonstrate TaskManager functionality.
    Provides a simple interactive console interface.
    """
    manager = TaskManager()
    
    print("Todo List Application")
    print("====================")
    
    # Add some sample tasks
    try:
        task1_id = manager.add("Complete project", "Finish the Python project by Friday")
        task2_id = manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
        task3_id = manager.add("Call mom", "Discuss weekend plans")
        
        print("\nAll tasks:")
        for task in manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
        # Mark a task as completed
        manager.finish(task1_id)
        print("\nAfter marking task 1 as completed:")
        
        # Search for tasks
        results = manager.search("project")
        print(f"\nSearch results for 'project': {len(results)} task(s) found")
        for task in results:
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
        # Remove a task
        manager.remove(task3_id)
        print("\nAfter removing task 3:")
        for task in manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
        # Clear all tasks
        manager.clear_all()
        print("\nAfter clearing all tasks:")
        print(f"Tasks remaining: {len(manager.get_all())}")
        
    except (ValueError, KeyError) as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
