#Sue Ji 33337876

import connectfour
import connectfour_basics

            

def _setup()->None:
    '''
    runs the console-mode interface from start to finish
    '''
    print("Welcome to Connectfour Game!\n")
    gamestate=connectfour.new_game()
    
    while True:
        
        connectfour_basics.printboard(gamestate.board)
        
        if connectfour.winner(gamestate)==1:
            print('Red player has won! See you!')
            quit()
        elif connectfour.winner(gamestate)==2:
            print('Yellow player has won! See you!')
            quit()
            

        if gamestate.turn==1:
            print("\nRed player's turn\n")
            
        if gamestate.turn==2:
            print("\nYellow player's turn\n")


        move=connectfour_basics.get_valid_move(gamestate)


        gamestate=connectfour_basics.update_gamestate(gamestate,move)

        if gamestate.turn==2:

            print('Red: ',connectfour_basics.print_move(move),'\n')
        else:
            print('Yellow: ',connectfour_basics.print_move(move),'\n')

            
if __name__=='__main__':
    _setup()
    
