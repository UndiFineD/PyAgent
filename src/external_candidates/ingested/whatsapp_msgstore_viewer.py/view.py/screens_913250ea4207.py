# Extracted from: C:\DEV\PyAgent\.external\whatsapp-msgstore-viewer\View\screens.py
# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.
from Controller.chat_screen import ChatScreenController
from Controller.login_screen import LoginScreenController
from Controller.main_screen import MainScreenController
from Model.chat_screen import ChatScreenModel
from Model.login_screen import LoginScreenModel
from Model.main_screen import MainScreenModel

screens = {
    "login screen": {
        "model": LoginScreenModel,
        "controller": LoginScreenController,
    },
    "main screen": {
        "model": MainScreenModel,
        "controller": MainScreenController,
    },
    "chat screen": {
        "model": ChatScreenModel,
        "controller": ChatScreenController,
    },
}
