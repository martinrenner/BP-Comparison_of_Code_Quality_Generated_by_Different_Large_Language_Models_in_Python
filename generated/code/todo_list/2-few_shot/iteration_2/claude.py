class TaskManager:
    """
    A task management class that provides functionality to create, modify,
    search, and manage to-do tasks.
    
    This class implements the following ISO/IEC 25010 quality characteristics:
    - Functional suitability (correctness, completeness)
    - Performance efficiency (optimized data structures)
    - Usability (clear interface)
    - Reliability (error handling)
    - Maintainability (modular, documented code)
    - Security (input validation)
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task dictionary and counter."""
        self._tasks = {}  # Dictionary to store tasks with ID as key
        self._id_counter = 1  # Counter for task IDs

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
        # Input validation
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
            
        # Create a new task
        task_id = self._id_counter
        self._tasks[task_id] = {
            'id': task_id,
            'name': task_name,
            'description': task_description,
            'is_finished': False
        }
        
        # Increment the ID counter
        self._id_counter += 1
        
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The ID of the task to remove.
            
        Returns:
            bool: True if the task was removed successfully, False otherwise.
            
        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if task exists and remove it
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False

    def search(self, task_term: str) -> list[dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions.
            
        Returns:
            list[dict]: A list of task dictionaries that match the search term.
            
        Raises:
            ValueError: If task_term is empty.
            TypeError: If task_term is not a string.
        """
        # Input validation
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        if not task_term:
            raise ValueError("Search term cannot be empty")
        
        # Case-insensitive search
        task_term = task_term.lower()
        
        # Search through tasks
        result = []
        for task in self._tasks.values():
            if (task_term in task['name'].lower() or 
                task_term in task['description'].lower()):
                result.append(dict(task))  # Return a copy of the task
        
        return result

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was marked as completed, False if the task doesn't exist.
            
        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if task exists and mark it as finished
        if task_id in self._tasks:
            self._tasks[task_id]['is_finished'] = True
            return True
        
        return False

    def get_all(self) -> list[dict]:
        """
        Get all tasks.
        
        Returns:
            list[dict]: A list of all task dictionaries.
        """
        # Return a copy of all tasks to prevent external modification
        return [dict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Remove all tasks.
        
        Returns:
            bool: True if the tasks were successfully cleared, False otherwise.
        """
        self._tasks.clear()  # Remove all tasks
        return True


def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    task_manager = TaskManager()
    
    try:
        print("=== Todo List Application ===")
        
        # Example usage
        task1_id = task_manager.add("Complete assignment", "Finish the Python homework by Friday")
        task2_id = task_manager.add("Buy groceries", "Milk, eggs, bread, and vegetables")
        print(f"Added two tasks with IDs: {task1_id}, {task2_id}")
        
        print("\nAll Tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "✗"
            print(f"[{status}] {task['id']}: {task['name']} - {task['description']}")
        
        print("\nSearching for 'milk':")
        search_results = task_manager.search("milk")
        for task in search_results:
            status = "✓" if task['is_finished'] else "✗"
            print(f"[{status}] {task['id']}: {task['name']} - {task['description']}")
        
        print(f"\nMarking task {task1_id} as completed: {task_manager.finish(task1_id)}")
        
        print("\nAll Tasks after completing one:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "✗"
            print(f"[{status}] {task['id']}: {task['name']} - {task['description']}")
        
        print(f"\nRemoving task {task2_id}: {task_manager.remove(task2_id)}")
        
        print("\nAll Tasks after removal:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "✗"
            print(f"[{status}] {task['id']}: {task['name']} - {task['description']}")
            
        print(f"\nClearing all tasks: {task_manager.clear_all()}")
        print(f"Tasks remaining: {len(task_manager.get_all())}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
