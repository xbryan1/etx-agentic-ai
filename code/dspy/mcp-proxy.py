from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient
import os

TAVILY_API_KEY=
URL=

# Bridge remote SSE server to local stdio
#remote_proxy = FastMCP.as_proxy(
#    ProxyClient("http://localhost:8321/v1"), # http://example.com/mcp/sse
#    name="Remote-to-Local Bridge"
#)

config = {
    "mcpServers": {
        "mcp::openshift": {
            "url": "http://localhost:8000/sse",
            "transport": "sse"
        },
        "mcp::github": {
            "url": "http://localhost:8080/sse",
            "transport": "sse"
        },
        # "websearch": {
        #     "url": URL,
        #     "transport": "http"
        # }
    }
}

# Create a unified proxy to multiple servers
composite_proxy = FastMCP.as_proxy(config, name="Composite Proxy")

# Run locally via stdio for Claude Desktop
if __name__ == "__main__":
    composite_proxy.run()  # Defaults to stdio transport