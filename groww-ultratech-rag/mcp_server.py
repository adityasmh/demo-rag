import json
from urllib.request import urlopen

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    from mcp.server.fastmcp import FastMCP as MCPServer

from search import search

mcp = MCPServer("company-docs")


@mcp.tool()
def search_docs(company: str, question: str) -> str:
    """Search through the company documents. companies must only be 'groww' or 'ultratech'.
    Use this before answering any question about charges, products or policies."""
    paragraphs = json.load(urlopen(f"http://127.0.0.1:8001/documents?company={company}"))
    results = search(paragraphs, question)
    if len(results) == 0:
        return "NO_RESULTS"
    text = ""
    for score, p in results:
        text += p["heading"] + ": " + p["text"] + "\n\n"
    return text


if __name__ == "__main__":
    mcp.run("stdio")