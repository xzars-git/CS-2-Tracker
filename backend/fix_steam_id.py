import sqlite3

# Connect to database
conn = sqlite3.connect('cs2_tracker.db')
cursor = conn.cursor()

# Get current user
cursor.execute("SELECT id, steam_id, steam_username FROM users ORDER BY id DESC LIMIT 1")
user = cursor.fetchone()

if user:
    print(f"Current user in DB:")
    print(f"  ID: {user[0]}")
    print(f"  Steam ID (OLD): {user[1]}")
    print(f"  Username: {user[2]}")
    print()
    
    # Update with correct Steam ID
    correct_steam_id = "76561199629904226"
    
    cursor.execute(
        "UPDATE users SET steam_id = ? WHERE id = ?",
        (correct_steam_id, user[0])
    )
    
    conn.commit()
    
    print(f"✅ Updated Steam ID to: {correct_steam_id}")
    
    # Verify
    cursor.execute("SELECT steam_id FROM users WHERE id = ?", (user[0],))
    new_id = cursor.fetchone()[0]
    print(f"✅ Verified: {new_id}")
else:
    print("No users found")

conn.close()
