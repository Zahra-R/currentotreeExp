import random
import json

from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'task'
    PLAYERS_PER_GROUP = None
    payment_per_correct_answer = .1
    
    FOOTPRINT_COMBINATIONS_TABLE = [
        ['<b>vegetarian diet</b>', '<b>renewable-based electricity</b>', '<b> recycles</b>',
         '<b>only regional food</b>', '<b>by bike</b>', '<b> does not fly </b> '],
        ['<b>vegetarian diet</b>', '<b>renewable-based electricity</b>', '<b> recycles </b>',
         '<b>regional and imported food</b>', '<b>by bus</b>','<b> does not fly </b> '],
        ['<b>meat-based diet</b>','<b>renewable-based electricity</b>','<b>  does not recycle</b>',
         '<b>regional and imported food</b>','<b>by bike</b>','<b> does not fly </b> '],
        ['<b>meat-based diet</b>', '<b>renewable-based electricity</b>','<b>  does not recycle</b>',
         '<b>only regional food</b>', '<b>by bus</b>', '<b> does not fly </b> '],
        ['<b>vegetarian diet</b>', '<b>fossil-based electricity</b>', '<b>  does not recycle</b>',
         '<b>only regional food</b>', '<b>by bike</b>', '<b> does not fly </b> '],
        ['<b>vegetarian diet</b>', '<b>renewable-based electricity</b>','<b>  does not recycle</b>',
            '<b>regional and imported food</b>','<b>by bike</b>',' <b>flies twice a year</b>'],
        ['<b>vegetarian diet</b>', '<b>fossil-based electricity</b>', '<b> does not recycle</b>',
         '<b>regional and imported food</b>','<b>by bus</b>','<b> does not fly </b> '],
        ['<b>meat-based diet</b>', '<b>fossil-based electricity</b>','<b> recycles</b>',
         '<b>regional and imported food</b>', '<b>by bike</b>','<b> does not fly </b> '],
        ['<b>vegetarian diet</b>', '<b>renewable-based electricity</b>', '<b>  does not recycle</b>',
         '<b>only regional food</b>','<b>by bus</b>',' <b>flies twice a year</b>'],
        ['<b>meat-based diet</b>','<b>renewable-based electricity</b>','<b> recycles </b>',
         '<b>only regional food</b>','<b>by bike</b>',' <b>flies twice a year</b>'],
        ['<b>meat-based diet</b>','<b>fossil-based electricity</b>','<b> recycles </b>',
         '<b>only regional food</b>','<b>by bus</b>','<b> does not fly </b> '],
        ['<b>meat-based diet</b>','<b>renewable-based electricity</b>', '<b> recycles</b>',
         '<b>regional and imported food</b>','<b>by bus</b>',' <b>flies twice a year</b>'],
        ['<b>vegetarian diet</b>','<b>fossil-based electricity</b>','<b> recycles</b>',
         '<b>regional and imported food</b>', '<b>by bike</b>', ' <b>flies twice a year</b>'],
        ['<b>vegetarian diet</b>','<b>fossil-based electricity</b>','<b> recycles</b>',
         '<b>only regional food</b>', '<b>by bus</b>', ' <b>flies twice a year</b>'],
        ['<b>meat-based diet</b>','<b>fossil-based electricity</b>','<b>  does not recycle</b>',
         '<b>only regional food</b>','<b>by bike</b>',' <b>flies twice a year</b>'],
        ['<b>meat-based diet</b>','<b>fossil-based electricity</b>','<b>  does not recycle</b>',
         '<b>regional and imported food</b>','<b>by bus</b>', ' <b>flies twice a year</b>']
    ]
    NUM_ROUNDS = len(FOOTPRINT_COMBINATIONS_TABLE)

    FOOTPRINT_COMBINATIONS_IMAGES = [
        ['diet_image_1', 'household_image_1', 'recycling_image_1', 'regional_image_1', 'commute_image_1', 'vacation_image_1'],
        ['diet_image_1', 'household_image_1', 'recycling_image_1', 'regional_image_2', 'commute_image_2', 'vacation_image_1'],
        ['diet_image_2', 'household_image_1', 'recycling_image_2', 'regional_image_2', 'commute_image_1', 'vacation_image_1'],
        ['diet_image_2', 'household_image_1', 'recycling_image_2', 'regional_image_1', 'commute_image_2', 'vacation_image_1'],
        ['diet_image_1', 'household_image_2', 'recycling_image_2', 'regional_image_1', 'commute_image_1', 'vacation_image_1'],
        ['diet_image_1', 'household_image_1', 'recycling_image_2', 'regional_image_2', 'commute_image_1', 'vacation_image_2'],
        ['diet_image_1', 'household_image_2', 'recycling_image_2', 'regional_image_2', 'commute_image_2', 'vacation_image_1'],
        ['diet_image_2', 'household_image_2', 'recycling_image_1', 'regional_image_2', 'commute_image_1', 'vacation_image_1'],
        ['diet_image_1', 'household_image_1', 'recycling_image_2', 'regional_image_1', 'commute_image_2', 'vacation_image_2'],
        ['diet_image_2', 'household_image_1', 'recycling_image_2', 'regional_image_1', 'commute_image_1', 'vacation_image_2'],
        ['diet_image_2', 'household_image_2', 'recycling_image_1', 'regional_image_1', 'commute_image_2', 'vacation_image_1'],
        ['diet_image_2', 'household_image_1', 'recycling_image_1', 'regional_image_2', 'commute_image_2', 'vacation_image_2'],
        ['diet_image_1', 'household_image_2', 'recycling_image_1', 'regional_image_2', 'commute_image_1', 'vacation_image_2'],
        ['diet_image_1', 'household_image_2', 'recycling_image_1', 'regional_image_1', 'commute_image_2', 'vacation_image_2'],
        ['diet_image_2', 'household_image_2', 'recycling_image_2', 'regional_image_1', 'commute_image_1', 'vacation_image_2'],
        ['diet_image_2', 'household_image_2', 'recycling_image_2', 'regional_image_2', 'commute_image_2', 'vacation_image_2']

    ]




