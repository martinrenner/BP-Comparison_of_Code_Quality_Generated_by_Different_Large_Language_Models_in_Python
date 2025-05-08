"""
Todo List Application

A console-based todo list manager with functionality to add, remove, search,
complete tasks and more, implemented according to ISO/IEC 25010 quality standards.
"""

from typing import Dict, List, Optional, Union
import datetime


class TaskManager:
    """
    Manages a collection of tasks with operations for adding, removing,
    searching, and marking tasks as complete.
    
    Attributes:
        _tasks (Dict[int, Dict]): Internal storage for task data
        _next_id (int): Counter for generating unique task IDs
    """

    def __init__(self):
        """Initializes an empty task manager with a task counter."""
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task manager.
        
        Args:
            task_name (str): The name of the task
            task_description (str): The description of the task
            
        Returns:
            int: The unique ID assigned to the new task
            
        Raises:
            ValueError: If task_name or task_description is empty
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
            
        # Create task
        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
            "created_at": datetime.datetime.now(),
            "completed_at": None
        }
        self._next_id += 1
        
        return task_id
        
    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove
            
        Returns:
            bool: True if the task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
        
    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions
            
        Returns:
            List[Dict]: A list of tasks matching the search term
            
        Raises:
            ValueError: If search term is empty
        """
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
            
        task_term = task_term.lower()
        results = []
        
        for task in self._tasks.values():
            if (task_term in task["task_name"].lower() or 
                task_term in task["task_description"].lower()):
                results.append(self._format_task_output(task))
                
        return results
        
    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as completed
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id in self._tasks:
            # Only update if the task isn't already finished
            if not self._tasks[task_id]["is_finished"]:
                self._tasks[task_id]["is_finished"] = True
                self._tasks[task_id]["completed_at"] = datetime.datetime.now()
            return True
        return False
        
    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.
        
        Returns:
            List[Dict]: A list of all tasks with their details
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
        
    def clear_all(self) -> bool:
        """
        Removes all tasks from the task manager.
        
        Returns:
            bool: True if the operation was successful
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Creates a standardized format for task output.
        
        Args:
            task (Dict): The internal task dictionary
            
        Returns:
            Dict: A dictionary with standardized task information
        """
        return {
            "id": task["id"],
            "task_name": task["task_name"],
            "task_description": task["task_description"],
            "is_finished": task["is_finished"]
        }


def main():
    """
    Main function to demonstrate TaskManager functionality with a simple interactive console.
    """
    manager = TaskManager()
    
    # Add sample tasks
    try:
        task1_id = manager.add("Complete project", "Finish the Python project by Friday")
        task2_id = manager.add("Buy groceries", "Milk, bread, eggs, and vegetables")
        print(f"Added sample tasks with IDs: {task1_id}, {task2_id}")
        
        # Display all tasks
        print("\nAll Tasks:")
        for task in manager.get_all():
            status = "✓" if task["is_finished"] else "☐"
            print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
        
        # Search for a task
        search_results = manager.search("project")
        print(f"\nSearch results for 'project': {len(search_results)} task(s) found")
        for task in search_results:
            print(f"- {task['task_name']}")
        
        # Mark a task as completed
        manager.finish(task1_id)
        print(f"\nMarked task {task1_id} as completed")
        
        # Display all tasks again
        print("\nUpdated Tasks:")
        for task in manager.get_all():
            status = "✓" if task["is_finished"] else "☐"
            print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
            
        # Remove a task
        manager.remove(task2_id)
        print(f"\nRemoved task {task2_id}")
        
        # Display remaining tasks
        print("\nRemaining Tasks:")
        for task in manager.get_all():
            status = "✓" if task["is_finished"] else "☐"
            print(f"[{status}] {task['id']}: {task['task_name']} - {task['task_description']}")
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
