import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Send username to server
client.send(username.encode())

print("==============================")
print("       CHAT CLIENT")
print("==============================")
print("Connected as", username)
print("Type 'exit' to leave.\n")


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()

            if not message:
                break

            print("\n" + message)
            print("You: ", end="", flush=True)

        except:
            break


thread = threading.Thread(
    target=receive_messages,
    daemon=True
)

thread.start()

while True:
    message = input("You: ")

    if message == "exit":
        break

    client.send(message.encode())

client.close()
