import sqlite3
import pandas as pd

conn = sqlite3.connect('social_engine.db')

# Check schema
print('=== SCHEMA ===')
for row in conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall():
    print(row[0][:300])
    print()

# Check column names
print('=== POSTS COLUMNS ===')
cols = pd.read_sql('SELECT * FROM posts LIMIT 1', conn)
print(list(cols.columns))

print('\n=== USERS COLUMNS ===')
cols = pd.read_sql('SELECT * FROM users LIMIT 1', conn)
print(list(cols.columns))

# Quick stats
print('\n=== KEY STATS ===')
print('Total posts:', pd.read_sql('SELECT COUNT(*) as c FROM posts', conn)['c'][0])
print('Posts with NULL likes:', pd.read_sql('SELECT COUNT(*) as c FROM posts WHERE likes IS NULL', conn)['c'][0])
print('Posts with negative likes:', pd.read_sql('SELECT COUNT(*) as c FROM posts WHERE likes < 0', conn)['c'][0])
print('Posts with NULL platform:', pd.read_sql("SELECT COUNT(*) as c FROM posts WHERE platform IS NULL OR platform = ''", conn)['c'][0])
print('Posts with NULL text:', pd.read_sql("SELECT COUNT(*) as c FROM posts WHERE text_content IS NULL OR text_content = ''", conn)['c'][0])
print('Posts with HTML tags:', pd.read_sql("SELECT COUNT(*) as c FROM posts WHERE text_content LIKE '%<%>%'", conn)['c'][0])
print('Posts with &amp;:', pd.read_sql("SELECT COUNT(*) as c FROM posts WHERE text_content LIKE '%&amp;%'", conn)['c'][0])
print('Posts with &lt;:', pd.read_sql("SELECT COUNT(*) as c FROM posts WHERE text_content LIKE '%&lt;%'", conn)['c'][0])

conn.close()
