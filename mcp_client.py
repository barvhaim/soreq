from dotenv import load_dotenv
import asyncio
from fastmcp import Client

load_dotenv()

# Standard MCP configuration with multiple servers
# config = {
#     "mcpServers": {
#         "telegram": {
#             "command": "uv",
#             "args": [
#                 "--directory",
#                 "<PATH>/soreq",
#                 "run",
#                 "mcp_server.py"
#             ],
#             "env": {
#             }
#         }
#     }
# }
#
#
# async def main():
#     async with Client(config) as client:
#         tools = await client.list_tools()
#         print(f"Available tools: {tools}")


async def main():
    # Connect via stdio to a local script
    async with Client("mcp_server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        tool_1 = await client.call_tool("sync_project_docs", {})
        print(f"Result: {tool_1}")

        tool_2 = await client.call_tool(
            "query_project_docs", {"query": "How to update the swagger?"}
        )
        print(f"Result: {tool_2}")


if __name__ == "__main__":
    asyncio.run(main())
