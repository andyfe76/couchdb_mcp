# Understanding CouchDB Indexes for Mango Queries

## The Problem

You might see this situation:
```
User: "Search omnibot database where type equals 'name'"
Result: { "docs": [], "count": 0 }
```

Even though you know documents with `"type": "name"` exist in your database!

## Why This Might Happen

According to the [CouchDB documentation](https://docs.couchdb.org/en/stable/api/database/find.html), CouchDB's Mango queries **do not require** indexes, but without them:

1. **Slow Performance**: CouchDB falls back to scanning all documents, which "can be arbitrarily slow"
2. **Unreliable Results**: Some query operators work better with indexes
3. **Resource Intensive**: Full database scans use more memory and CPU

Common causes for empty results:
- Field name doesn't match exactly (case-sensitive)
- Field value doesn't match (case-sensitive)
- Field doesn't exist in the documents
- Documents actually don't match the query

## The Solution: Create Indexes for Better Performance

While not required, creating indexes ensures reliable and fast query results.

### Step 1: Create an Index

Tell Claude Code to create an index:

```
Create an index in the omnibot database for the field "type"
```

Or for multiple fields:

```
Create an index in the omnibot database for fields: type and name
```

This executes once and creates a persistent index that CouchDB will use for all future queries on those fields.

### Step 2: Search Again

Now your search will work:

```
Search omnibot database where type equals "name"
```

Result:
```json
{
  "docs": [
    {"_id": "...", "_rev": "...", "type": "name", "value": "..."},
    {"_id": "...", "_rev": "...", "type": "name", "value": "..."}
  ],
  "count": 2
}
```

## Common Scenarios

### Scenario 1: Simple Field Search

**Goal**: Find all documents where `status = "active"`

**Steps**:
1. `Create an index in mydb for field "status"`
2. `Search mydb where status equals "active"`

### Scenario 2: Multiple Field Search

**Goal**: Find documents where `type = "user"` AND `role = "admin"`

**Steps**:
1. `Create an index in mydb for fields: type and role`
2. `Search mydb where type equals "user" and role equals "admin"`

### Scenario 3: Range Queries

**Goal**: Find products where `price > 100`

**Steps**:
1. `Create an index in products for field "price"`
2. `Search products where price is greater than 100`

## Checking Existing Indexes

Before creating an index, you can check what indexes already exist:

```
List all indexes in the omnibot database
```

This shows:
- Built-in indexes (like `_all_docs`)
- Custom indexes you've created
- Which fields each index covers

## Index Best Practices

1. **Create indexes for frequently queried fields**
   - If you often search by `type`, create an index on `type`
   - If you search by `type` AND `status`, create a compound index: `["type", "status"]`

2. **Index order matters for compound indexes**
   - Index `["type", "status"]` works well for:
     - Queries on just `type`
     - Queries on `type` AND `status`
   - But NOT for queries on just `status`

3. **Don't over-index**
   - Indexes use disk space and slow down writes
   - Only create indexes for fields you actually query

4. **One-time operation**
   - You only need to create an index once
   - CouchDB maintains it automatically as documents change

## Technical Details

### What Happens Under the Hood

When you create an index:
```json
{
  "index": {
    "fields": ["type"]
  },
  "type": "json"
}
```

CouchDB builds a B-tree index mapping field values to document IDs. When you search with a Mango query, CouchDB uses this index to quickly find matching documents.

### Without an Index

If you query a field without an index:
- CouchDB *may* return a warning
- Results might be empty or incomplete
- Performance is poor (especially on large databases)

### With an Index

If you query a field with an index:
- CouchDB uses the index for fast lookups
- All matching documents are returned
- Performance is excellent even with millions of documents

## Practical Example

Let's say you have a `users` database with documents like:

```json
{
  "_id": "user1",
  "type": "user",
  "role": "admin",
  "name": "Alice",
  "email": "alice@example.com"
}
```

### Workflow

1. **Check existing indexes**:
   ```
   List indexes in the users database
   ```

2. **Create needed indexes**:
   ```
   Create an index in users for fields: type, role
   ```

3. **Now you can search efficiently**:
   - `Search users where type equals "user"`
   - `Search users where role equals "admin"`
   - `Search users where type equals "user" and role equals "admin"`

4. **If you want to search by email later**:
   ```
   Create an index in users for field email
   Search users where email equals "alice@example.com"
   ```

## Summary

**Problem**: Mango queries return no results
**Cause**: Missing index on queried fields
**Solution**: Create an index on those fields
**How**: `Create an index in <database> for field(s) <field_names>`
**Frequency**: Once per field combination

After creating the necessary indexes, all your searches will work as expected!
