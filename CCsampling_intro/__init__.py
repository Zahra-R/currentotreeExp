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
class Player(BasePlayer):
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)
    mobileDevice= models.BooleanField(initial=False, blank=True)
    prolificIDMissing= models.BooleanField(initial=False)
    range_ccconcern = models.IntegerField( min=-100, max=100)
   



        



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
    


class beforeTask(Page):
    form_model='player'
    form_fields = ['range_ccconcern']


page_sequence = [
    Consent, 
    Introduction,
    beforeTask
]
