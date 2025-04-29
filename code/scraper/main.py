"""
This script generates code and response files for each challenge, prompt, and iteration using different language models (LLMs).
"""

from os import makedirs

from config import LLMS, CHALLENGES, ITERATIONS
from helpers import exctract_python_code


def prompt_for_code() -> None:
    """
    Generates code and response files for each challenge, prompt, and iteration using different language models (LLMs).

    The function iterates over a list of challenges, each containing multiple prompts. For each prompt, it iterates over
    a list of LLMs and a specified number of iterations. For each combination, it creates directories to store the generated
    code and response files. It then queries the LLM with the prompt and writes the response and extracted Python code to
    the respective files.

    Returns:
        None

    Directories created:
        - generated/code/{challenge.name}/{prompt.name}/iteration_{i}
        - generated/response/{challenge.name}/{prompt.name}/iteration_{i}

    Files created:
        - generated/response/{challenge.name}/{prompt.name}/iteration_{i}/{llm.name}_response.txt
        - generated/code/{challenge.name}/{prompt.name}/iteration_{i}/{llm.name}.py
    """
    for challenge in CHALLENGES:
        for prompt in challenge.prompts:
            for llm in LLMS:
                for i in range(1, ITERATIONS + 1):
                    makedirs(
                        f"generated/code/{challenge.name}/{prompt.name}/iteration_{i}",
                        exist_ok=True,
                    )
                    makedirs(
                        f"generated/response/{challenge.name}/{prompt.name}/iteration_{i}",
                        exist_ok=True,
                    )

                    print(
                        f"Generating code for {challenge.name} - {prompt.name} - iteration [{i}] ({llm.name})"
                    )
                    answer = llm.query(prompt.prompt)

                    with open(
                        f"generated/response/{challenge.name}/{prompt.name}/iteration_{i}/{llm.name}_response.txt",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(answer.choices[0].message.content)

                    with open(
                        f"generated/code/{challenge.name}/{prompt.name}/iteration_{i}/{llm.name}.py",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(exctract_python_code(answer.choices[0].message.content))


if __name__ == "__main__":
    prompt_for_code()
