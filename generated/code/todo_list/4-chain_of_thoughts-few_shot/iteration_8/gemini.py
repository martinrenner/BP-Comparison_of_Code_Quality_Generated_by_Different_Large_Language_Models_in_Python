class TaskManager:
    """
    Manages a list of tasks.  Implements ISO/IEC 25010 quality characteristics.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a counter for unique IDs.
        """
        self.tasks = {}  # Key: task_id, Value: {task_name, task_description, is_finished}
        self.next_id = 1  # Counter for generating unique task IDs



    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is empty.
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
        Removes a task from the list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
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
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of dictionaries, each representing a matching task.
                        Each dictionary contains 'id', 'task_name', 'task_description', and 'is_finished'.

        Raises:
            ValueError: If task_term is empty
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
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """

        if not isinstance(task_id, int) or task_id <= 0:
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
            list[dict]: A list of dictionaries, each representing a task.
                        Each dictionary contains 'id', 'task_name', 'task_description', and 'is_finished'.
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
        Clears all tasks from the list.

        Returns:
            bool: Always returns True, indicating that the list has been cleared.
        """
        self.tasks = {}
        self.next_id = 1  # Reset the ID counter
        return True


class TaskManager:
    """
    Manages a list of tasks.  Implements ISO/IEC 25010 quality characteristics.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a counter for unique IDs.
        """
        self.tasks = {}  # Key: task_id, Value: {task_name, task_description, is_finished}
        self.next_id = 1  # Counter for generating unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is empty.
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
        Removes a task from the list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
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
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of dictionaries, each representing a matching task.
                        Each dictionary contains 'id', 'task_name', 'task_description', and 'is_finished'.

        Raises:
            ValueError: If task_term is empty
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
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """

        if not isinstance(task_id, int) or task_id <= 0:
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
            list[dict]: A list of dictionaries, each representing a task.
                        Each dictionary contains 'id', 'task_name', 'task_description', and 'is_finished'.
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
        Clears all tasks from the list.

        Returns:
            bool: Always returns True, indicating that the list has been cleared.
        """
        self.tasks = {}
        self.next_id = 1  # Reset the ID counter
        return True


if __name__ == "__main__":
    tm = TaskManager()

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
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = tm.add(name, description)
                print(f"Task added with ID: {task_id}")

            elif choice == "2":
                task_id = int(input("Enter task ID to remove: "))
                if tm.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")

            elif choice == "3":
                term = input("Enter search term: ")
                results = tm.search(term)
                if results:
                    print("Search results:")
                    for task in results:
                        print(
                            f"  ID: {task['id']}, Name: {task['task_name']}, Description: {task['task_description']}, Finished: {task['is_finished']}"
                        )
                else:
                    print("No tasks found matching the search term.")

            elif choice == "4":
                task_id = int(input("Enter task ID to mark as finished: "))
                if tm.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")

            elif choice == "5":
                tasks = tm.get_all()
                if tasks:
                    print("All tasks:")
                    for task in tasks:
                        print(
                            f"  ID: {task['id']}, Name: {task['task_name']}, Description: {task['task_description']}, Finished: {task['is_finished']}"
                        )
                else:
                    print("No tasks in the list.")

            elif choice == "6":
                tm.clear_all()
                print("All tasks cleared.")

            elif choice == "7":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
