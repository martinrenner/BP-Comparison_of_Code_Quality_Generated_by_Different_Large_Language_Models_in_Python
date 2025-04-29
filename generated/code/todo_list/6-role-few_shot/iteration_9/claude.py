from typing import List, Dict, Optional, Union
import re


class TaskManager:
    """
    A class to manage a to-do list with tasks.
    
    This class provides functionality to add, remove, search, finish, and manage tasks
    in a to-do list. Tasks are stored in memory with unique IDs.
    """

    def __init__(self):
        """Initialize an empty TaskManager with a counter for task IDs."""
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            
        Returns:
            int: The unique ID of the newly added task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Validate inputs
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty")
            
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative.
            KeyError: If no task with the given ID exists.
        """
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id not in self._tasks:
            raise KeyError(f"No task found with ID {task_id}")
            
        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description containing the given term.
        
        Args:
            task_term (str): The term to search for in task names and descriptions.
            
        Returns:
            List[Dict]: A list of dictionaries containing matching tasks.
            
        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
            
        task_term = task_term.strip().lower()
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
            task_id (int): The ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative.
            KeyError: If no task with the given ID exists.
        """
        if task_id < 1:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id not in self._tasks:
            raise KeyError(f"No task found with ID {task_id}")
            
        # Only update if not already finished
        if not self._tasks[task_id]['is_finished']:
            self._tasks[task_id]['is_finished'] = True
            return True
            
        return False  # Task was already finished

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            List[Dict]: A list of dictionaries containing all tasks.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if all tasks were successfully deleted, False otherwise.
        """
        self._tasks.clear()
        return True


def main():
    """Simple demonstration of the TaskManager class."""
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        task1_id = task_manager.add("Complete project", "Finish the Python project by Friday")
        task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
        task3_id = task_manager.add("Call John", "Discuss the meeting agenda")
        
        print("All tasks:")
        for task in task_manager.get_all():
            status = "Completed" if task['is_finished'] else "Pending"
            print(f"[{task['id']}] {task['task_name']} - {status}")
            print(f"    {task['task_description']}")
        
        # Mark a task as completed
        task_manager.finish(task1_id)
        
        # Search for tasks containing "meet"
        print("\nSearch results for 'meet':")
        for task in task_manager.search("meet"):
            status = "Completed" if task['is_finished'] else "Pending"
            print(f"[{task['id']}] {task['task_name']} - {status}")
            print(f"    {task['task_description']}")
        
        # Remove a task
        task_manager.remove(task2_id)
        
        print("\nAfter removing task 2:")
        for task in task_manager.get_all():
            status = "Completed" if task['is_finished'] else "Pending"
            print(f"[{task['id']}] {task['task_name']} - {status}")
            print(f"    {task['task_description']}")
        
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
