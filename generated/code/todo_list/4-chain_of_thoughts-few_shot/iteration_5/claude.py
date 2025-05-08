class TaskManager:
    """
    A task management system that allows users to create, track, and manage tasks.
    
    This class implements a complete task management interface with functionality
    for adding, removing, searching, and manipulating tasks while maintaining
    data integrity and providing proper validation.
    """
    
    def __init__(self):
        """
        Initialize an empty task manager with a task storage and ID counter.
        """
        self._tasks = {}  # Dictionary to store tasks with ID as key
        self._id_counter = 1  # Counter to generate unique IDs
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): A detailed description of the task.
            
        Returns:
            int: The unique ID of the newly added task.
            
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        # Validate input parameters
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
        
        # Create a new task with a unique ID
        task_id = self._id_counter
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'is_finished': False
        }
        
        # Increment the ID counter for the next task
        self._id_counter += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the task manager by its ID.
        
        Args:
            task_id (int): The unique identifier of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        # Validate the task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if the task exists and remove it
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
            list[dict]: A list of tasks that match the search criteria.
            
        Raises:
            ValueError: If task_term is empty or not a string.
        """
        # Validate the search term
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
        
        # Convert search term to lowercase for case-insensitive search
        task_term = task_term.lower()
        
        # Search for tasks matching the term in name or description
        matching_tasks = []
        for task in self._tasks.values():
            if (task_term in task['task_name'].lower() or 
                task_term in task['task_description'].lower()):
                matching_tasks.append(task.copy())
        
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique identifier of the task to mark as completed.
            
        Returns:
            bool: True if the task was successfully marked as completed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        # Validate the task_id
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if the task exists and mark it as finished
        if task_id in self._tasks:
            # Only update if task is not already finished
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                return True
            return False  # Task was already finished
        
        return False  # Task not found
    
    def get_all(self) -> list[dict]:
        """
        Retrieve all tasks in the task manager.
        
        Returns:
            list[dict]: A list of all tasks with their details.
        """
        # Return a deep copy of all tasks to prevent external modification
        return [task.copy() for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the task manager.
        
        Returns:
            bool: True if all tasks were successfully cleared, False if there were no tasks.
        """
        if not self._tasks:
            return False  # No tasks to clear
        
        self._tasks.clear()
        # Reset the ID counter (optional, could keep incrementing for historical purposes)
        # self._id_counter = 1
        return True


def main():
    """
    Main function to demonstrate the TaskManager functionality through a console interface.
    """
    task_manager = TaskManager()
    
    while True:
        print("\n===== Todo List Application =====")
        print("1. Add a new task")
        print("2. Remove a task")
        print("3. Search for tasks")
        print("4. Mark a task as completed")
        print("5. View all tasks")
        print("6. Clear all tasks")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        try:
            if choice == '1':
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
                
            elif choice == '2':
                task_id = int(input("Enter task ID to remove: ").strip())
                if task_manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully")
                else:
                    print(f"No task found with ID {task_id}")
                
            elif choice == '3':
                term = input("Enter search term: ").strip()
                tasks = task_manager.search(term)
                if tasks:
                    print(f"\nFound {len(tasks)} matching task(s):")
                    for task in tasks:
                        status = "Completed" if task['is_finished'] else "Pending"
                        print(f"ID: {task['id']}, Status: {status}")
                        print(f"Name: {task['task_name']}")
                        print(f"Description: {task['task_description']}")
                        print("-" * 40)
                else:
                    print("No matching tasks found")
                
            elif choice == '4':
                task_id = int(input("Enter task ID to mark as completed: ").strip())
                if task_manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as completed")
                else:
                    print(f"Failed to mark task as completed: either task doesn't exist or is already completed")
                
            elif choice == '5':
                tasks = task_manager.get_all()
                if tasks:
                    print("\nAll Tasks:")
                    for task in tasks:
                        status = "Completed" if task['is_finished'] else "Pending"
                        print(f"ID: {task['id']}, Status: {status}")
                        print(f"Name: {task['task_name']}")
                        print(f"Description: {task['task_description']}")
                        print("-" * 40)
                else:
                    print("No tasks found")
                
            elif choice == '6':
                if task_manager.clear_all():
                    print("All tasks cleared successfully")
                else:
                    print("No tasks to clear")
                
            elif choice == '7':
                print("Thank you for using the Todo List Application. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