class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    rating0 = models.IntegerField(choices=[['1', 'small footprint (1)'], ['2', '2'], ['3', '3'], ['4', '4'],
                                           ['5', '5'],['6', '6'], ['7', '7'], ['8', '8'],['9', '9'], ['10', 'large footprint (10)']], 
                                  widget=widgets.RadioSelectHorizontal,
                                  label='How large or small do you think this persons footprint is?')
    vignetteNumber = models.IntegerField(initial= 0)
    order_behavior_types = models.StringField()
   

# FUNCTIONS
# for random order of tasks
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            round_numbers = list(range(0, C.NUM_ROUNDS))
            random.shuffle(round_numbers)
            p.participant.task_rounds = round_numbers

# for this all to work, need to add 'task_rounds' as PARTICIPANT_FIELDS in settings.py!!
# PAGES

class task_page00(Page):

    # 0 is diet, 1 is electricity, 2 is recycling, 3 is regional food, 4 is commute, 5 vacation
    form_model = 'player'
    form_fields = ['rating0']
    @staticmethod
    def vars_for_template(player: Player):
        # this determines which vignette
        task_in_round = player.participant.task_rounds[player.round_number - 2]
        player.vignetteNumber = task_in_round
        my_vignette_table = C.FOOTPRINT_COMBINATIONS_TABLE[task_in_round]
        my_vignette_table_images = C.FOOTPRINT_COMBINATIONS_IMAGES[task_in_round]
        # this determines which order within vignette
        random_behavior_order = list(range(0,6))
        random.shuffle(random_behavior_order)
        current_footprint_table_shuffled = []
        current_footprint_table_images_shuffled = []
        behavior_types = ["Diet", "Electricity", "Recycling", "Food", "Commute", "Vacation"]
        order_behavior_types = []
        for i in random_behavior_order:
            current_footprint_table_shuffled.append(my_vignette_table[i])
            current_footprint_table_images_shuffled.append(my_vignette_table_images[i])
            order_behavior_types.append(behavior_types[i])
        player.order_behavior_types = str(order_behavior_types)
        return {
            "current_footprint_table": current_footprint_table_shuffled,
            "current_footprint_table_images": current_footprint_table_images_shuffled,
            "random_behavior_order": random_behavior_order
        }
    

# Page sequence
page_sequence = [
    task_page00
    ]
