from random import random, seed, choice as random_choice, randint
from otree.api import *
import numpy as np
#import scipy.stats as stats

author = 'Zahra Rahmani'
doc = """
Description Experience Gap with Carbon Externalities
"""

class C(BaseConstants):
    NAME_IN_URL = 'EDEG_Intro'
    PLAYERS_PER_GROUP = None
    ROUNDS_PER_CONDITION = 1
    NUM_ROUNDS = 1
    safe_outcome = 2
    high_lottery = 20 # typical outcome of the lottery
    low_lottery = -200 # rare disaster 
    carbonB = 25
    carbonA = 0


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Exp_Con = models.IntegerField()  # This is a between subjects variable, 1 is first block safe is neutral, 2 is first block safe is carbon negative
    SwitchPayoffs = models.BooleanField()
    Salience = models.BooleanField()
    reversedbuttons = models.BooleanField()
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)
    realEmissions = models.IntegerField(choices=[[1,'True'], [0,'False']], label="Does the decision that will determine your bonus have a real consequence for the environment?")
    attention = models.StringField(max_length=60, blank=True)
    attention2 = models.StringField(max_length=360, blank=True)
    mobileDevice= models.BooleanField(initial=False, blank=True)
    prolificIDMissing= models.BooleanField(initial=False)
    amountEmissionsRisky = models.IntegerField(blank = True, min_length=1)
    amountEmissionsSafe = models.IntegerField(blank = True, min_length=1)
    amountEmissionsRisky2 = models.IntegerField(blank = True, min_length=1)
    amountEmissionsSafe2 = models.IntegerField(blank = True, min_length=1)
    preference = models.StringField( choices=[ 'A', 'B'])  # , widget=widgets.RadioSelect)
    
    
    
# FUNCTIONS

def creating_session(subsession: Subsession):
    import itertools
    conditions = itertools.cycle([1, 2])
    reverse_display = itertools.cycle([True, False, False, True])
    salientEmissions = itertools.cycle([True, True, False, False])
    blockswitchPayoffs = itertools.cycle([True, True, True, True, False, False, False, False])
    # randomize to treatments
    for player in subsession.get_players():
        if subsession.round_number == 1:
            if 'Exp_Con' in player.session.config:
                player.Exp_Con = player.session.config['Exp_Con']
            else:
                player.Exp_Con = next(conditions)
            if 'Salience' in player.session.config:
                player.Salience = player.session.config['Salience']
            else:
                player.Salience = next(salientEmissions)
            if 'SwitchPayoffs' in player.session.config:
                player.SwitchPayoffs = player.session.config['SwitchPayoffs']
            else:
                player.SwitchPayoffs = next(blockswitchPayoffs)
            
            player.reversedbuttons = next(reverse_display)

            player.participant.Exp_Con=player.Exp_Con
            player.participant.reversedbuttons= player.reversedbuttons
            player.participant.Salience = player.Salience
            player.participant.SwitchPayoffs = player.SwitchPayoffs



def make_choice(player: Player, choiceMade):
    reversedbuttons = player.participant.reversedbuttons
    # if player.round_number % C.ROUNDS_PER_CONDITION == 0:
    player.preference = choiceMade
    if reversedbuttons == True:
        if choiceMade == 'A':
            player.preference = 'B'
        elif choiceMade == 'B':
            player.preference = 'A'


# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------
class Consent(Page):
    form_model = 'player'
    form_fields = ['dataScience', 'dataTeach', 'mobileDevice']
    
    @staticmethod
    def vars_for_template(player: Player):
        # while testing this experiment do not check for prolificID (replace False with commented code) (make nolabel and prolificID Missing false for testing)
        player.prolificIDMissing = player.participant.label == None
        return {
            "particpantlabel": player.participant.label,
            "nolabel": False # player.participant.label == None
            }
    


class Intro_1(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    
class Intro_2(Page):
    form_model = 'player'
    form_fields = ['realEmissions']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).Exp_Con > 1
    
class Intro_3(Page):
    form_model = 'player'
    form_fields = ['attention']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    
