import contextlib
import os
import sys
from collections.abc import AsyncIterator

from mcp.server.fastmcp import FastMCP
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send

from markitdown import MarkItDown
import uvicorn


# Create MCP server
mcp = FastMCP("markitdown")


@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """
    Convert a resource described by an http:, https:, file:
    or data: URI to Markdown.
    """
    return MarkItDown(
        enable_plugins=check_plugins_enabled()
    ).convert_uri(uri).markdown


def check_plugins_enabled() -> bool:
    return os.getenv(
        "MARKITDOWN_ENABLE_PLUGINS", "false"
    ).strip().lower() in (
        "true",
        "1",
        "yes",
    )


def create_starlette_app(
    mcp_server: Server,
    *,
    debug: bool = False
) -> Starlette:

    session_manager = StreamableHTTPSessionManager(
        app=mcp_server,
        event_store=None,
        json_response=True,
        stateless=True,
    )

    async def handle_streamable_http(
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:
        await session_manager.handle_request(
            scope,
            receive,
            send
        )

    @contextlib.asynccontextmanager
    async def lifespan(
        app: Starlette
    ) -> AsyncIterator[None]:

        async with session_manager.run():
            print(
                "Application started with "
                "StreamableHTTP session manager!"
            )

            try:
                yield
            finally:
                print(
                    "Application shutting down..."
                )

    return Starlette(
        debug=debug,
        routes=[
            Mount(
                "/mcp",
                app=handle_streamable_http
            ),
        ],
        lifespan=lifespan,
    )


def main():

    mcp_server = mcp._mcp_server

    host = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    port = int(
        os.getenv(
            "PORT",
            "10000"
        )
    )

    starlette_app = create_starlette_app(
        mcp_server,
        debug=True
    )

    uvicorn.run(
        starlette_app,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    main()
