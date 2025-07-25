## github-mcp-server

Some notes on what is actually running.

The first version we had deployed came from here - https://github.com/opendatahub-io/llama-stack-demos/tree/main/kubernetes/mcp-servers/github-mcp

This was built from here - https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github

Which is the NodeJS version - now DEPRECTED.

The supported version is now - https://github.com/github/github-mcp-server

Unfortunately it seems this new supported version is written to be hosted by GitHub itself - read this issue when trying to self host:

-- MCP Github Server Docker Image not compatible for GKE deployment due to no persistent server mode #457
https://github.com/github/github-mcp-server/issues/457

So .. the Containerfile in this directory builds an image that can host the mcp-server using mcp-proxy OK.

This is the version i have pushed to `quay.io/eformat/github-mcp-server:latest` for now.
