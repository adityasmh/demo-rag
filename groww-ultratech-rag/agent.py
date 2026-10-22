import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = os.path.dirname(os.path.abspath(__file__))

AGENTS = {
    "groww": {"name": "Groww Bot"},
    "ultratech": {"name": "UltraTech Bot"},
}


def get_text(result):
    return "\n".join(block.text for block in result.content if hasattr(block, "text"))


async def ask(company, session, question):
    result = await session.call_tool("search_docs", {"company": company, "question": question})
    text = get_text(result)
    if text == "NO_RESULTS":
        return "I could not find this in the documents."
    return text.split("\n\n")[0]


async def run(company, question):
    agent = AGENTS[company]
    server = StdioServerParameters(command=sys.executable, args=[os.path.join(HERE, "mcp_server.py")])
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            print(agent["name"], "| tools:", [t.name for t in tools])
            return await ask(company, session, question)


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in AGENTS:
        print('Usage: python agent.py groww|ultratech "your question"')
        sys.exit(1)
    print("\nANSWER:", asyncio.run(run(sys.argv[1], " ".join(sys.argv[2:]))))
