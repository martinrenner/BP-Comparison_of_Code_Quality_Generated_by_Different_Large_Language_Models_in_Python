class TaskManager:
    """
    Manages a to-do list with add, remove, search, finish, get_all, and clear_all functionalities.
    Uses a dictionary for efficient task storage and retrieval.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a counter for unique IDs.
        """
        self.tasks = {}  # Dictionary to store tasks: {id: {task details}}
        self.next_id = 1  # Counter for assigning unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name: The name of the task (must not be empty).
            task_description: The description of the task (must not be empty).

        Returns:
            The unique ID of the newly added task.

        Raises:
            ValueError: If either task_name or task_description is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self.next_id += 1
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
            ValueError: If task_id is not positive
        """

        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID must be positive")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks matching a given term in either the name or description.

        Args:
            task_term: The term to search for.

        Returns:
            A list of dictionaries, each representing a matching task.  Returns an empty list if no matches are found.

        Raises:
             ValueError: If search term is empty
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        results = []
        for task_id, task_details in self.tasks.items():
            if (
                task_term.lower() in task_details["task_name"].lower()
                or task_term.lower() in task_details["task_description"].lower()
            ):
                results.append(
                    {
                        "id": task_id,
                        "task_name": task_details["task_name"],
                        "task_description": task_details["task_description"],
                        "is_finished": task_details["is_finished"],
                    }
                )
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.
        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not positive
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID must be positive")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        else:
            return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the to-do list.

        Returns:
            A list of dictionaries, each representing a task.  Returns an empty list if there are no tasks.
        """
        return [
            {
                "id": task_id,
                "task_name": task_details["task_name"],
                "task_description": task_details["task_description"],
                "is_finished": task_details["is_finished"],
            }
            for task_id, task_details in self.tasks.items()
        ]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the to-do list.

        Returns:
           Always returns True after clearing the tasks.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True


def main():
    """
    Demonstrates the usage of the TaskManager class with a simple console interface.
    """
    manager = TaskManager()

    while True:
        print("\nChoose an action:")
        print("1. Add task")
        print("2. Remove task")
        print("3. Search tasks")
        print("4. Finish task")
        print("5. Get all tasks")
        print("6. Clear all tasks")
        print("7. Exit")

        choice = input("> ")

        try:
            if choice == "1":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"Task added with ID: {task_id}")

            elif choice == "2":
                task_id = int(input("Enter task ID to remove: "))
                if manager.remove(task_id):
                    print("Task removed.")
                else:
                    print("Task not found.")

            elif choice == "3":
                term = input("Enter search term: ")
                results = manager.search(term)
                if results:
                    for task in results:
                        print(task)
                else:
                    print("No tasks found matching that term.")

            elif choice == "4":
                task_id = int(input("Enter task ID to finish: "))
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")

            elif choice == "5":
                tasks = manager.get_all()
                if tasks:
                    for task in tasks:
                        print(task)
                else:
                    print("No tasks in the list.")

            elif choice == "6":
                manager.clear_all()
                print("All tasks cleared.")

            elif choice == "7":
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


import unittest

class TestTaskManager(unittest.TestCase):

    def test_add_task(self):
        manager = TaskManager()
        task_id = manager.add("Buy groceries", "Milk, eggs, bread")
        self.assertEqual(task_id, 1)
        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(manager.tasks[1]["task_name"], "Buy groceries")
        self.assertEqual(manager.tasks[1]["is_finished"], False)

    def test_add_task_empty_name(self):
        manager = TaskManager()
        with self.assertRaises(ValueError):
            manager.add("", "Description")

    def test_remove_task(self):
        manager = TaskManager()
        task_id = manager.add("Test Task", "Description")
        success = manager.remove(task_id)
        self.assertTrue(success)
        self.assertEqual(len(manager.tasks), 0)

    # ... more tests for remove, search, finish, get_all, clear_all ...

    def test_search_finds_match(self):
        manager = TaskManager()
        manager.add("TaskOne", "Description For TaskOne")
        results = manager.search("TaskOne")
        self.assertEqual(len(results), 1)

    def test_finish_task(self):
        manager = TaskManager()
        task_id = manager.add("Test Task", "Description")
        manager.finish(task_id)
        self.assertTrue(manager.tasks[task_id]["is_finished"])
