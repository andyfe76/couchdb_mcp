#!/usr/bin/env python3
"""
CouchDB MCP Server
Provides tools for interacting with CouchDB databases.
"""

import asyncio
import json
from typing import Any

import couchdb
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server


class CouchDBServer:
    """MCP Server for CouchDB operations."""

    def __init__(self, url: str = "http://localhost:5984"):
        """Initialize CouchDB connection.

        Args:
            url: CouchDB server URL (default: http://localhost:5984)
        """
        self.url = url
        self.couch: couchdb.Server | None = None
        self.app = Server("couchdb-mcp-server")
        self._setup_handlers()

    def connect(self) -> bool:
        """Establish connection to CouchDB server."""
        try:
            self.couch = couchdb.Server(self.url)
            # Test connection
            _ = self.couch.version()
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to connect to CouchDB at {self.url}: {str(e)}")

    def _get_server(self) -> couchdb.Server:
        """Return the CouchDB server, connecting if needed."""
        if self.couch is None:
            self.connect()
        assert self.couch is not None
        return self.couch

    def _setup_handlers(self):
        """Set up MCP tool handlers."""

        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            """List available CouchDB tools."""
            return [
                Tool(
                    name="couchdb_list_databases",
                    description="List all databases in the CouchDB server",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                Tool(
                    name="couchdb_create_database",
                    description="Create a new database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the database to create",
                            },
                        },
                        "required": ["name"],
                    },
                ),
                Tool(
                    name="couchdb_delete_database",
                    description="Delete a database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the database to delete",
                            },
                        },
                        "required": ["name"],
                    },
                ),
                Tool(
                    name="couchdb_create_document",
                    description="Create a new document in a database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Name of the database",
                            },
                            "document": {
                                "type": "object",
                                "description": "Document data as JSON object",
                            },
                            "doc_id": {
                                "type": "string",
                                "description": "Optional document ID (if not provided, CouchDB generates one)",
                            },
                        },
                        "required": ["database", "document"],
                    },
                ),
                Tool(
                    name="couchdb_get_document",
                    description="Retrieve a document from a database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Name of the database",
                            },
                            "doc_id": {
                                "type": "string",
                                "description": "Document ID",
                            },
                        },
                        "required": ["database", "doc_id"],
                    },
                ),
                Tool(
                    name="couchdb_update_document",
                    description="Update an existing document in a database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Name of the database",
                            },
                            "doc_id": {
                                "type": "string",
                                "description": "Document ID",
                            },
                            "document": {
                                "type": "object",
                                "description": "Updated document data (must include _rev)",
                            },
                        },
                        "required": ["database", "doc_id", "document"],
                    },
                ),
                Tool(
                    name="couchdb_delete_document",
                    description="Delete a document from a database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Name of the database",
                            },
                            "doc_id": {
                                "type": "string",
                                "description": "Document ID",
                            },
                            "rev": {
                                "type": "string",
                                "description": "Document revision (_rev)",
                            },
                        },
                        "required": ["database", "doc_id", "rev"],
                    },
                ),
                Tool(
                    name="couchdb_search_documents",
                    description="Search for documents in a database using a Mango query. Works without indexes but creating indexes (via couchdb_create_index) improves performance significantly.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Name of the database",
                            },
                            "query": {
                                "type": "object",
                                "description": "Mango query selector (e.g., {'name': 'John'} for exact match, {'age': {'$gt': 18}} for comparisons)",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of documents to return (default: 25)",
                            },
                            "skip": {
                                "type": "integer",
                                "description": "Number of documents to skip (default: 0)",
                            },
                        },
                        "required": ["database", "query"],
                    },
                ),
                Tool(
                    name="couchdb_list_documents",
                    description="List all documents in a database with their IDs and revisions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Name of the database",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of documents to return",
                            },
                            "include_docs": {
                                "type": "boolean",
                                "description": "Include full document content (default: false)",
                            },
                        },
                        "required": ["database"],
                    },
                ),
                Tool(
                    name="couchdb_create_index",
                    description="Create an index to improve Mango query performance. While optional, indexes dramatically speed up queries and ensure reliable results.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Name of the database",
                            },
                            "fields": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Fields to index (e.g., ['type', 'name'])",
                            },
                            "index_name": {
                                "type": "string",
                                "description": "Optional name for the index",
                            },
                        },
                        "required": ["database", "fields"],
                    },
                ),
                Tool(
                    name="couchdb_list_indexes",
                    description="List all indexes in a database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Name of the database",
                            },
                        },
                        "required": ["database"],
                    },
                ),
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls."""
            try:
                if name == "couchdb_list_databases":
                    return await self._list_databases()
                elif name == "couchdb_create_database":
                    return await self._create_database(arguments["name"])
                elif name == "couchdb_delete_database":
                    return await self._delete_database(arguments["name"])
                elif name == "couchdb_create_document":
                    return await self._create_document(
                        arguments["database"],
                        arguments["document"],
                        arguments.get("doc_id")
                    )
                elif name == "couchdb_get_document":
                    return await self._get_document(
                        arguments["database"],
                        arguments["doc_id"]
                    )
                elif name == "couchdb_update_document":
                    return await self._update_document(
                        arguments["database"],
                        arguments["doc_id"],
                        arguments["document"]
                    )
                elif name == "couchdb_delete_document":
                    return await self._delete_document(
                        arguments["database"],
                        arguments["doc_id"],
                        arguments["rev"]
                    )
                elif name == "couchdb_search_documents":
                    return await self._search_documents(
                        arguments["database"],
                        arguments["query"],
                        arguments.get("limit", 25),
                        arguments.get("skip", 0)
                    )
                elif name == "couchdb_list_documents":
                    return await self._list_documents(
                        arguments["database"],
                        arguments.get("limit"),
                        arguments.get("include_docs", False)
                    )
                elif name == "couchdb_create_index":
                    return await self._create_index(
                        arguments["database"],
                        arguments["fields"],
                        arguments.get("index_name")
                    )
                elif name == "couchdb_list_indexes":
                    return await self._list_indexes(arguments["database"])
                else:
                    raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def _list_databases(self) -> list[TextContent]:
        """List all databases."""
        databases = list(self._get_server())
        result = {
            "databases": databases,
            "count": len(databases)
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    async def _create_database(self, name: str) -> list[TextContent]:
        """Create a new database."""
        try:
            self._get_server().create(name)
            return [TextContent(type="text", text=f"Database '{name}' created successfully")]
        except couchdb.http.PreconditionFailed:
            return [TextContent(type="text", text=f"Database '{name}' already exists")]

    async def _delete_database(self, name: str) -> list[TextContent]:
        """Delete a database."""
        try:
            self._get_server().delete(name)
            return [TextContent(type="text", text=f"Database '{name}' deleted successfully")]
        except couchdb.http.ResourceNotFound:
            return [TextContent(type="text", text=f"Database '{name}' not found")]

    async def _create_document(self, database: str, document: dict, doc_id: str | None = None) -> list[TextContent]:
        """Create a new document."""
        try:
            db = self._get_server()[database]
            if doc_id:
                doc_id, rev = db.save({"_id": doc_id, **document})
            else:
                doc_id, rev = db.save(document)

            result = {
                "id": doc_id,
                "rev": rev,
                "message": "Document created successfully"
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except KeyError:
            return [TextContent(type="text", text=f"Database '{database}' not found")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error creating document: {str(e)}")]

    async def _get_document(self, database: str, doc_id: str) -> list[TextContent]:
        """Retrieve a document."""
        try:
            db = self._get_server()[database]
            doc = db[doc_id]
            return [TextContent(type="text", text=json.dumps(doc, indent=2))]
        except KeyError:
            return [TextContent(type="text", text=f"Database '{database}' or document '{doc_id}' not found")]
        except couchdb.http.ResourceNotFound:
            return [TextContent(type="text", text=f"Document '{doc_id}' not found")]

    async def _update_document(self, database: str, doc_id: str, document: dict) -> list[TextContent]:
        """Update an existing document."""
        try:
            db = self._get_server()[database]

            # Ensure document has _id
            if "_id" not in document:
                document["_id"] = doc_id

            # Save the document
            saved_id, rev = db.save(document)

            result = {
                "id": saved_id,
                "rev": rev,
                "message": "Document updated successfully"
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except KeyError:
            return [TextContent(type="text", text=f"Database '{database}' not found")]
        except couchdb.http.ResourceConflict:
            return [TextContent(type="text", text="Document update conflict - document was modified, please get the latest revision")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error updating document: {str(e)}")]

    async def _delete_document(self, database: str, doc_id: str, rev: str) -> list[TextContent]:
        """Delete a document."""
        try:
            db = self._get_server()[database]
            db.delete({"_id": doc_id, "_rev": rev})
            return [TextContent(type="text", text=f"Document '{doc_id}' deleted successfully")]
        except KeyError:
            return [TextContent(type="text", text=f"Database '{database}' not found")]
        except couchdb.http.ResourceNotFound:
            return [TextContent(type="text", text=f"Document '{doc_id}' not found")]
        except couchdb.http.ResourceConflict:
            return [TextContent(type="text", text="Document delete conflict - revision mismatch")]

    async def _search_documents(self, database: str, query: dict, limit: int, skip: int) -> list[TextContent]:
        """Search documents using Mango query."""
        try:
            db = self._get_server()[database]

            # Build Mango query using the find() method
            mango_query = {
                "selector": query,
                "limit": limit,
                "skip": skip
            }

            # Use the db.find() method (available in CouchDB >= 2.0)
            docs = list(db.find(mango_query))

            response = {
                "docs": docs,
                "count": len(docs)
            }

            # If no results, provide helpful suggestion
            if len(docs) == 0:
                response["note"] = "No documents matched the query. To verify documents exist, use couchdb_list_documents with include_docs=true"

            return [TextContent(type="text", text=json.dumps(response, indent=2))]
        except KeyError:
            return [TextContent(type="text", text=f"Database '{database}' not found")]
        except AttributeError:
            # Fallback to REST API if find() method not available
            return await self._search_documents_fallback(database, query, limit, skip)
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching documents: {str(e)}")]

    async def _search_documents_fallback(self, database: str, query: dict, limit: int, skip: int) -> list[TextContent]:
        """Fallback search using raw REST API."""
        try:
            db = self._get_server()[database]

            mango_query = {
                "selector": query,
                "limit": limit,
                "skip": skip
            }

            # Make a request to the _find endpoint
            result = db.resource.post_json('_find', body=mango_query)

            docs = result[1].get("docs", [])
            warning = result[1].get("warning", None)

            response = {
                "docs": docs,
                "count": len(docs)
            }

            if warning:
                response["warning"] = warning

            if len(docs) == 0:
                response["note"] = "No documents matched the query. To verify documents exist, use couchdb_list_documents with include_docs=true"

            return [TextContent(type="text", text=json.dumps(response, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error in fallback search: {str(e)}")]

    async def _list_documents(self, database: str, limit: int | None = None, include_docs: bool = False) -> list[TextContent]:
        """List all documents in a database."""
        try:
            db = self._get_server()[database]

            # Build view query parameters
            params: dict[str, Any] = {"include_docs": include_docs}
            if limit is not None:
                params["limit"] = limit

            # Get all documents
            all_docs = db.view('_all_docs', **params)

            docs = []
            for row in all_docs:
                if include_docs:
                    docs.append(row.doc)
                else:
                    docs.append({
                        "id": row.id,
                        "key": row.key,
                        "value": row.value
                    })

            result = {
                "documents": docs,
                "count": len(docs)
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except KeyError:
            return [TextContent(type="text", text=f"Database '{database}' not found")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing documents: {str(e)}")]

    async def _create_index(self, database: str, fields: list, index_name: str | None = None) -> list[TextContent]:
        """Create an index for Mango queries."""
        try:
            db = self._get_server()[database]

            # Build index specification
            index_spec = {
                "index": {
                    "fields": fields
                },
                "type": "json"
            }

            if index_name:
                index_spec["name"] = index_name

            # Create the index
            result = db.resource.post_json('_index', body=index_spec)

            response = {
                "result": result[1].get("result"),
                "id": result[1].get("id"),
                "name": result[1].get("name"),
                "message": f"Index created successfully on fields: {fields}"
            }

            return [TextContent(type="text", text=json.dumps(response, indent=2))]
        except KeyError:
            return [TextContent(type="text", text=f"Database '{database}' not found")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error creating index: {str(e)}")]

    async def _list_indexes(self, database: str) -> list[TextContent]:
        """List all indexes in a database."""
        try:
            db = self._get_server()[database]

            # Get all indexes
            result = db.resource.get_json('_index')

            indexes = result[1].get("indexes", [])

            response = {
                "indexes": indexes,
                "count": len(indexes),
                "total_rows": result[1].get("total_rows")
            }

            return [TextContent(type="text", text=json.dumps(response, indent=2))]
        except KeyError:
            return [TextContent(type="text", text=f"Database '{database}' not found")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing indexes: {str(e)}")]

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )


async def main():
    """Main entry point."""
    import sys

    # Get CouchDB URL from environment or use default
    import os
    couchdb_url = os.getenv("COUCHDB_URL", "http://localhost:5984")

    # Check for URL argument
    if len(sys.argv) > 1:
        couchdb_url = sys.argv[1]

    server = CouchDBServer(url=couchdb_url)

    try:
        server.connect()
    except ConnectionError as e:
        print(f"Warning: {e}", file=sys.stderr)
        print("Server will attempt to connect when first tool is called", file=sys.stderr)

    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
