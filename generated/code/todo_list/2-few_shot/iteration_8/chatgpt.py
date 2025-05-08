#!/usr/bin/env python3
"""
Console-Based Todo List App

This module implements a console-based todo list application using OOP. It
provides a TaskManager class that meets the requirements of ISO/IEC 25010,
supporting functions such as add, remove, search, finish, get_all, and clear_all.
Each task is stored in an in-memory dictionary with the keys:
    - id: Unique integer identifier
    - task_name: The name of the task
    - task_description: A description of the task
    - is_finished: A boolean indicating if the task is completed

Usage:
    Run this script, and follow the on-screen prompts to interact with the todo list.
"""

from typing import List, Dict

class TaskManager:
    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task dictionary and a counter for unique IDs.
        """
        self.tasks: Dict[int, dict] = {}
        self.next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the todo list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: A unique identifier for the newly added task.

        Raises:
            ValueError: If task_name or task_description are empty.
        """
        if not task_name.strip() or not task_description.strip():
            raise ValueError("Task name and description cannot be empty.")
        
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
        Removes a task by its unique ID.

        Args:
            task_id (int): The unique identifier of the task to remove.

        Returns:
            bool: True if the task was successfully removed.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If the task with the provided ID does not exist.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            raise KeyError(f"Task with id {task_id} does not exist.")
        del self.tasks[task_id]
        return True

    def search(self, task_term: str) -> List[dict]:
        """
        Searches for tasks that contain the given search term in their name or description.

        Args:
            task_term (str): The search term to look for within the task name or description.

        Returns:
            List[dict]: A list of task dictionaries that match the search criteria.

        Raises:
            ValueError: If the search term is empty.
        """
        if not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        
        # Case-insensitive search in both name and description
        term_lower = task_term.lower()
        results = [
            task for task in self.tasks.values() 
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The unique identifier of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked as finished.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If the task with the provided ID does not exist.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            raise KeyError(f"Task with id {task_id} does not exist.")
        self.tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[dict]:
        """
        Retrieves all tasks in the todo list.

        Returns:
            List[dict]: A list of all task dictionaries.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the todo list.

        Returns:
            bool: True if all tasks were successfully cleared.
        """
        self.tasks.clear()
        self.next_id = 1
        return True

def main() -> None:
    """
    Provides a console-based interface for interacting with the TaskManager.
    Users can add, remove, search, finish tasks, retrieve all tasks, or clear the list.
    """
    task_manager = TaskManager()
    print("Welcome to the Console-based Todo List App!")
    print("Available commands: add, remove, search, finish, get_all, clear_all, exit")

    while True:
        command = input("\nEnter command: ").strip().lower()
        if command == "add":
            try:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = task_manager.add(task_name, task_description)
                print(f"Task added with ID: {task_id}")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif command == "remove":
            try:
                task_id_str = input("Enter task ID to remove: ").strip()
                if not task_id_str.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(task_id_str)
                task_manager.remove(task_id)
                print(f"Task with ID {task_id} removed successfully.")
            except (ValueError, KeyError) as e:
                print(f"Error: {e}")

        elif command == "search":
            try:
                task_term = input("Enter search term: ").strip()
                results = task_manager.search(task_term)
                if results:
                    print("Matching tasks:")
                    for task in results:
                        print(f"ID: {task['id']} | Name: {task['task_name']} | "
                              f"Description: {task['task_description']} | Finished: {task['is_finished']}")
                else:
                    print("No matching tasks found.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif command == "finish":
            try:
                task_id_str = input("Enter task ID to mark as finished: ").strip()
                if not task_id_str.isdigit():
                    raise ValueError("Task ID must be a positive integer.")
                task_id = int(task_id_str)
                task_manager.finish(task_id)
                print(f"Task with ID {task_id} marked as finished.")
            except (ValueError, KeyError) as e:
                print(f"Error: {e}")

        elif command == "get_all":
            tasks = task_manager.get_all()
            if tasks:
                print("All tasks:")
                for task in tasks:
                    print(f"ID: {task['id']} | Name: {task['task_name']} | "
                          f"Description: {task['task_description']} | Finished: {task['is_finished']}")
            else:
                print("No tasks available.")

        elif command == "clear_all":
            confirm = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirm == "y":
                task_manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Operation cancelled.")

        elif command == "exit":
            print("Exiting the Todo List App. Goodbye!")
            break

        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
