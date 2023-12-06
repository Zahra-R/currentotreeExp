import random

from otree.api import *
import numpy as np
import json


author = 'Zahra Rahmani'
doc = """
Sampling Paradigma
"""

class C(BaseConstants):
    NAME_IN_URL = 'SAMPLING'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 15
    misinfofile = open('CCsampling/ClimateMisinfo.json')
    infofile = open('CCsampling/ClimateInfo.json')
    misinfo = json.load(misinfofile)['CCMisinfo']
    info = json.load(infofile)['CCInfo']


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    boxChoice = models.StringField( choices = ['i', 'm'])
    range_agree = models.IntegerField( min=-100, max=100)
    # range_likelyTrue = models.IntegerField( min=-100, max=100)
    range_ccconcern = models.IntegerField( min=-100, max=100)
    statementText =models.StringField()
    statementID = models.StringField()
    boxlikingInfo = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9],label='How much do you like Box<b> A</b>?', widget = widgets.RadioSelect )
    boxrecommendationInfo = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9],label='Would you follow Box A if it were its own social media channel?',widget = widgets.RadioSelect )
    boxlikingMisinfo = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9],label='How much do you like Box B?' , widget = widgets.RadioSelect)
    boxrecommendationMisinfo = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9],label='Would you follow Box B if it were its own social media channel?',widget = widgets.RadioSelect )
    boxpoliticsMisinfo = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9], widget = widgets.RadioSelect)
    boxpoliticsInfo = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9], widget = widgets.RadioSelect )
    boxtrustInfo = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9], widget = widgets.RadioSelect )
    boxtrustMisinfo = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9], widget = widgets.RadioSelect )
    InfohasDebrief = models.BooleanField()
   
    reverseBoxes = models.BooleanField()
    tellingBoxLabels = models.BooleanField()

    click_debunk = models.BooleanField()
    click_mechanism = models.BooleanField()
    click_ipcc = models.BooleanField()
    click_consequences = models.BooleanField()
   


def creating_session(subsession:Subsession):
    import itertools
    reverse_display = itertools.cycle([True, False])
    for player in subsession.get_players():
        if subsession.round_number == 1: 
            player.participant.randomInfoArray = random.sample(range(1,147),C.NUM_ROUNDS)
            player.participant.randomMisinfoArray = random.sample(range(1,79),C.NUM_ROUNDS)
            player.participant.reverseBoxes = next(reverse_display)
            player.participant.seenMisinfo = []
            player.participant.seenMislInfo = []





#----------------------------------------------------------------
#------------------Custum Functions------------------------------------
#----------------------------------------------------------------

def allocateBoxNames(player: Player):
    reversed = player.participant.reverseBoxes
    # if player.round_number % C.ROUNDS_PER_CONDITION == 0:
    likingA = player.boxlikingInfo
    likingB = player.boxlikingMisinfo
    recomA = player.boxrecommendationInfo
    recomB = player.boxrecommendationMisinfo
    if reversed == True:
        player.boxlikingInfo = likingB
        player.boxlikingMisinfo = likingA
        player.boxrecommendationInfo = recomB
        player.boxrecommendationMisinfo = recomA
    print('in make choice again')


def saveParticipantVarsToPlayer(player: Player): 
    player.reverseBoxes = player.participant.reverseBoxes
    player.tellingBoxLabels = player.participant.telling_box_label


# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------

class sampling(Page):
    form_model = 'player'
    form_fields = ['boxChoice','statementText', 'statementID', 'range_ccconcern', 'range_agree']
    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        misinfofile = open('CCsampling/ClimateMisinfo.json')
        infofile = open('CCsampling/ClimateInfo.json')
        misinfo = json.load(misinfofile)['CCMisinfo']
        info = json.load(infofile)['CCInfo']
        MisinfoText = C.misinfo[player.participant.randomMisinfoArray[round_number-1]]['finalStatement']
        InfoText = C.info[player.participant.randomInfoArray[round_number-1]]['finalStatement']
        player.InfohasDebrief = True if "correctedStatement" in C.info[player.participant.randomInfoArray[round_number-1]] else False
        print("hello mislieading info", C.info[player.participant.randomInfoArray[round_number-1]])
        # these are tweetids, we are not submitting them. We only submit the index of the statement in the json file (internal statementID)
        #MisinfoID = misinfo[player.participant.randomMisinfoArray[round_number-1]]['tweetid']
        #InfoID = info[player.participant.randomInfoArray[round_number-1]]['tweetid']
        return {
            'round_number': round_number,
            'randomInfo': player.participant.randomInfoArray[round_number-1],
            'randomMisinfo': player.participant.randomMisinfoArray[round_number-1],
            'reverseBoxes': player.participant.reverseBoxes,
            'MisinfoText': MisinfoText,
            'InfoText': InfoText, 
            'tellingBoxNames': player.participant.telling_box_label
        }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if(player.boxChoice == "m"):
            player.participant.seenMisinfo.append(player.participant.randomMisinfoArray[player.round_number-1])
        else:
            if(player.InfohasDebrief == True ):
               player.participant.seenMislInfo.append(player.participant.randomInfoArray[player.round_number-1]) 




class boxrating(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        if player.round_number == C.NUM_ROUNDS:
            return ['boxlikingInfo', 'boxrecommendationInfo', 'boxlikingMisinfo', 'boxrecommendationMisinfo', 'boxpoliticsInfo', 'boxpoliticsMisinfo', 'boxtrustInfo', 'boxtrustMisinfo' ]
        else:
            return ['boxlikingInfo', 'boxrecommendationInfo', 'boxlikingMisinfo', 'boxrecommendationMisinfo' ]
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'round_number': player.round_number,
        }
    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number % 5 == 0)
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        print('in before next page function', player.boxlikingInfo, player.boxlikingMisinfo, player.boxrecommendationInfo, player.boxrecommendationMisinfo )
        allocateBoxNames(player)
        if (player.round_number % C.NUM_ROUNDS == 0):
            saveParticipantVarsToPlayer(player)


page_sequence = [
    #betweenGames,
    sampling, boxrating
]