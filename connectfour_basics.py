#Sue Ji 33337876
import connectfour



def printboard(board:[[int]])->None:
    '''
    prints the visual board
    '''
    for num in range (1,connectfour.BOARD_COLUMNS+1):
        if num==connectfour.BOARD_COLUMNS:
            print(num)
        else:
            print(num,end=' ')
            
    for row in range(connectfour.BOARD_ROWS):
        tile=''
        for col in range(connectfour.BOARD_COLUMNS):
            if board[col][row]==1:
                tile+='R '
            if board[col][row]==2:
                tile+='Y '
            if board[col][row]==connectfour.NONE:
                tile+='. '
        print(tile[:-1])



def _poppable(gamestate:tuple)->list:
    '''
    takes the gamestate and checks if it is empty tile at the bottom
    returns a list of all the non-empty tiles at the bottom
    '''
    valid=[]

    for col in range(len(gamestate.board)):
        if gamestate.board[col][-1]==gamestate.turn:
            valid.append(col)
    return valid
     
            

def column_command()->int:
    '''
    takes and returns the column number user wants to drop or pop
    '''
    col=None
    
    while col==None:
        try:
            col=int(input('Please input the column number\
 you want to move your disc\n'))-1
            if col<0 or col>6:
                print('Please enter a valid number\n')
                col=None
            else:
                return col
            
        except ValueError:
            print('Please enter a valid number\n')
            col=None

    return col


           
def pop_or_drop()->str:
    '''
    asks the user to pop or drop and returns pop or drop
    '''
    request=False
    while request==False:
        command=input('Would you like to pop or drop your disc?\n')
        if command.lower()=='drop':
            request=True
            return 'DROP'
        if command.lower()=='pop':
            request=True
            return 'POP'
        else:
            print('Please type "pop" or "drop"')
            request=False



def update_gamestate(gamestate:connectfour.GameState,move:str)->"Connectfour.GameState":
    '''
    while playing the game and the exception is not raised after proceeding one move,
    update the board
    '''


    if move.startswith('DROP'):

        
        move_col=int(move[5])
        
        gamestate=connectfour.drop(gamestate,move_col)

    else:

        move_col=int(move[4])
        
        gamestate=connectfour.pop(gamestate,move_col)


    return gamestate



def get_valid_move(gamestate:connectfour.GameState)->str:
    '''
    asks the player to input a move and test if it is a valid move,
    if yes, return the move type and col as one str
    '''
    while True:

        try:
        
            move_type=pop_or_drop()
            
            move_col=column_command()
            

            if move_type=='DROP':
                gamestate=connectfour.drop(gamestate,move_col)
            else:
                gamestate=connectfour.pop(gamestate,move_col)

            if gamestate!=None:

                return '{} {}'.format(move_type,move_col)

        except KeyboardInterrupt:
            quit()

        except:
            print('Invalid move. Please try again!')


def print_move(move:str)->str:
    '''
    get the move col and add 1 onto it before sending the
    move to the server or print out in the interface,
    since the server reads on 1-base and the move right now is 0-based
    '''
    if move.startswith('D'):
        
        col=int(move[5])+1

        return "{}{}".format(move[:5],col)

    else:
        
        col=int(move[4])+1

        return "{}{}".format(move[:4],col)
                
