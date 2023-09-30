# Metaphor Expert Finder

This project is a creative solution for the Metaphor API coding challenge. 
The main idea is to facilitate the discovery of domain-specific experts based on user input. 
Not only does it generate a tailored search query, but it also extracts and presents pertinent information about each 
expert, including their website, location, and social profiles.

Because of the given time constraint and the fact that I first needed to learn how to use the API well,
I decided to make this a command-line application. However, the core idea can be extended to a
web application quite easily

## Idea

With the vast expanse of knowledge available online, finding genuine experts in specific domains can be like looking for a needle in a haystack. The Metaphor Expert Finder leverages the power of the Metaphor API, combined with OpenAI, to generate search queries that pinpoint these experts based on user questions. It then parses the website content to extract and present meaningful information about each expert.

For example, if a user queries, "RL experts in California," the tool would return relevant experts, their affiliations, locations, a brief summary of their work, and available social profiles. This application offers a streamlined and user-friendly way to identify and connect with domain experts, researchers, or professionals.

## Features

- **Dynamic Query Generation:** Understands user input and crafts a precise search query.
- **Expert Information Extraction:** Parses the website content to extract valuable information about each expert.
- **Neat Presentation:** Presents the extracted information in a clean and easily digestible format.

## Setup & Usage

### Requirements
Python 3.10 or above
A .env file with the necessary API keys for Metaphor and OpenAI.

### Running the Application
From the root directory of the project, run:
```python
python main.py
```
Follow the on-screen prompts to generate expert search results.


