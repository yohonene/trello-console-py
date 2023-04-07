from trello import TrelloClient
from rich import print,pretty
from rich.tree import Tree
from rich.console import Console
from dotenv import load_dotenv
import os

load_dotenv()

TRELLO_API = os.environ.get('TRELLO_API_KEY')
TRELL_TOKEN = os.environ.get('TRELLO_TOKEN')

console = Console()
BOARD_NAME = 'Uni'
pretty.install()

client = TrelloClient(
    api_key=TRELLO_API,
    token=TRELL_TOKEN
)

#Gets the board (Only have one)
board = client.list_boards()
for x in board:
    #Find the specific board you need
    if x.name == BOARD_NAME:
        print('[u]Board Name: '+x.name+'[/u]\n')
        board = x
        break

lists = board.list_lists()

#Find the ids of all lists
id_list = []
for list in lists:
    #This is here because I don't want the 
    #Lists past [3] being included
    if len(id_list) > 3:
        break
    id_list.append(list.id)

#Make a new tree for displayment
tree = Tree(BOARD_NAME)

#Displays loading animations
with console.status("[bold green]Working on tasks...",spinner='line') as status:
    #Loop through id list from id_list.append
    for id in id_list:
        fl_list = board.get_list(id)
        #Subtree header and Subtree init
        sub_tree = tree.add(f"[bold blue]{fl_list.name}[/bold blue]")
        for card in fl_list.list_cards():
            #Add cards to subtrees
            sub_tree.add(f"[green][reverse]{card.name}[/reverse][/green]",guide_style="bold")

console.print(tree)
