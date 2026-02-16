import sys
import os
from utils import SessionManager

def main():
    session_manager = SessionManager()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python user_manager.py add <username>")
        print("  python user_manager.py remove <username>")
        print("  python user_manager.py list")
        print("  python user_manager.py bulk-add <file_path>")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Specify a username.")
            return
        username = sys.argv[2]
        session_manager.add_user(username)
        print(f"User '{username}' added.")

    elif command == "remove":
        if len(sys.argv) < 3:
            print("Error: Specify a username.")
            return
        username = sys.argv[2]
        session_manager.remove_user(username)
        print(f"User '{username}' removed.")

    elif command == "list":
        users = session_manager.get_all_users()
        print(f"Total allowed users: {len(users)}")
        for i, user in enumerate(users, 1):
            print(f"{i}. {user}")

    elif command == "bulk-add":
        if len(sys.argv) < 3:
            print("Error: Specify a file path containing usernames (one per line).")
            return
        file_path = sys.argv[2]
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return
        
        with open(file_path, "r") as f:
            count = 0
            for line in f:
                user = line.strip()
                if user:
                    session_manager.add_user(user)
                    count += 1
            print(f"Bulk-add complete. Added {count} users.")

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
