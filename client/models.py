from pydantic import BaseModel, Field
from datetime import datetime
import enum


class Game(BaseModel):
    id: str
    created_at: datetime = Field(alias='createdAt')
    is_finished: bool = Field(alias='isFinished')
    scoreboard: list['Player']
    comments: list[str]

    def __str__(self):
        return f'Game #{self.id}'


class Player(BaseModel):
    name: str
    game_role: 'Role' = Field(alias='gameRole')
    is_alive: bool = Field(alias='isAlive')


class Role(enum.Enum):
    MAFIA = 'MAFIA'
    CIVILIAN = 'CIVILIAN'
    SHERIFF = 'SHERIFF'

    def __repr__(self):
        return self.name


Game.update_forward_refs()
Player.update_forward_refs()
