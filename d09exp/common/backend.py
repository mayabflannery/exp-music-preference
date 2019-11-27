"""
    ...
"""
from d09exp.common import config
from pathlib import Path
import csv
import os

class Backend:
    """
    Handle experiment...
    """
    
    def __init__(self):
        self.user_id = None

        if config.SURVEY:
            self.load_survey(config.SURVEY_FILE)

        print('Backend initialized')

    def load_survey(self, survey_path):
        """
        Get survey from csv file
        """
        QFileName = Path(survey_path)
        with open(QFileName, 'r') as csvfile:
            self.survey = csv.reader(csvfile)
            #for row in self.survey:
            #    print(row[1])
            self.survey_loaded = True
            self.survey_complete = False
            self.q_id = 0
            print('Loaded Survey')

    def get_survey_row(self, question_list, question_id):
        if question_id == 0:
            print ("First question")
            return "Ready to begin"
        print('Presenting question id: ', question_id)
        print(question_list[question_id])
    
    def inc_question(self, question_id):
        self.q_id += 1


    # def load_personality(self, personality_path):
    #     """
    #     Get big 5 questions from csv file
    #     """
    #     QFileName = Path(personality_path)
    #     with open(QFileName, 'r') as csvfile:
    #         self.personality = csv.reader(csvfile)
    #         for row in self.personality:
    #             print(row[1])

