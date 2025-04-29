class TaskManager:
    """
    Manages a to-do list, providing functions to add, remove, search,
    finish, retrieve, and clear tasks.  Implements ISO/IEC 25010
    quality characteristics.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and an ID counter.
        """
        self.tasks = {}  # Dictionary to store tasks: {task_id: task_data}
        self.next_id = 1  # Counter for generating unique task IDs



    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

        Raises:
            ValueError: If task_name or task_description are empty strings.
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
        Removes a task from the to-do list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

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
            task_term (str): The term to search for within task names and descriptions.

        Returns:
            list[dict]: A list of matching task dictionaries.  Returns an empty
                       list if no matches are found.

        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

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
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished,
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
        Retrieves all tasks in the to-do list.

        Returns:
            list[dict]: A list of all task dictionaries.
        """
        return list(self.tasks.values())



    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            bool: Always returns True, indicating successful deletion.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True


class TaskManager:
    """
    Manages a to-do list, providing functions to add, remove, search,
    finish, retrieve, and clear tasks.  Implements ISO/IEC 25010
    quality characteristics.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and an ID counter.
        """
        self.tasks = {}  # Dictionary to store tasks: {task_id: task_data}
        self.next_id = 1  # Counter for generating unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name (str): The name of the task.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

        Raises:
            ValueError: If task_name or task_description are empty strings.
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
        Removes a task from the to-do list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

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
            task_term (str): The term to search for within task names and descriptions.

        Returns:
            list[dict]: A list of matching task dictionaries.  Returns an empty
                       list if no matches are found.

        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

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
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished,
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
        Retrieves all tasks in the to-do list.

        Returns:
            list[dict]: A list of all task dictionaries.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            bool: Always returns True, indicating successful deletion.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True


if __name__ == "__main__":
    tm = TaskManager()

    # Add tasks
    try:
        id1 = tm.add("Grocery Shopping", "Buy milk, eggs, bread, and cheese")
        id2 = tm.add("Book Doctor Appointment", "Schedule checkup for next week")
        id3 = tm.add("Pay Bills", "Electricity and internet bills")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = tm.get_all()
    print(f"All tasks: {all_tasks}")

    # Search for tasks
    try:
        search_results = tm.search("doctor")
        print(f"Search results for 'doctor': {search_results}")

        search_results = tm.search("  ")  # Test empty search term
        print(f"Search results: {search_results}")
    except ValueError as e:
        print(f"Error searching: {e}")


    # Finish a task
    try:
        finished = tm.finish(id2)
        print(f"Task {id2} finished: {finished}")
        finished = tm.finish(999)  # Non-existent ID
        print(f"Task 999 finished: {finished}")
    except (TypeError, ValueError) as e:
        print(f"Error finishing task: {e}")

    # Remove a task
    try:
        removed = tm.remove(id1)
        print(f"Task {id1} removed: {removed}")
        removed = tm.remove(-5)  # Invalid ID

    except (TypeError, ValueError) as e:
        print(f"Error removing task: {e}")
    # Get all tasks again
    all_tasks = tm.get_all()
    print(f"All tasks after finishing and removing: {all_tasks}")
    
    # Clear all tasks
    tm.clear_all()
    print(f"All tasks after clearing: {tm.get_all()}")
