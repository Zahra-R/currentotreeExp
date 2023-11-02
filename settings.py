from os import environ


SESSION_CONFIGS = [
    ### EDEG -3
    dict(
        name='EDEG_study_FullDesing_Reps', 
        app_sequence=['EDEGIntro', 'EDEG3', 'EDEGScales',], 
        num_demo_participants=5, 
        group = "reps"
    ),

    dict(
        name='EDEG_study2_FullDesign_Dems', 
        app_sequence=['EDEGIntro', 'EDEG3', 'EDEGScales',], 
        num_demo_participants=5, 
        group = "dems"
    ),

    dict(
        name='EDEG_study2_Salient_PayoffSwitches_SafeEmitsFirst',
        app_sequence=['EDEGIntro', 'EDEG3', 'EDEGScales',], 
        num_demo_participants=5,
        Exp_Con=2,
        Salience= True,
        PayoffSwitches = True
    ),
    dict(
        name='DEG_study2_EmissionsDecay',
        app_sequence=['EDEGIntro', 'EDEG3', 'EDEGScales',], 
        num_demo_participants=5,
        Exp_Con=3
    ),
    dict(
        name='DEG_study2_Control',
        app_sequence=['EDEGIntro', 'EDEG3', 'EDEGScales',], 
        num_demo_participants=5,
        Exp_Con=1,
        doc="""
         Here you can make potential comments that will be displayed to the admin
         """
    ),
    ### CC SAMPLING
    dict(
        name='samplingPilot',
        app_sequence=['CCsampling_intro', 'CCsampling', 'CCsampling_scales'],
        num_demo_participants=5,
    ),
    ### FINANCIAL DECISION MAKING
     dict(
        name='FinancialDM_CertainFirst',
        app_sequence=['FinancialDM_Intro', 'FinancialDM_C', 'FinancialDM_U'],
        num_demo_participants=5,
        certainFirst = True
    ),
    dict(
        name='FinancialDM_CertainSecond',
        app_sequence=['FinancialDM_Intro', 'FinancialDM_U', 'FinancialDM_C'],
        num_demo_participants=5,
        certainFirst = False
    ),
    
    dict(
        name='FinancialDM_new',
        app_sequence=['FinancialDM_Intro', 'FinancialDM_united'],
        num_demo_participants=5
    ),

     dict(
         name='carbontask',
         app_sequence=['Nina_survey', 'Nina_carbontask',  'Nina_questionnaire', 'Nina_footprint_calculator'],
         num_demo_participants=10,
     ),

     dict(
       name='tracking_demo',
       display_name="Tracking Demo",
       num_demo_participants=3,
       app_sequence=['tracking_demo']
    ),


]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    # EDEG FIELDS
    'Exp_Con',
    'Salience',
    'reversedbuttons',
    'outcomeA',
    'outcomeB',
    'chosen_round',
    'chosen_round_outcome',
    'chosen_round_choice',
    'payoff_decimal',
    'game_rounds', 
    'finished',
    'SwitchPayoffs',

    #CC SAMPLING FIELDS
    'randomInfoArray',
    'randomMisinfoArray', 
    'reverseBoxes',
    'seenMisinfo',
    'telling_box_label',

    ### FINANCIAL DECISION MAKING
    'shuffledOrderC',
    'shuffledOrderU',
    'carbonLeft', 
    'certainFirst',

    'comprehension_C1_correct' ,
    'comprehension_C2_correct' ,
    'comprehension_U1_correct',
    'comprehension_U2_correct',

    ### CarbonTask Nina
    'task_rounds'

]


SESSION_FIELDS = [
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3153268574945'

INSTALLED_APPS = ['otree']
