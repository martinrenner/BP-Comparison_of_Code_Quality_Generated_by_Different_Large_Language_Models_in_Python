from datetime import datetime
from typing import List, Dict, Union, Optional
import re


class TaskManager:
    """
    Task Manager class for managing a todo list.
    
    This class provides functionality to add, remove, search, complete,
    and manage tasks in a todo list application, following ISO/IEC 25010
    quality standards.
    """
    
    def __init__(self):
        """
        Initialize a new TaskManager instance with an empty task store and counter.
        """
        self._tasks: Dict[int, Dict] = {}
        self._task_id_counter: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            
        Returns:
            int: The unique ID of the newly created task.
            
        Raises:
            ValueError: If task_name or task_description is empty or not a string.
        """
        # Validate inputs
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty and must be a string")
        
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string")
        
        # Create a new task with a unique ID
        task_id = self._task_id_counter
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.now(),
            'completed_at': None
        }
        
        # Increment the counter for the next task
        self._task_id_counter += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        # Validate the task ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Remove the task if it exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions.
            
        Returns:
            list[dict]: A list of tasks that match the search term.
            
        Raises:
            ValueError: If task_term is empty or not a string.
        """
        # Validate the search term
        if not isinstance(task_term, str):
            raise ValueError("Search term must be a string")
        
        task_term = task_term.strip().lower()
        
        # Return empty list for empty search terms
        if not task_term:
            return []
        
        # Search for matches in task names and descriptions
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
            task_id (int): The ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        # Validate the task ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Mark the task as complete if it exists and isn't already completed
        if task_id in self._tasks:
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                self._tasks[task_id]['completed_at'] = datetime.now()
                return True
            return False  # Task was already completed
        
        return False  # Task not found
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            list[dict]: A list of all tasks with their details.
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self._tasks.clear()
        # Reset the task ID counter
        self._task_id_counter = 1
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output, including only the required fields.
        
        Args:
            task (dict): The task to format.
            
        Returns:
            dict: A formatted task dictionary with required fields.
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }

    def get_task(self, task_id: int) -> Optional[Dict]:
        """
        Get a single task by ID.
        
        Args:
            task_id (int): The ID of the task to retrieve.
            
        Returns:
            Optional[dict]: The task if found, None otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id in self._tasks:
            return self._format_task_output(self._tasks[task_id])
        
        return None


def main():
    """
    Main function to demonstrate the usage of the TaskManager class.
    """
    task_manager = TaskManager()
    
    print("Todo List Application")
    print("=" * 20)
    
    # Add some sample tasks
    task1_id = task_manager.add("Complete project", "Finish the Python project by Friday")
    task2_id = task_manager.add("Buy groceries", "Get milk, eggs, and bread")
    
    print(f"Added task with ID: {task1_id}")
    print(f"Added task with ID: {task2_id}")
    
    # Display all tasks
    print("\nAll tasks:")
    for task in task_manager.get_all():
        status = "✓" if task['is_finished'] else "□"
        print(f"[{status}] ID: {task['id']} - {task['task_name']}: {task['task_description']}")
    
    # Mark a task as completed
    task_manager.finish(task1_id)
    
    # Display all tasks again
    print("\nAfter completing a task:")
    for task in task_manager.get_all():
        status = "✓" if task['is_finished'] else "□"
        print(f"[{status}] ID: {task['id']} - {task['task_name']}: {task['task_description']}")
    
    # Search for tasks
    print("\nSearch results for 'project':")
    for task in task_manager.search("project"):
        status = "✓" if task['is_finished'] else "□"
        print(f"[{status}] ID: {task['id']} - {task['task_name']}: {task['task_description']}")
    
    # Remove a task
    task_manager.remove(task2_id)
    
    # Display all tasks again
    print("\nAfter removing a task:")
    for task in task_manager.get_all():
        status = "✓" if task['is_finished'] else "□"
        print(f"[{status}] ID: {task['id']} - {task['task_name']}: {task['task_description']}")
    
    # Clear all tasks
    task_manager.clear_all()
    
    # Display all tasks again
    print("\nAfter clearing all tasks:")
    tasks = task_manager.get_all()
    if tasks:
        for task in tasks:
            status = "✓" if task['is_finished'] else "□"
            print(f"[{status}] ID: {task['id']} - {task['task_name']}: {task['task_description']}")
    else:
        print("No tasks available")


if __name__ == "__main__":
    main()
