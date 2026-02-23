# CouchDB MCP Server - Usage Examples

This document provides detailed examples of how to use the CouchDB MCP server with Claude Code.

## Getting Started

After configuring the MCP server in Claude Code, you can start using natural language to interact with your CouchDB instance.

## Database Management

### Creating Databases

**Simple request**:
```
Create a database called "products"
```

**Multiple databases**:
```
Create three databases: customers, orders, and inventory
```

### Listing Databases

```
Show me all databases
```

```
List all databases in the CouchDB server
```

### Deleting Databases

```
Delete the database named "test_db"
```

```
Remove the products database
```

## Working with Documents

### Creating Documents

**Simple document**:
```
Create a document in the customers database with:
- name: "Alice Johnson"
- email: "alice@example.com"
- age: 28
```

**With custom ID**:
```
Create a document in the products database with ID "prod-001" containing:
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics",
  "stock": 50
}
```

**Multiple documents**:
```
Create the following products in the products database:
1. name: "Mouse", price: 25.99, category: "Accessories"
2. name: "Keyboard", price: 79.99, category: "Accessories"
3. name: "Monitor", price: 299.99, category: "Electronics"
```

### Reading Documents

**By ID**:
```
Get the document with ID "prod-001" from the products database
```

**List all documents**:
```
List all documents in the customers database
```

```
Show me all documents in the orders database with their full content
```

### Updating Documents

```
Update the document "prod-001" in the products database to set the price to 899.99
```

**Note**: When updating, you'll need the current revision (`_rev`). Claude will typically:
1. First get the document to retrieve the current `_rev`
2. Then update it with the new data

Example conversation:
```
User: Update customer alice@example.com's age to 29
Claude: I'll get the document first to retrieve its revision, then update it.
```

### Deleting Documents

```
Delete the document with ID "prod-001" from the products database
```

Claude will automatically retrieve the document's `_rev` before deleting.

## Searching Documents

### Simple Queries

**Exact match**:
```
Find all products in the products database where category is "Electronics"
```

**Multiple conditions**:
```
Search the products database for items where:
- category is "Electronics"
- price is less than 500
```

### Advanced Queries

**Range queries**:
```
Find all customers older than 25 in the customers database
```

**Pattern matching**:
```
Search for all customers with email addresses ending in "@example.com"
```

**With pagination**:
```
Find the first 10 products in the Electronics category, skip the first 5
```

## Real-World Scenarios

### E-commerce Product Catalog

```
1. Create a products database
2. Add these products:
   - Laptop: $999, Electronics, 50 in stock
   - Mouse: $25, Accessories, 200 in stock
   - Desk: $299, Furniture, 30 in stock
3. Find all products under $100
4. Update the Laptop price to $899
5. List all products with their stock levels
```

### User Management System

```
1. Create a users database
2. Add a user with username "john_doe", email "john@example.com", role "admin"
3. Add another user with username "jane_smith", email "jane@example.com", role "user"
4. Find all admin users
5. Update jane_smith's role to "moderator"
```

### Order Tracking

```
1. Create an orders database
2. Create an order:
   - customer: "Alice Johnson"
   - items: ["Laptop", "Mouse"]
   - total: 1024.98
   - status: "pending"
3. Find all pending orders
4. Update the order status to "shipped"
```

## Complex Queries

### Mango Query Operators

CouchDB supports MongoDB-style query operators:

**Comparison operators**:
- `$eq`: Equal to
- `$ne`: Not equal to
- `$gt`: Greater than
- `$gte`: Greater than or equal to
- `$lt`: Less than
- `$lte`: Less than or equal to

**Logical operators**:
- `$and`: All conditions must be true
- `$or`: At least one condition must be true
- `$not`: Inverts the condition

**Example queries you can ask Claude to execute**:

```
Search products where price is between 50 and 500
```
(Translates to: `{"$and": [{"price": {"$gte": 50}}, {"price": {"$lte": 500}}]}`)

```
Find customers who are either under 18 or over 65
```
(Translates to: `{"$or": [{"age": {"$lt": 18}}, {"age": {"$gt": 65}}]}`)

```
Find all products that are NOT in the Electronics category
```
(Translates to: `{"category": {"$ne": "Electronics"}}`)

## Tips for Natural Interaction

1. **Be specific about the database**: Always mention which database you're working with

2. **Use natural language**: Claude understands context
   - "Add a product..." → Claude will create a document
   - "Show me all..." → Claude will list or search
   - "Change the price..." → Claude will update the document

3. **Chain operations**: You can request multiple operations in sequence
   ```
   Create a books database, add three books (title, author, price),
   then show me all books priced under $20
   ```

4. **Ask for help**: If you're unsure about the query format
   ```
   How do I search for documents where the date is after January 1, 2024?
   ```

## Troubleshooting with Claude

If something goes wrong, Claude can help debug:

```
I'm getting an error when trying to update a document, can you help?
```

```
Why can't I delete this document?
```

```
Show me the structure of the document "prod-001" so I can update it correctly
```

## Best Practices

1. **Always get the document before updating**: CouchDB requires the `_rev` field
2. **Use meaningful IDs**: Instead of auto-generated IDs, use descriptive ones like "user-001"
3. **Include metadata**: Add timestamps, version numbers, or status fields to documents
4. **Test queries on small datasets**: Before running complex queries, test on a few documents
5. **Keep document structure consistent**: Use the same field names across similar documents

## Integration Examples

### Backup Documents

```
List all documents in the customers database with full content,
then save the results so I can back them up
```

### Data Migration

```
Get all documents from the old_products database,
then recreate them in the new_products database
```

### Reporting

```
Search the orders database for all orders from the last month
where the total is over $1000, then count how many there are
```

### Data Validation

```
Find all customer documents that are missing the email field
```

```
Show me all products where the price is 0 or negative
```
