import sqlite3

# Connect to database
conn = sqlite3.connect('cs2_tracker.db')
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT id, steam_id, steam_username, avatar_url, created_at FROM users")
users = cursor.fetchall()

print("Users in database:")
print("=" * 80)
for user in users:
    print(f"\nUser ID: {user[0]}")
    print(f"Steam ID: {user[1]}")
    print(f"Username: {user[2]}")
    print(f"Avatar: {user[3][:50] if user[3] else 'None'}...")
    print(f"Created: {user[4]}")

# Get items count
cursor.execute("SELECT user_id, COUNT(*) FROM items GROUP BY user_id")
items_count = cursor.fetchall()

print("\n" + "=" * 80)
print("Items per user:")
for uid, count in items_count:
    print(f"  User {uid}: {count} items")

if not items_count:
    print("  (No items in database yet)")

conn.close()
