from fastmcp import FastMCP
import random

mcp = FastMCP('MCP Demo Server')

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool
def roll_dice(no_of_times_to_roll: int) -> list[int]:
    """Roll a six-sided die a specified number of times."""
    return [random.randint(1, 6) for _ in range(no_of_times_to_roll)]

if __name__ == "__main__":
    mcp.run()