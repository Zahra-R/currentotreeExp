from otree.api import *
import numpy as np
import random
from random import choice as random_draw
import csv

doc = """
Read quiz quest 
"""


def read_csv():
    f = open(__name__ + '/stimuliC.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    return rows


class C(BaseConstants):
    NAME_IN_URL = 'safechoice'
    PLAYERS_PER_GROUP = None
    QUESTIONS_C = read_csv()
    NUM_ROUNDS =  len(QUESTIONS_C)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            shuffledOrderC = np.arange(len(C.QUESTIONS_C)) 
            random.shuffle(shuffledOrderC)
            player.participant.shuffledOrderC = shuffledOrderC 
        current_question = C.QUESTIONS_C[player.participant.shuffledOrderC[subsession.round_number-1]]
        player.moneyA =  int(current_question['moA'])
        player.moneyB = int(current_question['moB'])
        player.carbonA = int(current_question['coA'])
        player.carbonB = int(current_question['coB'])
        player.stimulusID = int(current_question['sid'])
        player.OptionARight = random_draw([0, 1])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    moneyA = models.IntegerField()
    moneyB = models.IntegerField()
    carbonA = models.IntegerField()
    carbonB = models.IntegerField()
    choice = models.StringField()
    input_keyboard = models.IntegerField()
    timedout = models.BooleanField(default=False)
    page_load = models.StringField(initial = '0', default = '0')
    page_submit = models.StringField(null=True)
    responsetime = models.IntegerField()
    stimulusID = models.IntegerField()
    OptionARight = models.IntegerField()
    newResponseTime = models.FloatField()
    carbonLeft = models.BooleanField()
    # @property
    # def response_time(player):
    #     if player.page_submit != None:
    #         return player.page_submit - player.page_load
        
        
class choiceTask(Page):
    form_model = 'player'
    form_fields = ["choice","input_keyboard", "page_load", "page_submit", "newResponseTime"]
    @staticmethod
    def vars_for_template(player: Player):
        player.carbonLeft = player.participant.carbonLeft
        return {
            'reverse': player.OptionARight,
            'carbonLeft': player.participant.carbonLeft,
            'game_round': player.round_number
        }
    @staticmethod
    def before_next_page(player, timeout_happened):
        print("made it till here")
        if player.page_submit != None:
            player.responsetime = int(player.page_submit) - int(player.page_load)

class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_players=player.in_all_rounds())


page_sequence = [choiceTask]
