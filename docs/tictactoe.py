PLAYERS = ('X', 'O')


def print_board(board):
    print()
##############################################################################    print(board)
    for row in board:
        print (row)

def make_a_move(game, row, col, player):
    game[row] [col]= player



def play_the_game(game):
    index = 0
    i = 9
    while i > 0:
        move = input('enter row,col: ')
        #####################################2,text = 'your move was {}'.format(move)
        row,col = move.split(',')
        row = int(row)
        col=int(col)
        make_a_move(game, row, col, PLAYERS[index])
        index = (index+1) % 2
        print_board(game)
        i -= 1


def create_game_board(size=3):
    board = list()
    for i in range(size):
        row = [' ' for i in range(size)]
        board.append(row)
    return board    


def unittest():
    print ('hi')
    x = create_game_board()
    print_board(x)
    play_the_game(x)


if __name__=='__main__':
    unittest()
