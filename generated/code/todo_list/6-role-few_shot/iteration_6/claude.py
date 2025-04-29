from typing import List, Dict, Optional, Union
import re
from datetime import datetime


class TaskManager:
    """
    A class for managing a to-do list with the ability to add, remove, search,
    mark tasks as finished, retrieve all tasks, and clear the task list.
    
    Tasks are stored in-memory and are accessible through their unique IDs.
    """
    
    def __init__(self):
        """Initialize the TaskManager with an empty task dictionary and ID counter."""
        self._tasks = {}  # Dict to store tasks with ID as key
        self._next_id = 1  # Counter for assigning unique IDs
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            
        Returns:
            int: The unique ID assigned to the created task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
        
        # Create and store the task
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.now()
        }
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its unique ID.
        
        Args:
            task_id (int): The unique ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is not valid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description containing the given term.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions.
            
        Returns:
            List[Dict]: A list of matching task dictionaries.
            
        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
        
        task_term = task_term.lower().strip()
        results = []
        
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                results.append(self._format_task_output(task))
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed by its unique ID.
        
        Args:
            task_id (int): The unique ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is not valid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id in self._tasks:
            # Only update if not already finished
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                self._tasks[task_id]['completed_at'] = datetime.now()
                return True
            return True  # Task was already finished, still return success
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            List[Dict]: A list of all task dictionaries.
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if the operation was successful.
        """
        self._tasks = {}
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output according to the required format.
        
        Args:
            task (Dict): The task dictionary from internal storage.
            
        Returns:
            Dict: A formatted task dictionary with only the required fields.
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }


def main():
    """Example usage of the TaskManager class."""
    task_manager = TaskManager()
    
    try:
        # Add some tasks
        task1_id = task_manager.add("Complete project", "Finish the Python project by Friday")
        task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread, and cheese")
        task3_id = task_manager.add("Call mom", "Discuss weekend plans")
        
        # Display all tasks
        print("All tasks:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Finished: {task['is_finished']}")
        
        # Mark a task as finished
        task_manager.finish(task2_id)
        
        # Search for tasks
        print("\nSearch results for 'project':")
        for task in task_manager.search("project"):
            print(f"ID: {task['id']}, Name: {task['task_name']}")
        
        # Remove a task
        task_manager.remove(task3_id)
        
        # Display all tasks after modifications
        print("\nAll tasks after modifications:")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Finished: {task['is_finished']}")
        
        # Clear all tasks
        task_manager.clear_all()
        print("\nTasks after clearing:", task_manager.get_all())
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
