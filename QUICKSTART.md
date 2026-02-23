# CouchDB MCP Server - Quick Start Guide

Get up and running with the CouchDB MCP server in 5 minutes!

## Step 1: Install Dependencies

Using [uv](https://docs.astral.sh/uv/) (recommended):
```bash
cd /path/to/couchdb_mcp
uv sync
```

Or using pip:
```bash
cd /path/to/couchdb_mcp
pip install -e .
```

## Step 2: Start CouchDB

### Option A: Local Installation
If you have CouchDB installed:
```bash
# macOS with Homebrew
brew services start couchdb

# Or start manually
couchdb
```

### Option B: Docker (Recommended for Testing)
```bash
docker run -d \
  --name couchdb \
  -p 5984:5984 \
  -e COUCHDB_USER=admin \
  -e COUCHDB_PASSWORD=password \
  couchdb:latest
```

## Step 3: Test Connection

```bash
# Test default connection
uv run python test_connection.py

# Test with custom URL
uv run python test_connection.py http://admin:password@localhost:5984
```

You should see:
```
✓ Connected successfully!
✓ CouchDB version: 3.x.x
✓ All tests passed! CouchDB is ready for MCP server.
```

## Step 4: Configure Claude Code

1. Create or edit the Claude Code configuration file:

**macOS/Linux**:
```bash
mkdir -p ~/.config/claude
nano ~/.config/claude/claude_desktop_config.json
```

**Windows**:
```
Create: %APPDATA%\Claude\claude_desktop_config.json
```

2. Add this configuration (adjust the path to match your setup):

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

**For Docker setup with authentication**:
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

3. Save and restart Claude Code

## Step 5: Test in Claude Code

Open Claude Code and try these commands:

```
List all databases
```

```
Create a database called "test"
```

```
Create a document in the test database with data: {"name": "Alice", "age": 30}
```

```
Search the test database for all documents
```

## Troubleshooting

### "Connection refused"
- Check if CouchDB is running: `curl http://localhost:5984`
- If using Docker: `docker ps` (should show couchdb container)

### "Authentication required"
- Update COUCHDB_URL with credentials: `http://user:pass@localhost:5984`

### "Module not found: mcp"
- Install dependencies: `uv sync` or `pip install -e .`

### "CouchDB tools not appearing in Claude Code"
- Verify the file path in configuration is absolute (not relative)
- Check configuration JSON syntax is valid
- Restart Claude Code

### Check CouchDB Web Interface
- Open in browser: `http://localhost:5984/_utils`
- Default credentials (if using Docker): admin/password

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [example_usage.md](example_usage.md) for usage examples
- Explore the [CouchDB documentation](https://docs.couchdb.org/)

## Common Operations Quick Reference

| Operation | Example Request |
|-----------|----------------|
| List databases | "Show me all databases" |
| Create database | "Create a database called 'users'" |
| Add document | "Create a document in users: {name: 'John'}" |
| Get document | "Get document 'abc123' from users" |
| Search | "Find all users where age > 18" |
| Update | "Update user 'abc123' set name to 'Jane'" |
| Delete | "Delete the document 'abc123' from users" |

## File Structure

```
couchdb_mcp/
├── couchdb_mcp_server.py   # Main MCP server
├── test_connection.py      # Connection test utility
├── pyproject.toml          # Project configuration & dependencies
├── uv.lock                 # uv lock file (auto-generated)
├── requirements.txt        # Pip dependencies (legacy)
├── README.md               # Full documentation
├── QUICKSTART.md           # This file
├── INDEXES.md              # Guide to CouchDB indexes
├── example_usage.md        # Usage examples
└── .gitignore              # Git ignore rules
```

## Support

If you encounter issues:
1. Run `uv run python test_connection.py` to verify CouchDB connectivity
2. Check the Claude Code logs
3. Verify your configuration file syntax
4. Ensure Python 3.10+ and [uv](https://docs.astral.sh/uv/) are installed

Happy coding with CouchDB and Claude!
