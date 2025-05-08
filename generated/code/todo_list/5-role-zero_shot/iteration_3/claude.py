"""
Todo List Application

A console-based todo list application implementing task management functionality
with a focus on clean architecture, efficiency and maintainability.
"""
from typing import List, Dict, Union, Optional
import uuid


class TaskManager:
    """
    Manages a collection of tasks with operations for adding, removing, searching,
    completing, and retrieving tasks.
    
    Tasks are stored in memory with efficient access patterns.
    """
    
    def __init__(self):
        """Initialize the TaskManager with an empty task store."""
        # Using a dictionary for O(1) lookups by ID
        self._tasks = {}
        # Track the next ID to assign
        self._next_id = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The name of the task (must be non-empty)
            task_description: The description of the task (must be non-empty)
            
        Returns:
            int: The unique ID of the newly added task
            
        Raises:
            ValueError: If task_name or task_description is empty
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name must be a non-empty string")
        
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description must be a non-empty string")
        
        # Create task with a unique ID
        task_id = self._next_id
        self._next_id += 1
        
        # Store the task
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The unique ID of the task to remove
            
        Returns:
            bool: True if the task was successfully removed, False otherwise
            
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
        Search for tasks by name or description.
        
        Args:
            task_term: The search term to look for in task names or descriptions
            
        Returns:
            list[dict]: A list of matching task dictionaries
            
        Raises:
            ValueError: If task_term is empty
        """
        # Validate search term
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term must be a non-empty string")
        
        # Convert search term to lowercase for case-insensitive search
        term_lower = task_term.lower()
        
        # Search for matching tasks
        results = []
        for task in self._tasks.values():
            if (term_lower in task["task_name"].lower() or 
                term_lower in task["task_description"].lower()):
                results.append(task.copy())
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique ID of the task to mark as completed
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if task exists and mark it as finished
        if task_id in self._tasks:
            task = self._tasks[task_id]
            # Only update if not already finished
            if not task["is_finished"]:
                task["is_finished"] = True
                return True
            return False  # Task was already finished
        return False  # Task not found
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            list[dict]: A list of all task dictionaries
        """
        # Return a copy of all tasks to prevent external modification
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if tasks were cleared successfully
        """
        self._tasks.clear()
        # Don't reset _next_id to ensure unique IDs even after clearing
        return True
    

# Example usage (optional)
def main():
    """
    Example usage of the TaskManager class.
    """
    manager = TaskManager()
    
    # Add tasks
    task1_id = manager.add("Complete project", "Finish the Python project by Friday")
    task2_id = manager.add("Buy groceries", "Milk, eggs, bread")
    
    # Display all tasks
    print("All Tasks:")
    for task in manager.get_all():
        status = "✓" if task["is_finished"] else "✗"
        print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
    
    # Mark a task as finished
    manager.finish(task1_id)
    
    # Search for tasks
    print("\nSearch Results for 'project':")
    for task in manager.search("project"):
        status = "✓" if task["is_finished"] else "✗"
        print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
    
    # Remove a task
    manager.remove(task2_id)
    
    # Show remaining tasks
    print("\nRemaining Tasks:")
    for task in manager.get_all():
        status = "✓" if task["is_finished"] else "✗"
        print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")


if __name__ == "__main__":
    main()
