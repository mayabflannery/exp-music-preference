# App Configuration Settings
VERSION = '0.1'

# Window Mode - DON'T TOUCH!
FULLSCREEN = 'auto'
WINDOWED = 0

# Set Window Mode HERE!
WINDOW_MODE = FULLSCREEN

# Select audio backend (kivy or pygame in lowercase)
AUDIO_BACKEND = 'kivy'

# Options: db, csv
SAVE_DIR = 'resources/results/'
STIMULI_DIR = 'resources/stimuli/'

# These must be STRINGS
TRIALS = '48'
USER_ID = '1'

# Experiment parameters
# Is there a participant survey?
SURVEY = True
SURVEY_FILE = 'd09exp/resources/Survey.csv'

# Is there a personality test?
PERSONALITY = True
PERSONALITY_FILE = 'd09exp/resources/BigFiveQuestions.csv'

# Display in center of the screen when playing stimuli
RATEMEASURE = "Listen carefully to the following selection.\nThen rate your preference."

# The scale extremes, user input will be rounded to one decimal point
# Display above the slider, max/min/text... should make sense
SCALEDESC = "Please rate your preference for the music you just heard."
SCALEMAX = 100
MAXTEXT = "I really like"
SCALEMIN = 0
MINTEXT = "I really dislike"

#---------------------------------------------------------------------
# Theme
#---------------------------------------------------------------------
# Color theme from http://clrs.cc/
NAVY = '#001F3F'
BLUE = '#0074D9'
AQUA = '#7FDBFF'
TEAL = '#39CCCC'
OLIVE = '#3D9970'
GREEN = '#2ECC40'
LIME = '#01FF70'
YELLOW = '#FFDC00'
ORANGE = '#FF851B'
RED = '#FF4136'
MAROON = '#85144B'
PURPLE = '#B10DC9'
GRAY = '#AAAAAA'
SILVER = '#DDDDDD'
WHITE = '#FFFFFF'
BLACK = '#000000'

# Background = wallpaper, foreground = titlebar
BACKGROUND_COLOR = NAVY
FOREGROUND_COLOR = GRAY
FONT_COLOR = WHITE
TITLEBAR_FONT_COLOR = BLACK

#-----------------------------------------------------------------------
# Images
#-----------------------------------------------------------------------
# McMaster Logo that appears on start page
LOGO = 'resources/img/mcmaster_shield.png'
# Title bar icon (top left corner)
ICON = 'resources/img/icon.png'
# Wallpaper
WALLPAPER = 'resources/img/wallM.png'
PLAYB = 'resources/img/play.png'

#-----------------------------------------------------------------------
# Fonts
#-----------------------------------------------------------------------
FONT = 'resources/fonts/Ubuntu-R.ttf'
BOLD_FONT = 'resources/fonts/Ubuntu-B.ttf'
ITALIC_FONT = 'resources/fonts/Ubuntu-RI.ttf'