"""Confluence FastMCP server instance with mock search tool."""

import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP instance
mcp = FastMCP("confluence")

# Mock data for responses
MOCK_PAGES = [
    {
        "id": "123456789",
        "title": "Project Documentation",
        "space": {"key": "DEV", "name": "Development"},
        "url": "https://example.atlassian.net/wiki/spaces/DEV/pages/123456789/Project+Documentation",
        "content": "# Project Documentation\n\nThis is the main documentation for our project.\n\n## Overview\n\nThe project aims to solve X problem by implementing Y solution.",
        "created": "2023-01-15T10:30:45.000Z",
        "creator": {"name": "John Doe", "email": "john.doe@example.com"},
        "lastModified": "2023-04-20T14:22:33.000Z",
        "lastModifier": {"name": "Jane Smith", "email": "jane.smith@example.com"},
        "version": 5,
        "labels": ["documentation", "project", "overview"]
    },
    {
        "id": "987654321",
        "title": "API Reference",
        "space": {"key": "DEV", "name": "Development"},
        "url": "https://example.atlassian.net/wiki/spaces/DEV/pages/987654321/API+Reference",
        "content": "# API Reference\n\n## Endpoints\n\n### GET /api/v1/users\n\nReturns a list of all users.\n\n### POST /api/v1/users\n\nCreates a new user.",
        "created": "2023-02-10T09:15:30.000Z",
        "creator": {"name": "Jane Smith", "email": "jane.smith@example.com"},
        "lastModified": "2023-04-18T11:45:22.000Z",
        "lastModifier": {"name": "Jane Smith", "email": "jane.smith@example.com"},
        "version": 3,
        "labels": ["api", "reference", "documentation"]
    },
    {
        "id": "456789123",
        "title": "Meeting Notes - Q1 Review",
        "space": {"key": "TEAM", "name": "Team Space"},
        "url": "https://example.atlassian.net/wiki/spaces/TEAM/pages/456789123/Meeting+Notes+-+Q1+Review",
        "content": "# Q1 Review Meeting\n\n**Date**: 2023-03-31\n**Attendees**: John, Jane, Bob, Alice\n\n## Agenda\n\n1. Q1 Results\n2. Q2 Planning\n3. Open Issues",
        "created": "2023-03-31T15:00:00.000Z",
        "creator": {"name": "Bob Johnson", "email": "bob.johnson@example.com"},
        "lastModified": "2023-03-31T17:30:45.000Z",
        "lastModifier": {"name": "Bob Johnson", "email": "bob.johnson@example.com"},
        "version": 1,
        "labels": ["meeting", "review", "q1"]
    },
    {
        "id": "135792468",
        "title": "Product Roadmap",
        "space": {"key": "PROD", "name": "Product"},
        "url": "https://example.atlassian.net/wiki/spaces/PROD/pages/135792468/Product+Roadmap",
        "content": "# Product Roadmap\n\n## Q2 2023\n\n- Feature A implementation\n- Bug fixes for module B\n\n## Q3 2023\n\n- New UI design\n- Performance improvements",
        "created": "2023-01-05T11:20:15.000Z",
        "creator": {"name": "Alice Williams", "email": "alice.williams@example.com"},
        "lastModified": "2023-04-10T09:45:30.000Z",
        "lastModifier": {"name": "John Doe", "email": "john.doe@example.com"},
        "version": 8,
        "labels": ["roadmap", "planning", "product"]
    },
    {
        "id": "246813579",
        "title": "Development Guidelines",
        "space": {"key": "DEV", "name": "Development"},
        "url": "https://example.atlassian.net/wiki/spaces/DEV/pages/246813579/Development+Guidelines",
        "content": "# Development Guidelines\n\n## Coding Standards\n\n- Use PEP 8 for Python code\n- Use ESLint for JavaScript code\n\n## Git Workflow\n\n1. Create feature branch\n2. Implement changes\n3. Submit PR for review",
        "created": "2023-02-20T13:40:25.000Z",
        "creator": {"name": "John Doe", "email": "john.doe@example.com"},
        "lastModified": "2023-04-15T10:35:20.000Z",
        "lastModifier": {"name": "Bob Johnson", "email": "bob.johnson@example.com"},
        "version": 4,
        "labels": ["guidelines", "development", "standards"]
    }
]

