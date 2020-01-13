from d09exp.temp import backend
from d09exp.temp import config

# Configure Kivy - Must be done before import
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'minimum_width', 800)
Config.set('graphics', 'minimum_height', 600)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Required files for Kivy (tutorials on techwithtim.net)
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
# Add these to get question responses
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput

# Classes required for Kivy application, used in exp.kv
class expApp(App):
    '''Main Kivy application'''
    def build(self):
        self.exp = backend.Backend()
        # PRELOAD LOAD A .WAV!!! -- on_stop does not work with .mp3 (but works after...)
        self.sound = SoundLoader.load('d09exp\\resources\\stimuli\\Untitled.wav')
        print ('init load: ', self.sound.source, '\tLength: ', self.sound.length)
        return Builder.load_file("temp/exp.kv")

class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    parNum = ObjectProperty()
    def get(self):
        self.parNum.text = str(App.get_running_app().exp.participant.get_current())
        return self.parNum.text
    def set(self):
        App.get_running_app().exp.participant.set_current(self.parNum.text)
        #print('participant number confirmed: ', self.parNum.text)

class ParticipantScreen(Screen):
    '''Control for participant survey questions and answers'''
    parQuestion = ObjectProperty()
    parBtn1 = ObjectProperty()
    parBtn2 = ObjectProperty()
    grid1 = ObjectProperty()
    
    def submit(self):
        for n in range(0, len(self.grid1.children)):
            if isinstance(self.grid1.children[n], TextInput):
                App.get_running_app().exp.participant.hold(self.parQuestion.text, self.grid1.children[n].text)
            elif isinstance(self.grid1.children[n], ToggleButton) and (self.grid1.children[n].state == "down"):
                App.get_running_app().exp.participant.hold(self.parQuestion.text, self.grid1.children[n].text)

    def get_q(self):
        '''Get next available question, and response type'''
        self.current = App.get_running_app().exp.survey.get_nextq()
        self.parQuestion.text = self.current[0]
        if self.parQuestion.text == "Complete":
            self.grid1.clear_widgets()
            self.parBtn1.disabled = True
            self.parBtn2.disabled = False
            return
        if self.current[1][0] == "select":
            self.grid1.clear_widgets()
            self.grid1.cols = len(self.current[1])
            #print('create buttons: ', self.grid1.cols)
            for n in range(1, self.grid1.cols):
                self.button = ToggleButton(text = self.current[1][n], group = "select")
                #print('create: ', self.current[1][n])
                self.grid1.add_widget(self.button)
        elif self.current[1][0] == "int":
            self.grid1.clear_widgets()
            self.grid1.cols = 1
            #print('create number input')
            self.input = TextInput(multiline = False, input_filter = "int", hint_text = "Enter age", halign = "center")
            self.grid1.add_widget(self.input)
        elif self.current[1][0] == "text":
            self.grid1.clear_widgets()
            self.grid1.cols = 1
            #print('create text input')
            self.input = TextInput(multiline = True, hint_text = "Enter text")
            self.grid1.add_widget(self.input)


class PersonalityScreen(Screen):
    '''Control for participant survey questions and answers'''
    perQuestion = ObjectProperty()
    perBtn1 = ObjectProperty()
    perBtn2 = ObjectProperty()
    grid2 = ObjectProperty()
    
    def submit(self):
        for n in range(0, len(self.grid2.children)):
            if isinstance(self.grid2.children[n], ToggleButton) and (self.grid2.children[n].state == "down"):
                App.get_running_app().exp.participant.hold(self.perQuestion.text, self.grid2.children[n].id)

    def get_q(self):
        '''Get next available question, and response type'''
        self.current = App.get_running_app().exp.personality.get_nextq()
        self.perQuestion.text = self.current[0]
        if self.perQuestion.text == "Complete":
            self.grid2.clear_widgets()
            self.perBtn1.disabled = True
            self.perBtn2.disabled = False
            return
        if self.current[1][0] == "int":
            self.grid2.clear_widgets()
            self.grid2.cols = len(self.current[1])
            #print('create buttons: ', self.grid2.cols)
            for n in range(1, self.grid2.cols):
                self.button = ToggleButton(text = self.current[1][n], halign = "center", group = "5-point", id = str(n))
                self.grid2.add_widget(self.button)

class StimuliScreen(Screen):
    '''Play stimuli and get rating'''
    slider = ObjectProperty()
    plyBtn = ObjectProperty()
    nxtBtn = ObjectProperty()
    contBtn = ObjectProperty()
    #Volume

    def play_stimulus(self):
        '''Play the current stimulus'''
        self.slider.disabled = True
        self.plyBtn.disabled = True
        self.plyBtn.text = "Playing"
        self.nxtBtn.disabled = True
        self.contBtn.disabled = True

        App.get_running_app().sound.bind(on_stop = self.play_done)
        print('Play Now: ', self.sound.source, '\tLength: ', self.sound.length)
        App.get_running_app().sound.play()

    def play_done(self, unused_arg):
        self.plyBtn.text = "Play"
        self.slider.disabled = False
        self.nxtBtn.disabled = False

    def submit(self):
        '''Submit the stimulus rating'''
        if self.stimulus:
            App.get_running_app().exp.participant.hold(self.stimulus['Name'], self.slider.value)

    def get_s(self):
        '''Get the next stimulus'''
        self.stimulus = App.get_running_app().exp.music.get_nextS()
        self.slider.disabled = True
        self.plyBtn.disabled = False
        self.nxtBtn.disabled = True
        self.contBtn.disabled = True

        print ('[exp] trial: ', self.stimulus)
        
        if ".mp3" in self.stimulus['Name']:
            st = config.STIMULI_PATH + '\\' + self.stimulus['Name']
            print('Load: ', st)
            self.sound = SoundLoader.load(st)
        else:
            print ('ERROR: Cannot load file (type): ', self.stimulus['Name'])


        if self.stimulus == "Complete":
            self.slider.disabled = True
            self.plyBtn.disabled = True
            self.nxtBtn.disabled = True
            self.contBtn.disabled = False

class ExitScreen(Screen):
    pass

class NavBar(GridLayout):
    '''Navigation bar layout'''
    pass

def run():
    '''Run the experiment
    Initialize backend, run Kivy application'''
    expApp().run()

# c:/Users/sotas/programming/d09exp/kivy_venv/Scripts/activate.ps1
# Run in root folder (cd d09exp/) with "python -m d09exp"