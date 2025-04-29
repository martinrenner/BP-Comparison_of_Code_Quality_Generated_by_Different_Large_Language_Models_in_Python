class TaskManager:
    """
    Manages a to-do list with add, remove, search, finish, get_all, and clear_all functionalities.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and an ID counter.
        """
        self.tasks = {}  # Dictionary to store tasks: {task_id: {task_details}}
        self.id_counter = 1  # Counter to generate unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name: The name of the task (must not be empty).
            task_description: The description of the task (must not be empty).

        Returns:
            The unique ID of the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.id_counter
        self.tasks[task_id] = {
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self.id_counter += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the to-do list by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.

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
        else:
            return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term: The term to search for (can be part of the name or description).

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found.

        Raises:
            ValueError: if the task_term is empty
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        results = []
        for task_id, task_data in self.tasks.items():
            if (
                task_term.lower() in task_data["task_name"].lower()
                or task_term.lower() in task_data["task_description"].lower()
            ):
                results.append(
                    {
                        "id": task_id,
                        "task_name": task_data["task_name"],
                        "task_description": task_data["task_description"],
                        "is_finished": task_data["is_finished"],
                    }
                )
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.

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
        else:
            return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the to-do list.

        Returns:
            A list of dictionaries, where each dictionary represents a task.
        """
        return [
            {
                "id": task_id,
                "task_name": task_data["task_name"],
                "task_description": task_data["task_description"],
                "is_finished": task_data["is_finished"],
            }
            for task_id, task_data in self.tasks.items()
        ]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            True indicating all tasks have been cleared
        """
        self.tasks.clear()
        return True


def main():
    """
    Main function to run the console-based to-do list application.
    """
    task_manager = TaskManager()

    while True:
        print("\nChoose an action:")
        print("1. Add task")
        print("2. Remove task")
        print("3. Search tasks")
        print("4. Finish task")
        print("5. Get all tasks")
        print("6. Clear all tasks")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

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
                    print("Search results:")
                    for task in results:
                        print(task)
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
                    print("All tasks:")
                    for task in tasks:
                        print(task)
                else:
                    print("No tasks in the list.")

            elif choice == "6":
                task_manager.clear_all()
                print("All tasks cleared.")

            elif choice == "7":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        except ValueError as e:
            print(f"Error: {e}")
        except TypeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
