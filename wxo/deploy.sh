#!/bin/bash
# THIS SCRIPT USES SOREQ MCP SERVER

echo "Deploying Soreq MCP server and agents..."

# Get local IP address dynamically
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ipconfig getifaddr en0)
    if [ -z "$LOCAL_IP" ]; then
        # Try alternative interface if en0 is not available
        LOCAL_IP=$(ipconfig getifaddr en1)
    fi
else
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}')
fi

if [ -z "$LOCAL_IP" ]; then
    echo "Error: Could not determine local IP address"
    exit 1
fi

echo "Using local IP: $LOCAL_IP"

# Import toolkits
## Soreq MCP
uv run orchestrate toolkits import \
    --kind mcp \
    --name "soreq-mcp-server" \
    --description "My Soreq MCP server" \
    --package-root . \
    --command "uvx mcp-proxy --headers x-api-key dummy http://$LOCAL_IP:5555/sse" \
    --tools "*"

# Import agents
## SoreqAgent
uv run orchestrate agents import -f "wxo/agent.yaml"