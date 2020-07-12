
class TicTacToe(object):
    def __init__(self, size=3):
        self.Players =  (' X ', ' O ')
        self.next_player = 0
        self.board = list()
        for i in range(size):
            row = [' _ ' for i in range(size)]
            self.board.append(row)

    def __repr__(self):
        text = ''
        for row in self.board:
            for col in row:
                text = text + col
            text = text + '\n'
        return text

    def move(self):
        move = input('enter row,col: ')
        row,col = move.split(',')
        row = int(row)
        col=int(col)
        self.board[row] [col]= self.Players[self.next_player]
        self.next_player +=1
        self.next_player = self.next_player % 2        
     

def play_the_game():
    game = TicTacToe()
    i = 9
    while i > 0:
        game.move()
        print(game)
        i -= 1


play_the_game()

