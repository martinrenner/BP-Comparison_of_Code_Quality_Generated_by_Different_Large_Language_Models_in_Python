import re
from os import path

from config import ITERATIONS, MODELS, MODEL_DETAILS, PROMPTS, RESULTS_DIR, CHALLENGES


# Helper functions
def get_search_match(file_content: str, regex: str) -> re.Match:
    """
    Returns the match object of the regex in the file.

    Args:
        file_path (str): The path to the file to be checked.
        regex (str): The regex to be used to search the file.

    Returns:
        re.Match: The match object of the regex in the file.
    """
    return re.search(regex, file_content)


def get_all_search_matches(file_content: str, regex: str) -> list[re.Match]:
    """
    Returns a list of match objects of the regex in the file.

    Args:
        file_path (str): The path to the file to be checked.
        regex (str): The regex to be used to search the file.

    Returns:
        list[re.Match]: A list of match objects of the regex in the file.
    """
    return re.findall(regex, file_content)


def append_column_header_in_buffer_header(column: str, BUFFER_HEADER: list[str]) -> None:
    """
    Checks if the column is in the BUFFER_HEADER and appends it if not.

    Args:
        column (str): The column to be checked.
        BUFFER_HEADER (list): A list to store header information.

    Returns:
        None
    """
    if column not in BUFFER_HEADER:
        BUFFER_HEADER.append(column)


def get_file_content(file_path: str) -> str:
    """
    Returns the content of the file.

    Args:
        file_path (str): The path to the file to be checked.

    Returns:
        str: The content of the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def delete_old_file_content(file_path: str) -> None:
    """
    Deletes the old content of the file.

    Args:
        file_path (str): The path to the file to be checked.

    Returns:
        None
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("")


def process_regex(file_path: str, rule: dict, buffer: list[str], buffer_header: list[str]) -> None:
    """
    Processes a file based on regex rules and updates the buffer and buffer_header.

    Args:
        file_path (str): The path to the file to be processed.
        rule (dict): A dictionary containing the regex rules and columns to be processed.
        buffer (list[str]): A list to store the processed values.
        buffer_header (list[str]): A list to store the column headers.

    Returns:
        None
    """
    for col in rule["columns"]:
        if col not in buffer_header:
            buffer_header.append(col)

    content = get_file_content(file_path)

    for regex in rule["regex"]:
        if regex["type"] == "bool":
            match = get_search_match(content, regex["rule"])
            buffer.append(1 if match else 0)

        elif regex["type"] == "int":
            match = get_search_match(content, regex["rule"])
            buffer.append(int(match.group(1)) if match else "")

        elif regex["type"] == "float":
            match = get_search_match(content, regex["rule"])
            buffer.append(float(match.group(1) + "." + match.group(2)) if match else "")

        elif regex["type"] == "float_multiple":
            matches = get_all_search_matches(content, regex["rule"])
            if len(matches) == regex["expected_rows"]:
                for match in matches:
                    if len(match) == regex["expected_columns"]:
                        for i in range(0, len(match), 2):
                            buffer.append(float(match[i] + "." + match[i+1]) if match else "")
                    else:
                        for _ in range(regex["expected_columns"]):
                            buffer.append("")
            else:
                expected_floats = regex["expected_columns"] // 2
                for _ in range(regex["expected_rows"]):
                    for _ in range(expected_floats):
                        buffer.append("")



def main() -> None:
    for challenge in CHALLENGES:
        first = True
        BUFFER_HEADER = ["challenge", "provider", "model", "prompt_type", "iteration"]
        delete_old_file_content(f"{RESULTS_DIR}/{challenge}/results.csv")

        for prompt_type in PROMPTS:
            for iteration in range(1, ITERATIONS + 1):
                for model in MODELS:
                    BUFFER = [
                        challenge,
                        MODEL_DETAILS[model]["provider"],
                        MODEL_DETAILS[model]["model"],
                        prompt_type,
                        iteration,
                    ]

                    for rule in CHALLENGES[challenge]["regex_rules"]:
                        file_path = f"{RESULTS_DIR}/{challenge}/{prompt_type}/iteration_{iteration}/{rule['file'].replace('{model}', model)}"
                        if path.exists(file_path):
                            process_regex(file_path, rule, BUFFER, BUFFER_HEADER)
                        else:
                            for _ in rule["columns"]:
                                BUFFER.append("")
                        
                    with open(f"{RESULTS_DIR}/{challenge}/results.csv", "a") as file:
                        file.write(",".join(BUFFER_HEADER) + "\n") if first else None
                        first = False
                        file.write(",".join(map(str, BUFFER)) + "\n")

if __name__ == "__main__":
    main()
