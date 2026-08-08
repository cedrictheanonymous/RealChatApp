import socket
import threading

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock


HOST = "127.0.0.1"
PORT = 5000


class ChatApp(App):

    def build(self):
        self.client = None
        self.username = ""

        main = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        title = Label(
            text="💬 ChatApp",
            font_size=30,
            size_hint_y=None,
            height=60
        )

        main.add_widget(title)

        self.username_input = TextInput(
            hint_text="Enter username",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        main.add_widget(self.username_input)

        self.chat = TextInput(
            text="",
            readonly=True,
            multiline=True,
            font_size=18
        )

        main.add_widget(self.chat)

        message_layout = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=5
        )

        self.message_input = TextInput(
            hint_text="Type a message...",
            multiline=False
        )

        send_button = Button(
            text="SEND",
            size_hint_x=None,
            width=100
        )

        send_button.bind(on_press=self.send_message)

        message_layout.add_widget(self.message_input)
        message_layout.add_widget(send_button)

        main.add_widget(message_layout)

        connect_button = Button(
            text="CONNECT",
            size_hint_y=None,
            height=50
        )

        connect_button.bind(on_press=self.connect)

        main.add_widget(connect_button)

        return main

    def connect(self, instance):

        self.username = self.username_input.text.strip()

        if not self.username:
            self.chat.text += "Please enter a username.\n"
            return

        try:
            self.client = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.client.connect((HOST, PORT))

            self.client.send(self.username.encode())

            self.chat.text += (
                f"Connected as {self.username}\n"
            )

            thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )

            thread.start()

        except Exception as error:

            self.chat.text += (
                f"Connection error: {error}\n"
            )

    def receive_messages(self):

        while True:

            try:

                message = self.client.recv(4096).decode()

                if not message:
                    break

                Clock.schedule_once(
                    lambda dt, msg=message:
                    self.show_message(msg)
                )

            except:
                break

    def show_message(self, message):

        self.chat.text += message

    def send_message(self, instance):

        message = self.message_input.text.strip()

        if not message:
            return

        if self.client is None:

            self.chat.text += (
                "Connect to the server first.\n"
            )

            return

        try:

            self.client.send(message.encode())

            self.chat.text += (
                f"You: {message}\n"
            )

            self.message_input.text = ""

        except:

            self.chat.text += (
                "Message could not be sent.\n"
            )


if __name__ == "__main__":
    ChatApp().run()
