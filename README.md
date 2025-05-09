# Mock Confluence MCP Server

This is a minimal reproduction of a Confluence search tool implemented as an MCP server with mock responses, using the same definitions as: https://github.com/sooperset/mcp-atlassian

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python confluence_mcp.py
```

By default, the server runs on port 8002. You can change this by setting the `PORT` environment variable:

```bash
PORT=8003 python confluence_mcp.py
```

The server provides mock implementations of Confluence search functionality without requiring an actual Confluence instance.

## Test Basic Authentication

You can set a mock bearer token in the environment variable `MOCK_BEARER_TOKEN` to test authentication.

```bash
export MOCK_BEARER_TOKEN=your_mock_token
```

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