from d09exp.temp import config
from pathlib import Path
import csv
import os

class backend:
    def __init__(self):
        """Initialize backend:
        Load survey, personality test, stimuli"""
        self.log = open("log.txt","w+")
        print ('Initializing backend...', file=self.log)
        self.participant = 0
        
        # Load questionnaires if they exist
        if config.SURVEY_PATH:
            self.survey = questions(config.SURVEY_PATH, self.log)
        if config.PERSONALITY_PATH:
            self.personality = questions(config.PERSONALITY_PATH, self.log)

        # Load stimuli
        if config.STIMULI_PATH:
            self.music = stimuli(config.STIMULI_PATH, self.log)

        print ('...done backend init', file=self.log)
    
    def __del__(self):
        print ('Backend deleted', file=self.log)
        self.log.close()

class questions:
    def __init__(self, csv_path, l):
        self.get_path = Path(csv_path)
        print ("Getting questions from: ", str(self.get_path), file=l)
        with open(self.get_path, 'r') as csvfile:
            self.questions = list(csv.reader(csvfile))
            self.loaded = True
            self.complete = False
            self.q_id = 0
        #...more
        print ('...done question init', file=l)

    def get(self, number):
        """Returns a question at number"""
        return self.questions[number][1]

    def get_nextq(self):
        """Returns the next question in the list, indicates when complete"""
        if self.loaded == True:
            if self.complete == False:
                nextq = self.get(self.q_id)
                self.q_id += 1
            else:
                nextq = "Participant survey complete"
                self.q_id = 999
        else:
            nextq = "Error: Questions failed to load"
        return nextq

class stimuli:
    def __init__(self, folder_path, l):
        self.get_path = Path(folder_path)
        print ('Getting stimuli from: ', self.get_path, file=l)
        self.in_dir = os.listdir(self.get_path)
        self.trials = len(self.in_dir)

        self.stimulus = list()
        self.all_stim = list()

        print ('...Found ', self.trials, ' files:', file=l)
        for i, files in enumerate(self.in_dir):
            self.stimulus = files.strip('.mp3')
            self.stimulus = self.stimulus.split('_')
            self.all_stim.insert(i, self.stimulus)
            
            print ('  ', files, '\t', self.all_stim[i], file=l)
        
        # Read file name to get factors
        print ('...There are ', len(self.all_stim[0]), " factors:", file=l)
        for i, factors in enumerate(self.all_stim[0]):
            print ('  Factor ', i, " ", factors, file=l)

        print ('...done stimuli', file=l)