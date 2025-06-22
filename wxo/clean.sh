#!/bin/bash

# Remove existing agents
## SoreqAgent
uv run orchestrate agents remove -n SoreqAgent -k native

# Remove existing toolkits
uv run orchestrate toolkits remove -n soreq-mcp-server