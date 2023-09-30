import json
import os
from dataclasses import dataclass, asdict
import textwrap

import openai
from dotenv import load_dotenv
from metaphor_python import Metaphor

load_dotenv()


@dataclass
class Socials:
    """Class representing the social media handles and contact details of an expert."""

    twitter: str
    linkedin: str
    github: str
    website: str
    email: str

    def to_dict(self) -> dict:
        """Converts the instance to a dictionary representation."""
        return asdict(self)


@dataclass
class ExpertInformation:
    """Class representing the information/details about an expert."""

    name: str
    affiliation: str
    location: str
    summary: str
    socials: Socials

    def to_dict(self) -> dict:
        """Converts the instance to a dictionary representation."""
        return asdict(self)


class Assistant:
    """Class representing an assistant to find and display expert information."""

    SYSTEM_MESSAGE = ("You are a helpful assistant that generates search queries based on user questions. "
                      "Only generate one search query. The query should help to find experts on the topic of "
                      "the user question. It should be INDIVIDUAL perople, so no organisation as a whole or "
                      "something in that direction. A personal website is preferable over LinkedIn. "
                      "Expand abbreviations into full words to make it more specific. I.e. RL to Reinforcement Learning. "
                      "Or LLM to Large Language Model. "
                      "Ideally their website and optionally within a certain location or close to it.")

    def __init__(self):
        self.openai_key = os.environ["OPENAI_API_KEY"]
        self.metaphor = Metaphor(os.environ["METAPHOR_API_KEY"])
        openai.api_key = self.openai_key

    def get_search_query(self, user_question: str) -> str:
        """Generates a search query based on the provided user question."""

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.SYSTEM_MESSAGE},
                {"role": "user", "content": user_question},
            ],
        )
        return completion.choices[0].message.content


    def get_expert_from_html(self, html_content: str) -> ExpertInformation | None:
        """Extracts expert information from the provided HTML content."""
        functions = [
            {
                "name": "get_expert_information",
                "description": "Get the important information about the expert",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The full name (first name and last name) of the expert"
                        },
                        "affiliation": {
                            "type": "string",
                            "description": "The affiliation of the expert",
                        },
                        "location": {
                            "type": "string",
                            "description": "The location of the expert",
                        },
                        "summary": {
                            "type": "string",
                            "description": "Short summary, around 3 sentences of what the expert is doing and the experience. "
                                           "Translate it into English if that's not already the case. Write it ABOUT the person, in third person.",
                        },
                        "socials": {
                            "type": "object",
                            "properties": {
                                "twitter": {
                                    "type": "string",
                                    "description": "The twitter handle of the expert",
                                },
                                "linkedin": {
                                    "type": "string",
                                    "description": "The linkedin handle of the expert",
                                },
                                "github": {
                                    "type": "string",
                                    "description": "The github handle of the expert",
                                },
                                "website": {
                                    "type": "string",
                                    "description": "The website of the expert",
                                },
                                "email": {
                                    "type": "string",
                                    "description": "The email of the expert",
                                },
                            },
                            "description": "The socials of the expert, if available",
                        },
                    },
                }}
        ]

        print(html_content)

        messages = [
            {"role": "system",
             "content": "You are reading extracted HTML data from a website. "
                        "Try to find information about the expert on that page, about their name, "
                        "affiliation, location, summary and socials. If you can't find their name directly, "
                        "try to extract it from the text or email or possible links"},
            {"role": "user", "content": html_content}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto",
        )

        response_message = response["choices"][0]["message"]
        print(response_message)
        if response_message.get("function_call"):
            function_args = json.loads(response_message["function_call"]["arguments"])
            return ExpertInformation(
                name=function_args.get("name"),
                affiliation=function_args.get("affiliation"),
                location=function_args.get("location"),
                summary=function_args.get("summary"),
                socials=function_args.get("socials"),
            )
        return None

    def display_expert(self, expert_info: ExpertInformation, url: str) -> None:
        """Displays the details of the given expert."""

        print("\n" + "-" * 40)

        # Name and Affiliation
        print(f"Name: \033[1m{expert_info.name}\033[0m")  # Bold
        print(f"Affiliation: {expert_info.affiliation}")
        print(f"Location: {expert_info.location}")
        print(f"URL: {url}")

        # Summarized text with wrapping
        if expert_info.summary:  # Check if summary is not None
            wrapper = textwrap.TextWrapper(width=60)
            wrapped_summary = wrapper.fill(text=expert_info.summary)
            print(f"\nSummary:\n{wrapped_summary}\n")

        if expert_info.socials:
            socials = expert_info.socials
            if any(socials.values()):
                print("\033[4mSocials:\033[0m")  # Underlined
                for key, value in socials.items():
                    if value:
                        print(f"{key.capitalize()}: {value}")

        print("-" * 40 + "\n")

    def main(self) -> None:
        """The main interactive loop of the Assistant."""

        user_question = input("Enter your query (e.g., 'RL experts in California'): ")
        num_experts = int(input("Enter the number of experts you'd like to see: "))

        query = self.get_search_query(user_question)
        print(f"\nQuery: {query}\n")

        search_response = self.metaphor.search(query, use_autoprompt=True, num_results=num_experts)
        results = search_response.get_contents().contents

        for result in results:
            if expert_info := self.get_expert_from_html(result.extract):
                self.display_expert(expert_info, result.url)


if __name__ == "__main__":
    assistant = Assistant()
    assistant.main()