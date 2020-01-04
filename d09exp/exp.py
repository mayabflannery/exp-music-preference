from d09exp.temp import backend
from d09exp.temp import config

# Configure Kivy - Must be done before import
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'minimum_width', 800)
Config.set('graphics', 'minimum_height', 600)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Required files for Kivy
import kivy
kivy.require('1.11.1')
from kivy.app import App

class expApp(App):
    def build(self):
        pass

def run():
    exp = backend.backend()
    expApp().run()
    print(exp.survey.get(1))
    print(exp.personality.get(1))

# Run in root folder (cd d09exp/) with "python -m d09exp"