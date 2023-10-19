from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'demographics'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # demographics
    age = models.IntegerField(label='What is your <b>age</b>', min=18, max=90)
    
    gender = models.StringField( label='How do you identify?',
        choices=[['Male', 'Male'], ['Female', 'Female'], 
        ['Prefer not to answer/ diverse', 'Prefer not to answer/ diverse']],
        widget = widgets.RadioSelect
    )
    education = models.StringField( label='What is your <b>highest education</b>?',
        choices=[['No formal education', 'No formal education'],
                 ['Obligatory school', 'Obligatory school'], 
                 ['Secondary school', 'Secondary school'],
                 ['Higher education (Bachelor, Master, Degree)', 'Higher education (Bachelor, Master, Degree)']],
                widget = widgets.RadioSelect
    )

    income = models.StringField( blank=True,
                                label='How high is your <b>yearly personal income before tax </b>? <br> <i> You may skip this question if you wish to </i>',
        choices=[['< 18.000£', '< 18.000£'],
                 ['18.000£ to 23.000£', '18.000£ to 23.000£'], 
                 ['23.001£ to 30.500£', '23.001£ to 30.500£'], 
                 ['30.501£ to 45.000£', '30.500£ to 45.000£'], 
                 ['> 45.001£', '> 45.001£']],
                  widget = widgets.RadioSelect
    )
# consent
    
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)
    
    
# FUNCTIONS
# PAGES

class introduction_consent(Page):
    form_model = 'player'
    form_fields = ['dataScience', 'dataTeach']

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'income']


class instructions(Page):
    form_model = 'player'

class task_example(Page):
    form_model = 'player'
    

# Page sequence
page_sequence = [
    introduction_consent,
    Demographics,
    instructions,
    task_example
]
