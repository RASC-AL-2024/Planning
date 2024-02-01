# Import Required Packages
import os
import openai
from jinja2 import Environment, PackageLoader, FileSystemLoader
from typing import List, Dict, Tuple

# Configure Jinja
#template_loader = FileSystemLoader(searchpath = 'intelligence/gpt/prompts/')
env = Environment(
    loader = PackageLoader(package_name = "src/highlevel", package_path='prompts')
)
#env = Environment(loader = template_loader, autoescape = True)

# Define Persona Class
class Persona():
    def __init__(self, 
                 name: str,
                 prompt_path: str = None,
                 prompt: str = None,
                 system_prompt: str = "",
                 model_name: str = "gpt-3.5-turbo",
                 temperature: float = 0.8):
        """
        Persona
        Creates and maintains a persona that you can interact with using the conversation
        API from openAI. Either the prompt path (which is a jinja txt file stored in DroneFormer-CF/prompts)
        or a naive string format string ({var_name} for arguments) must be passed. If both are passed,
        jinja files are preferred. If none are passed, throws an exception
        """
        if not os.getenv("OPENAI_API_KEY"):
            raise Exception("OpenAI API key not found, pelase set OPENAI_API_KEY env var")
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if prompt_path is None and prompt is None:
            raise ValueError("Either prompt_path or prompt parameters should be specified, but both cannot be empty.")

        self.prompt = prompt
        self.system_prompt = system_prompt
        if prompt_path:
            self.prompt = env.get_template("user/{}".format(prompt_path))
            self.system_prompt = env.get_template("system/{}".format(prompt_path))

        self.name = name
        self.model_name = model_name
        self.temperature = temperature


    def format_prompt(self, args: Dict, system: bool = False) -> str:
        """
        Formats the prompt depending on whether it's a string prompt or a more complex jinja prompt
        if it's the latter, then render with the appropriate arguments, and if former, format.

        Params:
            args (Dict): argument dictionary
            system (bool): whether the arguments should be applied to system prompt

        Returns:
            str: complete formatted prompt
        """
        if not isinstance(self.prompt, str):
            return self.system_prompt.render(**args) if system else self.prompt.render(**args)
        return self.system_prompt.format(**args) if system else self.prompt.format(**args)

    def chat_simple(self, prompt):
        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
            model = self.model_name,
            messages = messages,
            temperature = self.temperature
        )

        content = response.choices[0]["message"]["content"]
        return content

    def chat(self, system_args: Dict, prompt_args: Dict, prev_context: List[Dict[str, str]] = None) -> Tuple[str, List[Dict]]:
        """
        sends a request to the OpenAI API to generate a response.
        If the prompt_args does not cover all the fields specified in the prompt string,
        then it will throw a KeyError exception. Previous context is a list of dicts formatted
        as such: [{"role": "assistant", "content", "bla bla"}, {"role", "user",
        "content": "bla bla"}, ...].

        Method will return a tuple of the immediately returned message as well as an updated list
        of previous messages that can be used as context to be passed into this method.
        
        Params:
            prompt_args (Dict): specifies arguments to the prompt
            prev_context (List[Dict[str,str]]): context for previous conversations
        """
        complete_prompt = self.format_prompt(prompt_args, system=False) 
        messages = [{"role": "system", "content": self.format_prompt(system_args, system=True)}]

        if prev_context:
            messages.extend(prev_context)
        messages.append({"role": "user", "content": complete_prompt})

        response = openai.ChatCompletion.create(
            model = self.model_name,
            messages = messages,
            temperature = self.temperature
        )
        
        content = response.choices[0]["message"]["content"]
        messages = messages[1:] + [{"role": "assistant", "content": content}]
        return content, messages
    