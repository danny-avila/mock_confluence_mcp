# Mock Confluence MCP Server

This is a minimal reproduction of a Confluence search tool implemented as an MCP server with mock responses, using the same definitions as: https://github.com/sooperset/mcp-atlassian

## Installation

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
# Basic run
python confluence_mcp.py

# Run with environment variables
source venv/bin/activate
DEBUG=true MOCK_BEARER_TOKEN=test PORT=8002 python confluence_mcp.py
```

By default, the server runs on port 8002. You can change this by setting the `PORT` environment variable.

The server provides mock implementations of Confluence search functionality without requiring an actual Confluence instance.

## Test Basic Authentication

You can set a mock bearer token in the environment variable `MOCK_BEARER_TOKEN` to test authentication.

```bash
export MOCK_BEARER_TOKEN=your_mock_token
```

## VSCode Debugging Setup

This project includes VSCode configuration files for easy debugging:

1. **Launch Configuration**: Press F5 or use the Run and Debug panel to start the server with debugging enabled.
2. **Tasks**: Use the Command Palette (Ctrl+Shift+P) and select "Tasks: Run Task" to:
   - Run the Confluence MCP Server
   - Test SSE Connection

### How to Debug

1. Open the project in VSCode
2. Set breakpoints in the code by clicking in the gutter next to line numbers
3. Press F5 to start debugging
4. When a breakpoint is hit, you can:
   - Step through code (F10)
   - Step into functions (F11)
   - Continue execution (F5)
   - View variables in the Debug panel

You can also add `debug_breakpoint()` anywhere in the code to trigger a manual breakpoint.

### Test with LibreChat

`librechat.yaml`
```yaml
mcpServers:
  confluence:
    type: sse
    url: http://localhost:8002/sse # or use the port you set
    timeout: 300000  # 5 minutes timeout for long operations
    # If you want to test with a bearer token:
    headers:
      Authorization: Bearer ${MOCK_BEARER_TOKEN}
```
