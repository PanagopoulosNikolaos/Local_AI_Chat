import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTextEdit, QListWidget, QLabel, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider
from gpt4all import GPT4All
import markdown2

class ChatGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPT4ALL Chat")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #3E5463; color: white;")
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.setup_left_panel()
        self.setup_right_panel()

        self.current_model = None
        self.current_chat = None
        
        # Explicitly call load_models() here
        self.load_models()
        
        self.load_chats()

    def setup_left_panel(self):
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Add a spacer item at the top
        top_spacer = QWidget()
        
        top_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(top_spacer)

        self.chat_list = QListWidget()
        self.chat_list.itemClicked.connect(self.load_chat)
        left_layout.addWidget(self.chat_list)

        new_chat_button = QPushButton("New Chat")
        
        new_chat_button.clicked.connect(self.create_new_chat)
        new_chat_button.setStyleSheet("background-color: #2889CC; color: white;")
        left_layout.addWidget(new_chat_button)

        left_panel.setFixedWidth(200)  # You can adjust this value as needed
        # left_panel.setStyleSheet("background-color: #1CA3A7; color: white;")
        left_panel.setFixedHeight(800)
        
        self.layout.addWidget(left_panel)
        
        
        

    def setup_right_panel(self):
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)

        self.model_dropdown = QComboBox()
        top_bar_layout.addWidget(self.model_dropdown)

        eject_button = QPushButton("Eject Model")
        eject_button.clicked.connect(self.eject_model)
        top_bar_layout.addWidget(eject_button)

        right_layout.addWidget(top_bar)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #334C5D; color: white;")
        right_layout.addWidget(self.chat_display)

        """add the slider to the setup_right_panel method"""
        self.user_input = QTextEdit()
        self.user_input.setFixedHeight(100)
        right_layout.addWidget(self.user_input)
        self.max_tokens_slider = QSlider(Qt.Horizontal)
        self.max_tokens_slider.setMinimum(100)
        self.max_tokens_slider.setMaximum(4096)
        self.max_tokens_slider.setValue(2048)
        self.max_tokens_slider.setTickPosition(QSlider.TicksBelow)
        self.max_tokens_slider.setTickInterval(500)
        right_layout.addWidget(QLabel("Max Tokens:"))
        right_layout.addWidget(self.max_tokens_slider)
        """d----------------------------------------------------------b"""

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet("background-color: #2889CC; color: white;")
        right_layout.addWidget(send_button)

        self.layout.addWidget(right_panel)

    def load_models(self):
        if not os.path.exists("./MODELS"):
            print("Error: MODELS folder not found.")
            return
        models = [f for f in os.listdir("./MODELS") if f.endswith(".gguf")]
        self.model_dropdown.clear()  # Clear existing items
        self.model_dropdown.addItems(models)
        
        # Connect the dropdown to the load_model function
        self.model_dropdown.currentIndexChanged.connect(self.load_model)

    def load_model(self, index):
        if index < 0:
            return
        model_name = self.model_dropdown.currentText()
        model_path = os.path.abspath(os.path.join("./MODELS", model_name))
        print(f"Attempting to load model: {model_path}")  # Debug print
        try:
            self.current_model = GPT4All(model_path, device='gpu')
            print(f"Successfully loaded model: {model_name}")
            QMessageBox.information(self, "Model Loaded", f"Model {model_name} has been loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load model: {str(e)}")
            self.current_model = None

    def eject_model(self):
        self.current_model = None
        self.model_dropdown.setCurrentIndex(-1)

    def load_chats(self):
        if not os.path.exists("./Chat_Data"):
            os.makedirs("./Chat_Data")
        chats = [f for f in os.listdir("./Chat_Data") if f.endswith(".md")]
        self.chat_list.addItems(chats)

    def create_new_chat(self):
        chat_name = f"chat_{len(os.listdir('./Chat_Data')) + 1}.md"
        with open(f"./Chat_Data/{chat_name}", "w") as f:
            f.write("# New Chat\n\n")
        self.chat_list.addItem(chat_name)
        self.load_chat(self.chat_list.item(self.chat_list.count() - 1))

    def load_chat(self, item):
        self.current_chat = item.text()
        with open(f"./Chat_Data/{self.current_chat}", "r") as f:
            content = f.read()
        html_content = markdown2.markdown(content)
        self.chat_display.setHtml(html_content)
        if self.current_model:
            self.chat_session = self.current_model.chat_session()
            print("Chat session reset for loaded chat")

    def send_message(self):
        if not self.current_model:
            print("No model is currently loaded.")  # Debug print
            QMessageBox.warning(self, "No Model Loaded", "Please select and load a model before sending a message.")
            return
        if not self.current_chat:
            QMessageBox.warning(self, "No Chat Selected", "Please select or create a new chat before sending a message.")
            return

        user_message = self.user_input.toPlainText()
        if not user_message.strip():
            return

        self.user_input.clear()

        with open(f"./Chat_Data/{self.current_chat}", "a") as f:
            f.write(f"\n\n**User:** {user_message}\n\n")

        max_tokens = getattr(self, 'max_tokens_slider', None)
        if max_tokens is None:
            max_tokens = 2048  # Default value if slider is not available
        else:
            max_tokens = max_tokens.value()

        try:
            with self.current_model.chat_session():
                response = self.current_model.generate(user_message, max_tokens=max_tokens)
            print(f"Model response ({max_tokens} tokens): {response}")  # Debug print
        except Exception as e:
            print(f"Error generating response with {max_tokens} tokens: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred while generating the response: {str(e)}")
            return

        with open(f"./Chat_Data/{self.current_chat}", "a") as f:
            f.write(f"**Assistant:**\n {response}\n\n")

        self.load_chat(self.chat_list.findItems(self.current_chat, Qt.MatchExactly)[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGUI()
    window.show()
    window.eject_model()
    sys.exit(app.exec_())
