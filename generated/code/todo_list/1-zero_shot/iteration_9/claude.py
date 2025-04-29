from typing import List, Dict, Optional, Union
import re

class TaskManager:
    """
    TaskManager class for managing a todo list.
    
    This class provides functionality to add, remove, search, finish, retrieve all,
    and clear all tasks in a todo list. Tasks are stored in memory and each has a
    unique identifier.
    """
    
    def __init__(self):
        """Initialize an empty task manager with a tasks dictionary and ID counter."""
        self._tasks = {}  # Dictionary to store tasks: {id: {name, description, is_finished}}
        self._id_counter = 1  # Counter for generating unique task IDs
    
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
            TypeError: If inputs are not strings
        """
        # Validate inputs
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        # Create task with a unique ID
        task_id = self._id_counter
        self._tasks[task_id] = {
            'name': task_name.strip(),
            'description': task_description.strip(),
            'is_finished': False
        }
        self._id_counter += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: The ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Validate input
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
            
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
            
        # Remove task if it exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search tasks by name or description.
        
        Args:
            task_term: The search term to look for in task names and descriptions
            
        Returns:
            List[Dict]: A list of tasks matching the search term
            
        Raises:
            TypeError: If task_term is not a string
        """
        # Validate input
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        
        # If search term is empty, return empty list (no matches)
        if not task_term.strip():
            return []
            
        results = []
        search_pattern = re.compile(re.escape(task_term.strip()), re.IGNORECASE)
        
        for task_id, task in self._tasks.items():
            if (search_pattern.search(task['name']) or
                search_pattern.search(task['description'])):
                results.append(self._format_task(task_id, task))
                
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The ID of the task to mark as completed
            
        Returns:
            bool: True if task was successfully marked as completed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Validate input
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
            
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
            
        # Mark task as finished if it exists
        if task_id in self._tasks:
            # If task is already finished, return False to indicate no change
            if self._tasks[task_id]['is_finished']:
                return False
            
            self._tasks[task_id]['is_finished'] = True
            return True
            
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            List[Dict]: A list of all tasks with their details
        """
        return [self._format_task(task_id, task) for task_id, task in self._tasks.items()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if tasks were cleared, False if no tasks existed
        """
        if not self._tasks:
            return False
            
        self._tasks.clear()
        return True
    
    def _format_task(self, task_id: int, task: Dict) -> Dict:
        """
        Format a task for output with standard structure.
        
        Args:
            task_id: The ID of the task
            task: The task dictionary with name, description, and status
            
        Returns:
            Dict: A formatted task dictionary with id, name, description, and is_finished
        """
        return {
            'id': task_id,
            'task_name': task['name'],
            'task_description': task['description'],
            'is_finished': task['is_finished']
        }


def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    task_manager = TaskManager()
    
    # Example usage
    try:
        print("Adding tasks...")
        task1_id = task_manager.add("Implement TaskManager", "Create a Todo list app in Python")
        task2_id = task_manager.add("Write tests", "Ensure code quality with unit tests")
        task3_id = task_manager.add("Document code", "Add proper docstrings and comments")
        
        print("\nAll tasks:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Finished: {task['is_finished']}")
        
        print("\nMarking task as finished...")
        task_manager.finish(task1_id)
        
        print("\nSearching for 'test'...")
        for task in task_manager.search("test"):
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Description: {task['task_description']}")
        
        print("\nRemoving task...")
        task_manager.remove(task3_id)
        
        print("\nRemaining tasks:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Finished: {task['is_finished']}")
        
        print("\nClearing all tasks...")
        task_manager.clear_all()
        
        print("\nTasks after clearing:")
        print(task_manager.get_all())
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
