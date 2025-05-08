from typing import List, Dict, Union, Optional
import time


class TaskManager:
    """
    A task manager that handles creating, retrieving, updating, and deleting tasks.
    
    This class implements a complete task management system with features for adding,
    removing, searching, and managing tasks.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task storage and ID counter."""
        # Dictionary to store tasks with task_id as key
        self._tasks: Dict[int, Dict] = {}
        # Counter for generating unique task IDs
        self._id_counter: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.
            
        Returns:
            int: The unique ID of the newly created task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Validate inputs
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        # Create a new task
        task_id = self._id_counter
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
            "created_at": time.time()
        }
        
        # Increment the ID counter for the next task
        self._id_counter += 1
        
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative or not an integer.
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
            
        # Check if task exists and remove it
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
            list[dict]: A list of tasks that match the search criteria.
            
        Raises:
            ValueError: If task_term is empty.
        """
        # Validate search term
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")
            
        # Search for tasks matching the term
        results = []
        search_term_lower = task_term.lower()
        
        for task in self._tasks.values():
            if (search_term_lower in task["task_name"].lower() or 
                search_term_lower in task["task_description"].lower()):
                results.append(self._format_task_output(task))
                
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is negative or not an integer.
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
            
        # Check if task exists and mark it as finished
        if task_id in self._tasks:
            if self._tasks[task_id]["is_finished"]:
                return False  # Task already finished
            self._tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Get all tasks stored in the task manager.
        
        Returns:
            list[dict]: A list of all tasks.
        """
        return [self._format_task_output(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.
        
        Returns:
            bool: True if tasks were cleared successfully.
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format a task for output.
        
        Args:
            task (dict): The task to format.
            
        Returns:
            dict: A formatted task dictionary with required fields.
        """
        return {
            "id": task["id"],
            "task_name": task["task_name"],
            "task_description": task["task_description"],
            "is_finished": task["is_finished"]
        }


# Example usage:
if __name__ == "__main__":
    # Create a task manager
    manager = TaskManager()
    
    try:
        # Add some tasks
        task1_id = manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
        task2_id = manager.add("Finish report", "Complete the quarterly sales report")
        task3_id = manager.add("Call mom", "Wish her a happy birthday")
        
        # Display all tasks
        print("All tasks:")
        for task in manager.get_all():
            status = "✓" if task["is_finished"] else "✗"
            print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as completed
        manager.finish(task1_id)
        print(f"\nMarked task {task1_id} as finished")
        
        # Search for tasks
        print("\nSearch results for 'report':")
        for task in manager.search("report"):
            status = "✓" if task["is_finished"] else "✗"
            print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
        
        # Remove a task
        manager.remove(task3_id)
        print(f"\nRemoved task {task3_id}")
        
        # Display all tasks after modifications
        print("\nUpdated task list:")
        for task in manager.get_all():
            status = "✓" if task["is_finished"] else "✗"
            print(f"{task['id']}. [{status}] {task['task_name']}: {task['task_description']}")
        
        # Clear all tasks
        manager.clear_all()
        print("\nCleared all tasks")
        print(f"Tasks remaining: {len(manager.get_all())}")
        
    except ValueError as e:
        print(f"Error: {e}")
