# Install dependencies
!pip install nest_asyncio openai mcp

# Allow nested use of asyncio.run in notebooks
import nest_asyncio
nest_asyncio.apply()


# MCP Daily Scheduler - GitHub Trending to Slack
#%%writefile githubtrending_mcp_notifier.py

# Import standard libs
import asyncio
import json
import os

# Load config (contains OPENAI_API_KEY and SLACK_WEBHOOK_URL or token)
with open("config.json", "r") as f:
    config = json.load(f)

os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
SLACK_POST_AGENT_COMMAND = config["SLACK_POST_AGENT_COMMAND"]
PUPPETEER_COMMAND = config["PUPPETEER_COMMAND"]

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

# Define MCPClient
class MCPClient:
    def __init__(self):
        #self.session = None
        #self.exit_stack = asyncio.ExitStack()
        #self.client = OpenAI()
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = OpenAI()
        
    async def connect_to_server(self, command, args):
        server_params = StdioServerParameters(command=command, args=args)
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()
        tools = await self.session.list_tools()
        print("Connected to server with tools:", [t.name for t in tools.tools])

    async def summarize_url(self, url):
        # Step 1: connect to puppeteer
        await self.connect_to_server(command="npx", args=["-y", "@modelcontextprotocol/server-puppeteer"])
        response = await self.session.call_tool("fetch_page_text", {"url": url})
        text = response.content[0].text.strip()
        await self.exit_stack.aclose()

        # Step 2: summarize via OpenAI
        prompt = f"Please summarize this article for daily tech briefing:{text}"
        summary = self.client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()

        return summary

    async def post_to_slack(self, message):
        # Step 3: post to slack MCP
        await self.connect_to_server(command="npx", args=["-y", "@modelcontextprotocol/server-slack"])
        response = await self.session.call_tool("slack_post_message", {"message": message})
        await self.exit_stack.aclose()
        print("Posted to Slack.")

# === MAIN EXECUTION ===
async def main():
    url = input("Masukkan URL berita teknologi: ").strip()
    client = MCPClient()
    summary = await client.summarize_url(url)
    print("\nRingkasan:", summary)
    await client.post_to_slack(summary)

await main()
