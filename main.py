import random
import json
import os

user_data_file = 'user_data.json'

def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            return json.load(file)
    return {}

def save_user_data(data):
    with open(user_data_file, 'w') as file:
        json.dump(data, file, indent=4)

def register():
    users = load_user_data()
    username = input("Enter a new username: ")
    if username in users:
        print("Username already exists. Please try again.")
        return None
    password = input("Enter a new password: ")
    users[username] = {
        'password': password,
        'coin': 0,
        'xp': 0,
        'health': 100,
        'total_health': 100,
        'attack': 10,
        'defense': 5
    }
    save_user_data(users)
    print("Registration successful!")
    return username

def login():
    users = load_user_data()
    username = input("Enter your username: ")
    if username not in users:
        print("Username not found. Please register first.")
        return None
    password = input("Enter your password: ")
    if users[username]['password'] != password:
        print("Incorrect password. Please try again.")
        return None
    print(f"Login successful! Welcome, {username}!")
    return username

def delete_user(username):
    users = load_user_data()
    if username in users:
        del users[username]
        save_user_data(users)
        print("User {username} has been deleted.")
    else:
        print("User not found.")

def get_level(xp):
    return min(xp // 200 + 1, 10)

def rpghunt(level, user):
    events = [
        {"creature": "Goblin", "coins": (1, 5), "xp": (5, 10), "hp_loss": (1, 2)},
        {"creature": "Wolf", "coins": (3, 6), "xp": (8, 12), "hp_loss": (2, 3)},
        {"creature": "Bear", "coins": (5, 10), "xp": (15, 20), "hp_loss": (3, 4)},
        {"creature": "Golem", "coins": (7, 12), "xp": (18, 22), "hp_loss": (4, 5)},
        {"creature": "Slime", "coins": (10, 15), "xp": (25, 30), "hp_loss": (5, 6)},
        {"creature": "Spider", "coins": (12, 18), "xp": (28, 33), "hp_loss": (6, 7)},
        {"creature": "Reptile", "coins": (15, 20), "xp": (35, 40), "hp_loss": (7, 8)},
        {"creature": "Deer", "coins": (17, 22), "xp": (38, 44), "hp_loss": (8, 9)},
        {"creature": "Frog", "coins": (20, 25), "xp": (45, 50), "hp_loss": (9, 10)},
        {"creature": "Creeper", "coins": (23, 28), "xp": (50, 55), "hp_loss": (10, 11)},
    ]

    event = events[level - 1]
    coins = random.randint(*event["coins"])
    xp_gain = random.randint(*event["xp"])
    hp_loss = random.randint(*event["hp_loss"])

    user['coin'] += coins
    user['xp'] += xp_gain
    user['health'] -= hp_loss

    print(f"------------------------------------------------")
    print(f"                    Level {level}:")
    print(f"------------------------------------------------")
    print(f"⚔️ Encountered a {event['creature']}!")
    print(f"💔 Lost {hp_loss} health points.")
    print(f"⭐ Gained {xp_gain} experience points.")
    print(f"💰 Collected {coins} coins.")
    print(f"------------------------------------------------")
    print(f"❤️ Health: {user['health']}/{user['total_health']}")
    print(f"------------------------------------------------")
    if user['health'] <= 0:
        print("💀 You have been defeated and lost all your experience points.")
        user['xp'] = 0
    print("💵 Total coins: {user['coin']}, ⭐ Total experience points: {user['xp']}")

def main():
    user = None
    while user is None:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        choice = input("Enter your choice: ")

        if choice == '1':
            user = register()
        elif choice == '2':
            user = login()
        else:
            print("Invalid choice. Please enter 1 or 2.")

    users = load_user_data()
    current_user = users[user]

    while True:
        print("\nMenu:")
        print("1. Hunt")
        print("2. Delete User")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            level = get_level(current_user['xp'])
            if current_user['health'] > 0:
                rpghunt(level, current_user)
                if current_user['health'] <= 0:
                    break
                save_user_data(users)
            else:
                print("You have no health left. Game over.")
                break
        elif choice == '2':
            delete_user(user)
            break
        elif choice == '3':
            print("Exiting the game.")
            save_user_data(users)
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()