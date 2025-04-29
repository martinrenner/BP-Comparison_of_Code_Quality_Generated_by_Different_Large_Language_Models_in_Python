class TaskManager:
    """
    Manages a to-do list with functionalities to add, remove, search,
    finish, get, and clear tasks.  Implements an in-memory storage
    using a dictionary for efficient task management.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a counter for task IDs.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID
        self.next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the to-do list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

        Raises:
            ValueError: if task_name or task_description is empty.
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description or not task_description.strip():
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
            task_id (int): The ID of the task to be removed.

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
        Searches for tasks by name or description.

        Args:
            task_term (str): The term to search for in task names and descriptions.

        Returns:
            list[dict]: A list of tasks (dictionaries) matching the search term.
                        Returns an empty list if no matches are found.

        Raises:
            ValueError: if task_term is empty.
        """

        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty.")

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
            task_id (int): The ID of the task to be marked as finished.

        Returns:
            bool: True if the task was successfully marked as finished,
                  False if the task ID does not exist.

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
        Retrieves all tasks in the to-do list.

        Returns:
            list[dict]: A list of all tasks, where each task is represented
                        as a dictionary.  Returns an empty list if there are
                        no tasks.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the to-do list.

        Returns:
            bool: Always returns True, indicating successful clearing of tasks.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset task ID counter
        return True



def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    manager = TaskManager()

    # Add tasks
    try:
        task1_id = manager.add("Grocery Shopping", "Buy milk, eggs, and bread")
        task2_id = manager.add("Book Appointment", "Schedule a doctor's appointment")
        print(f"Added task with ID: {task1_id}")
        print(f"Added task with ID: {task2_id}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print("\nAll tasks:")
    for task in all_tasks:
        print(task)

    # Search for a task
    try:
        search_results = manager.search("grocery")
        print("\nSearch results for 'grocery':")
        for task in search_results:
            print(task)

        search_results = manager.search("appointment")
        print("\nSearch results for 'appointment':")
        for task in search_results:
            print(task)
    except ValueError as e:
         print(f"Error searching task: {e}")

    # Finish a task
    try:
        finish_status = manager.finish(task1_id)
        print(f"\nFinished task {task1_id}: {finish_status}")
    except ValueError as e:
        print(f"Error finish task: {e}")

    # Get all tasks again (to see the updated status)
    all_tasks = manager.get_all()
    print("\nAll tasks (after finishing one):")
    for task in all_tasks:
        print(task)
    
    # Remove task
    try:
        remove_status = manager.remove(task2_id)
        print(f"\nRemove task {task2_id}: {remove_status}")
    except ValueError as e:
        print(f"Error remove task: {e}")
    
    # Get all tasks again
    all_tasks = manager.get_all()
    print("\nAll tasks (after remove one):")
    for task in all_tasks:
        print(task)


    # Clear all tasks
    clear_status = manager.clear_all()
    print(f"\nCleared all tasks: {clear_status}")

    # Try to get all tasks (should be empty)
    all_tasks = manager.get_all()
    print("\nAll tasks (after clearing):")
    for task in all_tasks:  # This loop won't execute as the list is empty
        print(task)

    try:
        add_empty_name_task = manager.add("", "description")
    except ValueError as e:
        print(f"\nError adding task: {e}")
    
    try:
        add_empty_description_task = manager.add("name", "")
    except ValueError as e:
        print(f"\nError adding task: {e}")

    try:
        search_empty = manager.search("")
    except ValueError as e:
        print(f"\nError searching task: {e}")
    
    try:
        remove_negative_id = manager.remove(-1)
    except ValueError as e:
        print(f"\nError remove task: {e}")
    
    try:
        finish_incorrect_id = manager.finish(5)
        print(f"\nFinished not existed: {finish_incorrect_id}") # Need print, because no error
    except ValueError as e:
        print(f"\nError finish task: {e}")

if __name__ == "__main__":
    main()