def search_pages(query: str, limit: int = 10, spaces_filter: Optional[str] = None) -> List[Dict]:
    """Mock search function."""
    # Parse spaces filter
    space_keys = []
    if spaces_filter:
        space_keys = [s.strip() for s in spaces_filter.split(",")]
    
    # Simple search implementation
    results = []
    query_lower = query.lower()
    
    # Check if it's a CQL query or simple text
    is_cql = any(x in query for x in ["=", "~", ">", "<", " AND ", " OR ", "currentUser()"])
    
    # For demo purposes, we'll just do a simple text search regardless of query type
    for page in MOCK_PAGES:
        # Simple text matching in title and content
        if (query_lower in page["title"].lower() or 
            query_lower in page["content"].lower() or
            any(query_lower in label.lower() for label in page["labels"])):
            
            # Apply space filter if provided
            if not space_keys or page["space"]["key"] in space_keys:
                # Create a simplified dict for the response
                simplified_page = {
                    "id": page["id"],
                    "title": page["title"],
                    "space": page["space"],
                    "url": page["url"],
                    "excerpt": page["content"][:150] + "..." if len(page["content"]) > 150 else page["content"],
                    "created": page["created"],
                    "creator": page["creator"],
                    "lastModified": page["lastModified"],
                    "lastModifier": page["lastModifier"],
                    "version": page["version"],
                    "labels": page["labels"]
                }
                results.append(simplified_page)
                
                # Respect the limit
                if len(results) >= limit:
                    break
    
    return results

@mcp.tool()
async def search(query: str, limit: int = 10, spaces_filter: Optional[str] = None) -> str:
    """Search Confluence content using simple terms or CQL.

    Args:
        query: Search query - can be simple text or a CQL query string.
        limit: Maximum number of results (1-50).
        spaces_filter: Comma-separated list of space keys to filter by.

    Returns:
        JSON string representing a list of simplified Confluence page objects.
    """
    logger.info(f"Searching Confluence with query: {query}, limit: {limit}, spaces_filter: {spaces_filter}")
    
    # Check if the query is a simple search term or already a CQL query
    if query and not any(
        x in query for x in ["=", "~", ">", "<", " AND ", " OR ", "currentUser()"]
    ):
        original_query = query
        try:
            query = f'siteSearch ~ "{original_query}"'
            logger.info(
                f"Converting simple search term to CQL using siteSearch: {query}"
            )
            pages = search_pages(original_query, limit=limit, spaces_filter=spaces_filter)
        except Exception as e:
            logger.warning(f"siteSearch failed ('{e}'), falling back to text search.")
            query = f'text ~ "{original_query}"'
            logger.info(f"Falling back to text search with CQL: {query}")
            pages = search_pages(original_query, limit=limit, spaces_filter=spaces_filter)
    else:
        # For mock purposes, we'll just use the same search function regardless of query type
        pages = search_pages(query, limit=limit, spaces_filter=spaces_filter)

    return json.dumps(pages, indent=2, ensure_ascii=False)

@mcp.tool()
async def get_page(page_id: str) -> str:
    """Get content of a specific Confluence page by ID.

    Args:
        page_id: Confluence page ID.

    Returns:
        JSON string representing the page content and metadata.
    """
    logger.info(f"Getting page content for page ID: {page_id}")
    
    # Find the page in our mock data
    page = None
    for p in MOCK_PAGES:
        if p["id"] == page_id:
            page = p
            break
    
    if not page:
        return json.dumps({"error": f"Page with ID {page_id} not found"}, indent=2, ensure_ascii=False)
    
    # Create a response with metadata and content
    result = {
        "metadata": {
            "id": page["id"],
            "title": page["title"],
            "space": page["space"],
            "url": page["url"],
            "created": page["created"],
            "creator": page["creator"],
            "lastModified": page["lastModified"],
            "lastModifier": page["lastModifier"],
            "version": page["version"],
            "labels": page["labels"]
        },
        "content": page["content"]
    }
    
    return json.dumps(result, indent=2, ensure_ascii=False)

# SSE server setup
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.requests import Request
import uvicorn

# Create SSE transport
sse = SseServerTransport("/messages")

# Define handler function
async def handle_sse(request: Request):
    """Handle SSE connections."""
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp._mcp_server.run(
            streams[0], 
            streams[1], 
            mcp._mcp_server.create_initialization_options()
        )

# Create Starlette app with routes
starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages", app=sse.handle_post_message),
    ]
)

# Entry point for running the server
if __name__ == "__main__":
    import os
    
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8002))
    
    # Run the server
    print(f"Starting Confluence MCP server with SSE transport on port {port}")
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)
