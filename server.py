import asyncio
from fastmcp import FastMCP
from tools.db_tools import DBTools
from tools.math_tools import MathTools
from tools.retrival_tools import RetrievalTools

mcp = FastMCP(name="myserver", version="1.0.0")

# Instantiate class and register its tools
MathTools(mcp)
RetrievalTools(mcp)
DBTools(mcp)


if __name__ == "__main__":
    asyncio.run(mcp.run_async(transport="http", host="0.0.0.0", port=8080))
