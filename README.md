# CouchDB MCP Server

A Model Context Protocol (MCP) server that provides tools for interacting with CouchDB databases. This server enables Claude Code and other MCP clients to perform database operations, document management, and search queries on CouchDB instances.

## Features

### Database Operations
- **List Databases**: View all databases on the CouchDB server
- **Create Database**: Create new databases
- **Delete Database**: Remove databases

### Document Operations
- **Create Document**: Insert new documents with optional custom IDs
- **Get Document**: Retrieve documents by ID
- **Update Document**: Modify existing documents
- **Delete Document**: Remove documents
- **List Documents**: View all documents in a database with optional full content

### Search & Indexing
- **Search Documents**: Query documents using CouchDB Mango queries with pagination support
- **Create Index**: Create indexes for better query performance
- **List Indexes**: View all indexes in a database

## Requirements

- Python 3.10 or higher
- CouchDB server (local or remote)
- Claude Code CLI

## Installation

1. Clone or download this repository to your local machine.

2. Install dependencies using [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

## CouchDB Setup

Make sure you have CouchDB installed and running. You can:

1. **Install CouchDB locally**:
   - macOS: `brew install couchdb`
   - Ubuntu/Debian: `sudo apt-get install couchdb`
   - Or download from [couchdb.apache.org](https://couchdb.apache.org/)

2. **Use Docker**:
   ```bash
   docker run -d -p 5984:5984 --name couchdb \
     -e COUCHDB_USER=admin \
     -e COUCHDB_PASSWORD=password \
     couchdb:latest
   ```

3. **Access CouchDB**:
   - Default URL: `http://localhost:5984`
   - Web UI (Fauxton): `http://localhost:5984/_utils`

## Adding to Claude Code

To use this MCP server with Claude Code, you need to add it to your Claude Code configuration file.

### Configuration File Location

The Claude Code configuration file is located at:
- **macOS/Linux**: `~/.config/claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Configuration Steps

1. Open or create the configuration file:

```bash
# macOS/Linux
mkdir -p ~/.config/claude
nano ~/.config/claude/claude_desktop_config.json
```

2. Add the CouchDB MCP server to the `mcpServers` section:

**Using uv (recommended)**:
```json
{
  "mcpServers": {
    "couchdb": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/couchdb_mcp",
        "python", "couchdb_mcp_server.py"
      ],
      "env": {
        "COUCHDB_URL": "http://localhost:5984"
      }
    }
  }
}
```

**Using python directly** (requires manual dependency install):
```json
{
  "mcpServers": {
    "couchdb": {
      "command": "python",
      "args": [
        "/path/to/couchdb_mcp_server.py"
      ],
      "env": {
        "COUCHDB_URL": "http://localhost:5984"
      }
    }
  }
}
```

3. **For authenticated CouchDB instances**, include credentials in the URL:

```json
{
  "mcpServers": {
    "couchdb": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/couchdb_mcp",
        "python", "couchdb_mcp_server.py"
      ],
      "env": {
        "COUCHDB_URL": "http://admin:password@localhost:5984"
      }
    }
  }
}
```

4. **For remote CouchDB servers**:

```json
{
  "mcpServers": {
    "couchdb": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/couchdb_mcp",
        "python", "couchdb_mcp_server.py"
      ],
      "env": {
        "COUCHDB_URL": "https://username:password@your-server.com:5984"
      }
    }
  }
}
```

5. Save the configuration file and restart Claude Code.

## Usage Examples

Once configured, you can use Claude Code to interact with your CouchDB instance. Here are some example requests:

### Database Operations

```
Create a new database called "users"
```

```
List all databases
```

```
Delete the database named "test_db"
```

### Document Operations

```
Create a document in the users database with data: {"name": "John Doe", "email": "john@example.com"}
```

```
Get the document with ID "user123" from the users database
```

```
Update document user123 in users database with new email address
```

```
List all documents in the users database
```

### Search Operations

```
Search the users database for all documents where name equals "John Doe"
```

```
Search for documents in the products database where price is greater than 100
```

## Tool Reference

### couchdb_list_databases
Lists all databases on the CouchDB server.

**Parameters**: None

### couchdb_create_database
Creates a new database.

**Parameters**:
- `name` (string, required): Name of the database to create

### couchdb_delete_database
Deletes a database.

**Parameters**:
- `name` (string, required): Name of the database to delete

### couchdb_create_document
Creates a new document in a database.

**Parameters**:
- `database` (string, required): Name of the database
- `document` (object, required): Document data as JSON object
- `doc_id` (string, optional): Document ID (auto-generated if not provided)

### couchdb_get_document
Retrieves a document from a database.

**Parameters**:
- `database` (string, required): Name of the database
- `doc_id` (string, required): Document ID

### couchdb_update_document
Updates an existing document.

**Parameters**:
- `database` (string, required): Name of the database
- `doc_id` (string, required): Document ID
- `document` (object, required): Updated document data (must include `_rev`)

### couchdb_delete_document
Deletes a document from a database.

**Parameters**:
- `database` (string, required): Name of the database
- `doc_id` (string, required): Document ID
- `rev` (string, required): Document revision (`_rev`)

### couchdb_search_documents
Searches for documents using Mango queries.

**Parameters**:
- `database` (string, required): Name of the database
- `query` (object, required): Mango query selector (e.g., `{"name": "John"}`)
- `limit` (integer, optional): Maximum number of documents to return (default: 25)
- `skip` (integer, optional): Number of documents to skip (default: 0)

### couchdb_list_documents
Lists all documents in a database.

**Parameters**:
- `database` (string, required): Name of the database
- `limit` (integer, optional): Maximum number of documents to return
- `include_docs` (boolean, optional): Include full document content (default: false)

### couchdb_create_index
Creates an index to dramatically improve Mango query performance.

**Parameters**:
- `database` (string, required): Name of the database
- `fields` (array, required): Fields to index (e.g., `["type", "name"]`)
- `index_name` (string, optional): Name for the index

**Note**: While indexes are optional, they are **highly recommended**. Without indexes, CouchDB scans all documents which can be very slow on large databases.

### couchdb_list_indexes
Lists all indexes in a database.

**Parameters**:
- `database` (string, required): Name of the database

## About Indexes and Mango Queries

CouchDB's Mango query system (`couchdb_search_documents`) **does not require** indexes, but they are **strongly recommended** for performance.

According to the [CouchDB documentation](https://docs.couchdb.org/en/stable/api/database/find.html):
- Without an index, CouchDB falls back to scanning all documents (`_all_docs`)
- This works but "can be arbitrarily slow" on large databases
- Creating indexes dramatically improves query performance

**When to create indexes**:
- Your database has many documents (>1000)
- Queries are slow
- You frequently query the same fields

**When you can skip indexes**:
- Small databases (<100 documents)
- Infrequent queries
- You don't mind slower response times

**Example**:
```
1. Try searching: "Search omnibot database where type equals 'name'"
2. If it works but is slow, create an index: "Create an index on the 'type' field in omnibot database"
3. Future queries will be much faster
```

## Troubleshooting

### Connection Issues

If you see connection errors:

1. Verify CouchDB is running: `curl http://localhost:5984`
2. Check the URL in your configuration
3. Verify credentials if using authentication
4. Check firewall settings for remote connections

