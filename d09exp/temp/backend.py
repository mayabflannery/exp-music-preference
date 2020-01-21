from d09exp.temp import config
from pathlib import Path
import csv
import os
import pandas
import datetime
import random

class Backend:
    '''Setup study, hold data, load/save files'''
    def __init__(self):
        """Initialize backend:
        Load survey, personality test, stimuli"""

        # Open a file for program output
        self.log = open("log.txt","w+")
        print ('Initializing backend...', file=self.log)
        
        # Load participant data
        self.participant = Response()

        # Load survey questionnaire
        if config.SURVEY_PATH:
            self.survey = questions(config.SURVEY_PATH, self.log)

        # Load Big Five personality
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
    """"""
    def __init__(self, csv_path, l):
        """"""
        self.get_path = Path(csv_path)
        print ("Getting questions from: ", str(self.get_path), file=l)
        with open(self.get_path, 'r') as csvfile:
            self.questions = list(csv.reader(csvfile))
            self.loaded = True
            self.complete = False
            self.q_id = 1
            self.total = len(self.questions)
        #...more
        print ('Found', self.total, 'questions', file=l)
        print ('...done question init', file=l)

    def get(self, number):
        """Returns a question at number"""
        q = str(number) + ". " + str(self.questions[number][1])
        return q

    def get_ops(self, number):
        """Get option list: choices related to question"""
        return self.questions[number][2:]

    def get_nextq(self):
        """Returns the next question and answer options in the list, indicates when complete"""
        if self.loaded == True:
            if self.q_id >= self.total:
                self.complete = True
            if self.complete == False:
                self.nextq = self.get(self.q_id)
                self.nextop = self.get_ops(self.q_id)
                self.q_id += 1
            else:
                self.nextq = "Complete"
                self.q_id = 999
        else:
            self.nextq = "Error: Questions failed to load"
        return [self.nextq, self.nextop]

class stimuli:
    """Handle the musical stimuli for study"""
    def __init__(self, folder_path, l):
        """Create a list of stimuli from files in folder"""
        self.get_path = Path(folder_path)
        print ('Getting stimuli from: ', self.get_path, file=l)
        self.in_dir = os.listdir(self.get_path)

        self.stimulus = []

        print ('...Found ', len(self.in_dir), ' files:', file=l)
        for i, files in enumerate(self.in_dir):
            temp_stimulus = files
            temp_stimulus = files.strip('.wav')
            temp_stimulus = temp_stimulus.split('_')
            
            # Small check for naming convention, then add stimulus
            if len(temp_stimulus) == 5:
                self.stimulus.append({'Name': files, 'Piece': temp_stimulus[0], 'Mode': temp_stimulus[1],
                'Tempo': temp_stimulus[2], 'Register': temp_stimulus[3], 'Dynamics': temp_stimulus[4]})
            else:
                print ('WARNING: ', i, ' Invalid file will not be used:', files, file=l)

        self.trials = len(self.stimulus)
        print ('There are: ', self.trials, ' valid stimuli:', file=l)
        for pt in range(0, self.trials):
            st = self.stimulus[pt]
            print ('\t', pt, '  ', st, file=l)

        # Read file name to get factors
        print ('...There are ', len(self.stimulus[0]), " factors:", file=l)
        for i, factors in enumerate(self.stimulus[0]):
            print ('  Factor ', i, " ", factors, file=l)

        # Generate a random presentation order
        self.pres_list = random.sample(range(self.trials), self.trials)
        self.s_id = 0
        print ('Randomized presentation list', self.pres_list, file=l)
        print ('...done stimuli', file=l)

    def get_nextS(self):
        '''Return the next trial from the randomized presentation list'''
        if self.s_id < self.trials:
            next_stimulus = self.stimulus[self.pres_list[self.s_id]]
            print ('Next stimulus: ', next_stimulus, '\tid:', self.s_id, '\trandom: ', self.pres_list[self.s_id])
            self.s_id += 1
        else:
            next_stimulus = "Complete"
            print ('Stimuli complete')
        return next_stimulus
    

class Response:
    """Handle response data particular to participant"""
    def __init__(self):
        """Create a unique identifier for study, open study data file"""
        self.uid = datetime.datetime.now()
        print (self.uid)

        self.responseData = pandas.read_csv('d09exp/resources/dataAll.csv')
        print(self.responseData)
    
    def set_current(self, number):
        """Set participant number, confirmed in mainscreen"""
        self.current = number
        self.new_file = str(self.uid.strftime('%Y_%m_%d_%H_%M_%S_%f_P_')) + str(self.current) + ".csv"
        self.new_row = {'uid':self.uid, 'Participant': self.current}

    def get_current(self):
        """Return the next participant in the study"""
        #print("The last participant is: ", self.responseData.iloc[-1, 1])
        return int(self.responseData.iloc[-1, 0]) + 1

    def hold(self, name, value):
        """Hold the response values in a new row, not applied to data yet..."""
        self.new_row[name] = value

    def saveData(self):
        """Create a new .csv file with data"""
        # Create an individual participant record
        tdf = pandas.DataFrame.from_dict(self.new_row, orient = 'index')
        tdf.to_csv(self.new_file)
        # update data file
        self.responseData.to_csv('d09exp/resources/dataAll.csv', na_rep = "NoRs", index = False)
    
    def __del__(self):
        """Add participant responses to the entire dataset and create save it before closing"""
        self.responseData = self.responseData.append(self.new_row, ignore_index = True)
        self.saveData()