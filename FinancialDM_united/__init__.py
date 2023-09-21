from otree.api import *
import numpy as np
import random
from random import choice as random_draw
import csv

doc = """
Read quiz quest 
"""


def read_csvC():
    f = open(__name__ + '/stimuliC.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    return rows


def read_csvU():
    f = open(__name__ + '/stimuliU.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    print("new print with rows")
    return rows




class C(BaseConstants):
    NAME_IN_URL = 'fdmchoice'
    PLAYERS_PER_GROUP = None
    QUESTIONS_C = read_csvC()
    QUESTIONS_U = read_csvU()
    NUM_ROUNDS = 4
    #NUM_ROUNDS =  len(QUESTIONS_C) + len(QUESTIONS_U)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        player.certainFirst = player.participant.certainFirst
        if subsession.round_number == 1:
            ######### this is for the bonus payoff later on ########
            seqa = range(6,80)
            seqb = range(86,160)
            seq = np.concatenate((seqa, seqb), axis = None)
            # this line needs to be removed
            seq = [1,2,3,4]
            player.drawn_round = random_draw(seq)
            #############################################
            shuffledOrderC = np.arange(len(C.QUESTIONS_C)) 
            random.shuffle(shuffledOrderC)
            player.participant.shuffledOrderC = shuffledOrderC 
            shuffledOrderU = np.arange(len(C.QUESTIONS_U)) 
            random.shuffle(shuffledOrderU)
            player.participant.shuffledOrderU = shuffledOrderU
        if player.participant.certainFirst == False:
            player.mod_round_number = (( subsession.round_number + int(C.NUM_ROUNDS/2) ) % C.NUM_ROUNDS)
            if player.mod_round_number == 0:
                player.mod_round_number = C.NUM_ROUNDS
        else: 
            player.mod_round_number = subsession.round_number
        if player.mod_round_number <= int(C.NUM_ROUNDS/2): 
            current_questionC = C.QUESTIONS_C[player.participant.shuffledOrderC[(subsession.round_number-1) % (int(C.NUM_ROUNDS/2))]]
            player.moneyA =  int(current_questionC['moA'])
            player.moneyB = int(current_questionC['moB'])
            player.carbonA = int(current_questionC['coA'])
            player.carbonB = int(current_questionC['coB'])
            player.stimulusIDC = int(current_questionC['sid'])
            player.OptionARight = random_draw([0, 1])
        else:
            current_questionU = C.QUESTIONS_U[player.participant.shuffledOrderU[(subsession.round_number-1) % (int(C.NUM_ROUNDS/2))]]
            player.moneyA1 = int(current_questionU['moA1'])
            player.moneyA2 = int(current_questionU['moA2'])
            player.carbonA1 = int(current_questionU['coA1'])
            player.carbonA2 = int(current_questionU['coA2'])
            player.probA1 = 100* float(current_questionU['pA1'])
            player.probA2 = 100 -  (100* float(current_questionU['pA1']))
            
            player.moneyB1 = int(current_questionU['moB1'])
            player.moneyB2 = int(current_questionU['moB2'])
            player.carbonB1 = int(current_questionU['coB1'])
            player.carbonB2 = int(current_questionU['coB2'])
            player.probB1 =   100* float(current_questionU['pB1'])
            player.probB2 = 100 - (100* float(current_questionU['pB1']))
            player.OptionAoutcomeOneTop = random_draw([True, False])
            player.OptionBoutcomeOneTop = random_draw([True, False])
            
            player.stimulusIDU = int(current_questionU['sid'])
            player.OptionARight = random_draw([0, 1])




class Group(BaseGroup):
    pass


class Player(BasePlayer):
    mod_round_number = models.IntegerField()

    moneyA = models.IntegerField()
    moneyB = models.IntegerField()
    carbonA = models.IntegerField()
    carbonB = models.IntegerField()
    choice = models.StringField()

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


    input_keyboard = models.IntegerField()
    timedout = models.BooleanField(default=False)
    page_load = models.StringField(initial = '0', default = '0')
    page_submit = models.StringField(null=True)
    responsetime = models.IntegerField()
    stimulusID = models.IntegerField()
    OptionARight = models.IntegerField()
    newResponseTime = models.FloatField()
    carbonLeft = models.BooleanField()
    certainFirst = models.BooleanField()
    OptionAoutcomeOneTop = models.BooleanField()
    OptionBoutcomeOneTop = models.BooleanField()


    drawn_round = models.IntegerField()
    outcome_money = models.FloatField()
    outcome_carbon = models.FloatField()

    # @property
    # def response_time(player):
    #     if player.page_submit != None:
    #         return player.page_submit - player.page_load
        
        
class choiceTaskC(Page):
    form_model = 'player'
    form_fields = ["choice","input_keyboard", "page_load", "page_submit", "newResponseTime"]
    @staticmethod
    def vars_for_template(player: Player):
        print("--------------------------HIiiiiiiii------------")
        print(player.mod_round_number)
        print(player.participant.certainFirst)
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
    @staticmethod
    def is_displayed(player: Player):
        #show = (player.participant.certainFirst & player.round_number <=80) | (not player.participant.certainFirst & player.round_number >80 )
        return player.mod_round_number <= int(C.NUM_ROUNDS/2)


   
class choiceTaskU(Page):
    form_model = 'player'
    form_fields = ["choice","input_keyboard", "page_load", "page_submit"]
    @staticmethod
    def vars_for_template(player: Player):
        print("--------------------------Uuuuuuuuuncertain------------")
        print(player.mod_round_number)
        print(player.participant.certainFirst)
        player.carbonLeft = player.participant.carbonLeft
        return {
            'reverse': player.OptionARight,
            'carbonLeft': player.participant.carbonLeft,
            'AoutcomeOneTop': player.OptionAoutcomeOneTop,
            'BoutcomeOneTop': player.OptionBoutcomeOneTop,
            'game_round': player.round_number
        }
    @staticmethod
    def before_next_page(player, timeout_happened):
        print("made it till here")
        if player.page_submit != None:
            player.responsetime = int(player.page_submit) - int(player.page_load)
    @staticmethod
    def is_displayed(player: Player):
        return player.mod_round_number > int(C.NUM_ROUNDS/2)
    



class betweenGames(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number == int(C.NUM_ROUNDS/2)
        )  

class afterPractice(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number %(int(C.NUM_ROUNDS/2)) == 5
        )





def outcome_certain(player: Player, drawn_round):
    round_choice = player.in_round(drawn_round).choice 
    if round_choice == "A":
        outcome_money = player.in_round(drawn_round).moneyA
        outcome_carbon = player.in_round(drawn_round).carbonA
    else: 
        outcome_money = player.in_round(drawn_round).moneyB
        outcome_carbon = player.in_round(drawn_round).carbonB

    ### recode for participants if what they saw was reversed  
    if player.in_round(drawn_round).OptionARight == 1 :
        if round_choice == "A":
            round_choice = "B"
        else: 
            round_choice = "A"
    return round_choice, outcome_money, outcome_carbon


def outcome_risky(player:Player, drawn_round):
    round_choice = player.in_round(drawn_round).choice 
    if round_choice == "A":
        rnd = random.random()
        if rnd < player.in_round(drawn_round).probA1:
            outcome_money = player.in_round(drawn_round).moneyA1
            outcome_carbon = player.in_round(drawn_round).carbonA1
        else:
            outcome_money = player.in_round(drawn_round).moneyA2
            outcome_carbon = player.in_round(drawn_round).carbonA2

    else: 
        rnd = random.random()
        if rnd < player.in_round(drawn_round).probB1:
            outcome_money = player.in_round(drawn_round).moneyB1
            outcome_carbon = player.in_round(drawn_round).carbonB1
        else:
            outcome_money = player.in_round(drawn_round).moneyB2
            outcome_carbon = player.in_round(drawn_round).carbonB2
    
    ### recode for participants if what they saw was reversed  
    if player.in_round(drawn_round).OptionARight == 1 :
        if round_choice == "A":
            round_choice = "B"
        else: 
            round_choice = "A"
    return round_choice, outcome_money, outcome_carbon



class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        drawn_round = player.in_round(1).drawn_round
        drawn_game= "certain"
        if drawn_round > int(C.NUM_ROUNDS/2) and player.participant.certainFirst == True:
            drawn_game = "risky"
        if drawn_round <= int(C.NUM_ROUNDS/2) and player.participant.certainFirst == False:
            drawn_game = "risky"
        print(drawn_game)
        print(drawn_round)
        print(player.participant.certainFirst)
        print("----------------------------agian--------------")
        if(drawn_game == "risky"):
            relevant_round_choice, player.outcome_money, player.outcome_carbon = outcome_risky(player, drawn_round)
        else:
            relevant_round_choice, player.outcome_money, player.outcome_carbon = outcome_certain(player, drawn_round)
        return{
            'drawn_round': drawn_round,
            'drawn_game': drawn_game,
            'relevant_round_choice': relevant_round_choice,
            'outcome_money': player.outcome_money,
            'outcome_carbon': player.outcome_carbon
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    

page_sequence = [choiceTaskU, choiceTaskC, afterPractice, betweenGames, Results]
