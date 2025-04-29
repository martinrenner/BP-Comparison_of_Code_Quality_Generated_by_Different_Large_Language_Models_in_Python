#!/usr/bin/env python3
"""
Todo List Application

A console-based task management application that allows users to create, manage,
and track tasks with full CRUD operations and search functionality.

This implementation follows ISO/IEC 25010 quality standards.
"""
from typing import List, Dict, Union, Optional
import datetime
import re


class TaskManager:
    """
    Manages a collection of tasks with operations for adding, removing,
    searching, and updating task status.
    
    Attributes:
        _tasks (Dict[int, Dict]): Internal storage for tasks
        _next_id (int): Auto-incrementing ID for task creation
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks = {}
        self._next_id = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The title/name of the task
            task_description: A detailed description of the task
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If task_name or task_description is empty
        """
        # Validate inputs
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty")
        
        # Create task with unique ID
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        # Increment ID for next task
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is negative
        """
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
        
        # Remove task if it exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks that match the given term in name or description.
        
        Args:
            task_term: The search term to look for in task name or description
            
        Returns:
            list: A list of task dictionaries that match the search criteria
            
        Raises:
            ValueError: If task_term is empty
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
        
        task_term = task_term.lower().strip()
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
            task_id: The unique identifier of the task to mark as complete
            
        Returns:
            bool: True if task was successfully marked as completed, False otherwise
            
        Raises:
            ValueError: If task_id is negative
        """
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id in self._tasks:
            # Only update if task isn't already finished
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                self._tasks[task_id]['completed_at'] = datetime.datetime.now().isoformat()
                return True
            return True  # Task was already finished
        
        return False  # Task not found
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            list: A list of all tasks with their details
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if operation was successful
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output, ensuring consistent structure.
        
        Args:
            task: The internal task representation
            
        Returns:
            dict: A dictionary with the standard output format
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


def main():
    """Run the Todo List Application with a simple command-line interface."""
    task_manager = TaskManager()
    
    # Example data
    try:
        task_manager.add("Implement Todo App", "Create a Python console-based todo list application")
        task_manager.add("Write Tests", "Create comprehensive tests for the todo app")
        task_manager.add("Document Code", "Add proper documentation to all classes and methods")
        
        task_manager.finish(1)  # Mark first task as complete
        
        print("All Tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "☐"
            print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
        
        print("\nSearch Results for 'test':")
        search_results = task_manager.search("test")
        for task in search_results:
            status = "✓" if task['is_finished'] else "☐"
            print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
    
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
