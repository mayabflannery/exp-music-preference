from d09exp.temp import backend
from d09exp.temp import config

def run():
    exp = backend.backend()
    print(exp.survey.get(1))
    print(exp.personality.get(1))

# Run in root folder (cd d09exp/) with "python -m d09exp"