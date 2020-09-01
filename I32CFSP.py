#Sue Ji 33337876

import connectfour
from collections import namedtuple
import socket

ConnectfourConnection=namedtuple('ConnectfourConnection',
                                 ['socket', 'socket_in', 'socket_out'])

_SHOW_DEBUG_TRACE = False



def connect(host:str,port:int)->ConnectfourConnection:
    '''
    connects to the server via socket
    '''
    
    connectfour_socket=socket.socket()
    connectfour_socket.connect((host,port))
    connectfour_in=connectfour_socket.makefile('r')
    connectfour_out=connectfour_socket.makefile('w')

    return ConnectfourConnection(connectfour_socket,connectfour_in,connectfour_out)

  

def write_line(connection:ConnectfourConnection,line:str)->None:
    '''
    writes a line to the server
    '''
    connection.socket_out.write(line.upper()+'\r\n')
    connection.socket_out.flush()
    

def _read_line(connection:ConnectfourConnection)->str:
    '''
    reads a line from the server and returns it with a newline at the end
    '''
    
    line=connection.socket_in.readline().upper()[:-1]
    
    if _SHOW_DEBUG_TRACE:
        print('RCVD: '+line)
    return line+'\r\n'



def hello(connection:ConnectfourConnection,username:str)->str:
    '''
    REQUIRES THE USER TO INPUT 'I32CFSP_HELLO '+NO-SPACED USERNAME TO CONTINUE
    CONVERSATION WITH SERVER
    '''
    write_line(connection, 'I32CFSP_HELLO {}'.format(username))
    response = _read_line(connection)

    return response    
   

def AI_game(connection:ConnectfourConnection,line:str)->str:
    '''
    REQUIRES THE USER TO INPUT AI_GAME IN ORDER TO START THE GAME 
    '''
    write_line(connection, 'AI_GAME')
    response = _read_line(connection)

    return response



def receive_move(connection:ConnectfourConnection)->str:
    '''
    receive the server's move from the server and convert it to str
    '''
    
    response_byte=connection.socket.recv(4096)


    response_message=response_byte.decode(encoding='utf-8').rstrip()

    
    return response_message



def send_move(connection:ConnectfourConnection,move:str)->None:
    '''
    sends the move to the server as binary str
    '''
    
    connection.socket_out.write(move+'\r\n')
   
    connection.socket_out.flush()
    

def close(connection:ConnectfourConnection)->None:
    '''
    CLOSES THE CONNECTION TO THE  SERVER ENTIRELY
    '''
    connection.socket.close()
    connection.socket_in.close()
    connection.socket_out.close()
    
        
