from d09exp.temp import backend
from d09exp.temp import config

# Configure Kivy - Must be done before import
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'minimum_width', 800)
Config.set('graphics', 'minimum_height', 600)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Required files for Kivy (tutorials on techwithtim.net - super resource!)
# note: pylint doesn't recognize ObjectProperty for some reason (disabled annoying warning)
import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty  # pylint: disable=no-name-in-module
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

# Classes required for Kivy application, used in exp.kv
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
    '''Navigation bar layout'''
    pass

class expApp(App):
    '''Main Kivy application'''
    def build(self):
        return Builder.load_file("temp/exp.kv")

def run():
    '''Run the experiment
    Initialize backend, run Kivy application'''
    expApp().run()

# Run in root folder (cd d09exp/) with "python -m d09exp"