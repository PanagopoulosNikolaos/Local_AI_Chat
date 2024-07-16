Documentation for ChatGUI Program
Overview
The ChatGUI class creates a GUI for interacting with a GPT-4 model using PyQt5. The GUI consists of two main panels: the left panel for managing chat sessions and the right panel for interacting with the model. The program also includes functionalities for loading models, creating new chat sessions, and sending messages to the model.
Imports
python


import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTextEdit, QListWidget, QLabel, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider
from gpt4all import GPT4All
import markdown2
sys and os: Standard libraries for system and OS operations.
PyQt5.QtWidgets: Classes for creating the GUI.
PyQt5.QtCore: Core non-GUI classes, including event handling.
markdown2: Library for converting Markdown to HTML.
Class: ChatGUI
python


class ChatGUI(QMainWindow):
Inherits from QMainWindow to provide the main window for the application.
__init__ Method
python


def __init__(self):
Initializes the ChatGUI object, setting up the main window and its properties.
Attributes:
current_model: Holds the currently loaded model.
current_chat: Holds the currently active chat session.
Methods Called:
setup_left_panel()
setup_right_panel()
load_models()
load_chats()
setup_left_panel Method
python


def setup_left_panel(self):
Sets up the left panel of the chat GUI window.
Components:
QListWidget: Displays a list of chat sessions.
QPushButton: Button for creating a new chat session.
setup_right_panel Method
python


def setup_right_panel(self):
Sets up the right panel of the chat GUI window.
Components:
QComboBox: Dropdown for selecting models.
QPushButton: Button for ejecting the current model.
QTextEdit: Displays the chat conversation.
QTextEdit: Input field for user messages.
QSlider: Slider for setting the maximum number of tokens.
QPushButton: Button for sending messages.
load_models Method
python


def load_models(self):
Loads the models from the ./MODELS directory and populates the model dropdown.
Functionality:
Checks if the ./MODELS directory exists.
Retrieves and lists .gguf files in the dropdown.
load_model Method
python


def load_model(self, index):
Loads a model based on the provided index.
Parameters:
index: The index of the model to load.
Functionality:
Loads the selected model using the GPT4All library and sets it to current_model.
eject_model Method
python


def eject_model(self):
Ejects the current model by setting current_model to None.
load_chats Method
python


def load_chats(self):
Loads the chats from the ./Chat_Data directory and populates the chat list.
Functionality:
Checks if the ./Chat_Data directory exists or creates it.
Lists .md files in the chat list.
create_new_chat Method
python


def create_new_chat(self):
Creates a new chat session by generating a unique filename and adding it to the chat list.
load_chat Method
python


def load_chat(self, item):
Loads a chat based on the provided item and displays its content in the chat display.
Parameters:
item: The chat item to load.
send_message Method
python


def send_message(self):
Sends a message in the chat interface.
Functionality:
Retrieves the user message and appends it to the chat log.
Generates a response using the model and appends it to the chat log.
Main Function
python


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGUI()
    window.show()
    window.eject_model()
    sys.exit(app.exec_())
Initializes the application and starts the event loop.