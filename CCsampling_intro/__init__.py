from random import random, seed, choice as random_choice, randint
from otree.api import *
import numpy as np
# import scipy.stats as stats



author = 'Zahra Rahmani'
doc = """
Description Experience Gap with Carbon Externalities
"""


# def truncnorm(lower, upper, mean, std):
#     return stats.truncnorm((lower - mean) / std, (upper - mean) / std, loc=mean, scale=std).rvs()

class C(BaseConstants):
    NAME_IN_URL = 'Sampling_Intro'
    PLAYERS_PER_GROUP = None
    ROUNDS_PER_CONDITION = 1
    NUM_ROUNDS = 1
    GAME_ROUNDS = 15

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass



def creating_session(subsession:Subsession):
    import itertools
    box_labels = itertools.cycle([True, True, False, False])
    for player in subsession.get_players():
        if subsession.round_number == 1: 
            player.participant.telling_box_label = next(box_labels)


#PLAYER FUNCTION 
def make_field(label):
        return models.IntegerField(
            choices=[1,2,3,4,5],
            label=label,
            widget=widgets.RadioSelect,
            )


#PLAYER Variables
class Player(BasePlayer):
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)
    mobileDevice= models.BooleanField(initial=False, blank=True)
    prolificIDMissing= models.BooleanField(initial=False)
    range_ccconcern = models.IntegerField( min=-100, max=100)

    ccc1 = make_field('We must protect the climate’s delicate equilibrium.') ## concern 4 items
    ccc2 = make_field('Climate protection is important for our future.')
    ccc3 = make_field('I worry about the climate’s state.')
    ccc4 = make_field('Climate change has severe consequences for humans and nature.')
    ccc10 = make_field('Climate change and its consequences are being exaggerated in the media.')     ### skepticism 6 items 
    ccc11 = make_field('Climate change is a racket.')
    ccc12 = make_field('As long as meteorologists are not even able to accurately forecast weather, climate cannot be reliably predicted either.')
    ccc13 = make_field('There are larger problems than climate protection.')
    ccc14 = make_field('I do not feel threatened by climate change.')
    ccc15 = make_field('The impacts of climate change are unpredictable; thus, my climate-friendly behavior is futile.')
    ccc16 = make_field('Climate protection needlessly impedes economic growth.')
   

# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------



class Consent(Page):
    form_model = 'player'
    form_fields = ['dataScience', 'dataTeach', 'mobileDevice']
    
    @staticmethod
    def vars_for_template(player: Player):
        # while testing this experiment do not check for prolificID (replace False with commented code) (make nolabel and prolificID Missing false for testing)
        player.prolificIDMissing = False # player.participant.label == None
        return {
            "particpantlabel": player.participant.label,
            "nolabel": player.participant.label == False  #None
            }
    
    
class Introduction(Page):
    form_model = 'player'
    

class CCConcern(Page):
    form_model='player'
    form_fields = ['range_ccconcern','ccc1', 'ccc2', 'ccc3', 'ccc4', 'ccc10', 'ccc11', 'ccc12', 'ccc13', 'ccc14', 'ccc15', 'ccc16']
    
page_sequence = [
    Consent, 
    Introduction,
    CCConcern
]
