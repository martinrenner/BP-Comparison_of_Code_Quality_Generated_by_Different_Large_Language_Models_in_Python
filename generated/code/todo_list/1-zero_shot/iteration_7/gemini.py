class TaskManager:
    """
    Manages a list of tasks, allowing users to add, remove, search,
    finish, get all tasks, and clear the entire list.  This class adheres
    to the principles outlined in ISO/IEC 25010, focusing on functionality,
    reliability, usability, efficiency, maintainability, and portability.

    Attributes:
        tasks (dict): A dictionary storing tasks, where the key is the task ID
                      and the value is a dictionary containing task details.
        next_id (int):  The next available ID for a new task.

    Methods:  (See individual docstrings below for details)
        add(task_name: str, task_description: str) -> int
        remove(task_id: int) -> bool
        search(task_term: str) -> list[dict]
        finish(task_id: int) -> bool
        get_all() -> list[dict]
        clear_all() -> bool
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets the
        next available ID to 1.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the task list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not positive.
        """

        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False  # Task not found

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks matching a given search term.  The search is
        case-insensitive and checks both the task name and description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of matching tasks.  Each task is represented
                        as a dictionary. Returns an empty list if no matches
                        are found.

        Raises:
            ValueError: if the task_term is not a string or is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string")


        results = []
        for task in self.tasks.values():
            if (
                task_term.lower() in task["task_name"].lower()
                or task_term.lower() in task["task_description"].lower()
            ):
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished,
                  False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not positive.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        else:
            return False  # Task not found

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the list.

        Returns:
            list[dict]: A list of all tasks, where each task is a dictionary.
                        Returns an empty list if there are no tasks.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Removes all tasks from the list.

        Returns:
            bool: Always returns True, indicating successful clearing.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset ID counter for consistency
        return True
def main():
    """
    Main function to demonstrate the TaskManager class functionality.
    Provides a simple console-based interface for interacting with the
    todo list.
    """
    task_manager = TaskManager()

    while True:
        print("\nTodo List Menu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Finish Task")
        print("5. View All Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                task_name = input("Enter task name: ")
                task_description = input("Enter task description: ")
                task_id = task_manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")

            elif choice == "2":
                task_id = int(input("Enter task ID to remove: "))
                if task_manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")

            elif choice == "3":
                task_term = input("Enter search term: ")
                results = task_manager.search(task_term)
                if results:
                    print("Search Results:")
                    for task in results:
                        print(
                            f"  ID: {task['id']}, Name: {task['task_name']}, "
                            f"Description: {task['task_description']}, "
                            f"Finished: {task['is_finished']}"
                        )
                else:
                    print("No tasks found matching your search term.")

            elif choice == "4":
                task_id = int(input("Enter task ID to mark as finished: "))
                if task_manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")

            elif choice == "5":
                tasks = task_manager.get_all()
                if tasks:
                    print("All Tasks:")
                    for task in tasks:
                        print(
                            f"  ID: {task['id']}, Name: {task['task_name']}, "
                            f"Description: {task['task_description']}, "
                            f"Finished: {task['is_finished']}"
                        )
                else:
                    print("No tasks in the list.")

            elif choice == "6":
                if task_manager.clear_all():
                    print("All tasks cleared.")
                else:
                    print("Error clearing tasks.")  # Should not happen

            elif choice == "7":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as e:
            print(f"Error: {e}")
        except TypeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

