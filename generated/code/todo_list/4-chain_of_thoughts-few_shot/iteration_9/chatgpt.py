#!/usr/bin/env python3
"""
Console-based Todo List Application

This application allows users to add, remove, search, finish, retrieve, and clear tasks from a todo list.
The TaskManager class implements the core functionality using an in-memory dictionary for efficient lookups,
insertions, and deletions.

The code is designed following ISO/IEC 25010 quality standards, emphasizing correctness, performance, modularity,
security, testability, readability, and maintainability.
"""

class TaskManager:
    """
    A class to manage tasks in a todo list.
    
    Each task is represented as a dictionary with the following structure:
        {
            'id': int,
            'task_name': str,
            'task_description': str,
            'is_finished': bool
        }
        
    Tasks are stored in an in-memory dictionary with task IDs as keys.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and sets the starting ID for tasks.
        """
        self.tasks = {}   # Dictionary to store tasks for O(1) access by task ID.
        self.next_id = 1  # Auto-incrementing ID for new tasks.

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with a given name and description.
        
        Args:
            task_name (str): The name of the task. Must be a non-empty string.
            task_description (str): The description of the task. Must be a non-empty string.
            
        Returns:
            int: The unique ID assigned to the newly added task.
            
        Raises:
            ValueError: If task_name or task_description is an empty string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self.next_id
        self.tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        self.next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.
        
        Args:
            task_id (int): The unique ID of the task to be removed. Must be a positive integer.
            
        Returns:
            bool: True if the task was successfully removed, False if the task does not exist.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        return True

    def search(self, task_term: str) -> list:
        """
        Searches for tasks whose name or description contains the search term.
        The search is case-insensitive.
        
        Args:
            task_term (str): The term to search for in task names and descriptions.
            
        Returns:
            list[dict]: A list of tasks (as dictionaries) that match the search criteria.
            
        Raises:
            ValueError: If task_term is not a string or is an empty string.
        """
        if not isinstance(task_term, str):
            raise ValueError("Search term must be a string.")
        term = task_term.strip()
        if not term:
            raise ValueError("Search term cannot be empty.")

        term_lower = term.lower()
        results = [
            task for task in self.tasks.values()
            if term_lower in task['task_name'].lower() or term_lower in task['task_description'].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished using its unique ID.
        
        Args:
            task_id (int): The unique ID of the task to mark as finished.
            
        Returns:
            bool: True if the task was found and marked as finished, False if the task does not exist.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

        if task_id not in self.tasks:
            return False

        self.tasks[task_id]['is_finished'] = True
        return True

    def get_all(self) -> list:
        """
        Retrieves all tasks with their details.
        
        Returns:
            list[dict]: A list of all tasks, each containing the task's id, name, description, and finish status.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the todo list.
        
        Returns:
            bool: True indicating that all tasks were cleared.
        """
        self.tasks.clear()
        return True


def main():
    """
    Main function to run the console-based todo list app.
    
    Provides a command-line interface for users to interact with the TaskManager.
    """
    manager = TaskManager()
    print("Welcome to the Console-Based Todo List App!")
    print("Available commands: add, remove, search, finish, get_all, clear_all, exit")
    print("------------------------------------------------------------")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == 'exit':
            print("Exiting the application. Goodbye!")
            break

        try:
            if command == 'add':
                task_name = input("Enter task name: ")
                task_description = input("Enter task description: ")
                task_id = manager.add(task_name, task_description)
                print(f"Task added successfully with ID: {task_id}")

            elif command == 'remove':
                task_id_input = input("Enter the task ID to remove: ")
                if not task_id_input.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_input)
                if manager.remove(task_id):
                    print(f"Task {task_id} removed successfully.")
                else:
                    print(f"Task with ID {task_id} does not exist.")

            elif command == 'search':
                term = input("Enter search term: ")
                results = manager.search(term)
                if results:
                    print("Matching Tasks:")
                    for task in results:
                        print(f"ID: {task['id']}, Name: {task['task_name']}, "
                              f"Description: {task['task_description']}, Finished: {task['is_finished']}")
                else:
                    print("No matching tasks found.")

            elif command == 'finish':
                task_id_input = input("Enter the task ID to mark as finished: ")
                if not task_id_input.isdigit():
                    print("Invalid input. Task ID must be a positive integer.")
                    continue
                task_id = int(task_id_input)
                if manager.finish(task_id):
                    print(f"Task {task_id} marked as finished.")
                else:
                    print(f"Task with ID {task_id} does not exist.")

            elif command == 'get_all':
                tasks = manager.get_all()
                if tasks:
                    print("All Tasks:")
                    for task in tasks:
                        print(f"ID: {task['id']}, Name: {task['task_name']}, "
                              f"Description: {task['task_description']}, Finished: {task['is_finished']}")
                else:
                    print("No tasks available.")

            elif command == 'clear_all':
                confirm = input("Are you sure you want to clear all tasks? (Y/N): ").strip().lower()
                if confirm == 'y':
                    if manager.clear_all():
                        print("All tasks have been cleared.")
                else:
                    print("Clear all operation cancelled.")

            else:
                print("Invalid command. Please try again with a valid command.")

        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

if __name__ == '__main__':
    main()
