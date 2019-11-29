"""
Start
"""
from d09exp.common import config
from d09exp.common import backend

#-----------------------------------------------------------------------
# Configure Kivy
# MUST be done BEFORE importing any kivy modules
# Window mode can be set in the config file.
#-----------------------------------------------------------------------
from kivy.config import Config
Config.set('graphics', 'fullscreen', config.WINDOW_MODE)
Config.set('graphics', 'minimum_width', 800)
Config.set('graphics', 'minimum_height', 600)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
#-----------------------------------------------------------------------
# Configure End
#-----------------------------------------------------------------------

import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
# Import Custom  Fonts
from kivy.core.text import LabelBase

class StyledScreen(FloatLayout):
    """
    Basic screen: wallpaper/backdrop
    """
    pass

class TrialScreen(StyledScreen):
    """
    Play stimuli screen: with...
    """
    slider = ObjectProperty()
    play_button = ObjectProperty()
    continue_button = ObjectProperty()
    backend = None

    def play(self):
        """
        Play stimulus file
        """
        # ...get backend something...
        
        self.play_button.disabled = True
        
        # Needs update...
        # midi_filename = self.backend.get_next_midi()
        
        stimulus_filename = "resources/stimuli/preload.mp3"
        
        if stimulus_filename:
            self.sound = SoundLoader.load(stimulus_filename)
            if self.sound:
                #self.sound.seek(0)
                self.sound.bind(on_stop=self.sound_stopped)
                self.sound.play()
            else:
                self.exit_on_error("Error", "No Audio File Available")
        
    def exit_on_error(self, pTitle, pMessage):
        """
        There is an error with no possible way to recover. Switch to
        the exit screen and allow the program to terminate normally.
        """
        alert(pTitle, pMessage)
        App.get_running_app().root.show_exit_screen()
        
    def sound_stopped(self, unused_arg):
        """Bound to the playing of the song. Gets activated
        when the song ends. At that point the user can make their
        input.
        - Unused_arg is needed ... a kivy thing? To check out later.
        """
        self.slider.disabled = False
        self.continue_button.disabled = False
    
    def continue_pressed(self):
        """
        Handle pressing of the continue button during the experiment
        Duties include:
         - save all data
         - either continue the experiment or ...
         - switch to the exit screen
         - enable/disable controls as necessary to continue experiment
        """
        # slider_val = round(self.slider.value, 1)
    
        # Save data
        # Backend stores all the data so no need for any other data
        # than the slider value
        
        # self.backend.save(slider_val)
        
        # # Goto next trial
        # self.backend.increment_trial()
        
        # if self.backend.is_next():
        #     self.slider.value = 3.5
        #     self.slider.disabled = True
        #     self.continue_button.disabled = True
        #     self.play_button.disabled = False
        # else:
        #     App.get_running_app().root.show_exit_screen()

class SurveyScreen(StyledScreen):
    # here...
    survey_continue = ObjectProperty()
    survey_next = ObjectProperty()
    survey_question = ObjectProperty()
    backend = None

    def next_pressed(self, q_id):
        if not self.backend:
            self.backend = App.get_running_app().get_backend()
        self.backend.inc_question(q_id)
        self.survey_question.text = self.backend.get_survey_row(self.backend.survey, self.backend.q_id)

class PersonalityScreen(StyledScreen):
    pass

class ExitScreen(StyledScreen):
    pass

class ApplicationRoot(BoxLayout):
    # LEAVE this here. W/out this the first time a MIDI file
    # plays it cuts out after 3 seconds. But if you preload
    # anything then you can load/play other files just fine. Wierd.
    sound = SoundLoader.load('resources/stimuli/preload.mp3')
    
    # Backend used to save/load data
    backend = None
        
    """This is the base screen & control center of the app. It controls 
    what is displayed, changes screens, handles user input, etc.
    """
    def start_survey(self, user_id, trials, midi_dir):
        """Setup the survey and switch to participant survey screen"""
        # call backend stuff to set up survey
        self.clear_widgets()
        self.add_widget(SurveyScreen())
        print("Survey started")

    def start_personality(self, user_id, trials, midi_dir):
        """Setup personality test and switch to personality screen"""
        self.clear_widgets()
        self.add_widget(PersonalityScreen())
        print("Personality test started")

    def start_experiment(self, user_id, trials, midi_dir):
        """Switch screen and setup everything for the experiment"""
        self.backend = App.get_running_app().get_backend()
        #self.backend.setup_experiment(user_id, trials, midi_dir)
        if config.SURVEY and not(self.backend.survey_complete):
            self.start_survey(user_id, trials, midi_dir)
        else:
            self.clear_widgets()
            self.add_widget(TrialScreen())
            print("Experiment started")
    
    def show_exit_screen(self):
        """Temporary method used to switch to exit screen"""
        self.clear_widgets()
        self.add_widget(ExitScreen())
    
    #def test_popup(Self):
    #    alert("Test title", "Content")


class expApp(App):
    def get_backend(self, backend = backend.Backend()):
        return backend
    def build(self):
        return Builder.load_file('common/exp.kv')

def alert(pTitle, pMessage):
    """Utility method that shows an allert"""
    popup = Popup(title=pTitle,
        content=Label(text=pMessage),
        size_hint=(None, None), size=(400, 400))
    popup.open()

def run():
    """
    Run...
    """
    LabelBase.register(name='AppFont',
       fn_regular = config.FONT,
       fn_bold = config.BOLD_FONT,
       fn_italic = config.ITALIC_FONT)
    expApp().run()
    print('Done')