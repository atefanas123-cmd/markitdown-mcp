import os

from markitdown import MarkItDown
from mcp.server.fastmcp import FastMCP


# Create MCP server
mcp = FastMCP("MarkItDown")


@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """
    Convert a URL or supported data URI into Markdown.

    Args:
        uri: HTTP/HTTPS URL or supported data URI.

    Returns:
        The converted content as Markdown.
    """

    enable_plugins = (
        os.getenv("MARKITDOWN_ENABLE_PLUGINS", "false")
        .strip()
        .lower()
        in ("true", "1", "yes")
    )

    converter = MarkItDown(
        enable_plugins=enable_plugins
    )

    result = converter.convert_uri(uri)

    return result.markdown


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )
