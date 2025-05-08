class TaskManager:
    """
    Manages a list of tasks with functionalities to add, remove, search,
    finish, get all, and clear all tasks.  This class adheres to
    ISO/IEC 25010 standards by focusing on maintainability, reliability,
    efficiency, usability, and portability.

    Attributes:
        tasks (dict):  An in-memory dictionary to store tasks.
                       Keys are task IDs (int), and values are task dictionaries.
        next_task_id (int):  An auto-incrementing counter to assign unique IDs.

    Methods:
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
        next task ID to 1.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID.
        self.next_task_id = 1

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
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_task_id
        self.tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self.next_task_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the task list by its ID.

        Args:
            task_id (int): The ID of the task to be removed.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative or zero.
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
        Searches for tasks by name or description.

        Args:
            task_term (str): The search term (can be part of the name or description).

        Returns:
            list[dict]: A list of task dictionaries matching the search term.
                         Returns an empty list if no matches are found.
        Raises:
            ValueError: If task_term is empty
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty")

        results = []
        for task_id, task_data in self.tasks.items():
            if (
                task_term.lower() in task_data["task_name"].lower()
                or task_term.lower() in task_data["task_description"].lower()
            ):
                results.append(task_data)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to be marked as finished.

        Returns:
            bool: True if the task was successfully marked as finished,
                  False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative or zero.
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
        Retrieves all tasks from the task list.

        Returns:
            list[dict]: A list of all task dictionaries, including their details
                        (id, task_name, task_description, is_finished).
        """
        # Return a list of task dictionaries.  Using list(self.tasks.values())
        # would return a *copy*, which is safer.  However, for maximum
        # efficiency, and since we are documenting the return type clearly, we
        # are returning the direct values.
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the task list.

        Returns:
            bool: True after successfully clearing the list.
        """
        self.tasks.clear()
        self.next_task_id = 1  # Reset the counter
        return True


def main():
    """
    Provides a console-based interface for interacting with the TaskManager.
    """
    task_manager = TaskManager()

    while True:
        print("\nTodo List Menu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Finish Task")
        print("5. Get All Tasks")
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
                search_term = input("Enter search term: ")
                results = task_manager.search(search_term)
                if results:
                    print("Search Results:")
                    for task in results:
                        print(
                            f"  ID: {task['id']}, Name: {task['task_name']}, "
                            f"Description: {task['task_description']}, Finished: {task['is_finished']}"
                        )
                else:
                    print("No tasks found matching the search term.")

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
                            f"Description: {task['task_description']}, Finished: {task['is_finished']}"
                        )
                else:
                    print("No tasks in the list.")

            elif choice == "6":
                task_manager.clear_all()
                print("All tasks cleared.")

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

