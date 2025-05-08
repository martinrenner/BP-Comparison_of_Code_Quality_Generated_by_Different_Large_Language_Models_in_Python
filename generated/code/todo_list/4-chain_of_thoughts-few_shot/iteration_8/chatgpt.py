class TaskManager:
    """
    A class to manage tasks in a console-based todo list app.
    
    This class implements functionality for adding, removing, searching, 
    finishing, retrieving, and clearing tasks. Each task is stored as a 
    dictionary with the keys: 'id', 'task_name', 'task_description', and 'is_finished'.
    """

    def __init__(self):
        """
        Initializes a new instance of TaskManager with in-memory storage for tasks.
        """
        self.tasks = {}  # Dictionary to store tasks: key -> task id, value -> task dict.
        self.next_id = 1  # Auto-incrementing task id for uniqueness.

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with a name and description.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is an empty string.
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
            "is_finished": False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task identified by its unique ID.

        Args:
            task_id (int): The unique ID of the task to be removed.

        Returns:
            bool: True if the task was found and removed, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> list:
        """
        Searches for tasks where the task name or description contains the search term.

        Args:
            task_term (str): The search term to filter tasks.

        Returns:
            list: A list of task dictionaries that match the search term.

        Raises:
            ValueError: If task_term is an empty string.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        results = []
        lower_term = task_term.lower()
        # Search the tasks for a matching term in name or description.
        for task in self.tasks.values():
            if (lower_term in task["task_name"].lower() or
                    lower_term in task["task_description"].lower()):
                results.append(task)
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks the task with the given ID as completed.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if the task exists and is marked as completed, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self.tasks:
            self.tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> list:
        """
        Retrieves all tasks.

        Returns:
            list: A list of task dictionaries, each containing:
                  (id, task_name, task_description, is_finished)
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Clears all tasks from the todo list.

        Returns:
            bool: True after all tasks have been cleared.
        """
        self.tasks.clear()
        return True


def main():
    """
    Provides console-based interaction for the todo list app.
    Users can add, remove, search, finish, display all, and clear tasks.
    """
    task_manager = TaskManager()
    menu = (
        "\nTodo List App Commands:\n"
        "1. add        - Add a new task\n"
        "2. remove     - Remove a task by ID\n"
        "3. search     - Search tasks by term\n"
        "4. finish     - Mark a task as finished\n"
        "5. get_all    - Display all tasks\n"
        "6. clear_all  - Clear all tasks\n"
        "7. exit       - Exit the application\n"
    )
    print("Welcome to the Todo List App!")
    
    while True:
        print(menu)
        command = input("Enter command: ").strip().lower()

        if command == "add" or command == "1":
            try:
                task_name = input("Enter task name: ").strip()
                task_desc = input("Enter task description: ").strip()
                task_id = task_manager.add(task_name, task_desc)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as e:
                print("Error:", e)

        elif command == "remove" or command == "2":
            try:
                task_id_input = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_input)
                if task_manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found. Please check the task ID and try again.")
            except (ValueError, TypeError) as e:
                print("Error:", e)

        elif command == "search" or command == "3":
            try:
                search_term = input("Enter search term: ").strip()
                results = task_manager.search(search_term)
                if results:
                    print("Found tasks:")
                    for task in results:
                        print(f"{task['id']}: {task['task_name']} - {task['task_description']} "
                              f"[Finished: {task['is_finished']}]")
                else:
                    print("No tasks match your search term.")
            except ValueError as e:
                print("Error:", e)

        elif command == "finish" or command == "4":
            try:
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_input)
                if task_manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found. Please check the task ID and try again.")
            except (ValueError, TypeError) as e:
                print("Error:", e)

        elif command == "get_all" or command == "5":
            tasks = task_manager.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    print(f"{task['id']}: {task['task_name']} - {task['task_description']} "
                          f"[Finished: {task['is_finished']}]")
            else:
                print("No tasks to display.")

        elif command == "clear_all" or command == "6":
            confirmation = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirmation == "yes":
                if task_manager.clear_all():
                    print("All tasks have been cleared.")
            else:
                print("Clear all tasks operation cancelled.")

        elif command == "exit" or command == "7":
            print("Exiting the Todo List App. Goodbye!")
            break

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
