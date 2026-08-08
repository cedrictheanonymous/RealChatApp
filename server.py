import socket
import threading
import sqlite3
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

clients = {}


def save_message(username, message):
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    time = datetime.now().strftime("%H:%M")

    cursor.execute(
        "INSERT INTO messages (username, message, time) VALUES (?, ?, ?)",
        (username, message, time)
    )

    connection.commit()
    connection.close()


def get_history():
    connection = sqlite3.connect("chat.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT username, message, time
        FROM messages
        ORDER BY id DESC
        LIMIT 20
    """)

    history = cursor.fetchall()
    connection.close()

    return history


def broadcast(message, sender):
    for client in list(clients):
        if client != sender:
            try:
                client.send(message.encode())
            except:
                if client in clients:
                    del clients[client]
                client.close()


def handle_client(client, address):
    try:
        username = client.recv(1024).decode()

        clients[client] = username

        print(username, "joined from", address)

        # Send previous messages
        history = get_history()

        client.send("\n===== RECENT MESSAGES =====\n".encode())

        for old_username, old_message, old_time in reversed(history):
            old_text = f"[{old_time}] {old_username}: {old_message}\n"
            client.send(old_text.encode())

        client.send("\n===== CHAT =====\n".encode())

        broadcast(f"{username} joined the chat!", client)

        while True:
            message = client.recv(1024).decode()

            if not message:
                break

            if message == "exit":
                break

            full_message = f"{username}: {message}"

            print(full_message)

            save_message(username, message)

            broadcast(full_message, client)

    except Exception as error:
        print("Error:", error)

    finally:
        username = clients.get(client, "Unknown")

        if client in clients:
            del clients[client]

        client.close()

        print(username, "disconnected")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()

print("==============================")
print("       CHAT SERVER")
print("==============================")
print("Server is running...")
print("Waiting for clients...")

while True:
    client, address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client, address),
        daemon=True
    )

    thread.start()
