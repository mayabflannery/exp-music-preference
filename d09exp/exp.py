import backend
import config

# Configure Kivy - Must be done before import
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'minimum_width', 800)
Config.set('graphics', 'minimum_height', 600)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('kivy', 'exit_on_escape', 0)

# Required files for Kivy (tutorials on techwithtim.net)
# note: pylint doesn't recognize ObjectProperty for some reason (disabled annoying warning)
import kivy
kivy.require('1.9.1')
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
from kivy.core.window import Window

# Classes required for Kivy application, used in exp.kv
class expApp(App):
    '''Main Kivy application'''
    def build(self):
        print("build expapp")
        self.exp = backend.Backend()
        Window.bind(on_key_down=self.on_keyboard_down)
        # PRELOAD LOAD A .WAV!!! -- on_stop does not work with .mp3 (but works after...)
        self.sound = SoundLoader.load('/resources/stimuli/Untitled.wav')
        return Builder.load_file("expKV.kv")
    
    ##### TO DO...
    ## gender question

    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if text == 'e' and 'ctrl' in modifiers and 'alt' in modifiers:
            self.get_running_app().root.current = "exit"
        elif text == 'm' and 'ctrl' in modifiers and 'alt' in modifiers:
            self.get_running_app().root.current = "main"
        elif text == 'q' and 'ctrl' in modifiers and 'alt' in modifiers:
            self.get_running_app().root.current = "participant"
        elif text == 'p' and 'ctrl' in modifiers and 'alt' in modifiers:
            self.get_running_app().root.current = "personality"
        elif text == 's' and 'ctrl' in modifiers and 'alt' in modifiers:
            self.get_running_app().root.current = "stimuli"

class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    '''Introduce study, confirm participant'''
    parNum = ObjectProperty()
    def get(self):
        '''Get the next participant number, can be modified if needed'''
        self.parNum.text = str(App.get_running_app().exp.participant.get_current())
        return self.parNum.text
    def set(self):
        '''Submit the number, confirm participant'''
        App.get_running_app().exp.participant.set_current(self.parNum.text)

class ParticipantScreen(Screen):
    '''Control for participant survey questions and answers'''
    parQuestion = ObjectProperty()
    parBtn1 = ObjectProperty()
    parBtn2 = ObjectProperty()
    grid1 = ObjectProperty()
    
    def check_age(self, unused_arg1, text):
        '''Verify there is a somewhat valid age entered before continue'''
        if text.isdigit():
            if int(text) > 5 and int(text) < 105: 
                self.parBtn1.disabled = False
            else:
                self.parBtn1.disabled = True

    def enable(self, unused_arg):
        '''Verify button selected before continue'''
        self.parBtn1.disabled = False

    def submit(self):
        '''Depending on inputs in grid1, submit to participant response handler'''
        for n in range(0, len(self.grid1.children)):
            if isinstance(self.grid1.children[n], TextInput):
                App.get_running_app().exp.participant.hold(self.parQuestion.text, self.grid1.children[n].text)
            elif isinstance(self.grid1.children[n], ToggleButton) and (self.grid1.children[n].state == "down"):
                App.get_running_app().exp.participant.hold(self.parQuestion.text, self.grid1.children[n].text)

    def get_q(self):
        '''Get next available question, and response type'''
        self.parBtn1.disabled = True
        self.current = App.get_running_app().exp.survey.get_nextq()
        self.parQuestion.text = self.current[0]
        # When all questions are complete, enable next step in study
        if self.parQuestion.text == "Complete":
            self.grid1.clear_widgets()
            self.parBtn1.disabled = True
            self.parBtn2.disabled = False
            return
        # If a question requires a selection between options, create buttons
        if self.current[1][0] == "select":
            self.grid1.clear_widgets()
            self.grid1.cols = len(self.current[1])
            for n in range(1, self.grid1.cols):
                if self.current[1][n] != "":
                    self.button = ToggleButton(text = self.current[1][n], group = "select", allow_no_selection = False)
                    self.button.bind(on_release = self.enable)
                    self.grid1.add_widget(self.button)
        # If a question requires and integer, create an int only text input field
        elif self.current[1][0] == "int":
            self.grid1.clear_widgets()
            self.grid1.cols = 1
            self.input = TextInput(multiline = False, input_filter = "int", hint_text = "Enter age", halign = "center")
            self.input.bind(text = self.check_age)
            self.grid1.add_widget(self.input)
        # If a question requires a longer answer, create a longer text input field
        elif self.current[1][0] == "text":
            self.grid1.clear_widgets()
            self.grid1.cols = 1
            self.input = TextInput(multiline = True, hint_text = "Enter text or press continue to skip...")
            self.parBtn1.disabled = False
            self.grid1.add_widget(self.input)

