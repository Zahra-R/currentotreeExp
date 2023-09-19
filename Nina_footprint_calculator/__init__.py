
from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'carbon_footprint_assessment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    CARBON_FOOTPRINT = {
        'footprint_1': { '1': 0.59, '2': 0.44 , '3':0.3 , '4': 0.15, '5': 0.04},
        'footprint_2': {'1': 1.73, '2': 1.16, '3': 0.58, '4': 0.28, '5':0.11, '6': 0.03 } ,
        'footprint_3': { '1': 0.12, '2': 0.1 , '3':0.05 , '4': 0.03 },
        'footprint_4': {'1': 1.45, '2': 1.21, '3':0.63, '4': 0.34, '5':0.14, '6': 0.06 } ,
        'footprint_5': { '1': 0.01, '2': -0.05 , '3': -0.1 },
        'footprint_6': {'1': 0.17, '2': 0, '3': -0.1}  
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
                                             label = '<b>Wht percentage of your food is regional (from within you country or region, not imported) ?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                             )
    footprint_2 = models.IntegerField(choices=[['1', 'I recylce: '],['2', 'I recylce: '],
                                             ['3', 'I recylce: '],['4', 'I recylce: '],
                                             ['5', 'I recylce: '], ['6', 'Never']],
                                             label = '<b>This question is about recycling in the household. Which of these best describes your recycling behavior?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                             )

    footprint_3 = models.IntegerField(choices=[['1', 'Vegan'],['2', 'Vegetarian'],
                                             ['3', 'Pescetarian'],['4', 'No red meat'],
                                             ['5', 'Flexitarian (rarely, but sometimes meat)'], ['6','Omnivore']],
                                             label = '<b>This question is about your food consumption. Which of these best describes your diet?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                             )
    
    footprint_4 = models.IntegerField(choices=[['1', 'More than 600 km'],['2', '360 - 600 km'],['3', '240 - 359 km'] ,
                                               ['4', '80 -239 km'], ['5', '60 - 79 km'],  ['6', '1 - 59 km '],['7', 'I never use public transport']  ],
                                             label = '<b>This question is about your travel / commuting behavior. How many km do you spend in which type of transport in a typical week? Please include all private journeys including the work commute, but not business travels.</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                              )
    footprint_5 = models.IntegerField(choices=[['1', 'More than 50 hours per year'],['2', '25 - 49 hours per year'],['3', '15 - 24 hours per year'],
                                             ['4', '8 - 14 hours per year'], ['5', '2 - 7 hours per year'],['6', '0.1 - 2 hours per year'], ['7', 'I did not fly in the last five years'] ],
                                             label = '<b>How many hours did you fly by plane in the last five years on average?</b>',
                                             widget=widgets.RadioSelectHorizontal,
                                              )
    
    footprint_6 = models.IntegerField(choices=[['1', 'I have green electricity entirely '],['2', 'I partly have green electricity (mixed)'] , 
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
    form_fields = ['footprint_1', 'footprint_2', 'footprint_3', 'footprint_4', 'footprint_5', 'footprint_6']


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        footprint_total = player.calculate_total_co2()  # Calculate the total CO2 emissions
        player.total_co2 = round(footprint_total, 1)  # Store the total in the player's field


class display_footprint(Page):
    form_model = 'player'
    form_fields = ['total_co2']

    def get_form_fields(self):
        # Make the total_co2 field read-only
        return ['total_co2']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'total_co2': player.total_co2
        }
    


# Page sequence
page_sequence = [
    questions_footprint,
    display_footprint
    
]




