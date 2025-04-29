class TaskManager:
    """
    Manages a list of tasks with functionalities to add, remove, search,
    finish, retrieve, and clear tasks.  This class adheres to ISO/IEC 25010
    standards by focusing on maintainability, reliability, usability,
    efficiency, and portability.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a unique ID counter.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups (ID -> Task)
        self.next_id = 1  # Counter to generate unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task list.

        Args:
            task_name: The name of the task (must be non-empty).
            task_description: The description of the task (must be non-empty).

        Returns:
            The unique ID assigned to the newly added task.

        Raises:
            ValueError: If task_name or task_description is empty.
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
            "is_finished": False,
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the task list by its ID.

        Args:
            task_id: The ID of the task to be removed.

        Returns:
            True if the task was successfully removed, False otherwise.

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
        Searches for tasks matching a given term in their name or description.

        Args:
            task_term: The term to search for (case-insensitive).

        Returns:
            A list of dictionaries, each representing a matching task. An empty
            list is returned if no tasks match or if the search term is empty.

        Raises:
            ValueError: If `task_term` is an empty string.
        """

        if not task_term.strip():
            raise ValueError("Search term cannot be empty")

        results = []
        task_term_lower = task_term.lower()
        for task in self.tasks.values():
            if (
                task_term_lower in task["task_name"].lower()
                or task_term_lower in task["task_description"].lower()
            ):
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to be marked as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.

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
            return False  # Task not found

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the task list.

        Returns:
           A list of dictionaries, each representing a task. The order of tasks is not guaranteed.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the task list.

        Returns:
           Always returns True, signifying the list has been cleared.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset ID counter
        return True


def main():
    """
    Main function to demonstrate the TaskManager usage through a console interface.
    Provides a command-line interface for interacting with the todo list.
    """
    task_manager = TaskManager()

    while True:
        print("\nTodo List Menu:")
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
                    print("Search Results:")
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
                    print("All Tasks:")
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

