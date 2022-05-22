from datetime import datetime, timedelta
from typing import Optional
import uuid
import strawberry
import enum
from random import seed, randint, randrange


@strawberry.type
class Game:
    id: strawberry.ID
    created_at: datetime
    is_finished: bool
    scoreboard: list['Player']
    comments: list[str]


@strawberry.type
class Player:
    name: str
    game_role: 'Role'
    is_alive: bool


@strawberry.enum
class Role(enum.Enum):
    MAFIA = 'mafia'
    CIVILIAN = 'civilian'
    SHERIFF = 'sheriff'


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_scoreboard():
    return [
        Player(name=uuid.uuid4(), game_role=Role.MAFIA, is_alive=randint(0, 1)),
        Player(name=uuid.uuid4(), game_role=Role.CIVILIAN, is_alive=randint(0, 1)),
        Player(name=uuid.uuid4(), game_role=Role.CIVILIAN, is_alive=randint(0, 1)),
        Player(name=uuid.uuid4(), game_role=Role.SHERIFF, is_alive=randint(0, 1)),
    ]


games = [
    Game(
        id=str(i),
        created_at=random_date(datetime(2000, 1, 1), datetime.now()),
        is_finished=randint(0, 1),
        scoreboard=generate_scoreboard(),
        comments=[]
    )
    for i in range(100)
]


def get_game(game_id: str) -> Optional[Game]:
    try:
        return games[int(game_id)]
    except IndexError:
        return None


def get_games(is_finished: bool) -> list[Game]:
    return list(filter(lambda game: game.is_finished == is_finished, games))


@strawberry.type
class Query:
    game: Optional[Game] = strawberry.field(resolver=get_game)
    games: list[Game] = strawberry.field(resolver=get_games)


@strawberry.type
class Mutation:
    @strawberry.field
    def add_comment(self, game_id: str, comment: str) -> Game:
        games[int(game_id)].comments.append(comment)
        return games[int(game_id)]


schema = strawberry.Schema(query=Query, mutation=Mutation)