### Permission Errors

If you see permission errors:

1. Ensure the user has appropriate CouchDB permissions
2. Check that the database exists before performing document operations
3. Verify document revisions (`_rev`) when updating or deleting

### Search Returns No Results

If you're searching for documents but getting no results:

1. **Verify documents exist**: Use `couchdb_list_documents` with `include_docs: true` to see actual document structure
2. **Check field names match exactly**: Field names are case-sensitive (`"Type"` ≠ `"type"`)
3. **Verify field values match**: Values are also case-sensitive (`"Name"` ≠ `"name"`)
4. **Check the field exists**: Queries only match documents where the field is present
5. **Consider creating an index**: While not required, indexes ensure queries work reliably and quickly

### Tool Not Found

If Claude Code doesn't recognize the CouchDB tools:

1. Verify the configuration file path is correct
2. Ensure the `--directory` path (uv) or Python script path is absolute, not relative
3. Restart Claude Code after configuration changes
4. Check that dependencies are installed (`uv sync` or `pip install -e .`)

## Mango Query Examples

Mango queries use MongoDB-style selectors:

**Equality**:
```json
{"name": "John Doe"}
```

**Comparison**:
```json
{"age": {"$gt": 18}}
```

**Multiple conditions**:
```json
{"$and": [{"age": {"$gte": 18}}, {"status": "active"}]}
```

**Pattern matching**:
```json
{"email": {"$regex": ".*@example\\.com$"}}
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
