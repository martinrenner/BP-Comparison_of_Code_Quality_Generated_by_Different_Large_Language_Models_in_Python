class TaskManager:
    """
    Task Manager class to handle todo list operations.
    
    This class implements a todo list manager with basic CRUD operations
    and follows ISO/IEC 25010 standards for software quality.
    """
    
    def __init__(self):
        """Initialize an empty task manager with a task dictionary and ID counter."""
        self._tasks = {}  # Dictionary to store tasks with ID as key
        self._task_id_counter = 1  # Counter to assign unique IDs to tasks
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The detailed description of the task.
            
        Returns:
            int: The unique ID of the newly created task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Validate inputs
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string.")
        
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string.")
        
        # Create new task
        task_id = self._task_id_counter
        self._tasks[task_id] = {
            'id': task_id,
            'name': task_name,
            'description': task_description,
            'is_finished': False
        }
        
        # Increment counter for next task
        self._task_id_counter += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        
        # Remove task if it exists
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
            list[dict]: A list of tasks that match the search term.
            
        Raises:
            ValueError: If task_term is empty.
        """
        # Validate search term
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string.")
        
        # Convert search term to lowercase for case-insensitive search
        search_term_lower = task_term.lower()
        
        # Find all tasks that match the search term
        matching_tasks = []
        for task in self._tasks.values():
            if (search_term_lower in task['name'].lower() or 
                search_term_lower in task['description'].lower()):
                matching_tasks.append(task.copy())
        
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        
        # Mark task as finished if it exists
        if task_id in self._tasks:
            # Only update if not already finished
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                return True
            return False
        
        return False
    
    def get_all(self) -> list[dict]:
        """
        Retrieve all tasks in the todo list.
        
        Returns:
            list[dict]: A list of all tasks with their details.
        """
        # Return a copy of all tasks to prevent external modification
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the todo list.
        
        Returns:
            bool: True if all tasks were successfully removed.
        """
        # Clear all tasks
        self._tasks.clear()
        # Reset the counter (optional, could also keep incrementing for unique IDs)
        self._task_id_counter = 1
        return True


# Example usage of TaskManager class
def main():
    """Demonstrate the TaskManager functionality with example tasks."""
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        task1_id = task_manager.add("Buy groceries", "Milk, bread, eggs, and vegetables")
        task2_id = task_manager.add("Call dentist", "Schedule appointment for next week")
        task3_id = task_manager.add("Finish project", "Complete the Python assignment")
        
        print("=== All Tasks ===")
        for task in task_manager.get_all():
            print(f"ID: {task['id']}, Name: {task['name']}, "
                  f"Done: {task['is_finished']}")
        
        # Mark a task as completed
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("\n=== Search Results for 'appointment' ===")
        search_results = task_manager.search("appointment")
        for task in search_results:
            print(f"ID: {task['id']}, Name: {task['name']}, "
                  f"Description: {task['description']}")
        
        # Remove a task
        task_manager.remove(task2_id)
        
        print("\n=== Updated Task List ===")
        for task in task_manager.get_all():
            status = "Done" if task['is_finished'] else "Pending"
            print(f"ID: {task['id']}, Name: {task['name']}, Status: {status}")
            
        # Clear all tasks
        print("\nClearing all tasks...")
        task_manager.clear_all()
        print(f"Tasks remaining: {len(task_manager.get_all())}")
        
    except ValueError as e:
        print(f"Error: {e}")
    

if __name__ == "__main__":
    main()
