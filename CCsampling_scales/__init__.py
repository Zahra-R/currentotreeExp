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
    hh_income = models.IntegerField(choices=[[1,'up to £18k'], [2,'between £18k and £24k'],[3,'between £24k and £35k'], [4,'more than £35k'], [5, "prefer not to say"]])
    conservative_liberal = models.IntegerField( widget=widgets.RadioSelect, choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4,5])
   
    ind1 = make_field('The government interferes far too much in our everyday lives.')
    ind2 = make_field('I feel that people who are successful in business have a right to enjoy their wealth as they see fit.')
    ind3 = make_field('Too many people expect society to do things for them that they should be doing for themselves.')
    hie1 = make_field('Our society would be better off if the distribution of wealth was more equal.')
    hie2 = make_field('A lot of problems in our society come from the decline in the traditional family, where the man works and the woman stays home.')
    hie3 = make_field('Discrimination against minorities is still a very serious problem in our country.')
    faithful = models.IntegerField(choices=[[1,'yes'], [0,'no']], label="Is there any reason why we should NOT use your data?")
    use_data = models.StringField(max_length=1000, blank=True, label="If we should NOT use your data, please specify why:")
    generalFeedback = models.StringField(max_length=3000, blank=True, label="Do you have any other comments or feedback on the study?")

    click_debunk = models.BooleanField()
    click_mechanism = models.BooleanField()
    click_ipcc = models.BooleanField()
    click_consequences = models.BooleanField()
  # FUNCTIONS


        



# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------



class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'hh_income', "conservative_liberal"]

    
      
class Pol_Att(Page):
    form_model = 'player'
    form_fields= ['ind1', 'ind2', 'ind3', 'hie1','hie2', 'hie3'  ]
    
""" class Conservative(Page):
    form_model = 'player'
    form_fields= [ "conservative_econ", "conservative_social" ] """

    




    

class Conclude2(Page):
    form_model = 'player'
    form_fields = ['click_consequences', 'click_debunk', 'click_ipcc', 'click_mechanism']
    @staticmethod
    def vars_for_template(player: Player):
        import string
        seenM = player.participant.seenMisinfo
        seenMlI = player.participant.seenMislInfo
        misinfofile = open('CCsampling/ClimateMisinfo.json')
        infofile = open('CCsampling/ClimateInfo.json')
        misinfo = json.load(misinfofile)['CCMisinfo']
        info = json.load(infofile)['CCInfo']
        seenMstatements = []
        seenMcorrections = []
        for x in seenM:
            #string.replace(old, new, count)
            statementstring = misinfo[x]['finalStatement']
            statementstring =statementstring.replace("'", "´")
            seenMstatements.append(statementstring)
            correctedstring = misinfo[x]['correctedStatement']
            correctedstring = correctedstring.replace("'", "´")
            seenMcorrections.append(correctedstring)
        for x in seenMlI: 
            statementstring = info[x]['finalStatement']
            statementstring =statementstring.replace("'", "´")
            seenMstatements.append(statementstring)
            correctedstring = info[x]['correctedStatement']
            correctedstring = correctedstring.replace("'", "´")
            seenMcorrections.append(correctedstring)
            
        return {
            'seenM': seenM,
            'seenMlI': seenMlI,
            'seenMstatements': seenMstatements,
            'seenMcorrections': seenMcorrections
        }

    

class End(Page):
    form_model = 'player'
    form_fields = ["faithful", "use_data", "generalFeedback"]







page_sequence = [
    Demographics,
    Pol_Att,
    End,
    Conclude2
]
