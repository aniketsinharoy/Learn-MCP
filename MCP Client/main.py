import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
load_dotenv()

SERVERS = {
    "mcp-demo": {
      "transport": "stdio",
      "command": "C:\\Users\\Aniket\\.local\\bin\\uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "d:\\Code\\Python\\MCP Demo\\main.py"
      ]
    },
    "simple-calculator": {
      "transport": "streamable_http",                           #if it fails, try sse. Remove this remote mcp server
      "url": "https://defeated-azure-roundworm.fastmcp.app/mcp" #as its not a public server so you will get auth error
    }
}
async def main():
    client = MultiServerMCPClient(SERVERS)
    available_tools = await client.get_tools()

    tool_mapping_by_name = {}
    for tool in available_tools:
        tool_mapping_by_name[tool.name] = tool

    model = ChatCohere(model='command-a-03-2025')
    model_with_tools = model.bind_tools(available_tools)

    input_text = input("Human: ")
    query = HumanMessage(content=input_text)

    messages_history = []
    messages_history.append(query)
    
    response = await model_with_tools.ainvoke(messages_history)

    while True:
        if not getattr(response, 'tool_calls', None):
            print("AI:", response.content)
            print(messages_history)
            return

        messages_history.append(response)

        for tool_call in response.tool_calls:
            selected_tool_name = tool_call['name']
            selected_tool_id = tool_call['id']
            tool_args = tool_call.get('args', {})

            tool_result = await tool_mapping_by_name[selected_tool_name].ainvoke(tool_args)
            tool_message = ToolMessage(content=tool_result, tool_call_id=selected_tool_id)
            messages_history.append(tool_message)

        response = await model_with_tools.ainvoke(messages_history)


if __name__ == "__main__":
    asyncio.run(main())
