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
    NAME_IN_URL = 'EDEG'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 4
    ROUNDS_PER_BLOCK = NUM_ROUNDS/2
    STARTING_PAYMENT = 1
    PAYRATIO = 200
    MINIMUM_PAYMENT = 0
    MAXIMUM_PAYMENT = 1.10
    safe_outcome = 7
    high_lottery = 30 # typical outcome of the lottery
    low_lottery = -200 # rare disaster 
    carbon = 30
    show_feedback = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

#PLAYER FUNCTION 

class Player(BasePlayer):
    choice = models.StringField( choices=[ 'A', 'B'])  # , widget=widgets.RadioSelect)
    outcomeA = models.FloatField()
    outcomeB = models.FloatField()
    carbonA = models.IntegerField()
    carbonB = models.IntegerField()
    round_carbon = models.FloatField()
    round_outcome = models.FloatField()  # This is the outcome of the selected button in each round
    riskyLeft = models.BooleanField()
    riskyCarbon = models.BooleanField()
    salient = models.BooleanField()
    block = models.IntegerField()
    switchPayoff = models.BooleanField()
    condition = models.IntegerField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            player.participant.game_rounds = C.NUM_ROUNDS


def output_outcome(player: Player):
    #tax = player.tax
    outcomeA = C.safe_outcome
    rnd = random()
    if rnd < 0.90:
        outcomeB = C.high_lottery
    else:
        outcomeB = C.low_lottery
    return outcomeA, outcomeB


### Internally (in database) A is always safe and B is always risky
## In reverse Condition A is the risky option and B is the safe option, therefore, we recode this here in the function
## Condition 1 first block: safe is carbon neutral, risky is carbon negative; second block: safe is carbon negative, risky is carbon neutral
## Condition 2: block order is reversed
def make_choice(player: Player, choiceMade):
    reversedbuttons = player.riskyLeft
    # if player.round_number % C.ROUNDS_PER_CONDITION == 0:
    player.choice = choiceMade
    player.outcomeA, player.outcomeB = output_outcome(player)
    if reversedbuttons == True:
        if choiceMade == 'A':
            player.choice = 'B'
        elif choiceMade == 'B':
            player.choice = 'A'
    if player.choice == "A":
        player.round_outcome = player.outcomeA
        player.round_carbon = player.carbonA
    if player.choice == "B":
        player.round_outcome = player.outcomeB
        player.round_carbon = player.carbonB

def determine_outcome(player:Player, chosen_round):
            player.participant.chosen_round_outcome = player.in_round(chosen_round).round_outcome
            player.participant.chosen_round_choice = player.in_round(chosen_round).choice
            #player.payoff = player.chosen_round_outcome / C.PAYRATIO
            player.participant.payoff_decimal = 1 + player.participant.chosen_round_outcome/ C.PAYRATIO 
            participant = player.participant
            participant.chosen_round = chosen_round


# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------

class Main(Page):
    form_model = 'player'
    form_fields = ['choice']
    @staticmethod
    def vars_for_template(player: Player):
        Salience = player.participant.Salience
        player.salient = Salience
        Exp_Con = player.participant.Exp_Con
        SwitchPayoffs = player.participant.SwitchPayoffs
        block = 1 if  player.round_number <= C.ROUNDS_PER_BLOCK else 2
        if block == 1: 
            reversedbuttons = player.participant.reversedbuttons
        else: 
            reversedbuttons = player.participant.reversedbuttons ^ SwitchPayoffs
        player.riskyLeft = reversedbuttons
        print("HElllllllo my friend here comes switched payoffs", SwitchPayoffs, reversedbuttons )
        carbonA = ((Exp_Con + block) % 2) * C.carbon
        player.carbonA = carbonA
        carbonB = ((1+ Exp_Con + block) % 2) * C.carbon
        player.carbonB = carbonB
        player.riskyCarbon = carbonB>0 # if reversedbuttons == True else carbonB>0
        carbonMiles = C.carbon * 20.2/11
        game_round = player.round_number
        player.block = block
        player.condition = Exp_Con
        player.switchPayoff = SwitchPayoffs
        return {
                'game_round': game_round,
                'reversedSides': reversedbuttons,
                'carbonB': carbonB,
                'carbonA': carbonA,
                'carbonMiles': carbonMiles, 
                'Salience' : Salience
            }
   

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        make_choice(player, player.choice)

class Feedback(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return 1 #(player.round_number >= C.show_feedback and player.participant.reversedbuttons== False)

    @staticmethod
    def vars_for_template(player: Player):
            Salience = player.participant.Salience
            Exp_Con = player.participant.Exp_Con
            reversedbuttons = player.riskyLeft
            #SwitchPayoffs = player.participant.SwitchPayoffs
            block = 1 if  player.round_number <= C.ROUNDS_PER_BLOCK else 2
            carbonA = ((Exp_Con + block) % 2) * C.carbon
            carbonB = ((1+ Exp_Con + block) % 2) * C.carbon
            previous_choice = player.choice
            previous_outcome = player.round_outcome
            if reversedbuttons == True:
                if previous_choice == "A":
                    previous_choice = "B"
                elif previous_choice == "B":
                    previous_choice = "A"
                previous_outcomeA = player.outcomeB
                previous_outcomeB = player.outcomeA
                temp = carbonA
                carbonA = carbonB
                carbonB = temp
            else:
                previous_outcomeA = player.outcomeA
                previous_outcomeB = player.outcomeB
            return {
                'previous_choice': previous_choice,
                'previous_outcome': previous_outcome,
                #'game': game,
                'previous_outcomeA': previous_outcomeA,
                'previous_outcomeB': previous_outcomeB,
                'Salience': Salience,
                'game_round': player.round_number,
                'lastRB': reversedbuttons,
                'carbonB' : carbonB, 
                'carbonA' : carbonA
            }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if (player.round_number == C.NUM_ROUNDS):
            chosen_round = randint(1,C.NUM_ROUNDS)
            determine_outcome(player,chosen_round)
            print('the chosen round is', chosen_round)
  
class betweenGames(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number == C.ROUNDS_PER_BLOCK
        )


page_sequence = [
    Main,
    Feedback,
    betweenGames,
]
