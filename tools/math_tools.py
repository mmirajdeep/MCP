import math
from loguru import logger
from fastmcp import FastMCP, Context

class MathTools:
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        logger.info("Registering basic MathTools methods...")
        self.register_tools()

    async def add(self, a: float, b: float, ctx: Context) -> float:
        """Add two numbers with client logging."""
        await ctx.debug(f"Starting addition: {a} + {b}")
        result = a + b
        await ctx.info(f"Addition complete: {a} + {b} = {result}", extra={"a": a, "b": b, "result": result})
        return result

    async def subtract(self, a: float, b: float, ctx: Context) -> float:
        """Subtract b from a with client logging."""
        await ctx.debug(f"Starting subtraction: {a} - {b}")
        result = a - b
        await ctx.info(f"Subtraction complete: {a} - {b} = {result}", extra={"a": a, "b": b, "result": result})
        return result

    async def multiply(self, a: float, b: float, ctx: Context) -> float:
        """Multiply two numbers with client logging."""
        await ctx.debug(f"Starting multiplication: {a} × {b}")
        result = a * b
        await ctx.info(f"Multiplication complete: {a} × {b} = {result}", extra={"a": a, "b": b, "result": result})
        return result

    async def divide(self, a: float, b: float, ctx: Context) -> float:
        """Divide a by b with client logging and error handling."""
        await ctx.debug(f"Starting division: {a} ÷ {b}")
        
        if b == 0:
            await ctx.error("Division by zero attempted", extra={"a": a, "b": b})
            raise ValueError("Division by zero is not allowed")
        
        result = a / b
        await ctx.info(f"Division complete: {a} ÷ {b} = {result}", extra={"a": a, "b": b, "result": result})
        return result

    async def power(self, a: float, b: float, ctx: Context) -> float:
        """Calculate a raised to the power of b with client logging."""
        await ctx.debug(f"Starting power calculation: {a} ^ {b}")
        
        try:
            result = a ** b
            await ctx.info(f"Power calculation complete: {a} ^ {b} = {result}", extra={"base": a, "exponent": b, "result": result})
            return result
        except Exception as e:
            await ctx.error(f"Power calculation failed: {str(e)}", extra={"base": a, "exponent": b})
            raise

    async def factorial(self, n: int, ctx: Context) -> int:
        """Calculate factorial of a number with client logging."""
        await ctx.debug(f"Starting factorial calculation for: {n}")
        
        if n < 0:
            await ctx.error("Factorial not defined for negative numbers", extra={"n": n})
            raise ValueError("Factorial not defined for negative numbers")
        
        if n > 20:
            await ctx.warning(f"Large factorial calculation (n={n}), this may take time", extra={"n": n})
        
        try:
            result = math.factorial(n)
            await ctx.info(f"Factorial complete: {n}! = {result}", extra={"n": n, "result": result})
            return result
        except Exception as e:
            await ctx.error(f"Factorial calculation failed: {str(e)}", extra={"n": n})
            raise

    def register_tools(self):
        """Register all math tools with the MCP server."""
        tools = [
            (self.add, "add", "Add two numbers"),
            (self.subtract, "subtract", "Subtract b from a"),
            (self.multiply, "multiply", "Multiply two numbers"),
            (self.divide, "divide", "Divide a by b"),
            (self.power, "power", "a raised to the power of b"),
            (self.factorial, "factorial", "Factorial of a number"),
        ]
        
        logger.info("="*40)
        logger.info("Starting MathTools registration")
        logger.info("="*40)
        
        for method, name, desc in tools:
            self.mcp.tool(method, name=name, description=desc)
            logger.info(f"✓ Registered tool: {name} - {desc}")
        
        logger.info("="*40)
        logger.info(f"Successfully registered {len(tools)} math tools")
        logger.info("="*40)
