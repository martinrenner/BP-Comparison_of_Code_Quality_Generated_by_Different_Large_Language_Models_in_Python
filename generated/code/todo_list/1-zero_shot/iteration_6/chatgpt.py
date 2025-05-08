#!/usr/bin/env python3
"""
Todo List Console Application

This module implements a console-based todo list application using OOP principles,
with functionality to add, remove, search, finish, retrieve, and clear tasks.
Each task is stored in memory with a unique ID, name, description, and status
(flagging whether the task is finished).

The TaskManager class methods are designed with input validation, error handling,
and efficiency in mind to meet high-quality standards (ISO/IEC 25010).
"""

class TaskManager:
    """
    Manages tasks with operations such as add, remove, search, finish, get_all, and clear_all.
    
    Each task is represented as a dictionary with the following keys:
        - id: A unique task identifier (int)
        - task_name: The name of the task (str)
        - task_description: A detailed description (str)
        - is_finished: A boolean indicating completion status
    """
    
    def __init__(self):
        """
        Initializes the TaskManager with an empty task store and sets the task ID counter.
        """
        self.tasks = {}  # Dictionary to store tasks with key as task id for O(1) lookups.
        self.next_task_id = 1  # Counter to assign unique task IDs.
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.
        
        Parameters:
            task_name (str): The name of the task.
            task_description (str): A detailed description of the task.
        
        Returns:
            int: The unique ID assigned to the new task.
        
        Raises:
            ValueError: If the task_name or task_description is empty or not a string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")
        
        task_id = self.next_task_id
        self.tasks[task_id] = {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': False
        }
        self.next_task_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.
        
        Parameters:
            task_id (int): The unique identifier of the task to remove.
        
        Returns:
            bool: True if the task was successfully removed.
        
        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If no task exists with the given task_id.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            raise KeyError(f"Task with id {task_id} does not exist.")
        
        del self.tasks[task_id]
        return True

    def search(self, task_term: str) -> list:
        """
        Searches for tasks matching the search term in either task name or description.
        
        Parameters:
            task_term (str): The search term to look for.
        
        Returns:
            list: A list of task dictionaries that match the search term.
        
        Raises:
            ValueError: If the search term is empty or not a string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")
        
        term = task_term.strip().lower()
        matching_tasks = []
        for task in self.tasks.values():
            if term in task['task_name'].lower() or term in task['task_description'].lower():
                matching_tasks.append(task)
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished (completed).
        
        Parameters:
            task_id (int): The unique identifier of the task to finish.
        
        Returns:
            bool: True if the task was successfully marked as finished.
        
        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If no task exists with the given task_id.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self.tasks:
            raise KeyError(f"Task with id {task_id} does not exist.")
        
        self.tasks[task_id]['is_finished'] = True
        return True

    def get_all(self) -> list:
        """
        Retrieves all tasks stored in the manager.
        
        Returns:
            list: A list of all task dictionaries.
        """
        return list(self.tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.
        
        Returns:
            bool: True after clearing all tasks.
        """
        self.tasks.clear()
        return True

def display_task(task: dict) -> None:
    """
    Prints a formatted representation of a single task.
    
    Parameters:
        task (dict): The task dictionary containing id, task_name, task_description, and is_finished.
    """
    status = "Finished" if task["is_finished"] else "Pending"
    print("---------------")
    print(f"ID           : {task['id']}")
    print(f"Task Name    : {task['task_name']}")
    print(f"Description  : {task['task_description']}")
    print(f"Status       : {status}")
    print("---------------")

def main():
    """
    Runs the console-based menu interface for the todo list application.
    Provides options for each of the task management functions.
    """
    print("Welcome to the Todo List App!")
    manager = TaskManager()
    
    menu = (
        "\nMenu:\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Finish Task\n"
        "5. Get All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
    )
    
    while True:
        print(menu)
        choice = input("Please select an option (1-7): ").strip()
        
        if choice == '1':  # Add Task
            try:
                task_name = input("Enter task name: ").strip()
                task_description = input("Enter task description: ").strip()
                task_id = manager.add(task_name, task_description)
                print(f"Task added successfully with ID: {task_id}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':  # Remove Task
            try:
                task_id_input = input("Enter task ID to remove: ").strip()
                task_id = int(task_id_input)
                manager.remove(task_id)
                print(f"Task with ID {task_id} removed successfully.")
            except ValueError as ve:
                print(f"Error: {ve}")
            except KeyError as ke:
                print(f"Error: {ke}")
        
        elif choice == '3':  # Search Tasks
            try:
                search_term = input("Enter search term for task name or description: ").strip()
                results = manager.search(search_term)
                if results:
                    print("Matching Tasks:")
                    for task in results:
                        display_task(task)
                else:
                    print("No matching tasks found.")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '4':  # Finish Task
            try:
                task_id_input = input("Enter task ID to mark as finished: ").strip()
                task_id = int(task_id_input)
                manager.finish(task_id)
                print(f"Task with ID {task_id} marked as finished.")
            except ValueError as ve:
                print(f"Error: {ve}")
            except KeyError as ke:
                print(f"Error: {ke}")
        
        elif choice == '5':  # Get All Tasks
            tasks = manager.get_all()
            if tasks:
                print("All Tasks:")
                for task in tasks:
                    display_task(task)
            else:
                print("No tasks found.")
        
        elif choice == '6':  # Clear All Tasks
            confirmation = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
            if confirmation == 'y':
                manager.clear_all()
                print("All tasks have been cleared.")
            else:
                print("Clear operation canceled.")
        
        elif choice == '7':  # Exit
            print("Exiting the Todo List App. Goodbye!")
            break
        
        else:
            print("Invalid selection. Please choose an option from 1 to 7.")

if __name__ == "__main__":
    main()
