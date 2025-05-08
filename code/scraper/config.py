"""
Configuration file for the scraper
Contains the following:
- LLMS - list of LLMs to be used
- CHALLENGES - list of challenges to be sent to the LLMs
- ITERATIONS - number of iterations for each prompt
"""

from llm import Llm
from challange import Challenge
from prompt import Prompt
from helpers import load_string_from_file

# LLMs - list of LLMs to be used
LLMS = [
    Llm("openai/o3-mini-high", "chatgpt"),  # LLM 1
    Llm("anthropic/claude-3.7-sonnet", "claude"),  # LLM 2
    Llm("google/gemini-2.0-pro-exp-02-05", "gemini"),  # LLM 3
]

# Challenges - list of challenges to be sent to the LLMs
CHALLENGES = [
    # Challenge 1 - Calculator
    Challenge(
        "calculator",
        [
            Prompt(
                "1-zero_shot",
                load_string_from_file("prompts/calculator/1-zero_shot.txt"),
            ),
            Prompt(
                "2-few_shot", load_string_from_file("prompts/calculator/2-few_shot.txt")
            ),
            Prompt(
                "3-chain_of_thoughts-zero_shot",
                load_string_from_file(
                    "prompts/calculator/3-chain_of_thoughts-zero_shot.txt"
                ),
            ),
            Prompt(
                "4-chain_of_thoughts-few_shot",
                load_string_from_file(
                    "prompts/calculator/4-chain_of_thoughts-few_shot.txt"
                ),
            ),
            Prompt(
                "5-role-zero_shot",
                load_string_from_file("prompts/calculator/5-role-zero_shot.txt"),
            ),
            Prompt(
                "6-role-few_shot",
                load_string_from_file("prompts/calculator/6-role-few_shot.txt"),
            ),
        ],
    ),
    # Challenge 2 - ASCII art
    Challenge(
        "ascii_art",
        [
            Prompt(
                "1-zero_shot",
                load_string_from_file("prompts/ascii_art/1-zero_shot.txt"),
            ),
            Prompt(
                "2-few_shot", load_string_from_file("prompts/ascii_art/2-few_shot.txt")
            ),
            Prompt(
                "3-chain_of_thoughts-zero_shot",
                load_string_from_file(
                    "prompts/ascii_art/3-chain_of_thoughts-zero_shot.txt"
                ),
            ),
            Prompt(
                "4-chain_of_thoughts-few_shot",
                load_string_from_file(
                    "prompts/ascii_art/4-chain_of_thoughts-few_shot.txt"
                ),
            ),
            Prompt(
                "5-role-zero_shot",
                load_string_from_file("prompts/ascii_art/5-role-zero_shot.txt"),
            ),
            Prompt(
                "6-role-few_shot",
                load_string_from_file("prompts/ascii_art/6-role-few_shot.txt"),
            ),
        ],
    ),
    # Challenge 3 - TODO list
    Challenge(
        "todo_list",
        [
            Prompt(
                "1-zero_shot",
                load_string_from_file("prompts/todo_list/1-zero_shot.txt"),
            ),
            Prompt(
                "2-few_shot", load_string_from_file("prompts/todo_list/2-few_shot.txt")
            ),
            Prompt(
                "3-chain_of_thoughts-zero_shot",
                load_string_from_file(
                    "prompts/todo_list/3-chain_of_thoughts-zero_shot.txt"
                ),
            ),
            Prompt(
                "4-chain_of_thoughts-few_shot",
                load_string_from_file(
                    "prompts/todo_list/4-chain_of_thoughts-few_shot.txt"
                ),
            ),
            Prompt(
                "5-role-zero_shot",
                load_string_from_file("prompts/todo_list/5-role-zero_shot.txt"),
            ),
            Prompt(
                "6-role-few_shot",
                load_string_from_file("prompts/todo_list/6-role-few_shot.txt"),
            ),
        ],
    ),
]

# ITERATIONS - number of iterations for each prompt
ITERATIONS = 10
