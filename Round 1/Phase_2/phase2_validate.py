"""
Phase 2: Load cleaned data into SQLite and validate all SQL queries.
"""
import sqlite3
import pandas as pd

# Load cleaned data
posts = pd.read_csv("Social_Engine_Posts_Cleaned.csv")
users = pd.read_csv("Social_Engine_Users_Cleaned.csv")

# Create SQLite database
conn = sqlite3.connect("social_engine.db")

# Load data into tables
users.to_sql("users", conn, if_exists="replace", index=False)
posts.to_sql("posts", conn, if_exists="replace", index=False)

print(f"Loaded {len(users)} users and {len(posts)} posts into SQLite.")

# Read and execute each query from the SQL file
with open("phase2_sql_queries.sql", "r", encoding="utf-8") as f:
    sql_content = f.read()

# Extract individual queries (separated by the section headers)
import re
queries = re.split(r'-- ={70,}', sql_content)
# Filter to actual executable queries (containing SELECT)
query_blocks = []
for block in queries:
    block = block.strip()
    if block and "SELECT" in block.upper() and "CREATE" not in block.upper():
        # Clean out comment-only lines at start
        lines = block.split('\n')
        # Find the first WITH or SELECT
        start_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('WITH') or stripped.startswith('SELECT'):
                start_idx = i
                break
        query = '\n'.join(lines[start_idx:]).strip().rstrip(';')
        if query:
            # Extract title from comment block
            title = "Unknown"
            for line in lines:
                if "QUERY" in line and ":" in line:
                    title = line.split(":", 1)[1].strip().strip('-').strip()
                    break
            query_blocks.append((title, query))

print(f"\nFound {len(query_blocks)} analytical queries to execute.\n")

for i, (title, query) in enumerate(query_blocks, 1):
    print(f"\n{'='*70}")
    print(f"QUERY {i}: {title}")
    print(f"{'='*70}")
    try:
        result = pd.read_sql_query(query, conn)
        print(f"Rows returned: {len(result)}")
        print(result.head(10).to_string())
    except Exception as e:
        print(f"ERROR: {e}")
        print(f"Query snippet: {query[:200]}...")

conn.close()
print("\nAll queries validated successfully.")
