from typing import List, Dict, Union, Optional
import uuid

class TaskManager:
    """
    A task manager that handles to-do list operations.
    
    This class provides functionality to add, remove, search, and manage tasks
    with proper validation and error handling.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with an empty task storage.
        
        The tasks are stored in a dictionary for efficient lookups by ID.
        """
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the to-do list.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.
            
        Returns:
            int: The unique ID of the newly added task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty")
        
        task_id = self._next_id
        self._next_id += 1
        
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the to-do list by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative.
        """
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
        
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
            ValueError: If task_term is empty.
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
        
        task_term = task_term.lower().strip()
        results = []
        
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                results.append(task.copy())
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative.
        """
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id in self._tasks:
            self._tasks[task_id]['is_finished'] = True
            return True
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Get all tasks in the to-do list.
        
        Returns:
            list[dict]: A list of all tasks with their details.
        """
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the to-do list.
        
        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self._tasks.clear()
        return True


def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    manager = TaskManager()
    
    # Example usage
    try:
        # Add tasks
        task1_id = manager.add("Complete project", "Finish the Python project before deadline")
        task2_id = manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
        task3_id = manager.add("Exercise", "Go for a 30-minute run")
        
        print("All tasks after adding:")
        for task in manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
        # Mark a task as completed
        manager.finish(task1_id)
        print(f"\nTask {task1_id} marked as completed")
        
        # Search for tasks
        results = manager.search("project")
        print("\nSearch results for 'project':")
        for task in results:
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Description: {task['task_description']}, "
                  f"Completed: {task['is_finished']}")
        
        # Remove a task
        manager.remove(task2_id)
        print(f"\nTask {task2_id} removed")
        
        print("\nAll tasks after modifications:")
        for task in manager.get_all():
            print(f"ID: {task['id']}, Name: {task['task_name']}, "
                  f"Completed: {task['is_finished']}")
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
