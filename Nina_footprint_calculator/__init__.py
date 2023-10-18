
from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'carbon_footprint_assessment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    CARBON_FOOTPRINT = {
        'footprint_1': { '1': 0, '2': -0.111 , '3':-0.222 , '4': -0.333, '5': -0.444},
        'footprint_2': {'1': -.0575 , '2': 0} ,
        'footprint_3': { '1': 0.955, '2': 1.053 , '3':1.431 , '4': 1.234, '5': 3.160, '6': 2.282 },
        'footprint_4': {'1': 4.0896, '2': 3.27168, '3':2.0414, '4': 1.0872, '5':0.2726, '6': 0.0 } ,
        'footprint_5': {'1': 2.3328, '2': 1.8662, '3':1.11645, '4': 0.6201, '5':0.1555, '6': 0.0 } ,
        'footprint_6': {'1': 1.0944, '2': 0.8755, '3':0.5463, '4': 0.2909, '5':0.0729, '6': 0.0 } ,
        'footprint_7': {'1': 13.48, '2': 6.74, '3':3.59, '4': 2.07, '5':0.90, '7': 0.36, '7': 0.0}  ,
        'footprint_8': {'1': 0.1031 , '2': 0.6988837, '3':1.294697,'4': 1.294697 } 
    }



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):


    # questionnaire
    footprint_1 = models.IntegerField(choices=[['1', 'Less than a quarter'],['2', 'About a quarter'],
                                             ['3', 'About half'],['4', 'About three quarters'],
                                             ['5', 'the largest part is regional']],
                                             label = '<b>What percentage of your food is regional (from within your country or region, not imported) ?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                             )
    
    footprint_2 = models.IntegerField(choices=[['1', 'I recylce'],['2', 'I do not recycle']],
                                             label = '<b>This question is about recycling in the household. Which of these best describes your recycling behavior?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                             )
    footprint_3 = models.IntegerField(choices=[['1', 'Vegan'],['2', 'Vegetarian'],
                                             ['3', 'Pescetarian'],['4', 'No red meat'],
                                             ['5', 'No pork'], ['6','Omnivore = meat-based']],
                                             label = '<b>This question is about your food consumption. Which of these best describes your diet?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                             )
    footprint_4 = models.IntegerField(choices=[['1', 'More than 600 km'],['2', '360 - 600 km'],['3', '240 - 359 km'] ,
                                               ['4', '80 -239 km'], ['5', '1 - 79 km '],['6', 'I never use a private car']  ],
                                             label = '<b>This question is about your travel / commuting behavior. How many km do you spend in the <b>car</b> in a typical week? Please include all private journeys including the work commute, but not business travels.</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                     )
    footprint_5 = models.IntegerField(choices=[['1', 'More than 600 km'],['2', '360 - 600 km'],['3', '240 - 359 km'] ,
                                               ['4', '80 -239 km'],  ['5', '1 - 79 km '],['6', 'I never use public transport']  ],
                                             label = '<b>This question is about your travel / commuting behavior. How many km do you spend in the <b>bus/metro/tram</b> in a typical week? Please include all private journeys including the work commute, but not business travels.</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                              )

    footprint_6 = models.IntegerField(choices=[['1', 'More than 600 km'],['2', '360 - 600 km'],['3', '240 - 359 km'] ,
                                               ['4', '80 -239 km'], ['5', '1 - 79 km'] ,['6', 'I never use public transport']  ],
                                             label = '<b>This question is about your travel / commuting behavior. How many km do you spend in the <b>train</b> in a typical week? Please include all private journeys including the work commute, but not business travels.</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                              )


    footprint_7 = models.IntegerField(choices=[['1', 'More than 50 hours per year'],['2', '25 - 49 hours per year'],['3', '15 - 24 hours per year'],
                                             ['4', '8 - 14 hours per year'], ['5', '2 - 7 hours per year'],['6', '0.1 - 2 hours per year'], ['7', 'I did not fly in the last five years'] ],
                                             label = '<b>How many hours did you fly by plane in 2022?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                              )
    
    footprint_8 = models.IntegerField(choices=[['1', 'I have green electricity entirely '],['2', 'I partly have green electricity (mixed)'] , 
                                                ['3', ' I have a conventional (fossil) supply'], ['4', 'I don’t know']   ],
                                             label = '<b>This question is about your electricity supply. What does your electricity supply look like?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                              )
    

    total_co2 = models.FloatField()

    def calculate_total_co2(self):
        total_co2 = 0
        for field_name, choice in self.__dict__.items():
            if field_name.startswith('footprint_'):
                question = field_name
                selected_choice = str(choice)
                co2_value = C.CARBON_FOOTPRINT.get(question, {}).get(selected_choice, 0)
                total_co2 += co2_value
        return total_co2
        
    

# FUNCTIONS



# PAGES

class questions_footprint(Page):
    form_model = 'player'
    form_fields = ['footprint_1', 'footprint_2', 'footprint_3','footprint_7', 'footprint_8', 'footprint_4', 'footprint_5', 'footprint_6']


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        footprint_total = player.calculate_total_co2()  # Calculate the total CO2 emissions
        player.total_co2 = round(footprint_total, 1)  # Store the total in the player's field



# Page sequence
page_sequence = [
    questions_footprint
    
]




