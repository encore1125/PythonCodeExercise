import os
import random 


def game_board(board):
    
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')


def player_input():
    player = ''
    
    while not (player == 'X' or player == 'O'):
        player = input('Welcome Player 1: Do you want to be X or O? ').upper()

    if player == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')
        
def player_first():
    
    if random.randint(0,1) == 0:
        return 'Player 1'
    else:
        return 'Player 2'

def player_place(board, player, position):
     
    board[position]= player
    

def win_check(board,move):
    
    return ((board[7] == move and board[8] == move and board[9] == move) 
    or 
    (board[4] == move and board[5] == move and board[6] == move) 
    or
    (board[1] == move and board[2] == move and board[3] == move)
     or
    (board[7] == move and board[4] == move and board[1] == move) 
     or 
    (board[8] == move and board[5] == move and board[2] == move) 
    or 
    (board[9] == move and board[6] == move and board[3] == move) 
    or 
    (board[7] == move and board[5] == move and board[3] == move) 
    or 
    (board[9] == move and board[5] == move and board[1] == move)
    ) 

def check_space(board, position):
     
     return board[position] == ' '

def full_or_not(board):
      
      for i in range(1,10):
         if check_space(board,i): 
            return False
      return True

def player_move(board):
     position = 0
     board_list = [1,2,3,4,5,6,7,8,9] 
     while position not in board_list or not check_space(board,position):
         position = int(input('Select your next move(1-9): ' ))
     return position

def play_again():
      
    replay = input('Do you want to play again? Yes or No: ')
    if replay == 'y':
        return True

print ('Welcome to Tic Tac Toe!') 

while True:
    
    
    gameboard= [' '] * 10 
    player1_move, player2_move = player_input()
    turn = player_first()
    print (turn + ' you will play your move first')
    
    play_game = input('Press y to play')
    
    if play_game[0] == 'y':
       game_start = True
    else:
       game_start = False
       
       
    while game_start:

        if turn == 'Player 1':
            game_board(gameboard)
            position = player_move(gameboard)
            player_place(gameboard, player1_move, position)
          
            if win_check(gameboard, player1_move):
                game_board(gameboard)
                print ('Congratulations! You won the game!')
                game_start = False
            else:
                if full_or_not(gameboard):
                    game_board(gameboard)
                    print ('Game is end, nobody won this time.')
                    break
                 
                else:
                    turn = 'Player 2'

        else:
           
           game_board(gameboard)
           position = player_move(gameboard)
           player_place(gameboard, player2_move, position)
          
           if win_check(gameboard, player2_move):
               game_board(gameboard)
               print ('Congratulations! You won the game!')
               game_start = False
           else:
               if full_or_not(gameboard):
                   game_board(gameboard)
                   print ('Game is end, nobody won this time.')
                   break
                 
               else:
                   turn = 'Player 1'
          
          
    if not play_again():
        break
        
    
