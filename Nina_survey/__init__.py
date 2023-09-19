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
    age = models.IntegerField(label='How old are you', min=18, max=90)
    
    gender = models.StringField( label='How do you identify?',
        choices=[['Male', 'Male'], ['Female', 'Female'], 
        ['prefer not to answer/ diverse', 'prefer not to answer/ diverse']],
        widget = widgets.RadioSelect
    )
    education = models.StringField( label='What is your highest education?',
        choices=[['no formal education', 'no formal education'],
                 ['obligatory school', 'obligatory school'], 
                 ['secondary school', 'secondary school'],
                 ['higher education (Bachelor, Master, Degree)', 'higher education (Bachelor, Master, Degree)']],
                widget = widgets.RadioSelect
    )

    income = models.StringField( blank=True,
                                label='How high is the monthly income in your household',
        choices=[['< x', '< x'],
                 ['x to x', 'x to x'], 
                 ['x to x', 'x to x'], 
                 ['x to x', 'x to x'], 
                 ['> x', '> x']],
                  widget = widgets.RadioSelect
    )
# consent
    
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)
    
    
# FUNCTIONS
# PAGES

class Introduction(Page):
    form_model = 'player'

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
    Introduction,
    introduction_consent,
    Demographics,
    instructions,
    task_example
]
