class TaskManager:
    """
    A class to manage a collection of tasks for a to-do list application.
    
    Each task is stored as a dictionary with the following keys:
        - id (int): Unique identifier for the task.
        - task_name (str): Name of the task.
        - task_description (str): Description of the task.
        - is_finished (bool): Completion status of the task.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task storage and a counter for unique IDs.
        """
        self.tasks = {}
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the given name and description.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The ID of the task to be removed.

        Returns:
            bool: True if the task was successfully removed, False if the task does not exist.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks by looking for the given term in the task name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of task dictionaries that match the search term.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = task_term.lower()
        matching_tasks = [
            task.copy() for task in self.tasks.values()
            if lower_term in task["task_name"].lower() or lower_term in task["task_description"].lower()
        ]
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished (completed) by its unique ID.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task exists and its status was updated, otherwise False.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self.tasks.get(task_id)
        if task:
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks managed by the TaskManager.

        Returns:
            list[dict]: A list of all tasks with their details.
        """
        # Returning copies to protect internal task data from external modification.
        return [task.copy() for task in self.tasks.values()]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the TaskManager.

        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self.tasks.clear()
        return True


def main():
    """
    Runs the console-based to-do list application.
    Provides a menu-driven interface for adding, removing, searching, finishing,
    retrieving all tasks, and clearing all tasks.
    """
    task_manager = TaskManager()
    menu = """
    To-Do List Application:
    -------------------------
    1. Add Task
    2. Remove Task
    3. Search Tasks
    4. Mark Task as Finished
    5. Get All Tasks
    6. Clear All Tasks
    7. Exit
    """

    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            # Add Task
            try:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = task_manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "2":
            # Remove Task
            try:
                task_id_str = input("Enter the task ID to remove: ").strip()
                if not task_id_str.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(task_id_str)
                if task_manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"No task found with ID {task_id}.")
            except (ValueError, TypeError) as e:
                print(f"Error: {e}")

        elif choice == "3":
            # Search Tasks
            try:
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                if results:
                    print("Search Results:")
                    for task in results:
                        status = "Finished" if task["is_finished"] else "Pending"
                        print(f'ID: {task["id"]}, Name: {task["task_name"]}, Description: {task["task_description"]}, Status: {status}')
                else:
                    print("No tasks found matching your search criteria.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "4":
            # Mark Task as Finished
            try:
                task_id_str = input("Enter the task ID to mark as finished: ").strip()
                if not task_id_str.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(task_id_str)
                if task_manager.finish(task_id):
                    print(f"Task with ID {task_id} has been marked as finished.")
                else:
                    print(f"No task found with ID {task_id}.")
            except (ValueError, TypeError) as e:
                print(f"Error: {e}")

        elif choice == "5":
            # Get All Tasks
            tasks = task_manager.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    status = "Finished" if task["is_finished"] else "Pending"
                    print(f'ID: {task["id"]}, Name: {task["task_name"]}, Description: {task["task_description"]}, Status: {status}')
            else:
                print("No tasks available.")

        elif choice == "6":
            # Clear All Tasks
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == "yes":
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Operation cancelled.")

        elif choice == "7":
            # Exit the application
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option (1-7).")


if __name__ == "__main__":
    main()
