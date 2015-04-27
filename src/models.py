from peewee import *

database = SqliteDatabase('pokerbot.db', **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Actions(BaseModel):
    action = CharField()

    class Meta:
        db_table = 'actions'

class BoardRanks(BaseModel):
    cards = IntegerField()

    class Meta:
        db_table = 'board_ranks'

class HandRanks(BaseModel):
    hands = CharField()

    class Meta:
        db_table = 'hand_ranks'

class Players(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'players'

class Rounds(BaseModel):
    round = IntegerField()

    class Meta:
        db_table = 'rounds'

class Probabilities(BaseModel):
    action = ForeignKeyField(db_column='action', rel_model=Actions, to_field='id')
    board_rank = ForeignKeyField(db_column='board_rank', rel_model=BoardRanks, to_field='id')
    hand_rank = ForeignKeyField(db_column='hand_rank', rel_model=HandRanks, to_field='id')
    player = ForeignKeyField(db_column='player', rel_model=Players, to_field='id')
    probability = DecimalField()
    round = ForeignKeyField(db_column='round', rel_model=Rounds, to_field='id')

    class Meta:
        db_table = 'probabilities'

class SqliteSequence(BaseModel):
    name = UnknownField()  # 
    seq = UnknownField()  # 

    class Meta:
        db_table = 'sqlite_sequence'

