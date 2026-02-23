#!/usr/bin/env python3
"""
Simple script to test CouchDB connection and verify the server is accessible.
Run this before configuring the MCP server to ensure CouchDB is working.
"""

import sys
import os

try:
    import couchdb
except ImportError:
    print("Error: couchdb package not installed")
    print("Install it with: pip install couchdb")
    sys.exit(1)


def test_connection(url="http://localhost:5984"):
    """Test connection to CouchDB server."""
    print(f"Testing connection to CouchDB at {url}...")
    print("-" * 60)

    try:
        # Connect to server
        server = couchdb.Server(url)

        # Get version
        version = server.version()
        print(f"✓ Connected successfully!")
        print(f"✓ CouchDB version: {version}")

        # List databases
        databases = list(server)
        print(f"✓ Found {len(databases)} database(s):")
        for db in databases:
            print(f"  - {db}")

        # Test creating and deleting a test database
        test_db_name = "_mcp_test_connection"
        print(f"\n✓ Testing database operations...")

        # Clean up if exists
        if test_db_name in server:
            del server[test_db_name]

        # Create test database
        db = server.create(test_db_name)
        print(f"  - Created test database '{test_db_name}'")

        # Create a test document
        doc_id, doc_rev = db.save({"type": "test", "message": "Hello from MCP!"})
        print(f"  - Created test document with ID: {doc_id}")

        # Retrieve the document
        doc = db[doc_id]
        print(f"  - Retrieved document: {doc.get('message')}")

        # Delete the document
        db.delete(doc)
        print(f"  - Deleted test document")

        # Delete test database
        del server[test_db_name]
        print(f"  - Deleted test database")

        print("\n" + "=" * 60)
        print("✓ All tests passed! CouchDB is ready for MCP server.")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n✗ Connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Is CouchDB running? Try: curl http://localhost:5984")
        print("2. Is the URL correct?")
        print("3. Do you need authentication? Use: http://user:pass@localhost:5984")
        print("4. Check firewall settings if connecting to remote server")
        return False


def main():
    """Main entry point."""
    # Get URL from command line or environment
    url = "http://localhost:5984"

    if len(sys.argv) > 1:
        url = sys.argv[1]
    elif "COUCHDB_URL" in os.environ:
        url = os.environ["COUCHDB_URL"]

    success = test_connection(url)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
