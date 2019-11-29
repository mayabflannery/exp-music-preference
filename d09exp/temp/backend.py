from d09exp.temp import config
from pathlib import Path
import csv
import os

class backend:
    def __init__(self):
        """Initialize backend:
        Load survey, personality test, stimuli"""
        print('Initializing backend...')
        self.participant = 0
        
        # Load questionnaires if they exist
        if config.SURVEY_PATH:
            self.survey = questions(config.SURVEY_PATH)
        if config.PERSONALITY_PATH:
            self.personality = questions(config.PERSONALITY_PATH)

        # Load stimuli
        if config.STIMULI_PATH:
            self.music = stimuli(config.STIMULI_PATH)

        print('...done backend')

class questions:
    def __init__(self, csv_path):
        self.get_path = Path(csv_path)
        print('Getting questions from: ', self.get_path)
        with open(self.get_path, 'r') as csvfile:
            self.questions = list(csv.reader(csvfile))
            self.loaded = True
            self.complete = False
            self.q_id = 0
        #...more
        print('...done questions')

    def get(self, number):
        """Returns a question at number"""
        return self.questions[number][1]

class stimuli:
    def __init__(self, folder_path):
        self.get_path = Path(folder_path)
        print('Getting stimuli from: ', self.get_path)
        self.in_dir = os.listdir(self.get_path)
        print('Found ', len(self.in_dir), ' files:')
        for files in self.in_dir:
            print(files)
        #...more
        print('...done stimuli')