"""
Todo List Application
A console-based task management system that follows ISO/IEC 25010 standards.
"""
from typing import List, Dict, Union, Optional
import datetime


class TaskManager:
    """
    Manages a collection of tasks with operations to create, search,
    update, and delete tasks.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task dictionary and ID counter."""
        self._tasks = {}  # Using a dictionary for O(1) lookups by ID
        self._next_id = 1  # Simple auto-incrementing ID counter

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task manager.
        
        Args:
            task_name: The name of the task (non-empty string)
            task_description: The description of the task
            
        Returns:
            int: The unique identifier for the added task
            
        Raises:
            ValueError: If task_name is empty
        """
        # Validate inputs
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        if task_description is None:
            task_description = ""  # Allow empty descriptions
        
        # Create a new task
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'name': task_name.strip(),
            'description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        
        self._next_id += 1
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.
        
        Args:
            task_id: The unique identifier of the task to remove
            
        Returns:
            bool: True if the task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is negative
            KeyError: If task doesn't exist
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
        
        del self._tasks[task_id]
        return True
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks where the name or description contains the search term.
        
        Args:
            task_term: The search term to look for
            
        Returns:
            List of task dictionaries that match the search criteria
        """
        if not task_term or not task_term.strip():
            return []
        
        search_term = task_term.lower().strip()
        results = []
        
        for task in self._tasks.values():
            if (search_term in task['name'].lower() or 
                search_term in task['description'].lower()):
                results.append(self._format_task_output(task))
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.
        
        Args:
            task_id: The unique identifier of the task to mark as completed
            
        Returns:
            bool: True if the task was successfully marked as completed
            
        Raises:
            ValueError: If task_id is negative
            KeyError: If task doesn't exist
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
        
        # Only update if not already finished
        if not self._tasks[task_id]['is_finished']:
            self._tasks[task_id]['is_finished'] = True
            self._tasks[task_id]['updated_at'] = datetime.datetime.now()
        
        return True
    
    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks with their details.
        
        Returns:  
            A list of dictionaries, each representing a task
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Removes all tasks from the task manager.
        
        Returns:
            bool: True if all tasks were successfully cleared
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Helper method to format a task for output according to the required format.
        
        Args:
            task: The internal task dictionary
            
        Returns:
            A dictionary with the required output format
        """
        return {
            'id': task['id'],
            'task_name': task['name'],
            'task_description': task['description'],
            'is_finished': task['is_finished']
        }


def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    manager = TaskManager()
    
    try:
        # Add some tasks
        task1_id = manager.add("Complete project", "Finish the Python todo application")
        task2_id = manager.add("Buy groceries", "Milk, eggs, bread")
        task3_id = manager.add("Exercise", "30 minutes cardio")
        
        # Display all tasks
        print("All tasks:")
        for task in manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
        # Mark a task as completed
        manager.finish(task1_id)
        
        # Search for tasks
        print("\nSearch results for 'project':")
        results = manager.search("project")
        for task in results:
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
        # Remove a task
        manager.remove(task2_id)
        
        # Show updated task list
        print("\nUpdated task list:")
        for task in manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
        # Clear all tasks
        manager.clear_all()
        print("\nTasks after clearing:", manager.get_all())
        
    except (ValueError, KeyError) as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
