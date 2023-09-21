from otree.api import *
import numpy as np
import random
from random import choice as random_draw
import csv

doc = """
Read quiz quest 
"""


def read_csv():
    f = open(__name__ + '/stimuliU.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    print("new print with rows")
    return rows


class C(BaseConstants):
    NAME_IN_URL = 'riskychoice'
    PLAYERS_PER_GROUP = None
    QUESTIONS_U = read_csv()
    NUM_ROUNDS = len(QUESTIONS_U)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            shuffledOrderU = np.arange(len(C.QUESTIONS_U)) 
            random.shuffle(shuffledOrderU)
            player.participant.shuffledOrderU = shuffledOrderU   
        current_question = C.QUESTIONS_U[player.participant.shuffledOrderU[subsession.round_number-1]]
        player.moneyA1 = int(current_question['moA1'])
        player.moneyA2 = int(current_question['moA2'])
        player.carbonA1 = int(current_question['coA1'])
        player.carbonA2 = int(current_question['coA2'])
        player.probA1 = 100* float(current_question['pA1'])
        player.probA2 = 100 -  (100* float(current_question['pA1']))
        
        player.moneyB1 = int(current_question['moB1'])
        player.moneyB2 = int(current_question['moB2'])
        player.carbonB1 = int(current_question['coB1'])
        player.carbonB2 = int(current_question['coB2'])
        player.probB1 =   100* float(current_question['pB1'])
        player.probB2 = 100 - (100* float(current_question['pB1']))
        
        player.stimulusID = int(current_question['sid'])
        player.OptionARight = random_draw([0, 1])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    moneyA1 = models.IntegerField()
    moneyA2 = models.IntegerField()
    moneyB1 = models.IntegerField()
    moneyB2 = models.IntegerField()
    carbonA1 = models.IntegerField()
    carbonA2 = models.IntegerField()
    carbonB1 = models.IntegerField()
    carbonB2 = models.IntegerField()
    probA1 = models.FloatField() 
    probA2 = models.FloatField()
    probB1 = models.FloatField()
    probB2 = models.FloatField()
    choice = models.StringField()
    input_keyboard = models.IntegerField()
    timedout = models.BooleanField(default=False)
    page_load = models.StringField(initial = 'a')
    page_submit = models.StringField(null=True, initial = "a")
    responsetime = models.IntegerField()
    stimulusID = models.IntegerField()
    OptionARight = models.IntegerField()
    carbonLeft = models.BooleanField()
    outcomeOneTop = models.BooleanField()
    @property
    def response_time(player):
        if player.page_submit != None:
            return int(player.page_submit) - int(player.page_load)
        
        

       
class choiceTask(Page):
    form_model = 'player'
    form_fields = ["choice","input_keyboard", "page_load", "page_submit"]
    @staticmethod
    def vars_for_template(player: Player):
        player.carbonLeft = player.participant.carbonLeft
        player.outcomeOneTop = player.participant.outcomeOneTop
        return {
            'reverse': player.OptionARight,
            'carbonLeft': player.participant.carbonLeft,
            'outcomeOneTop': player.participant.outcomeOneTop,
            'game_round': player.round_number
        }
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.responsetime = player.response_time



class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_players=player.in_all_rounds())


page_sequence = [choiceTask]
