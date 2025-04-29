class TaskManager:
    """
    Manages a list of tasks, allowing for adding, removing, searching,
    finishing, retrieving, and clearing tasks.  Implements ISO/IEC 25010
    quality characteristics.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and a starting ID.
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
        return False

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks matching a given term in their name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: A list of tasks matching the search term.  Returns an
                         empty list if no matches are found.

        Raises:
            ValueError: If task_term is empty.
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
            bool: True if the task was found and marked as finished,
                  False otherwise.

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
        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks in the task list.

        Returns:
            list[dict]: A list of all tasks, each represented as a dictionary.
        """
        # Return a list of copies of the task dictionaries to prevent
        # external modification of the internal task data.
        return [task.copy() for task in self.tasks.values()]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the task list.

        Returns:
            bool: Always returns True, indicating successful clearance.
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
        task2_id = manager.add("Book Appointment", "Dentist appointment next week")
        print(f"Added Task 1 ID: {task1_id}")  # Output Added Task 1 ID: 1
        print(f"Added Task 2 ID: {task2_id}")  # Output Added Task 2 ID: 2
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    all_tasks = manager.get_all()
    print(f"All Tasks: {all_tasks}")
    # Expected Output (order may vary):
    # All Tasks: [{'id': 1, 'name': 'Grocery Shopping', 'description': 'Buy milk, eggs, and bread', 'is_finished': False}, {'id': 2, 'name': 'Book Appointment', 'description': 'Dentist appointment next week', 'is_finished': False}]

    # Search for tasks
    try:
        search_results = manager.search("grocery")
        print(f"Search Results for 'grocery': {search_results}")
        # Expected Output: Search Results for 'grocery': [{'id': 1, 'name': 'Grocery Shopping', 'description': 'Buy milk, eggs, and bread', 'is_finished': False}]

        search_results = manager.search("appointment")
        print(f"Search Results for 'appointment': {search_results}")
        # Expected Output: Search Results for 'appointment': [{'id': 2, 'name': 'Book Appointment', 'description': 'Dentist appointment next week', 'is_finished': False}]
    except ValueError as e:
        print(f"Error searching for tasks: {e}")

    # Finish a task
    try:
        finish_status = manager.finish(task1_id)
        print(f"Finish Task 1: {finish_status}")  # Expected Output: Finish Task 1: True
        all_tasks = manager.get_all()
        print(f"All Tasks (after finishing one): {all_tasks}")
        # Expected Output(order may vary):
        # All Tasks: [{'id': 1, 'name': 'Grocery Shopping', 'description': 'Buy milk, eggs, and bread', 'is_finished': True}, {'id': 2, 'name': 'Book Appointment', 'description': 'Dentist appointment next week', 'is_finished': False}]

        finish_status = manager.finish(999)  # Non-existent task
        print(f"Finishing the non-existent task returned: {finish_status}")
        # Expected Output: Finishing the non-existent task returned: False

    except (TypeError, ValueError) as e:
        print(f"Error finishing task: {e}")

    
    # Remove by ID
    try:
        is_removed = manager.remove(task2_id)
        print(f"Removing the task with ID {task2_id} was: {is_removed}")
        # Expected Output Removing the task with ID 2 was: True
        all_tasks = manager.get_all()
        print(f"All Tasks (after removing Task 2): {all_tasks}")
        # All Tasks (after removing Task 2): [{'id': 1, 'name': 'Grocery Shopping', 'description': 'Buy milk, eggs, and bread', 'is_finished': True}]

        is_removed = manager.remove(999)  # non-existed ID
        print(f"Removing the non-existent task returned: {is_removed}")
        # Expected Output Removing the non-existent task returned: False
    
    except (TypeError, ValueError) as e:
         print(f"Removing Task 2 error: {e}")       

    # Clear all tasks
    clear_status = manager.clear_all()
    print(f"Clear All Tasks: {clear_status}")  # Expected Output: Clear All Tasks: True
    print(f"All tasks after clearing: {manager.get_all()}")  # ExpectedOutput: []

    # Add task with empty name
    try:
        manager.add("", "Description")
    except ValueError as e:
        print(f"Caught expected error: {e}")  # ExpectedOutput: Caught expected error: Task namecannot be empty.

    # Add task with empty description
    try:
        manager.add("Task Name", "")
    except ValueError as e:
        print(f"Caught expected error: {e}")  # ExpectedOutput: Caught expected error: Task description cannot be empty.

     # Removing a non-integer ID
    try:
        manager.remove("abc")
    except TypeError as e:
        print(f"Caught expected error (remove): {e}")  
        # Expected Output: Caught expected error (remove): Task ID must be an integer.

    # Removing a negative ID
    try:
        manager.remove(-1)
    except ValueError as e:
        print(f"Caught expected error (remove negative): {e}")  
        # Expected Output: Caught expected error (remove negative): Task ID cannot be negative.
    
     # Finishing a non-integer ID
    try:
        manager.finish("abc")
    except TypeError as e:
        print(f"Caught expected error (remove): {e}")  
        # Expected Output: Caught expected error (remove): Task ID must be an integer.

    # Finishing a negative ID
    try:
        manager.finish(-1)
    except ValueError as e:
        print(f"Caught expected error (remove negative): {e}")  
        # Expected Output: Caught expected error (remove negative): Task ID cannot be negative.

    # Search with empty task_term
    try:
        manager.search("")
    except ValueError as e:
        print(f"Caught expected error: {e}")  # ExpectedOutput: Caught expected error: Search term cannot be empty.


if __name__ == "__main__":
    main()