class NotAtt(Page):
    form_model = 'player'
    form_fields = ['attention2']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {'num_rounds': player.participant.game_rounds,
                'Exp_Con': Exp_Con}

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).attention is None:
            return True
        else:
            return not("thank" in player.in_round(1).attention.lower())
        

class Preview_Game(Page):
    form_model = 'player'
    form_fields = ['amountEmissionsRisky', 'amountEmissionsSafe']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        outcomeCarbon = 30 # player.participant.outcomeCarbon
        carbonMiles = outcomeCarbon * 20/11
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con,
            'outcomeCarbon': outcomeCarbon,
            'carbonMiles': carbonMiles
            }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).Exp_Con > 1 and player.participant.reversedbuttons == False
    

class Preview_Game_R(Page):
    form_model = 'player'
    form_fields = ['amountEmissionsRisky', 'amountEmissionsSafe']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        outcomeCarbon = 30 # player.participant.outcomeCarbon
        carbonMiles = outcomeCarbon * 20/11
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con,
            'outcomeCarbon': outcomeCarbon ,
            'carbonMiles': carbonMiles
            }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).Exp_Con > 1 and player.participant.reversedbuttons == True
        


class NoA2(Page):
    form_model = 'player'
    form_fields = ['amountEmissionsRisky2', 'amountEmissionsSafe2']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        outcomeCarbon = player.participant.outcomeCarbon
        carbonMiles = outcomeCarbon * 20/11
        return {'num_rounds': player.participant.game_rounds,
                'Exp_Con': Exp_Con, 
                'outcomeCarbon': outcomeCarbon ,
                'carbonMiles': carbonMiles}

    @staticmethod
    def is_displayed(player: Player):
        if 1 == 1: ### remove this and subsequent line
            return False 
        if player.in_round(1).Exp_Con == 1: 
            return False
        if player.participant.reversedbuttons == True:
            return False
        if player.amountEmissionsRisky == player.participant.outcomeCarbon and player.amountEmissionsSafe == 0 :
            return False
        return True
    

class NoA2_R(Page):
    form_model = 'player'
    form_fields = ['amountEmissionsRisky2', 'amountEmissionsSafe2']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        outcomeCarbon = player.participant.outcomeCarbon
        carbonMiles = outcomeCarbon * 20/11
        return {'num_rounds': player.participant.game_rounds,
                'Exp_Con': Exp_Con, 
                'outcomeCarbon': outcomeCarbon ,
                'carbonMiles': carbonMiles}

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).Exp_Con == 1: 
            return False
        if player.participant.reversedbuttons == False:
            return False
        if player.amountEmissionsRisky == player.participant.outcomeCarbon and player.amountEmissionsSafe == 0 :
            return False
        return True
    


class Preview_Game2(Page):
    form_model = 'player'
    form_fields = ['preference']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.participant.Exp_Con
        reversedbuttons = player.participant.reversedbuttons
        outcomeCarbon = 30 #player.participant.outcomeCarbon
        carbonMiles = outcomeCarbon * 20/11
        return {
                #'game': game,
                'Exp_Con': Exp_Con,
                'lastRB': reversedbuttons,
                'outcomeCarbon': outcomeCarbon,
                'carbonMiles': carbonMiles
            }
    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.reversedbuttons == False)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        make_choice(player, player.preference)

class Preview_GameR2(Page):
    form_model = 'player'
    form_fields = ['preference']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.participant.Exp_Con
        reversedbuttons = player.participant.reversedbuttons
        outcomeCarbon = 30 # player.participant.outcomeCarbon
        carbonMiles = outcomeCarbon * 20/11
        return {
                #'game': game,
                'Exp_Con': Exp_Con,
                'lastRB': reversedbuttons,
                'outcomeCarbon': outcomeCarbon,
                'carbonMiles': carbonMiles
            }
    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.reversedbuttons== True)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        make_choice(player, player.preference)





class before_Games(Page):
    form_model = 'player'




    



page_sequence = [
    Consent,
    Intro_1,
    Intro_2,
    Intro_3,
    NotAtt, 
    Preview_Game_R, 
    Preview_Game,
    NoA2,
    NoA2_R,
    Preview_GameR2, 
    Preview_Game2,
    before_Games
]
