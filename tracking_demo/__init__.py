from otree.api import *


author = 'Christian König gen. Kersting'

doc = """
Demo of element hover tracking using oTree 2.6b0
"""


class Constants(BaseConstants):
    name_in_url = 'tracking_demo'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def store_tracking_data(self, payload):
        HoverEvent.create(
            player=self,
            element_id=payload["element_id"],
            enter_time=payload["enter_time"],
            leave_time=payload["leave_time"],
            duration = payload["duration"],
            attributeType = payload["attributeType"],
            attributeValue = payload["attributeValue"],
        )


class HoverEvent(models.ExtraModel):
    player = models.Link(Player)
    element_id = models.StringField()
    enter_time = models.FloatField()
    leave_time = models.FloatField()
    duration = models.IntegerField()
    attributeType = models.StringField()
    attributeValue = models.StringField()


def custom_export(players):
    yield ["session", "participant_code", "round_number", "id_in_group", "element_id", "enter_time", "leave_time", "duration", "attributeType", "attributeValue"]
    for player in players:
        for e in HoverEvent.filter(player=player):
            yield [
                player.session.code,
                player.participant.code,
                player.round_number,
                player.id_in_group,
                e.element_id,
                e.enter_time,
                e.leave_time, 
                e.duration,
                e.attributeType,
                e.attributeValue
            ]





class Tracker(Page):
    form_model = 'player'
    @staticmethod
    def live_method(player, data):
        player.store_tracking_data(data)


page_sequence = [Tracker]
