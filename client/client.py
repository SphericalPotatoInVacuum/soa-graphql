from datetime import datetime
from typing import Any
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from models import Game, Player, Role
from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.completion import WordCompleter, Completion
from rich import print
from rich.text import Text
from rich.tree import Tree
import shlex

transport = AIOHTTPTransport(url='http://127.0.0.1:8000/graphql')

client = Client(transport=transport, fetch_schema_from_transport=True)


get_games_query = """query {
    games(isFinished: %s) {
        id,
        createdAt,
        isFinished,
        scoreboard {
            name,
            gameRole,
            isAlive
        },
        comments
    }
}
"""

get_game_query = """query {
    game(gameId: "%s") {
        id,
        createdAt,
        isFinished,
        scoreboard {
            name,
            gameRole,
            isAlive
        },
        comments
    }
}
"""


add_comment_query = """mutation {
    addComment(gameId: "%s", comment: "%s") {
        id,
        createdAt,
        isFinished,
        scoreboard {
            name,
            gameRole,
            isAlive
        },
        comments
    }
}
"""


def build_player_tree(player: Player, tree: Tree):
    role_style: str
    role_icon: str
    if player.game_role is Role.CIVILIAN:
        role_style = 'green'
        role_icon = '🧑'
    elif player.game_role is Role.MAFIA:
        role_style = 'red'
        role_icon = '😈'
    elif player.game_role is Role.SHERIFF:
        role_style = 'green'
        role_icon = '👮'
    tree.add(Text(f'Role: {role_icon} ').append(player.game_role.name, role_style))
    tree.add(
        Text('Is alive: ').append(
            Text("❤️ Yes" if player.is_alive else "💀 No",
                 "green" if player.is_alive else "red")
        )
    )


def build_scoreboard_tree(scoreboard: list[Player], tree: Tree):
    for player in scoreboard:
        build_player_tree(player, tree.add(Text(player.name, 'bold blue')))


def build_game_tree(game: Game, tree: Tree):
    tree.add(f'Created at: {game.created_at}')
    tree.add(f'Is finished: {"yes" if game.is_finished else "no"}')
    build_scoreboard_tree(game.scoreboard, tree.add(f'Scoreboard:'))
    branch = tree.add(f'Comments:')
    for comment in game.comments:
        branch.add(comment)


def build_games_tree(games: list[Game], tree: Tree):
    for game in games:
        build_game_tree(game, tree.add(Text(f'Game #{game.id}', 'bold green')))


def get_finished_games():
    result = client.execute(gql(get_games_query % 'true'))
    games = [Game.parse_obj(obj) for obj in result['games']]

    tree = Tree('Games')
    build_games_tree(games, tree)
    print(tree)


def get_unfinished_games():
    result = client.execute(gql(get_games_query % 'false'))
    games = [Game.parse_obj(obj) for obj in result['games']]

    tree = Tree('Games')
    build_games_tree(games, tree)
    print(tree)


def get_game(game_id):
    game = Game.parse_obj(client.execute(gql(get_game_query % game_id))['game'])

    tree = Tree(Text(f'Game #{game_id}', 'bold green'))
    build_game_tree(game, tree)
    print(tree)


def add_comment(game_id, comment):
    game = Game.parse_obj(client.execute(gql(add_comment_query % (game_id, comment)))['addComment'])

    tree = Tree(Text(f'Game #{game_id}', 'bold green'))
    build_game_tree(game, tree)
    print(tree)


def handle_command(cmd: str):
    cmd, *args = shlex.split(cmd)
    if cmd == 'game':
        get_game(*args)
    elif cmd == 'finished_games':
        get_finished_games(*args)
    elif cmd == 'unfinished_games':
        get_unfinished_games(*args)
    elif cmd == 'add_comment':
        add_comment(*args)


session = PromptSession()

while True:
    try:
        text = session.prompt('> ')
    except KeyboardInterrupt:
        print('To quit press Ctrl+D')
        continue
    except EOFError:
        break
    else:
        handle_command(text)
