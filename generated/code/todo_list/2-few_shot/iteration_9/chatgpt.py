class TaskManager:
    """
    A class that manages a collection of tasks for a todo list application.
    
    Each task is stored as a dictionary with the following keys:
        - id: Unique identifier for the task.
        - task_name: Name of the task.
        - task_description: Detailed description of the task.
        - is_finished: Boolean flag indicating if the task is completed.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a starting ID value.
        """
        self.tasks = {}  # Dictionary to store tasks with their unique ID as key
        self.next_id = 1  # The next available unique task ID

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the todo list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            TypeError: If either task_name or task_description is not a string.
            ValueError: If either task_name or task_description is an empty string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")

        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False,
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the todo list by its unique ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was removed successfully, False if not found.

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
        Searches tasks by a term in their name or description.

        Args:
            task_term (str): The string to search for in the task details.

        Returns:
            list[dict]: A list of tasks (as dictionaries) that match the search term.

        Raises:
            TypeError: If task_term is not a string.
            ValueError: If task_term is an empty string.
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string.")

        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.strip().lower()
        results = []
        # Iterate over tasks to check if the term is in the name or description
        for task in self.tasks.values():
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks from the todo list.

        Returns:
            list[dict]: A list of all tasks with their details.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the todo list.

        Returns:
            bool: True once all tasks have been cleared.
        """
        self.tasks.clear()
        self.next_id = 1
        return True


def print_task(task: dict) -> None:
    """
    Prints the details of a single task in a formatted manner.

    Args:
        task (dict): The task information.
    """
    status = "Finished" if task.get("is_finished") else "Pending"
    print(
        f"ID: {task.get('id')} | Name: {task.get('task_name')} | "
        f"Description: {task.get('task_description')} | Status: {status}"
    )


def main():
    """
    Main function to run the console-based todo list application.
    Implements a menu-driven interface for the user to interact with tasks.
    """
    task_manager = TaskManager()

    menu = (
        "\nTodo List Application\n"
        "---------------------\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Mark Task as Finished\n"
        "5. Get All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
        "Enter your choice (1-7): "
    )

    while True:
        choice = input(menu).strip()

        if choice == "1":
            # Add Task
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = task_manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
            except (ValueError, TypeError) as e:
                print(f"Error adding task: {e}")

        elif choice == "2":
            # Remove Task
            try:
                id_input = input("Enter task ID to remove: ").strip()
                if not id_input.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(id_input)
                if task_manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found. Removal failed.")
            except (ValueError, TypeError) as e:
                print(f"Error removing task: {e}")

        elif choice == "3":
            # Search Tasks
            try:
                search_term = input("Enter search term: ").strip()
                results = task_manager.search(search_term)
                if results:
                    print(f"Found {len(results)} matching task(s):")
                    for task in results:
                        print_task(task)
                else:
                    print("No matching tasks found.")
            except (ValueError, TypeError) as e:
                print(f"Error searching tasks: {e}")

        elif choice == "4":
            # Mark Task as Finished
            try:
                id_input = input("Enter task ID to mark as finished: ").strip()
                if not id_input.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(id_input)
                if task_manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found. Operation failed.")
            except (ValueError, TypeError) as e:
                print(f"Error marking task as finished: {e}")

        elif choice == "5":
            # Get All Tasks
            tasks = task_manager.get_all()
            if tasks:
                print("\nAll Tasks:")
                for task in tasks:
                    print_task(task)
            else:
                print("No tasks available.")

        elif choice == "6":
            # Clear All Tasks
            confirmation = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirmation == "y":
                task_manager.clear_all()
                print("All tasks cleared.")
            else:
                print("Operation cancelled.")

        elif choice == "7":
            # Exit
            print("Exiting Todo List Application. Goodbye!")
            break

        else:
            print("Invalid option. Please enter a choice between 1 and 7.")


if __name__ == "__main__":
    main()