class PersonalityScreen(Screen):
    '''Control for participant survey questions and answers'''
    perQuestion = ObjectProperty()
    perBtn1 = ObjectProperty()
    perBtn2 = ObjectProperty()
    grid2 = ObjectProperty()
    
    def enable(self, unused_arg):
        '''Do not allow next question until an option is selected'''
        self.perBtn1.disabled = False

    def submit(self):
        '''Submit the selected button to participant response data'''
        for n in range(0, len(self.grid2.children)):
            if isinstance(self.grid2.children[n], ToggleButton) and (self.grid2.children[n].state == "down"):
                App.get_running_app().exp.participant.hold(self.perQuestion.text, self.grid2.children[n].id)

    def get_q(self):
        '''Get next available question, and response type'''
        self.perBtn1.disabled = True
        self.current = App.get_running_app().exp.personality.get_nextq()
        self.perQuestion.text = self.current[0]
        # When all questions are complete, enable next step in study
        if self.perQuestion.text == "Complete":
            self.grid2.clear_widgets()
            self.perBtn1.disabled = True
            self.perBtn2.disabled = False
            return
        # Create buttons for likert scale
        if self.current[1][0] == "int":
            self.grid2.clear_widgets()
            self.grid2.cols = len(self.current[1])
            for n in range(1, self.grid2.cols):
                self.button = ToggleButton(text = self.current[1][n], halign = "center", group = "5-point", id = str(n), allow_no_selection = False)
                self.button.bind(on_release = self.enable)
                self.grid2.add_widget(self.button)

class StimuliScreen(Screen):
    '''Play stimuli and get rating'''
    slider = ObjectProperty()
    plyBtn = ObjectProperty()
    nxtBtn = ObjectProperty()
    contBtn = ObjectProperty()
    stimulus = None

    def play_stimulus(self):
        '''Play the current stimulus'''
        # Disable everything while playing
        self.slider.disabled = True
        self.plyBtn.disabled = True
        self.plyBtn.text = "Playing"
        self.nxtBtn.disabled = True
        self.contBtn.disabled = True

        self.sound.bind(on_stop = self.play_done)
        print('Play Now: ', self.sound.source, '\tLength: ', self.sound.length)
        self.sound.play()

    def play_done(self, unused_arg):
        '''Enable slider and next/submit button'''
        self.plyBtn.text = "Play"
        self.slider.disabled = False
        self.nxtBtn.disabled = False

    def submit(self):
        '''Submit the stimulus rating'''
        if self.stimulus:
            App.get_running_app().exp.participant.hold(self.stimulus['Name'], self.slider.value)
            self.slider.value = 50

    def get_s(self):
        '''Get the next stimulus'''
        self.stimulus = App.get_running_app().exp.music.get_nextS()
        self.slider.disabled = True
        self.plyBtn.disabled = False
        self.nxtBtn.disabled = True
        self.contBtn.disabled = True

        print ('[exp] trial: ', self.stimulus)

        # When list is complete, continue study
        if self.stimulus == "Complete":
            self.slider.disabled = True
            self.plyBtn.disabled = True
            self.nxtBtn.disabled = True
            self.contBtn.disabled = False
            return

        # Ensure wav file, then load the sound
        if ".wav" in self.stimulus['Name']:
            st = config.STIMULI_PATH + '\\' + self.stimulus['Name']
            print('Load: ', st)
            self.sound = SoundLoader.load(st)
        else:
            print ('ERROR: Cannot load file (type): ', self.stimulus['Name'])

class ExitScreen(Screen):
    '''Last screen of study'''
    pass

class NavBar(GridLayout):
    '''Navigation bar layout'''
    pass

def run():
    '''Run the experiment
    Initialize backend, run Kivy application'''
    print("expApp run")
    expApp().run()

if __name__ == '__main__':
    print("exp run")
    run()

# c:/Users/sotas/programming/d09exp/kivy_venv/Scripts/activate.ps1
# Run in root folder (cd d09exp/) with "python -m d09exp"