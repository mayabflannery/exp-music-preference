from d09exp.temp import backend
from d09exp.temp import config

# Configure Kivy - Must be done before import
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'minimum_width', 800)
Config.set('graphics', 'minimum_height', 600)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Required files for Kivy (tutorials on techwithtim.net - super resource!)
import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class ParticipantScreen(Screen):
    pass

class PersonalityScreen(Screen):
    pass

class StimuliScreen(Screen):
    pass

class ExitScreen(Screen):
    pass

class NavBar(GridLayout):
    pass

class expApp(App):
    def build(self):
        return Builder.load_file("temp/exp.kv")

def run():
    exp = backend.backend()
    expApp().run()
    print(exp.survey.get(1))
    print(exp.personality.get(1))

# Run in root folder (cd d09exp/) with "python -m d09exp"