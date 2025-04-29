class TaskManager:
    """
    Manages a list of tasks, allowing adding, removing, searching, finishing,
    getting, and clearing tasks.  This class adheres to ISO/IEC 25010 standards
    by focusing on maintainability, reliability, usability, efficiency, and portability.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets the initial ID to 1.
        """
        self.tasks = {}  # Use a dictionary for efficient lookups by ID
        self.next_id = 1

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
            task_id (int): The ID of the task to be removed.

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
        return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term (str): The search term (can be part of the name or description).

        Returns:
            list[dict]: A list of tasks (dictionaries) matching the search term.
                         Returns an empty list if no matches are found.

        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term.strip():
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
            bool: True if the task was found and marked as finished, False otherwise.

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
        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks with their details.

        Returns:
            list[dict]: A list of all tasks, where each task is a dictionary.
                         Returns an empty list if there are no tasks.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool:  Always returns True, indicating successful clearing of tasks.
        """
        self.tasks.clear()
        self.next_id = 1  # Reset the ID counter
        return True



def main():
    """
    Main function to demonstrate the TaskManager functionality.
    """
    manager = TaskManager()

    # Add tasks
    try:
        task1_id = manager.add("Grocery Shopping", "Buy milk, eggs, and bread")
        task2_id = manager.add("Book Doctor Appointment", "For annual checkup")
        print(f"Added Task 1 with ID: {task1_id}")  # Expected output: 1
        print(f"Added Task 2 with ID: {task2_id}")  # Expected output: 2
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print(f"All tasks: {all_tasks}")
    # Expected output (order may vary):  [{'id': 1, 'task_name': 'Grocery Shopping', 'task_description': 'Buy milk, eggs, and bread', 'is_finished': False}, {'id': 2, 'task_name': 'Book Doctor Appointment', 'task_description': 'For annual checkup', 'is_finished': False}]

    # Search for tasks
    try:
        search_results = manager.search("grocery")
        print(f"Search results for 'grocery': {search_results}")
        # Expected output: [{'id': 1, 'task_name': 'Grocery Shopping', 'task_description': 'Buy milk, eggs, and bread', 'is_finished': False}]

        search_results = manager.search("checkup")
        print(f"Search results for 'checkup': {search_results}")
         # Expected output: [{'id': 2, 'task_name': 'Book Doctor Appointment', 'task_description': 'For annual checkup', 'is_finished': False}]

        search_results = manager.search("NonExistentTask")  #test no matches found
        print(f"Search results for 'NonExistentTask': {search_results}") # Expected output: []


    except ValueError as e:
        print(f"Error searching: {e}")

    # Finish a task
    try:
        finish_status = manager.finish(task1_id)
        print(f"Finish task {task1_id}: {finish_status}")  # Expected: True
        finish_status = manager.finish(999)  # Test non-existent ID
        print(f"Finish task 999: {finish_status}")  # Expected: False


    except (TypeError, ValueError) as e:
        print(f"Error finishing task: {e}")


    # Remove a task
    try:
        remove_status = manager.remove(task2_id)
        print(f"Remove task {task2_id}: {remove_status}")  # Expected: True
        remove_status = manager.remove(999)  # Test non-existent ID
        print(f"Remove task 999: {remove_status}")  # Expected: False
    except (TypeError, ValueError) as e:
        print(f"Error removing task: {e}")

    # Get all tasks again (after finishing and removing)
    all_tasks = manager.get_all()
    print(f"All tasks after updates: {all_tasks}")
    # Expected output (order may vary): [{'id': 1, 'task_name': 'Grocery Shopping', 'task_description': 'Buy milk, eggs, and bread', 'is_finished': True}]

    # Clear all tasks
    clear_status = manager.clear_all()
    print(f"Clear all tasks: {clear_status}")  # Expected: True
    all_tasks = manager.get_all()
    print(f"All tasks after clearing: {all_tasks}") # Expected output: []

     # Test invalid input for add()
    try:
        manager.add("", "Description")  # Empty task name
    except ValueError as e:
        print(f"Expected error: {e}")   # Expected error: Task name cannot be empty.

    try:
        manager.add("Name", "")  # Empty task description
    except ValueError as e:
        print(f"Expected error: {e}")   # Expected error: Task description cannot be empty.
    
    # Test invalid inputs for finish()
    try:
        manager.finish(-1)   #negative ID
    except ValueError as e:
        print(f"Expected error: {e}")   #Expected error: Task ID must be a positive integer.

    try:
        manager.finish("abc")  #wrong ID type
    except TypeError as e:
        print(f"Expected error: {e}")   #Expected error: Task ID must be an integer.

    #Test empty input for search()
    try:
        manager.search("")
    except ValueError as e:
        print(f"Expected error: {e}")  #Expected error: Search term cannot be empty

    # Test invalid input for remove()
    try:
        manager.remove(0)  # zero ID
    except ValueError as e:
        print(f"Expected error: {e}")  # Expected error: Task ID must be a positive integer.


if __name__ == "__main__":
    main()

