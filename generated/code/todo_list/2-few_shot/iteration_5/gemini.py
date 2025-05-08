class TaskManager:
    """
    Manages a list of tasks, allowing adding, removing, searching, finishing,
    and retrieving tasks.  This class adheres to ISO/IEC 25010 standards
    regarding maintainability, reliability, usability, efficiency, and portability.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a starting ID.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups (task_id: task_details)
        self.next_id = 1  # Counter for assigning unique IDs to tasks

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the newly added task.

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
            "name": task_name,
            "description": task_description,
            "is_finished": False,
        }
        self.next_id += 1
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
            ValueError: If task_id is negative.
        """

        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        else:
            return False  # Task not found

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term (str): The search term (can be part of a name or description).

        Returns:
            list[dict]: A list of tasks (dictionaries) matching the search term.
                         Returns an empty list if no matches are found.

        Raises:
            ValueError: if the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        results = []
        for task in self.tasks.values():
            if task_term.lower() in task["name"].lower() or task_term.lower() in task[
                "description"
            ].lower():
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is negative.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative.")


        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        else:
            return False  # Task not found

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: A list of all tasks (dictionaries) in the task list.
                         Returns an empty list if there are no tasks.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the list

        Returns:
            bool: Always return True after clearing the list.
        """

        self.tasks.clear()
        return True



def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    manager = TaskManager()

    # Add tasks
    try:
        id1 = manager.add("Grocery Shopping", "Buy milk, eggs, and bread.")
        id2 = manager.add("Book Appointment", "Doctor appointment at 2 PM.")
        print(f"Added task with ID: {id1}")
        print(f"Added task with ID: {id2}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    print("\nAll tasks:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(task)

    # Search for tasks
    try:
        print("\nSearching for 'appointment':")
        search_results = manager.search("appointment")
        for task in search_results:
            print(task)
    except ValueError as e:
        print(f"Error searching for task: {e}")
    

    # Finish a task
    print("\nFinishing task with ID 1:")
    if manager.finish(1):
        print("Task finished successfully.")
    else:
        print("Task not found.")

    # Get all tasks again (to see the updated status)
    print("\nAll tasks after finishing one:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(task)
    
    # Remove task
    print("\nRemoving task:")
    removed_successfully = manager.remove(id2)
    if removed_successfully:
        print("Task remove successfully")
    else:
        print("Task could not be removed")
    
    # Get all tasks after finishing one
    print("\nAll tasks after removing one:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(task)
    
    # Try to remove a non-existent task and using incorrect type
    print("\nRemoving task error handling:")
    try:
        if not manager.remove(99): # ID 
            print("Task not found, as expected.")
        print("\nRemoving task using incorrect type")
        manager.remove("1")
    except TypeError as e:
        print(f"Exception was thrown: {e}")

    # Clear all tasks
    print("\nClearing all tasks...")
    manager.clear_all()
    print("All tasks cleared.")

    # Show empty todo list
    print("\nAll task after clearing:")
    print(manager.get_all())

if __name__ == "__main__":
    main()
