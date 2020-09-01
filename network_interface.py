#Sue Ji 33337876

import connectfour
import connectfour_basics
import I32CFSP
import socket


def _server_move(connection:I32CFSP.ConnectfourConnection,user_move:str,gamestate:
                 connectfour.GameState)->list:

    '''
    handles the server's move response by connecting
    the socket and taking the last user-move into socket
    '''
    
    print('\nThe AI is taking its turn...')

    
    response_message=I32CFSP.receive_move(connection)


    if response_message=='OKAY':
        
        AI_move=I32CFSP.receive_move(connection)
        if AI_move.startswith('DROP'):
            AI_move_type='DROP'
            AI_move_col=int(AI_move[5:6])-1
            
        else:
            AI_move_type='POP'
            AI_move_col=int(AI_move[4:5])-1
            
        print('\nAI turn: '+AI_move_type+' '+str(AI_move_col+1)+'\n')

        return "{} {}".format(AI_move_type,AI_move_col)
        



    if response_message.startswith('DROP'):
        
        AI_move_type='DROP'
        AI_move_col=int(AI_move[5:6])-1

        print('\nAI turn: '+AI_move_type+' '+str(AI_move_col+1)+'\n')

        return "{} {}".format(AI_move_type,AI_move_col)
        
        

    if response_message.startswith('POP'):
        
        AI_move_type='POP'
        AI_move_col=int(AI_move[4:5])-1

        print('\nAI turn: '+AI_move_type+' '+str(AI_move_col+1)+'\n')

        return "{} {}".format(AI_move_type,AI_move_col)
       
    

    if response_message.startswith('OKAY'):
        
        if response_message[6]=='D':
            AI_move_type="DROP"
            AI_move_col=int(response_message[11:13])-1

       
        if response_message[6]=='P':
            AI_move_type="POP"
            AI_move_col=int(response_message[10:12])-1


        print('\nAI turn: '+AI_move_type+' '+str(AI_move_col+1)+'\n')
        

        return "{} {}".format(AI_move_type,AI_move_col)


    if response_message=='READY':

        print("It is user's turn\n")

        return response_message


      

    if response_message=="INVALID":
        
        print('User has made an invalid move! please try again!')

        response_message=I32CFSP.receive_move(connection)

        return response_message
    

    if response_message.startswith('INVALID') and response_message.endswith('READY'):

        print(response_message)

        print('User has made an invalid move! please try again!')
        
        response_message='READY'

        return response_message


    if reponse_message=='ERROR':
        print(response_message)
        print('The AI cannot understand it...')
        print('Connectfour Game Connection closed. Bye-bye!')
        I32CFSP.close(connection)
        quit()
        

    else:

        print('reponse_message: '+response_message)
        
    

      

def _handle_AI(connection:I32CFSP.ConnectfourConnection)->None:
    '''
    asks the user to wirte AI_GAME in order to start the game,
    prints the response of the server if input correctly
    '''
    while True:

        launch=input('If you want to start the game, please input "PLAY"\n')

        if launch.upper()=="PLAY":
            print('\nThe AI IS '+I32CFSP.AI_game(connection,launch))
            break


def _ask_username(connection:I32CFSP.ConnectfourConnection)->str:
    '''
    asks and returns user's name
    '''

    while True:
        username=input('Please input your name: \n')

      
        if username!='' and ' ' not in list(username.strip()):
           
            AI_response=I32CFSP.hello(connection,username)

            print(AI_response)

            return username.upper()
    


def _port_num()->int:
    '''
    asks user for the port to connect to the server, return the port as an int
    '''
    while True:
        try:
            port=int(input('port: '))
            
            if port==4444:
                print()
                return port
            else:
                print('Please input 4444 in order to play ConnectFour Game!')
        
        except ValueError:
            print('Invalid port input. BYE~')
            quit()





def _playGame(connection:I32CFSP.ConnectfourConnection,username:str)->None:   
    '''
    PLAYS THE GAME WITH THE AI
    '''
    gamestate=connectfour.new_game()

    
    
    while True:


        connectfour_basics.printboard(gamestate.board)

        if connectfour.winner(gamestate)==1:
            print('The user has won! See you!')
            break
        elif connectfour.winner(gamestate)==2:
            print('The AI has won! See you!')
            break

        
        user_move=connectfour_basics.get_valid_move(gamestate)

        
        gamestate=connectfour_basics.update_gamestate(gamestate,user_move)

        user_move=connectfour_basics.print_move(user_move)

        print(username+"'s move: "+user_move+'\n')

        
        connectfour_basics.printboard(gamestate.board)

        if connectfour.winner(gamestate)==1:
            print(username+' has won! See you!')
            break
        elif connectfour.winner(gamestate)==2:
            print('The AI has won! See you!')
            break


        send_move=I32CFSP.send_move(connection,user_move)
        
        AI_move=_server_move(connection,user_move,gamestate)

        if AI_move=='READY':

            user_move=connectfour_basics.get_valid_move(gamestate)
            gamestate=connectfour_basics.update_gamestate(gamestate,user_move)
            
            user_move=connectfour_basics.print_move(user_move)
            print(username+' move: '+user_move+'\n')
            
            connectfour_basics.printboard(gamestate.board)

            if connectfour.winner(gamestate)==1:
                print(username+' has won! See you!')
                break
            elif connectfour.winner(gamestate)==2:
                print('The AI has won! See you!')
                break

            send_move=I32CFSP.send_move(user_move)
        
            AI_move=_server_move(connection,user_move,gamestate)


        gamestate=connectfour_basics.update_gamestate(gamestate,AI_move)



       
def _run_user_interface() -> None:
    '''
    RUNS THE NETWORK-MODE USER INTERFACE FROM START TO FINISH
    '''
    host=input('host: ')
    print()

    port=_port_num()
    
    print('Connecting to {} (port {})...\n'.format(host,port))

    try:
        connection = I32CFSP.connect(host,port)
        print('Welcome to "Connect Four" game!\n')

        user=_ask_username(connection)

        _handle_AI(connection)

        print('The connectfour game starts! '+user+', it is your turn now...')

        _playGame(connection,user)

    except socket.error:
        print('Connectfour Game Connection failed. Bye-bye!')
        quit()

    finally:
        print('Connectfour Game Connection closed. Bye-bye!')
        I32CFSP.close(connection)
        quit()
        
    


if __name__ == '__main__':
    _run_user_interface()
    

