import random
from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):


    def make_field(label):
        return models.IntegerField(
        choices=[['6', 'Agree completely'], ['5', 'Agree'], ['4', 'Somewhat agree '], 
                 ['3', 'Somehat disagree'], ['2', 'Disagree'], ['1', 'Completely disagree'] ],                                
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

    # questionnaire
    conservative_liberal = models.IntegerField( widget=widgets.RadioSelect, choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4,5])
    climate_change_concern1 = make_field('I worry about the climate´s state.')
    climate_change_concern2 = make_field('Climate protection is important for our future.')
    climate_change_concern3 = make_field('We must protect the climate´s delicate equilibrium.')
    climate_change_concern4 = make_field('Climate change has severe consequences for humans and nature.')
    
    def make_field(label):
        return models.IntegerField(
        choices=[['1', 'Strongly oppose (1)'],['2', '2'] ,   ['3', '3'], ['4', '4'] ,
                 ['5', '5'], ['6', '6'] , ['7', 'Strongly support (7)'] ],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )
    policy_item1 = make_field('Expand public transport (buses, trams, trains).')
    policy_item2 = make_field('Ban the sale of diesel and petrol-engine cars.')
    policy_item3 = make_field('Increasing subsidies for alternatives to flying.')
    policy_item4 = make_field('Increase or introduce taxes on air travel.')  
    policy_item5 = make_field('Increase subsidies for renewable energy projects (e.g., wind and solar energy).')
    policy_item6 = make_field('Requiring electric utilities to provide increasing amounts of low carbon power.')  
    policy_item7 = make_field('Increase or introduce taxes on red meat (e.g., beef, lamb, veal).')
    policy_item8 = make_field('Increase subsidies for food products with low greenhouse gas emissions (e.g., fruit, vegetables, legumes, cereals).')

    
# FUNCTIONS
# PAGES

class cc_concern(Page):
    form_model = 'player'
    form_fields = ['climate_change_concern1', 'climate_change_concern2', 'climate_change_concern3', 'climate_change_concern4', 'conservative_liberal']
class policy_support(Page):
    form_model = 'player'
    form_fields = []
    
class policy(Page):
    form_model = 'player'
    form_fields = ['policy_item1', 'policy_item2','policy_item3','policy_item4','policy_item5','policy_item6', 'policy_item7', 'policy_item8']

   



# Page sequence
page_sequence = [
    policy_support, 
    cc_concern,
    policy
]
