class TaskManager:
    """
    A class to manage tasks in a todo list.

    Attributes:
        tasks (dict): A dictionary mapping task IDs to task details.
        next_id (int): Counter for generating unique task IDs.
    """

    def __init__(self):
        """
        Initializes a new TaskManager instance with an empty task list.
        """
        self.tasks = {}  # { task_id: task_dict }
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the todo list.

        Args:
            task_name (str): Name of the task.
            task_description (str): Description of the task.

        Returns:
            int: The unique ID assigned to the task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        task = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False
        }
        self.tasks[task_id] = task
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The unique identifier for the task to be removed.

        Returns:
            bool: True if the task was successfully removed, False if the task was not found.

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
        Searches tasks by name or description for a given term (case insensitive).

        Args:
            task_term (str): The search term used for matching tasks.

        Returns:
            list[dict]: A list of tasks that match the search criteria.

        Raises:
            ValueError: If the search term is an empty string.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.lower()
        results = [
            task for task in self.tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The unique identifier for the task.

        Returns:
            bool: True if task is marked as finished, False if the task was not found.

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
            list[dict]: A list of all tasks stored in the manager.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the todo list.

        Returns:
            bool: True after the tasks have been cleared.
        """
        self.tasks.clear()
        return True


def main():
    """
    Provides a console-based interface for managing tasks in a todo list.
    Supports adding, removing, searching, finishing, showing, and clearing tasks.
    """
    manager = TaskManager()

    def print_menu():
        print("\n===== Todo List App =====")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Finish Task")
        print("5. Get All Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            # Add Task
            try:
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                task_id = manager.add(name, description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as error:
                print(f"Error adding task: {error}")

        elif choice == "2":
            # Remove Task
            try:
                task_id_input = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_input)
                if manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print(f"Task with ID {task_id} not found.")
            except ValueError as error:
                print(f"Error removing task: {error}")

        elif choice == "3":
            # Search Tasks
            try:
                search_term = input("Enter search term: ").strip()
                results = manager.search(search_term)
                if results:
                    print("Search results:")
                    for task in results:
                        print(f"(ID: {task['id']}, Name: {task['task_name']}, "
                              f"Description: {task['task_description']}, Finished: {task['is_finished']})")
                else:
                    print("No tasks found matching the search term.")
            except ValueError as error:
                print(f"Error searching tasks: {error}")

        elif choice == "4":
            # Finish Task
            try:
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_input)
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print(f"Task with ID {task_id} not found.")
            except ValueError as error:
                print(f"Error finishing task: {error}")

        elif choice == "5":
            # Get All Tasks
            tasks = manager.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    print(f"(ID: {task['id']}, Name: {task['task_name']}, "
                          f"Description: {task['task_description']}, Finished: {task['is_finished']})")
            else:
                print("No tasks available.")

        elif choice == "6":
            # Clear All Tasks
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == "yes":
                if manager.clear_all():
                    print("All tasks have been cleared.")
            else:
                print("Clear all action canceled.")

        elif choice == "7":
            print("Exiting Todo List App. Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from 1 to 7.")


if __name__ == "__main__":
    main()
