Overview

This code defines a system for fetching a tech news article from a given URL, summarizing it using OpenAI's GPT-4 model, and then posting the summary to Slack. It leverages the Model Context Protocol (MCP) for interacting with external tools like a web browser (Puppeteer) and Slack.

Code Explanation
1. Imports and Setup
- Import standard libs

import asyncio
import json
import os

- Load config (contains OPENAI_API_KEY and SLACK_WEBHOOK_URL or token)

with open("config.json", "r") as f:
    config = json.load(f)

os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
SLACK_POST_AGENT_COMMAND = config["SLACK_POST_AGENT_COMMAND"]
PUPPETEER_COMMAND = config["PUPPETEER_COMMAND"]

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
Use code with caution
import asyncio, json, os: Imports necessary libraries for asynchronous operations, handling JSON data, and interacting with the operating system.
with open("config.json", "r") as f:: Loads configuration data from a file named config.json. This file likely contains sensitive information like API keys.
os.environ["OPENAI_API_KEY"] = ...: Sets environment variables with values from the configuration file. These are used to authenticate with OpenAI and Slack.
from mcp import ...: Imports components from the MCP library for managing communication with external tools.
from openai import OpenAI: Imports the OpenAI library for using the GPT-4 language model.
2. MCPClient Class
class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = OpenAI()
        
    async def connect_to_server(self, command, args):
       # ... (details explained below)

    async def summarize_url(self, url):
       # ... (details explained below)

    async def post_to_slack(self, message):
       # ... (details explained below)
Use code with caution
This class encapsulates the logic for interacting with MCP and OpenAI:

__init__: Initializes the MCPClient with an OpenAI client and an asynchronous exit stack for managing resources.
connect_to_server: Establishes a connection to an MCP server, which acts as an intermediary for using external tools. It takes a command and args to specify the tool to connect to (e.g., Puppeteer or Slack).
summarize_url: This method fetches the content of a webpage, summarizes it using OpenAI's GPT-4, and returns the summary.
post_to_slack: This method posts a message to a Slack channel using MCP.
3. Main Execution
async def main():
    url = input("Masukkan URL berita teknologi: ").strip()
    client = MCPClient()
    summary = await client.summarize_url(url)
    print("\nRingkasan:", summary)
    await client.post_to_slack(summary)

await main()
Use code with caution
main: This asynchronous function is the entry point of the program.
It prompts the user for a URL of a tech news article.
It creates an instance of MCPClient.
It calls summarize_url to get the article summary.
It prints the summary to the console.
It calls post_to_slack to send the summary to Slack.
await main(): Executes the main function asynchronously.
In essence, this code automates the process of getting a tech news summary and sharing it on Slack, using powerful tools like OpenAI and MCP to handle the underlying tasks. I hope this explanation is helpful! Let me know if you have any other questions.
