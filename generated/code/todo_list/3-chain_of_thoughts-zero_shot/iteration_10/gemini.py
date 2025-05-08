class TaskManager:
    """
    Manages a list of tasks, providing functionality to add, remove,
    search, finish, retrieve, and clear tasks.  Uses an in-memory
    dictionary for efficient storage and retrieval.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets
        the next available ID to 1.
        """
        self.tasks = {}  # Dictionary to store tasks: {id: {task_details}}
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task (must not be empty).
            task_description: A description of the task.

        Returns:
            The unique ID of the newly added task.

        Raises:
            ValueError: If the task_name is empty.
        """
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "name": task_name,
            "description": task_description,
            "is_finished": False,
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the list by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If a task with the given ID does not exist.
        """

        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

        del self.tasks[task_id]
        return True
        
    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks whose name or description contains the given term.

        Args:
            task_term: The term to search for (case-insensitive).

        Returns:
            A list of dictionaries, where each dictionary represents a
            matching task.  Returns an empty list if no matches are found.

        Raises:
             ValueError: If the task_term is empty
        """
        if not task_term.strip():
            raise ValueError("Task term cannot be empty.")
            
        results = []
        for task in self.tasks.values():
            if (
                task_term.lower() in task["name"].lower()
                or task_term.lower() in task["description"].lower()
            ):
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished,
            False otherwise.

        Raises:
            TypeError: If the task_id is not an integer
            ValueError: If no task with the given ID is not found
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

        self.tasks[task_id]["is_finished"] = True
        return True


    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, where each dictionary represents a task.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            True, indicating that the task list was successfully cleared.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True


def main():
    """
    Main function to interact with TaskManager.
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

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"Task added with ID: {task_id}")

            elif choice == "2":
                task_id = int(input("Enter task ID to remove: "))
                manager.remove(task_id)
                print("Task removed successfully.")

            elif choice == "3":
                term = input("Enter search term: ")
                results = manager.search(term)
                if results:
                    print("Search Results:")
                    for task in results:
                        print(
                            f"  ID: {task['id']}, Name: {task['name']}, "
                            f"Description: {task['description']}, Finished: {task['is_finished']}"
                        )
                else:
                    print("No tasks found matching the search term.")

            elif choice == "4":
                task_id = int(input("Enter task ID to finish: "))
                manager.finish(task_id)
                print("Task marked as finished.")

            elif choice == "5":
                tasks = manager.get_all()
                if tasks:
                    print("All Tasks:")
                    for task in tasks:
                        print(
                            f"  ID: {task['id']}, Name: {task['name']}, "
                            f"Description: {task['description']}, Finished: {task['is_finished']}"
                        )
                else:
                    print("No tasks in the list.")

            elif choice == "6":
                manager.clear_all()
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

