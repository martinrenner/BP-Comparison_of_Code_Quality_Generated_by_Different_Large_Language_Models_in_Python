class TaskManager:
    """
    A class to manage tasks for a console-based todo list application.
    
    Each task is represented as a dictionary with the following keys:
      - id: Unique identifier for the task.
      - task_name: Name/title of the task.
      - task_description: Detailed description of the task.
      - is_finished: Boolean indicating if the task is completed.

    This class implements the following interface methods:
      - add(task_name: str, task_description: str) -> int
      - remove(task_id: int) -> bool
      - search(task_term: str) -> list[dict]
      - finish(task_id: int) -> bool
      - get_all() -> list[dict]
      - clear_all() -> bool
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty in-memory store and sets the starting task ID.
        """
        self.tasks = {}  # Store tasks in a dictionary for O(1) lookups, insertions and deletions.
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the todo list.
        
        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            
        Returns:
            int: The unique ID assigned to the new task.
            
        Raises:
            ValueError: If task_name is empty or task_description is not a string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty and must be a valid string.")
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task identified by its unique ID.
        
        Args:
            task_id (int): The unique identifier of the task to remove.
            
        Returns:
            bool: True if the task was successfully removed; False if the task does not exist.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks containing the given term in either the task name or description.
        
        Args:
            task_term (str): The search term to match.
            
        Returns:
            list: A list of dictionaries for tasks that match the search criteria.
            
        Raises:
            ValueError: If task_term is empty or not a string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")
        
        task_term = task_term.lower()
        return [
            task for task in self.tasks.values()
            if task_term in task["task_name"].lower() or task_term in task["task_description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.
        
        Args:
            task_id (int): The unique identifier of the task to mark as finished.
            
        Returns:
            bool: True if the task was successfully marked as finished; False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        
        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks with their details.
        
        Returns:
            list: A list of dictionaries representing all tasks.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the todo list.
        
        Returns:
            bool: True after successfully clearing all tasks.
        """
        self.tasks.clear()
        return True


def print_task(task: dict) -> None:
    """
    Prints a task in the standard format: (id, task_name, task_description, is_finished)
    
    Args:
        task (dict): A dictionary containing task details.
    """
    print(f"({task['id']}, {task['task_name']}, {task['task_description']}, {task['is_finished']})")


def main():
    """
    Console-based todo list application entry point.
    
    Displays a menu for users to interact with the TaskManager. Users can add, remove,
    search, finish tasks, view all tasks, clear all tasks, or exit the application.
    """
    task_manager = TaskManager()
    menu = (
        "\n--- Todo List App ---\n"
        "Please choose an option:\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Finish Task\n"
        "5. Show All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            print("\nAdd Task")
            task_name = input("Enter task name: ").strip()
            task_description = input("Enter task description: ").strip()
            try:
                task_id = task_manager.add(task_name, task_description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            print("\nRemove Task")
            task_id_str = input("Enter task ID to remove: ").strip()
            try:
                task_id = int(task_id_str)
                if task_manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task ID not found. Removal failed.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            print("\nSearch Tasks")
            search_term = input("Enter search term: ").strip()
            try:
                results = task_manager.search(search_term)
                if results:
                    print("Search Results:")
                    for task in results:
                        print_task(task)
                else:
                    print("No tasks matched the search criteria.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '4':
            print("\nFinish Task")
            task_id_str = input("Enter task ID to mark as finished: ").strip()
            try:
                task_id = int(task_id_str)
                if task_manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task ID not found. Could not mark task as finished.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '5':
            print("\nShow All Tasks")
            tasks = task_manager.get_all()
            if tasks:
                for task in tasks:
                    print_task(task)
            else:
                print("No tasks found.")

        elif choice == '6':
            print("\nClear All Tasks")
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == 'yes':
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Operation cancelled. No tasks were cleared.")

        elif choice == '7':
            print("Exiting Todo List App. Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a valid option (1-7).")


if __name__ == "__main__":
    main()
