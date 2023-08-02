from random import random, seed, choice as random_choice, randint
from otree.api import *
import numpy as np
import json
# import scipy.stats as stats



author = 'Zahra Rahmani'
doc = """
Description Experience Gap with Carbon Externalities
"""


# def truncnorm(lower, upper, mean, std):
#     return stats.truncnorm((lower - mean) / std, (upper - mean) / std, loc=mean, scale=std).rvs()

class C(BaseConstants):
    NAME_IN_URL = 'Scales'
    PLAYERS_PER_GROUP = None
    ROUNDS_PER_CONDITION = 1
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

#PLAYER FUNCTION 
def make_field(label):
        return models.IntegerField(
            choices=[1,2,3,4,5],
            label=label,
            widget=widgets.RadioSelect,
            )


class Player(BasePlayer):
    gender = models.IntegerField(choices=[[1,'Male'], [2,'Female'],[3,'Diverse'], [4,'Other']])
    age = models.IntegerField(min=18, max=100, max_length=2)
    hh_income = models.IntegerField(choices=[[1,'up to 30k'], [2,'between 30k and 50k'],[3,'between 50k and 80k'], [4,'more than 80k'], [5, "prefer not to say"]])
    hh_party = models.IntegerField(choices=[[1, "Democratic Party"], [2, "Republican Party"], [3, "Other"]])
    hh_party_other = models.StringField(max_length=150, blank=True, label="Please specify")
    conservative_liberal = models.IntegerField( widget=widgets.RadioSelect, choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4,5])
    ccc1 = make_field('We must protect the climate’s delicate equilibrium.') ## concern 4 items
    ccc2 = make_field('Climate protection is important for our future.')
    ccc3 = make_field('I worry about the climate’s state.')
    ccc4 = make_field('Climate change has severe consequences for humans and nature.')
    att_ccc = make_field('In this row, please mark the third circle (center circle) to indicate you are paying attention.')
    ccc10 = make_field('Climate change and its consequences are being exaggerated in the media.')     ### skepticism 6 items 
    ccc11 = make_field('Climate change is a racket.')
    ccc12 = make_field('As long as meteorologists are not even able to accurately forecast weather, climate cannot be reliably predicted either.')
    ccc13 = make_field('There are larger problems than climate protection.')
    ccc14 = make_field('I do not feel threatened by climate change.')
    ccc15 = make_field('The impacts of climate change are unpredictable; thus, my climate-friendly behavior is futile.')
    ccc16 = make_field('Climate protection needlessly impedes economic growth.')
    ind1 = make_field('The government interferes far too much in our everyday lives.')
    ind2 = make_field('I feel that people who are successful in business have a right to enjoy their wealth as they see fit.')
    ind3 = make_field('Too many people expect society to do things for them that they should be doing for themselves.')
    hie1 = make_field('Our society would be better off if the distribution of wealth was more equal.')
    hie2 = make_field('A lot of problems in our society come from the decline in the traditional family, where the man works and the woman stays home.')
    hie3 = make_field('Discrimination against minorities is still a very serious problem in our country.')
    faithful = models.IntegerField(choices=[[1,'yes'], [0,'no']], label="Is there any reason why we should NOT use your data?")
    use_data = models.StringField(max_length=1000, blank=True, label="If we should NOT use your data, please specify why:")
    generalFeedback = models.StringField(max_length=3000, blank=True, label="Do you have any other comments or feedback on the study?")
  # FUNCTIONS


def creating_session(subsession: Subsession):
    print('creating subsession scales')
        



# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------



class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'hh_income', "hh_party", "hh_party_other"]

    
class CCConcern(Page):
    form_model = 'player'
    form_fields= ['ccc1', 'ccc2', 'ccc3', 'ccc4', 'att_ccc', 'ccc10', 'ccc11', 'ccc12', 'ccc13', 'ccc14', 'ccc15', 'ccc16'  ]

      
class Pol_Att(Page):
    form_model = 'player'
    form_fields= ['ind1', 'ind2', 'ind3', 'hie1','hie2', 'hie3' , "conservative_liberal" ]
    
""" class Conservative(Page):
    form_model = 'player'
    form_fields= [ "conservative_econ", "conservative_social" ] """

    
class End(Page):
    form_model = 'player'
    form_fields = [   "faithful", "use_data", "generalFeedback"]


class Conclude(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        return {
             'seenM': player.participant.seenMisinfo
        }
    

class Conclude2(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        import string
        seenM = player.participant.seenMisinfo
        misinfofile = open('CCsampling/ClimateMisinfo.json')
        #infofile = open('sampling/ClimateInfo.json')
        misinfo = json.load(misinfofile)['CCMisinfo']
        #info = json.load(infofile)['CCInfo']
        seenMstatements = []
        seenMcorrections = []
        for x in seenM:
            #string.replace(old, new, count)
            statementstring = misinfo[x]['finalStatement']
            statementstring =statementstring.replace("'", "")
            print("##############################################")
            print(statementstring)
            seenMstatements.append(statementstring)
            seenMcorrections.append(misinfo[x]['correctedStatement'])
        return {
            'seenM': seenM,
            'seenMstatements': seenMstatements,
            'seenMcorrections': seenMcorrections
        }

    
        







page_sequence = [
   # Demographics,
   # CCConcern,
   # Pol_Att,
    End,
    Conclude2
]
