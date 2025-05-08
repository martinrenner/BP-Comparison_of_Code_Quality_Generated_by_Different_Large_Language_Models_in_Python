"""
This module contains the LLM class that is used to interact with the OpenAI chat completion model.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion


load_dotenv()


class Llm:
    """
    This class is used to interact with the OpenAI chat completion model.
    """

    def __init__(self, model: str, name: str):
        """
        Initializes the LLM class with the specified model and name.

        Args:
            model (str): The model identifier to be used.
            name (str): The name of the instance.

        Attributes:
            model (str): The model identifier.
            name (str): The name of the instance.
            client (OpenAI): The OpenAI client initialized with the base URL and API key from environment variables.
        """
        self.model = model
        self.name = name
        self.client = OpenAI(
            base_url=os.getenv("OPENROUTER_API_URL"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def query(self, question: str) -> ChatCompletion:
        """
        Sends a query to the chat completion model and returns the response.

        Args:
            question (str): The question or prompt to send to the chat model.

        Returns:
            ChatCompletion: The response from the chat completion model.
        """
        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": question},
            ],
        )
