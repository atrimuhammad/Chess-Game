#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# All Chess Pieces are represented by English Alphabets and if a there is more than 1 piece of same kind. Then, we also appended
# number with it. Like, R1 & R2 represents 2 Rook pieces of AI.
# AI Chess Pieces are represented by Capital English Alphabets i.e. R1, K1, B1, etc.

# AI Chess Pieces --v

    # P1, P2, P3, P4, P5, P6, P7, P8 -> AI Pawns
    # R1, R2 -> AI Rooks
    # K1, K2 -> AI Knights
    # B1, B2 -> AI Bishops
    # Q -> AI Queen
    # K -> AI King
    
# Player Chess Pieces --v

    # p1, p2, p3, p4, p5, p6, p7, p8 -> Player Pawns
    # r1, r2 -> Player Rooks
    # k1, k2 -> Player Kinghts
    # b1, b2 -> Player Bishops
    # q -> Player Queen
    # k -> Player King

import numpy as np
import pandas as pd
import copy

chess_board = [['R1','K1','B1','Q1','KK1','B2','K2','R2'],
               ['P1','P2','P3','P4','P5','P6','P7','P8'],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               ['p1','p2','p3','p4','p5','p6','p7','p8'],
               ['r1','k1','b1','q1','kk1','b2','k2','r2']]

player_pawns_move_no = {'p1': 0, 'p2': 0, 'p3': 0, 'p4': 0, 'p5': 0, 'p6': 0, 'p7': 0, 'p8': 0}
AI_pawns_move_no = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0, 'P5': 0, 'P6': 0, 'P7': 0, 'P8': 0}

def find_current_cell_of_piece(piece):
    i_t = 0
    j_t = 0
    
    flag = False
    
    for i in range(0, 8):
        for j in range(0, 8):
            if chess_board[i][j] == piece:
                i_t = i
                j_t = j
                flag = True
                break
        
        if flag == True:
            break
    
    return i_t, j_t

def find_cell_to_where_piece_has_to_be_moved(position):
    i_ = 0
    j_ = 0
    
    if position[1] == '1':
        i_ = 7
    if position[1] == '2':
        i_ = 6
    if position[1] == '3':
        i_ = 5
    if position[1] == '4':
        i_ = 4
    if position[1] == '5':
        i_ = 3
    if position[1] == '6':
        i_ = 2
    if position[1] == '7':
        i_ = 1
    if position[1] == '8':
        i_ = 0
        
    if position[0] == 'a':
        j_ = 0
    if position[0] == 'b':
        j_ = 1
    if position[0] == 'c':
        j_ = 2
    if position[0] == 'd':
        j_ = 3
    if position[0] == 'e':
        j_ = 4
    if position[0] == 'f':
        j_ = 5
    if position[0] == 'g':
        j_ = 6
    if position[0] == 'h':
        j_ = 7
    
    return i_, j_

def check_p_pawn_move_validity(p_piece, p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y):
    move_direction = ''
    
    if ((p_piece_current_position_y == p_piece_next_position_y) and (p_piece_current_position_x == p_piece_next_position_x)):
        return False
    
    # Pawn Never Moves Backward
    if p_piece_next_position_x >= p_piece_current_position_x:
        move_direction = 'invalid'
        return False, move_direction
    
    # If pawn has already been moved, it can not move more than 1 square at a time.
    if player_pawns_move_no[p_piece] != 0:
        if (p_piece_current_position_x - p_piece_next_position_x) > 1:
            move_direction = 'invalid'
            return False, move_direction

    # If pawn has not already been moved, it can not move more than 2 squares at a time
    if player_pawns_move_no[p_piece] == 0:
        if (p_piece_current_position_x - p_piece_next_position_x) > 2:
            move_direction = 'invalid'
            return False, move_direction

    # Other than straight or immediate forward diagonal move
    # Not straight move
    if p_piece_current_position_y != p_piece_next_position_y:
        if (p_piece_next_position_y - p_piece_current_position_y) != 1 and (p_piece_next_position_y - p_piece_current_position_y) != -1:
            move_direction = 'invalid'
            return False, move_direction
    
    # If immediate diagonal, but on immediate diagonal there is no opponent chess piece or there is player's own chess piece
    if p_piece_current_position_y != p_piece_next_position_y:
        if ((chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P1') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P2') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P3') and
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P4') and
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P5') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P6') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P7') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P8') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R1') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R2') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K1') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K2') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B1') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B2') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q1') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'KK1') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q2') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q3') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q4') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q5') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q6') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q7') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q8') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q9') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R3') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R4') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R5') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R6') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R7') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R8') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R9') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R10') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B3') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B4') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B5') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B6') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B7') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B8') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B9') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B10') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K3') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K4') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K5') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K6') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K7') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K8') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K9') and 
            (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K10')):
            move_direction = 'invalid'
            return False, move_direction

    # If pawn want to move 1 square ahead and immediate next square is not empty
    if p_piece_current_position_y == p_piece_next_position_y:
        if (p_piece_current_position_x - p_piece_next_position_x) == 1:
            if chess_board[p_piece_next_position_x][p_piece_next_position_y] != 0:
                move_direction = 'invalid'
                return False, move_direction

    # If pawn want to move 2 sqaure ahead and immediate next square or square after immediate next is not empty
    if p_piece_current_position_y == p_piece_next_position_y:
        if (p_piece_current_position_x - p_piece_next_position_x) == 2:
            if chess_board[p_piece_next_position_x][p_piece_next_position_y] != 0 or chess_board[p_piece_next_position_x - 1][p_piece_next_position_y] != 0:
                move_direction = 'invalid'
                return False, move_direction
            
    if p_piece_current_position_y == p_piece_next_position_y:
        move_direction = 'straight'
    else:
        move_direction = 'diagonal'

    return True, move_direction

def check_p_king_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y):
    if ((p_piece_current_position_y == p_piece_next_position_y) and (p_piece_current_position_x == p_piece_next_position_x)):
        return False
    
    # If destination is more than 1 square away
    if (not(((p_piece_next_position_x == (p_piece_current_position_x - 1)) and (p_piece_next_position_y == p_piece_current_position_y)) or 
        ((p_piece_next_position_x == (p_piece_current_position_x + 1)) and (p_piece_next_position_y == p_piece_current_position_y)) or 
        ((p_piece_next_position_x == p_piece_current_position_x) and (p_piece_next_position_y == (p_piece_current_position_y + 1))) or 
        ((p_piece_next_position_x == p_piece_current_position_x) and (p_piece_next_position_y == (p_piece_current_position_y - 1))) or 
        ((p_piece_next_position_x == (p_piece_current_position_x - 1)) and (p_piece_next_position_y == (p_piece_current_position_y - 1))) or 
        ((p_piece_next_position_x == (p_piece_current_position_x - 1)) and (p_piece_next_position_y == (p_piece_current_position_y + 1))) or 
        ((p_piece_next_position_x == (p_piece_current_position_x + 1)) and (p_piece_next_position_y == (p_piece_current_position_y - 1))) or 
        ((p_piece_next_position_x == (p_piece_current_position_x + 1)) and (p_piece_next_position_y == (p_piece_current_position_y + 1))))):
        return False

    # If on destination square is not empty or there is player's chess piece
    if ((chess_board[p_piece_next_position_x][p_piece_next_position_y] != 0) and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P3') and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'KK1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K10')):
        return False
    
    return True

def check_p_knight_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y):
    if ((p_piece_current_position_y == p_piece_next_position_y) and (p_piece_current_position_x == p_piece_next_position_x)):
        return False

    # If on destination square is not empty or there is player's chess piece
    if ((chess_board[p_piece_next_position_x][p_piece_next_position_y] != 0) and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P3') and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'KK1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K10')):
        return False
    
    # ----
    # UP RIGHT
    i0 = p_piece_current_position_x
    j0 = p_piece_current_position_y
    
    i0-=2
    j0+=1
    
    if ((i0 == p_piece_next_position_x) and (j0 == p_piece_next_position_y)):
        return True
        
    # UP LEFT
    i1 = p_piece_current_position_x
    j1 = p_piece_current_position_y

    i1-=2
    j1-=1
    
    if ((i1 == p_piece_next_position_x) and (j1 == p_piece_next_position_y)):
        return True
    
    # ----
    # DOWN RIGHT
    i2 = p_piece_current_position_x
    j2 = p_piece_current_position_y
    
    i2+=2
    j2-=1
    
    if ((i2 == p_piece_next_position_x) and (j2 == p_piece_next_position_y)):
        return True
        
    # DOWN LEFT
    i3 = p_piece_current_position_x
    j3 = p_piece_current_position_y

    i3+=2
    j3+=1
    
    if ((i3 == p_piece_next_position_x) and (j3 == p_piece_next_position_y)):
        return True
    
    # -----
    # RIGHT RIGHT
    i4 = p_piece_current_position_x
    j4 = p_piece_current_position_y
    
    i4-=1
    j4+=2
    
    if ((i4 == p_piece_next_position_x) and (j4 == p_piece_next_position_y)):
        return True
        
    # RIGHT LEFT
    i5 = p_piece_current_position_x
    j5 = p_piece_current_position_y

    i5+=1
    j5+=2
    
    if ((i5 == p_piece_next_position_x) and (j5 == p_piece_next_position_y)):
        return True
    
    # ----
    # LEFT RIGHT
    i6 = p_piece_current_position_x
    j6 = p_piece_current_position_y
    
    i6+=1
    j6-=2
    
    if ((i6 == p_piece_next_position_x) and (j6 == p_piece_next_position_y)):
        return True
        
    # LEFT LEFT
    i7 = p_piece_current_position_x
    j7 = p_piece_current_position_y

    i7-=1
    j7-=2
    
    if ((i7 == p_piece_next_position_x) and (j7 == p_piece_next_position_y)):
        return True
    
    return False

def check_p_rook_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y):
    valid = False
    
    if ((p_piece_current_position_y == p_piece_next_position_y) and (p_piece_current_position_x == p_piece_next_position_x)):
        return False
    
    # If on destination square is not empty or there is player's chess piece
    if ((chess_board[p_piece_next_position_x][p_piece_next_position_y] != 0) and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P3') and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'KK1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K10')):
        return False
        
    # If rook next position is in same column
    if p_piece_current_position_y == p_piece_next_position_y:
        # If moved upward in same column
        if p_piece_next_position_x < p_piece_current_position_x:
            i = p_piece_current_position_x
            
            valid = True
            
            # Checking whether the upward vertical path to destination is blocked or not by player's own or opponent chess piece
            while i > p_piece_next_position_x:
                i-=1
                
                if chess_board[i][p_piece_next_position_y] != 0:
                    valid = False
                    break
                
            if valid == False:
                return False
            else:
                return True
            
        # If moved downward in same column
        elif p_piece_next_position_x > p_piece_current_position_x:
            i = p_piece_current_position_x
            
            valid = True
            
            # Checking whether the downward vertical path to destination is blocked or not by player's own or opponent chess piece
            while i < p_piece_next_position_x:
                i+=1
                
                if chess_board[i][p_piece_next_position_y] != 0:
                    valid = False
                    break
                    
            if valid == False:
                return False
            else:
                return True
            
    # If rook next position is in same row
    elif p_piece_current_position_x == p_piece_next_position_x:
        # If moved Right in same row
        if p_piece_next_position_y > p_piece_current_position_y:
            j = p_piece_current_position_y
            
            valid = True
            
            # Checking whether the right horizontal path to destination is blocked or not by player's own or opponent chess piece
            while j < p_piece_next_position_y:
                j+=1
                
                if chess_board[p_piece_next_position_x][j] != 0:
                    valid = False
                    break

            if valid == False:
                return False
            else:
                return True
            
        # If moved Left in same row
        elif p_piece_next_position_y < p_piece_current_position_y:
            j = p_piece_current_position_y
            
            valid = True
            
            # Checking whether the left horizontal path to destination is blocked or not by player's own or opponent chess piece
            while j > p_piece_next_position_x:
                j-=1
                
                if chess_board[p_piece_next_position_x][j] != 0:
                    valid = False
                    break

            if valid == False:
                return False
            else:
                return True
            
    else:
        return False

def check_p_bishop_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y):
    valid = False
    valid1 = False
    
    if ((p_piece_current_position_y == p_piece_next_position_y) and (p_piece_current_position_x == p_piece_next_position_x)):
        return False

    # If on destination square is not empty or there is player's chess piece
    if ((chess_board[p_piece_next_position_x][p_piece_next_position_y] != 0) and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P3') and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'KK1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K10')):
        return False
    
    # UP LEFT SEGMENT
    if ((p_piece_next_position_x < p_piece_current_position_x) and (p_piece_next_position_y < p_piece_current_position_y)):
        i = p_piece_current_position_x
        j = p_piece_current_position_y
        
        valid = False
        
        while i >= 0 and j >= 0:
            i-=1
            j-=1
            
            if ((i == p_piece_next_position_x) and (j == p_piece_next_position_y)):
                valid = True
                break
                
        if valid == False:
            return False
        else:
            i_ = p_piece_current_position_x
            j_ = p_piece_current_position_y
            
            valid1 = False
            
            while ((i > p_piece_next_position_x) and (j > p_piece_next_position_y)):
                i_-=1
                j_-=1
                
                if chess_board[i][j] != 0:
                    valid1 = False
                    break
            
            if valid1 == False:
                return False
            else:
                return True
        
    # UP RIGHT SEGMENT
    elif ((p_piece_next_position_x < p_piece_current_position_x) and (p_piece_next_position_y > p_piece_current_position_y)):
        i = p_piece_current_position_x
        j = p_piece_current_position_y
        
        valid = False
        
        while i >= 0 and j <= 7:
            i-=1
            j+=1
            
            if ((i == p_piece_next_position_x) and (j == p_piece_next_position_y)):
                valid = True
                break
                
        if valid == False:
            return False
        else:
            i_ = p_piece_current_position_x
            j_ = p_piece_current_position_y
            
            valid1 = False
            
            while ((i > p_piece_next_position_x) and (j < p_piece_next_position_y)):
                i_-=1
                j_+=1
                
                if chess_board[i][j] != 0:
                    valid1 = False
                    break
            
            if valid1 == False:
                return False
            else:
                return True
        
    # DOWN LEFT SEGMENT
    elif ((p_piece_next_position_x > p_piece_current_position_x) and (p_piece_next_position_y < p_piece_current_position_y)):
        i = p_piece_current_position_x
        j = p_piece_current_position_y
        
        valid = False
        
        while i <= 7 and j >= 0:
            i+=1
            j-=1
            
            if ((i == p_piece_next_position_x) and (j == p_piece_next_position_y)):
                valid = True
                break
                
        if valid == False:
            return False
        else:
            i_ = p_piece_current_position_x
            j_ = p_piece_current_position_y
            
            valid1 = False
            
            while ((i < p_piece_next_position_x) and (j > p_piece_next_position_y)):
                i_+=1
                j_-=1
                
                if chess_board[i][j] != 0:
                    valid1 = False
                    break
            
            if valid1 == False:
                return False
            else:
                return True
        
    # DOWN RIGHT SEGMENT
    elif ((p_piece_next_position_x > p_piece_current_position_x) and (p_piece_next_position_y > p_piece_current_position_y)):
        i = p_piece_current_position_x
        j = p_piece_current_position_y
        
        valid = False
        
        while i <= 7 and j <= 7:
            i+=1
            j+=1
            
            if ((i == p_piece_next_position_x) and (j == p_piece_next_position_y)):
                valid = True
                break
                
        if valid == False:
            return False
        else:
            i_ = p_piece_current_position_x
            j_ = p_piece_current_position_y
            
            valid1 = False
            
            while ((i < p_piece_next_position_x) and (j < p_piece_next_position_y)):
                i_+=1
                j_+=1
                
                if chess_board[i][j] != 0:
                    valid1 = False
                    break
            
            if valid1 == False:
                return False
            else:
                return True
        
    else:
        return False

def check_p_queen_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y):
    if ((p_piece_current_position_y == p_piece_next_position_y) and (p_piece_current_position_x == p_piece_next_position_x)):
        return False

    # If on destination square is not empty or there is player's chess piece
    if ((chess_board[p_piece_next_position_x][p_piece_next_position_y] != 0) and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P3') and
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'P8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'KK1') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q2') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'Q9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'R10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'B10') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K3') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K4') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K5') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K6') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K7') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K8') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K9') and 
        (chess_board[p_piece_next_position_x][p_piece_next_position_y] != 'K10')):
        return False
    
    # If queen next position is in same column
    if p_piece_current_position_y == p_piece_next_position_y:
        # If moved upward in same column
        if p_piece_next_position_x < p_piece_current_position_x:
            i = p_piece_current_position_x
            
            valid = True
            
            # Checking whether the upward vertical path to destination is blocked or not by player's own or opponent chess piece
            while i > p_piece_next_position_x:
                i-=1
                
                if chess_board[i][p_piece_next_position_y] != 0:
                    valid = False
                    break
                
            if valid == False:
                return False
            else:
                return True
            
        # If moved downward in same column
        elif p_piece_next_position_x > p_piece_current_position_x:
            i = p_piece_current_position_x
            
            valid = True
            
            # Checking whether the downward vertical path to destination is blocked or not by player's own or opponent chess piece
            while i < p_piece_next_position_x:
                i+=1
                
                if chess_board[i][p_piece_next_position_y] != 0:
                    valid = False
                    break
                    
            if valid == False:
                return False
            else:
                return True
            
    # If queen next position is in same row
    elif p_piece_current_position_x == p_piece_next_position_x:
        # If moved Right in same row
        if p_piece_next_position_y > p_piece_current_position_y:
            j = p_piece_current_position_y
            
            valid = True
            
            # Checking whether the right horizontal path to destination is blocked or not by player's own or opponent chess piece
            while j < p_piece_next_position_y:
                j+=1
                
                if chess_board[p_piece_next_position_x][j] != 0:
                    valid = False
                    break

            if valid == False:
                return False
            else:
                return True
            
        # If moved Left in same row
        elif p_piece_next_position_y < p_piece_current_position_y:
            j = p_piece_current_position_y
            
            valid = True
            
            # Checking whether the left horizontal path to destination is blocked or not by player's own or opponent chess piece
            while j > p_piece_next_position_x:
                j-=1
                
                if chess_board[p_piece_next_position_x][j] != 0:
                    valid = False
                    break

            if valid == False:
                return False
            else:
                return True

    # UP LEFT SEGMENT
    elif ((p_piece_next_position_x < p_piece_current_position_x) and (p_piece_next_position_y < p_piece_current_position_y)):
        i = p_piece_current_position_x
        j = p_piece_current_position_y
        
        valid = False
        
        while i >= 0 and j >= 0:
            i-=1
            j-=1
            
            if ((i == p_piece_next_position_x) and (j == p_piece_next_position_y)):
                valid = True
                break
                
        if valid == False:
            return False
        else:
            i_ = p_piece_current_position_x
            j_ = p_piece_current_position_y
            
            valid1 = False
            
            while ((i > p_piece_next_position_x) and (j > p_piece_next_position_y)):
                i_-=1
                j_-=1
                
                if chess_board[i][j] != 0:
                    valid1 = False
                    break
            
            if valid1 == False:
                return False
            else:
                return True
        
    # UP RIGHT SEGMENT
    elif ((p_piece_next_position_x < p_piece_current_position_x) and (p_piece_next_position_y > p_piece_current_position_y)):
        i = p_piece_current_position_x
        j = p_piece_current_position_y
        
        valid = False
        
        while i >= 0 and j <= 7:
            i-=1
            j+=1
            
            if ((i == p_piece_next_position_x) and (j == p_piece_next_position_y)):
                valid = True
                break
                
        if valid == False:
            return False
        else:
            i_ = p_piece_current_position_x
            j_ = p_piece_current_position_y
            
            valid1 = False
            
            while ((i > p_piece_next_position_x) and (j < p_piece_next_position_y)):
                i_-=1
                j_+=1
                
                if chess_board[i][j] != 0:
                    valid1 = False
                    break
            
            if valid1 == False:
                return False
            else:
                return True
        
    # DOWN LEFT SEGMENT
    elif ((p_piece_next_position_x > p_piece_current_position_x) and (p_piece_next_position_y < p_piece_current_position_y)):
        i = p_piece_current_position_x
        j = p_piece_current_position_y
        
        valid = False
        
        while i <= 7 and j >= 0:
            i+=1
            j-=1
            
            if ((i == p_piece_next_position_x) and (j == p_piece_next_position_y)):
                valid = True
                break
                
        if valid == False:
            return False
        else:
            i_ = p_piece_current_position_x
            j_ = p_piece_current_position_y
            
            valid1 = False
            
            while ((i < p_piece_next_position_x) and (j > p_piece_next_position_y)):
                i_+=1
                j_-=1
                
                if chess_board[i][j] != 0:
                    valid1 = False
                    break
            
            if valid1 == False:
                return False
            else:
                return True
        
    # DOWN RIGHT SEGMENT
    elif ((p_piece_next_position_x > p_piece_current_position_x) and (p_piece_next_position_y > p_piece_current_position_y)):
        i = p_piece_current_position_x
        j = p_piece_current_position_y
        
        valid = False
        
        while i <= 7 and j <= 7:
            i+=1
            j+=1
            
            if ((i == p_piece_next_position_x) and (j == p_piece_next_position_y)):
                valid = True
                break
                
        if valid == False:
            return False
        else:
            i_ = p_piece_current_position_x
            j_ = p_piece_current_position_y
            
            valid1 = False
            
            while ((i < p_piece_next_position_x) and (j < p_piece_next_position_y)):
                i_+=1
                j_+=1
                
                if chess_board[i][j] != 0:
                    valid1 = False
                    break
            
            if valid1 == False:
                return False
            else:
                return True
        
    else:
        return False

def finding_present_chess_pieces_of_AI(chess_board):
    present_chess_pieces = dict()
    
    for i in range(0, 8):
        for j in range(0, 8):
            if ((chess_board[i][j] == 'P1') or 
                (chess_board[i][j] == 'P2') or 
                (chess_board[i][j] == 'P3') or
                (chess_board[i][j] == 'P4') or 
                (chess_board[i][j] == 'P5') or 
                (chess_board[i][j] == 'P6') or 
                (chess_board[i][j] == 'P7') or 
                (chess_board[i][j] == 'P8') or 
                (chess_board[i][j] == 'R1') or 
                (chess_board[i][j] == 'R2') or 
                (chess_board[i][j] == 'K1') or 
                (chess_board[i][j] == 'K2') or 
                (chess_board[i][j] == 'B1') or 
                (chess_board[i][j] == 'B2') or 
                (chess_board[i][j] == 'Q1') or 
                (chess_board[i][j] == 'KK1') or 
                (chess_board[i][j] == 'Q2') or 
                (chess_board[i][j] == 'Q3') or 
                (chess_board[i][j] == 'Q4') or 
                (chess_board[i][j] == 'Q5') or 
                (chess_board[i][j] == 'Q6') or 
                (chess_board[i][j] == 'Q7') or 
                (chess_board[i][j] == 'Q8') or 
                (chess_board[i][j] == 'Q9') or 
                (chess_board[i][j] == 'R3') or 
                (chess_board[i][j] == 'R4') or 
                (chess_board[i][j] == 'R5') or 
                (chess_board[i][j] == 'R6') or 
                (chess_board[i][j] == 'R7') or 
                (chess_board[i][j] == 'R8') or 
                (chess_board[i][j] == 'R9') or 
                (chess_board[i][j] == 'R10') or 
                (chess_board[i][j] == 'B3') or 
                (chess_board[i][j] == 'B4') or 
                (chess_board[i][j] == 'B5') or 
                (chess_board[i][j] == 'B6') or 
                (chess_board[i][j] == 'B7') or 
                (chess_board[i][j] == 'B8') or 
                (chess_board[i][j] == 'B9') or 
                (chess_board[i][j] == 'B10') or 
                (chess_board[i][j] == 'K3') or 
                (chess_board[i][j] == 'K4') or 
                (chess_board[i][j] == 'K5') or 
                (chess_board[i][j] == 'K6') or 
                (chess_board[i][j] == 'K7') or 
                (chess_board[i][j] == 'K8') or 
                (chess_board[i][j] == 'K9') or 
                (chess_board[i][j] == 'K10')):
                loc_i = str(i)
                loc_j = str(j)
                loc = ''
                loc+=loc_i
                loc+=loc_j
                
                present_chess_pieces[chess_board[i][j]] = loc

    return present_chess_pieces

def finding_present_chess_pieces(chess_board):
    present_chess_pieces = dict()
    
    for i in range(0, 8):
        for j in range(0, 8):
            if ((chess_board[i][j] == 'P1') or 
                (chess_board[i][j] == 'P2') or 
                (chess_board[i][j] == 'P3') or
                (chess_board[i][j] == 'P4') or 
                (chess_board[i][j] == 'P5') or 
                (chess_board[i][j] == 'P6') or 
                (chess_board[i][j] == 'P7') or 
                (chess_board[i][j] == 'P8') or 
                (chess_board[i][j] == 'R1') or 
                (chess_board[i][j] == 'R2') or 
                (chess_board[i][j] == 'K1') or 
                (chess_board[i][j] == 'K2') or 
                (chess_board[i][j] == 'B1') or 
                (chess_board[i][j] == 'B2') or 
                (chess_board[i][j] == 'Q1') or 
                (chess_board[i][j] == 'KK1') or 
                (chess_board[i][j] == 'Q2') or 
                (chess_board[i][j] == 'Q3') or 
                (chess_board[i][j] == 'Q4') or 
                (chess_board[i][j] == 'Q5') or 
                (chess_board[i][j] == 'Q6') or 
                (chess_board[i][j] == 'Q7') or 
                (chess_board[i][j] == 'Q8') or 
                (chess_board[i][j] == 'Q9') or 
                (chess_board[i][j] == 'R3') or 
                (chess_board[i][j] == 'R4') or 
                (chess_board[i][j] == 'R5') or 
                (chess_board[i][j] == 'R6') or 
                (chess_board[i][j] == 'R7') or 
                (chess_board[i][j] == 'R8') or 
                (chess_board[i][j] == 'R9') or 
                (chess_board[i][j] == 'R10') or 
                (chess_board[i][j] == 'B3') or 
                (chess_board[i][j] == 'B4') or 
                (chess_board[i][j] == 'B5') or 
                (chess_board[i][j] == 'B6') or 
                (chess_board[i][j] == 'B7') or 
                (chess_board[i][j] == 'B8') or 
                (chess_board[i][j] == 'B9') or 
                (chess_board[i][j] == 'B10') or 
                (chess_board[i][j] == 'K3') or 
                (chess_board[i][j] == 'K4') or 
                (chess_board[i][j] == 'K5') or 
                (chess_board[i][j] == 'K6') or 
                (chess_board[i][j] == 'K7') or 
                (chess_board[i][j] == 'K8') or 
                (chess_board[i][j] == 'K9') or 
                (chess_board[i][j] == 'K10') or
               
                (chess_board[i][j] == 'p1') or 
                (chess_board[i][j] == 'p2') or 
                (chess_board[i][j] == 'p3') or
                (chess_board[i][j] == 'p4') or 
                (chess_board[i][j] == 'p5') or 
                (chess_board[i][j] == 'p6') or 
                (chess_board[i][j] == 'p7') or 
                (chess_board[i][j] == 'p8') or 
                (chess_board[i][j] == 'r1') or 
                (chess_board[i][j] == 'r2') or 
                (chess_board[i][j] == 'k1') or 
                (chess_board[i][j] == 'k2') or 
                (chess_board[i][j] == 'b1') or 
                (chess_board[i][j] == 'b2') or 
                (chess_board[i][j] == 'q1') or 
                (chess_board[i][j] == 'kk1') or 
                (chess_board[i][j] == 'q2') or 
                (chess_board[i][j] == 'q3') or 
                (chess_board[i][j] == 'q4') or 
                (chess_board[i][j] == 'q5') or 
                (chess_board[i][j] == 'q6') or 
                (chess_board[i][j] == 'q7') or 
                (chess_board[i][j] == 'q8') or 
                (chess_board[i][j] == 'q9') or 
                (chess_board[i][j] == 'r3') or 
                (chess_board[i][j] == 'r4') or 
                (chess_board[i][j] == 'r5') or 
                (chess_board[i][j] == 'r6') or 
                (chess_board[i][j] == 'r7') or 
                (chess_board[i][j] == 'r8') or 
                (chess_board[i][j] == 'r9') or 
                (chess_board[i][j] == 'r10') or 
                (chess_board[i][j] == 'b3') or 
                (chess_board[i][j] == 'b4') or 
                (chess_board[i][j] == 'b5') or 
                (chess_board[i][j] == 'b6') or 
                (chess_board[i][j] == 'b7') or 
                (chess_board[i][j] == 'b8') or 
                (chess_board[i][j] == 'b9') or 
                (chess_board[i][j] == 'b10') or 
                (chess_board[i][j] == 'k3') or 
                (chess_board[i][j] == 'k4') or 
                (chess_board[i][j] == 'k5') or 
                (chess_board[i][j] == 'k6') or 
                (chess_board[i][j] == 'k7') or 
                (chess_board[i][j] == 'k8') or 
                (chess_board[i][j] == 'k9') or 
                (chess_board[i][j] == 'k10')):
                loc_i = str(i)
                loc_j = str(j)
                loc = ''
                loc+=loc_i
                loc+=loc_j
                
                present_chess_pieces[chess_board[i][j]] = loc

    return present_chess_pieces

def finding_present_chess_pieces_of_player(chess_board):
    present_chess_pieces = dict()
    
    for i in range(0, 8):
        for j in range(0, 8):
            if ((chess_board[i][j] == 'p1') or 
                (chess_board[i][j] == 'p2') or 
                (chess_board[i][j] == 'p3') or
                (chess_board[i][j] == 'p4') or 
                (chess_board[i][j] == 'p5') or 
                (chess_board[i][j] == 'p6') or 
                (chess_board[i][j] == 'p7') or 
                (chess_board[i][j] == 'p8') or 
                (chess_board[i][j] == 'r1') or 
                (chess_board[i][j] == 'r2') or 
                (chess_board[i][j] == 'k1') or 
                (chess_board[i][j] == 'k2') or 
                (chess_board[i][j] == 'b1') or 
                (chess_board[i][j] == 'b2') or 
                (chess_board[i][j] == 'q1') or 
                (chess_board[i][j] == 'kk1') or 
                (chess_board[i][j] == 'q2') or 
                (chess_board[i][j] == 'q3') or 
                (chess_board[i][j] == 'q4') or 
                (chess_board[i][j] == 'q5') or 
                (chess_board[i][j] == 'q6') or 
                (chess_board[i][j] == 'q7') or 
                (chess_board[i][j] == 'q8') or 
                (chess_board[i][j] == 'q9') or 
                (chess_board[i][j] == 'r3') or 
                (chess_board[i][j] == 'r4') or 
                (chess_board[i][j] == 'r5') or 
                (chess_board[i][j] == 'r6') or 
                (chess_board[i][j] == 'r7') or 
                (chess_board[i][j] == 'r8') or 
                (chess_board[i][j] == 'r9') or 
                (chess_board[i][j] == 'r10') or 
                (chess_board[i][j] == 'b3') or 
                (chess_board[i][j] == 'b4') or 
                (chess_board[i][j] == 'b5') or 
                (chess_board[i][j] == 'b6') or 
                (chess_board[i][j] == 'b7') or 
                (chess_board[i][j] == 'b8') or 
                (chess_board[i][j] == 'b9') or 
                (chess_board[i][j] == 'b10') or 
                (chess_board[i][j] == 'k3') or 
                (chess_board[i][j] == 'k4') or 
                (chess_board[i][j] == 'k5') or 
                (chess_board[i][j] == 'k6') or 
                (chess_board[i][j] == 'k7') or 
                (chess_board[i][j] == 'k8') or 
                (chess_board[i][j] == 'k9') or 
                (chess_board[i][j] == 'k10')):
                loc_i = str(i)
                loc_j = str(j)
                loc = ''
                loc+=loc_i
                loc+=loc_j
                
                present_chess_pieces[chess_board[i][j]] = loc

    return present_chess_pieces

def oppoent_piece(chess_board, i, j):
    if ((chess_board[i][j] != 'p1') and 
        (chess_board[i][j] != 'p2') and 
        (chess_board[i][j] != 'p3') and
        (chess_board[i][j] != 'p4') and 
        (chess_board[i][j] != 'p5') and 
        (chess_board[i][j] != 'p6') and 
        (chess_board[i][j] != 'p7') and 
        (chess_board[i][j] != 'p8') and 
        (chess_board[i][j] != 'r1') and 
        (chess_board[i][j] != 'r2') and 
        (chess_board[i][j] != 'k1') and 
        (chess_board[i][j] != 'k2') and 
        (chess_board[i][j] != 'b1') and 
        (chess_board[i][j] != 'b2') and 
        (chess_board[i][j] != 'q1') and 
        (chess_board[i][j] != 'kk1') and 
        (chess_board[i][j] != 'q2') and 
        (chess_board[i][j] != 'q3') and 
        (chess_board[i][j] != 'q4') and 
        (chess_board[i][j] != 'q5') and 
        (chess_board[i][j] != 'q6') and 
        (chess_board[i][j] != 'q7') and 
        (chess_board[i][j] != 'q8') and 
        (chess_board[i][j] != 'q9') and 
        (chess_board[i][j] != 'r3') and 
        (chess_board[i][j] != 'r4') and 
        (chess_board[i][j] != 'r5') and 
        (chess_board[i][j] != 'r6') and 
        (chess_board[i][j] != 'r7') and 
        (chess_board[i][j] != 'r8') and 
        (chess_board[i][j] != 'r9') and 
        (chess_board[i][j] != 'r10') and 
        (chess_board[i][j] != 'b3') and 
        (chess_board[i][j] != 'b4') and 
        (chess_board[i][j] != 'b5') and 
        (chess_board[i][j] != 'b6') and 
        (chess_board[i][j] != 'b7') and 
        (chess_board[i][j] != 'b8') and 
        (chess_board[i][j] != 'b9') and 
        (chess_board[i][j] != 'b10') and 
        (chess_board[i][j] != 'k3') and 
        (chess_board[i][j] != 'k4') and 
        (chess_board[i][j] != 'k5') and 
        (chess_board[i][j] != 'k6') and 
        (chess_board[i][j] != 'k7') and 
        (chess_board[i][j] != 'k8') and 
        (chess_board[i][j] != 'k9') and 
        (chess_board[i][j] != 'k10')):
        return False
    else:
        return True

def p_empty_or_oppoent_piece(chess_board, i, j):
    if ((chess_board[i][j] != 0) and 
        (chess_board[i][j] != 'P1') and 
        (chess_board[i][j] != 'P2') and 
        (chess_board[i][j] != 'P3') and
        (chess_board[i][j] != 'P4') and 
        (chess_board[i][j] != 'P5') and 
        (chess_board[i][j] != 'P6') and 
        (chess_board[i][j] != 'P7') and 
        (chess_board[i][j] != 'P8') and 
        (chess_board[i][j] != 'R1') and 
        (chess_board[i][j] != 'R2') and 
        (chess_board[i][j] != 'K1') and 
        (chess_board[i][j] != 'K2') and 
        (chess_board[i][j] != 'B1') and 
        (chess_board[i][j] != 'B2') and 
        (chess_board[i][j] != 'Q1') and 
        (chess_board[i][j] != 'KK1') and 
        (chess_board[i][j] != 'Q2') and 
        (chess_board[i][j] != 'Q3') and 
        (chess_board[i][j] != 'Q4') and 
        (chess_board[i][j] != 'Q5') and 
        (chess_board[i][j] != 'Q6') and 
        (chess_board[i][j] != 'Q7') and 
        (chess_board[i][j] != 'Q8') and 
        (chess_board[i][j] != 'Q9') and 
        (chess_board[i][j] != 'R3') and 
        (chess_board[i][j] != 'R4') and 
        (chess_board[i][j] != 'R5') and 
        (chess_board[i][j] != 'R6') and 
        (chess_board[i][j] != 'R7') and 
        (chess_board[i][j] != 'R8') and 
        (chess_board[i][j] != 'R9') and 
        (chess_board[i][j] != 'R10') and 
        (chess_board[i][j] != 'B3') and 
        (chess_board[i][j] != 'B4') and 
        (chess_board[i][j] != 'B5') and 
        (chess_board[i][j] != 'B6') and 
        (chess_board[i][j] != 'B7') and 
        (chess_board[i][j] != 'B8') and 
        (chess_board[i][j] != 'B9') and 
        (chess_board[i][j] != 'B10') and 
        (chess_board[i][j] != 'K3') and 
        (chess_board[i][j] != 'K4') and 
        (chess_board[i][j] != 'K5') and 
        (chess_board[i][j] != 'K6') and 
        (chess_board[i][j] != 'K7') and 
        (chess_board[i][j] != 'K8') and 
        (chess_board[i][j] != 'K9') and 
        (chess_board[i][j] != 'K10')):
        return False
    else:
        return True
    
def empty_or_oppoent_piece(chess_board, i, j):
    if ((chess_board[i][j] != 0) and 
        (chess_board[i][j] != 'p1') and 
        (chess_board[i][j] != 'p2') and 
        (chess_board[i][j] != 'p3') and
        (chess_board[i][j] != 'p4') and 
        (chess_board[i][j] != 'p5') and 
        (chess_board[i][j] != 'p6') and 
        (chess_board[i][j] != 'p7') and 
        (chess_board[i][j] != 'p8') and 
        (chess_board[i][j] != 'r1') and 
        (chess_board[i][j] != 'r2') and 
        (chess_board[i][j] != 'k1') and 
        (chess_board[i][j] != 'k2') and 
        (chess_board[i][j] != 'b1') and 
        (chess_board[i][j] != 'b2') and 
        (chess_board[i][j] != 'q1') and 
        (chess_board[i][j] != 'kk1') and 
        (chess_board[i][j] != 'q2') and 
        (chess_board[i][j] != 'q3') and 
        (chess_board[i][j] != 'q4') and 
        (chess_board[i][j] != 'q5') and 
        (chess_board[i][j] != 'q6') and 
        (chess_board[i][j] != 'q7') and 
        (chess_board[i][j] != 'q8') and 
        (chess_board[i][j] != 'q9') and 
        (chess_board[i][j] != 'r3') and 
        (chess_board[i][j] != 'r4') and 
        (chess_board[i][j] != 'r5') and 
        (chess_board[i][j] != 'r6') and 
        (chess_board[i][j] != 'r7') and 
        (chess_board[i][j] != 'r8') and 
        (chess_board[i][j] != 'r9') and 
        (chess_board[i][j] != 'r10') and 
        (chess_board[i][j] != 'b3') and 
        (chess_board[i][j] != 'b4') and 
        (chess_board[i][j] != 'b5') and 
        (chess_board[i][j] != 'b6') and 
        (chess_board[i][j] != 'b7') and 
        (chess_board[i][j] != 'b8') and 
        (chess_board[i][j] != 'b9') and 
        (chess_board[i][j] != 'b10') and 
        (chess_board[i][j] != 'k3') and 
        (chess_board[i][j] != 'k4') and 
        (chess_board[i][j] != 'k5') and 
        (chess_board[i][j] != 'k6') and 
        (chess_board[i][j] != 'k7') and 
        (chess_board[i][j] != 'k8') and 
        (chess_board[i][j] != 'k9') and 
        (chess_board[i][j] != 'k10')):
        return False
    else:
        return True
    
def Player_Pawn_Possible_Moves(chess_board, pawn, value, STACK):
    pawn_current_i = int(value[0])
    pawn_current_j = int(value[1])
    
    # If its 1st move of pawn
    if player_pawns_move_no[pawn] == 0:
        for i in range(0, 2):
            if i == 0:
                if chess_board[pawn_current_i - 1][pawn_current_j] != 0:
                    break
                else:
                    temp = copy.deepcopy(chess_board)
                    temp[pawn_current_i - 1][pawn_current_j] = temp[pawn_current_i][pawn_current_j]
                    temp[pawn_current_i][pawn_current_j] = 0
                    STACK.append(temp)
                    
            if i == 1:
                if chess_board[pawn_current_i - 2][pawn_current_j] != 0:
                    break
                else:
                    temp = copy.deepcopy(chess_board)
                    temp[pawn_current_i - 2][pawn_current_j] = temp[pawn_current_i][pawn_current_j]
                    temp[pawn_current_i][pawn_current_j] = 0
                    STACK.append(temp)
        
        if (((pawn_current_j - 1) >= 0 and (pawn_current_j - 1) <= 7) and ((pawn_current_i - 1) >= 0 and (pawn_current_i - 1) <= 7)):
            if oppoent_piece(chess_board, (pawn_current_i - 1), (pawn_current_j - 1)) == True:
                temp = copy.deepcopy(chess_board)
                temp[pawn_current_i - 1][pawn_current_j - 1] = temp[pawn_current_i][pawn_current_j]
                temp[pawn_current_i][pawn_current_j] = 0
                STACK.append(temp)
                
        if (((pawn_current_j + 1) >= 0 and (pawn_current_j + 1) <= 7) and ((pawn_current_i - 1) >= 0 and (pawn_current_i - 1) <= 7)):
            if oppoent_piece(chess_board, (pawn_current_i - 1), (pawn_current_j + 1)) == True:
                temp = copy.deepcopy(chess_board)
                temp[pawn_current_i - 1][pawn_current_j + 1] = temp[pawn_current_i][pawn_current_j]
                temp[pawn_current_i][pawn_current_j] = 0
                STACK.append(temp)

    # If it is not 1st move of pawn
    elif player_pawns_move_no[pawn] != 0:
        if chess_board[pawn_current_i - 1][pawn_current_j] == 0:
            temp = copy.deepcopy(chess_board)
            temp[pawn_current_i - 1][pawn_current_j] = temp[pawn_current_i][pawn_current_j]
            temp[pawn_current_i][pawn_current_j] = 0
            STACK.append(temp)
        
        if (((pawn_current_j - 1) >= 0 and (pawn_current_j - 1) <= 7) and ((pawn_current_i - 1) >= 0 and (pawn_current_i - 1) <= 7)):
            if oppoent_piece(chess_board, (pawn_current_i - 1), (pawn_current_j - 1)) == True:
                temp = copy.deepcopy(chess_board)
                temp[pawn_current_i - 1][pawn_current_j - 1] = temp[pawn_current_i][pawn_current_j]
                temp[pawn_current_i][pawn_current_j] = 0
                STACK.append(temp)
        
        if (((pawn_current_j + 1) >= 0 and (pawn_current_j + 1) <= 7) and ((pawn_current_i - 1) >= 0 and (pawn_current_i - 1) <= 7)):
            if oppoent_piece(chess_board, (pawn_current_i - 1), (pawn_current_j + 1)) == True:
                temp = copy.deepcopy(chess_board)
                temp[pawn_current_i - 1][pawn_current_j + 1] = temp[pawn_current_i][pawn_current_j]
                temp[pawn_current_i][pawn_current_j] = 0
                STACK.append(temp)

def Player_Rook_Possible_Moves(chess_board, rook, value, STACK):
    i1 = int(value[0])
    j1 = int(value[1])
    
    rook_current_i = int(value[0])
    rook_current_j = int(value[1])
    
    if i1 != 0:
        # UP Straight
        while i1 >= 0:
            i1-=1
        
            if p_empty_or_oppoent_piece(chess_board, i1, j1) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i1, j1) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i1][j1] = temp[rook_current_i][rook_current_j]
                temp[rook_current_i][rook_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i2 = int(value[0])
    j2 = int(value[1])
    
    if i2 != 7:
        # DOWN Straight
        while i2 <= 7:
            i2+=1
        
            if p_empty_or_oppoent_piece(chess_board, i2, j2) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i2, j2) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i2][j2] = temp[rook_current_i][rook_current_j]
                temp[rook_current_i][rook_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i3 = int(value[0])
    j3 = int(value[1])
    
    if j3 != 0:
        # LEFT Straight
        while j3 >= 0:
            j3-=1
        
            if p_empty_or_oppoent_piece(chess_board, i3, j3) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i3, j3) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i3][j3] = temp[rook_current_i][rook_current_j]
                temp[rook_current_i][rook_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break
                
    i4 = int(value[0])
    j4 = int(value[1])
    
    if j4 != 7:
        # RIGTH Straight
        while j4 <= 7:
            j4+=1
        
            if p_empty_or_oppoent_piece(chess_board, i4, j4) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i4, j4) == True:
                    valid = True
            
                temp = copy.deepcopy(chess_board)
                temp[i4][j4] = temp[rook_current_i][rook_current_j]
                temp[rook_current_i][rook_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break
                
def Player_Bishop_Possible_Moves(chess_board, bishop, value, STACK):
    i1 = int(value[0])
    j1 = int(value[1])
    
    bishop_current_i = int(value[0])
    bishop_current_j = int(value[1])
    
    if i1 > 0 and j1 > 0:
        # UP LEFT
        while i1 >= 0 and j1 >= 0:
            i1-=1
            j1-=1
        
            if p_empty_or_oppoent_piece(chess_board, i1, j1) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i1, j1) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i1][j1] = temp[bishop_current_i][bishop_current_j]
                temp[bishop_current_i][bishop_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i2 = int(value[0])
    j2 = int(value[1])
    
    if i2 > 0 and j2 < 7:
        # UP RIGHT
        while i2 >= 0 and j2 <= 7:
            i2-=1
            j2+=1
        
            if p_empty_or_oppoent_piece(chess_board, i2, j2) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i2, j2) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i2][j2] = temp[bishop_current_i][bishop_current_j]
                temp[bishop_current_i][bishop_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i3 = int(value[0])
    j3 = int(value[1])
    
    if i3 < 7 and j3 > 0:
        # DOWN LEFT
        while i3 <= 7 and j3 >= 0:
            i3+=1
            j3-=1
        
            if p_empty_or_oppoent_piece(chess_board, i3, j3) == False:
                break
            else:
                valid = False
                
                if oppoent_piece(chess_board, i3, j3) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i3][j3] = temp[bishop_current_i][bishop_current_j]
                temp[bishop_current_i][bishop_current_j] = 0
                STACK.append(temp)
    
                if valid == True:
                    break
                
    i4 = int(value[0])
    j4 = int(value[1])
    
    if i4 < 7 and j4 < 7:
    # DOWN RIGHT
        while i4 <= 7 and j4 <= 7:
            i4+=1
            j4+=1
        
            if p_empty_or_oppoent_piece(chess_board, i4, j4) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i4, j4) == True:
                    valid = True
            
                temp = copy.deepcopy(chess_board)
                temp[i4][j4] = temp[bishop_current_i][bishop_current_j]
                temp[bishop_current_i][bishop_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break

def Player_Knight_Possible_Moves(chess_board, knight, value, STACK):
    knight_current_i = int(value[0])
    knight_current_j = int(value[1])
    
    # UP RIGHT
    if knight_current_i > 1 and knight_current_j < 7:
        if p_empty_or_oppoent_piece(chess_board, (knight_current_i - 2), knight_current_j + 1) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i - 2][knight_current_j + 1] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
    
    # UP LEFT
    if knight_current_i > 1 and knight_current_j > 0:
        if p_empty_or_oppoent_piece(chess_board, (knight_current_i - 2), knight_current_j - 1) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i - 2][knight_current_j - 1] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # DOWN RIGHT
    if knight_current_i < 6 and knight_current_j < 7:
        if p_empty_or_oppoent_piece(chess_board, knight_current_i + 2, (knight_current_j + 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i + 2][knight_current_j + 1] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # DOWN LEFT
    if knight_current_i < 6 and knight_current_j > 0:
        if p_empty_or_oppoent_piece(chess_board, knight_current_i + 2, (knight_current_j - 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i + 2][knight_current_j - 1] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # LEFT RIGHT
    if knight_current_j > 1 and knight_current_i > 0:
        if p_empty_or_oppoent_piece(chess_board, (knight_current_i - 1), (knight_current_j - 2)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i - 1][knight_current_j - 2] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # LEFT LEFT
    if knight_current_j > 1 and knight_current_i < 7:
        if p_empty_or_oppoent_piece(chess_board, (knight_current_i + 1), (knight_current_j - 2)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i + 1][knight_current_j - 2] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
     
    # RIGHT RIGHT
    if knight_current_j < 6 and knight_current_i < 7:
        if p_empty_or_oppoent_piece(chess_board, (knight_current_i + 1), (knight_current_j + 2)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i + 1][knight_current_j + 2] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
    
    # RIGHT LEFT
    if knight_current_j < 6  and knight_current_i > 0:
        if p_empty_or_oppoent_piece(chess_board, (knight_current_i - 1), (knight_current_j + 2)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i - 1][knight_current_j + 2] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)

def Player_Queen_Possible_Moves(chess_board, queen, value, STACK):
    i1 = int(value[0])
    j1 = int(value[1])
    
    queen_current_i = int(value[0])
    queen_current_j = int(value[1])
    
    if i1 != 0:
        # UP Straight
        while i1 >= 0:
            i1-=1
        
            if p_empty_or_oppoent_piece(chess_board, i1, j1) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i1, j1) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i1][j1] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i2 = int(value[0])
    j2 = int(value[1])
    
    if i2 != 7:
        # DOWN Straight
        while i2 <= 7:
            i2+=1
        
            if p_empty_or_oppoent_piece(chess_board, i2, j2) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i2, j2) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i2][j2] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i3 = int(value[0])
    j3 = int(value[1])
    
    if j3 != 0:
        # LEFT Straight
        while j3 >= 0:
            j3-=1
        
            if p_empty_or_oppoent_piece(chess_board, i3, j3) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i3, j3) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i3][j3] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break
                
    i4 = int(value[0])
    j4 = int(value[1])
    
    if j4 != 7:
        # RIGTH Straight
        while j4 <= 7:
            j4+=1
        
            if p_empty_or_oppoent_piece(chess_board, i4, j4) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i4, j4) == True:
                    valid = True
            
                temp = copy.deepcopy(chess_board)
                temp[i4][j4] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break
                    
    i5 = int(value[0])
    j5 = int(value[1])
    
    if i5 != 0 and j5 != 0:
        # UP LEFT
        while i5 >= 0 and j5 >= 0:
            i5-=1
            j5-=1
        
            if p_empty_or_oppoent_piece(chess_board, i5, j5) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i5, j5) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i5][j5] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i6 = int(value[0])
    j6 = int(value[1])
    
    if i6 != 0 and j6 != 7:
        # UP RIGHT
        while i6 >= 0 and j6 <= 7:
            i6-=1
            j6+=1
        
            if p_empty_or_oppoent_piece(chess_board, i6, j6) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i6, j6) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i6][j6] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i7 = int(value[0])
    j7 = int(value[1])
    
    if i7 != 7 and j7 != 0:
        # DOWN LEFT
        while i7 <= 7 and j7 >= 0:
            i7+=1
            j7-=1
        
            if p_empty_or_oppoent_piece(chess_board, i7, j7) == False:
                break
            else:
                valid = False
                
                if oppoent_piece(chess_board, i7, j7) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i7][j7] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
    
                if valid == True:
                    break
                
    i8 = int(value[0])
    j8 = int(value[1])
    
    if i8 != 7 and j8 != 7:
    # DOWN RIGHT
        while i8 <= 7 and j8 <= 7:
            i8+=1
            j8+=1
        
            if p_empty_or_oppoent_piece(chess_board, i8, j8) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i8, j8) == True:
                    valid = True
            
                temp = copy.deepcopy(chess_board)
                temp[i8][j8] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break

def Player_King_Possible_Moves(chess_board, king, value, STACK):
    king_current_i = int(value[0])
    king_current_j = int(value[1])
    
    # UP
    if king_current_i != 0:
        if p_empty_or_oppoent_piece(chess_board, (king_current_i - 1), king_current_j) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i - 1][king_current_j] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
    
    # DOWN
    if king_current_i != 7:
        if p_empty_or_oppoent_piece(chess_board, (king_current_i + 1), king_current_j) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i + 1][king_current_j] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # LEFT
    if king_current_j != 0:
        if p_empty_or_oppoent_piece(chess_board, king_current_i, (king_current_j - 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i][king_current_j - 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # RIGHT
    if king_current_j != 7:
        if p_empty_or_oppoent_piece(chess_board, king_current_i, (king_current_j + 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i][king_current_j + 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # UP LEFT
    if king_current_i != 0 and king_current_j != 0:
        if p_empty_or_oppoent_piece(chess_board, (king_current_i - 1), (king_current_j - 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i - 1][king_current_j - 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # UP RIGHT
    if king_current_i != 0 and king_current_j != 7:
        if p_empty_or_oppoent_piece(chess_board, (king_current_i - 1), (king_current_j + 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i - 1][king_current_j + 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # DOWN LEFT
    if king_current_i != 7 and king_current_j != 0:
        if p_empty_or_oppoent_piece(chess_board, (king_current_i + 1), (king_current_j - 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i + 1][king_current_j - 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # DOWN RIGHT
    if king_current_i != 7 and king_current_j != 7:
        if p_empty_or_oppoent_piece(chess_board, (king_current_i + 1), (king_current_j + 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i + 1][king_current_j + 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
                
def AI_Pawn_Possible_Moves(chess_board, pawn, value, STACK):
    pawn_current_i = int(value[0])
    pawn_current_j = int(value[1])
    
    # If its 1st move of pawn
    if AI_pawns_move_no[pawn] == 0:
        for i in range(0, 2):
            if i == 0:
                if chess_board[pawn_current_i + 1][pawn_current_j] != 0:
                    break
                else:
                    temp = copy.deepcopy(chess_board)
                    temp[pawn_current_i + 1][pawn_current_j] = temp[pawn_current_i][pawn_current_j]
                    temp[pawn_current_i][pawn_current_j] = 0
                    STACK.append(temp)
                    
            if i == 1:
                if chess_board[pawn_current_i + 2][pawn_current_j] != 0:
                    break
                else:
                    temp = copy.deepcopy(chess_board)
                    temp[pawn_current_i + 2][pawn_current_j] = temp[pawn_current_i][pawn_current_j]
                    temp[pawn_current_i][pawn_current_j] = 0
                    STACK.append(temp)
        
        if (((pawn_current_j - 1) >= 0 and (pawn_current_j - 1) <= 7) and ((pawn_current_i + 1) >= 0 and (pawn_current_i + 1) <= 7)):
            if oppoent_piece(chess_board, (pawn_current_i + 1), (pawn_current_j - 1)) == True:
                temp = copy.deepcopy(chess_board)
                temp[pawn_current_i + 1][pawn_current_j - 1] = temp[pawn_current_i][pawn_current_j]
                temp[pawn_current_i][pawn_current_j] = 0
                STACK.append(temp)
                
        if (((pawn_current_j + 1) >= 0 and (pawn_current_j + 1) <= 7) and ((pawn_current_i + 1) >= 0 and (pawn_current_i + 1) <= 7)):
            if oppoent_piece(chess_board, (pawn_current_i + 1), (pawn_current_j + 1)) == True:
                temp = copy.deepcopy(chess_board)
                temp[pawn_current_i + 1][pawn_current_j + 1] = temp[pawn_current_i][pawn_current_j]
                temp[pawn_current_i][pawn_current_j] = 0
                STACK.append(temp)

    # If it is not 1st move of pawn
    elif AI_pawns_move_no[pawn] != 0:
        if chess_board[pawn_current_i + 1][pawn_current_j] == 0:
            temp = copy.deepcopy(chess_board)
            temp[pawn_current_i + 1][pawn_current_j] = temp[pawn_current_i][pawn_current_j]
            temp[pawn_current_i][pawn_current_j] = 0
            STACK.append(temp)
        
        if (((pawn_current_j - 1) >= 0 and (pawn_current_j - 1) <= 7) and ((pawn_current_i + 1) >= 0 and (pawn_current_i + 1) <= 7)):
            if oppoent_piece(chess_board, (pawn_current_i + 1), (pawn_current_j - 1)) == True:
                temp = copy.deepcopy(chess_board)
                temp[pawn_current_i + 1][pawn_current_j - 1] = temp[pawn_current_i][pawn_current_j]
                temp[pawn_current_i][pawn_current_j] = 0
                STACK.append(temp)
        
        if (((pawn_current_j + 1) >= 0 and (pawn_current_j + 1) <= 7) and ((pawn_current_i + 1) >= 0 and (pawn_current_i + 1) <= 7)):
            if oppoent_piece(chess_board, (pawn_current_i + 1), (pawn_current_j + 1)) == True:
                temp = copy.deepcopy(chess_board)
                temp[pawn_current_i + 1][pawn_current_j + 1] = temp[pawn_current_i][pawn_current_j]
                temp[pawn_current_i][pawn_current_j] = 0
                STACK.append(temp)
                
def AI_Rook_Possible_Moves(chess_board, rook, value, STACK):
    i1 = int(value[0])
    j1 = int(value[1])
    
    rook_current_i = int(value[0])
    rook_current_j = int(value[1])
    
    if i1 != 0:
        # UP Straight
        while i1 >= 0:
            i1-=1
        
            if empty_or_oppoent_piece(chess_board, i1, j1) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i1, j1) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i1][j1] = temp[rook_current_i][rook_current_j]
                temp[rook_current_i][rook_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i2 = int(value[0])
    j2 = int(value[1])
    
    if i2 != 7:
        # DOWN Straight
        while i2 <= 7:
            i2+=1
        
            if empty_or_oppoent_piece(chess_board, i2, j2) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i2, j2) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i2][j2] = temp[rook_current_i][rook_current_j]
                temp[rook_current_i][rook_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i3 = int(value[0])
    j3 = int(value[1])
    
    if j3 != 0:
        # LEFT Straight
        while j3 >= 0:
            j3-=1
        
            if empty_or_oppoent_piece(chess_board, i3, j3) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i3, j3) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i3][j3] = temp[rook_current_i][rook_current_j]
                temp[rook_current_i][rook_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break
                
    i4 = int(value[0])
    j4 = int(value[1])
    
    if j4 != 7:
        # RIGTH Straight
        while j4 <= 7:
            j4+=1
        
            if empty_or_oppoent_piece(chess_board, i4, j4) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i4, j4) == True:
                    valid = True
            
                temp = copy.deepcopy(chess_board)
                temp[i4][j4] = temp[rook_current_i][rook_current_j]
                temp[rook_current_i][rook_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break
                
def AI_Bishop_Possible_Moves(chess_board, bishop, value, STACK):
    i1 = int(value[0])
    j1 = int(value[1])
    
    bishop_current_i = int(value[0])
    bishop_current_j = int(value[1])
    
    if i1 > 0 and j1 > 0:
        # UP LEFT
        while i1 >= 0 and j1 >= 0:
            i1-=1
            j1-=1
        
            if empty_or_oppoent_piece(chess_board, i1, j1) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i1, j1) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i1][j1] = temp[bishop_current_i][bishop_current_j]
                temp[bishop_current_i][bishop_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i2 = int(value[0])
    j2 = int(value[1])
    
    if i2 > 0 and j2 < 7:
        # UP RIGHT
        while i2 >= 0 and j2 <= 7:
            i2-=1
            j2+=1
        
            if empty_or_oppoent_piece(chess_board, i2, j2) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i2, j2) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i2][j2] = temp[bishop_current_i][bishop_current_j]
                temp[bishop_current_i][bishop_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i3 = int(value[0])
    j3 = int(value[1])
    
    if i3 < 7 and j3 > 0:
        # DOWN LEFT
        while i3 <= 7 and j3 >= 0:
            i3+=1
            j3-=1
        
            if empty_or_oppoent_piece(chess_board, i3, j3) == False:
                break
            else:
                valid = False
                
                if oppoent_piece(chess_board, i3, j3) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i3][j3] = temp[bishop_current_i][bishop_current_j]
                temp[bishop_current_i][bishop_current_j] = 0
                STACK.append(temp)
    
                if valid == True:
                    break
                
    i4 = int(value[0])
    j4 = int(value[1])
    
    if i4 < 7 and j4 < 7:
    # DOWN RIGHT
        while i4 <= 7 and j4 <= 7:
            i4+=1
            j4+=1
        
            if empty_or_oppoent_piece(chess_board, i4, j4) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i4, j4) == True:
                    valid = True
            
                temp = copy.deepcopy(chess_board)
                temp[i4][j4] = temp[bishop_current_i][bishop_current_j]
                temp[bishop_current_i][bishop_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break

def AI_Knight_Possible_Moves(chess_board, knight, value, STACK):
    knight_current_i = int(value[0])
    knight_current_j = int(value[1])
    
    # UP RIGHT
    if knight_current_i > 1:
        if empty_or_oppoent_piece(chess_board, (knight_current_i - 2), knight_current_j + 1) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i - 2][knight_current_j + 1] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
    
    # UP LEFT
    if knight_current_i > 1:
        if empty_or_oppoent_piece(chess_board, (knight_current_i - 2), knight_current_j - 1) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i - 2][knight_current_j - 1] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # DOWN RIGHT
    if knight_current_i < 6:
        if empty_or_oppoent_piece(chess_board, knight_current_i + 2, (knight_current_j + 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i + 2][knight_current_j + 1] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # DOWN LEFT
    if knight_current_i < 6:
        if empty_or_oppoent_piece(chess_board, knight_current_i + 2, (knight_current_j - 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i + 2][knight_current_j - 1] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # LEFT RIGHT
    if knight_current_j > 1:
        if empty_or_oppoent_piece(chess_board, (knight_current_i - 1), (knight_current_j - 2)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i - 1][knight_current_j - 2] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # LEFT LEFT
    if knight_current_j > 1:
        if empty_or_oppoent_piece(chess_board, (knight_current_i + 1), (knight_current_j - 2)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i + 1][knight_current_j - 2] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # RIGHT RIGHT
    if knight_current_j < 6:
        if empty_or_oppoent_piece(chess_board, (knight_current_i + 1), (knight_current_j + 2)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i + 1][knight_current_j + 2] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)
        
    # RIGHT LEFT
    if knight_current_j < 6:
        if empty_or_oppoent_piece(chess_board, (knight_current_i - 1), (knight_current_j + 2)) == True:
            temp = copy.deepcopy(chess_board)
            temp[knight_current_i - 1][knight_current_j + 2] = temp[knight_current_i][knight_current_j]
            temp[knight_current_i][knight_current_j] = 0
            STACK.append(temp)

def AI_Queen_Possible_Moves(chess_board, queen, value, STACK):
    i1 = int(value[0])
    j1 = int(value[1])
    
    queen_current_i = int(value[0])
    queen_current_j = int(value[1])
    
    if i1 != 0:
        # UP Straight
        while i1 >= 0:
            i1-=1
        
            if empty_or_oppoent_piece(chess_board, i1, j1) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i1, j1) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i1][j1] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i2 = int(value[0])
    j2 = int(value[1])
    
    if i2 != 7:
        # DOWN Straight
        while i2 <= 7:
            i2+=1
        
            if empty_or_oppoent_piece(chess_board, i2, j2) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i2, j2) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i2][j2] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i3 = int(value[0])
    j3 = int(value[1])
    
    if j3 != 0:
        # LEFT Straight
        while j3 >= 0:
            j3-=1
        
            if empty_or_oppoent_piece(chess_board, i3, j3) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i3, j3) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i3][j3] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break
                
    i4 = int(value[0])
    j4 = int(value[1])
    
    if j4 != 7:
        # RIGTH Straight
        while j4 <= 7:
            j4+=1
        
            if empty_or_oppoent_piece(chess_board, i4, j4) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i4, j4) == True:
                    valid = True
            
                temp = copy.deepcopy(chess_board)
                temp[i4][j4] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break
                    
    i5 = int(value[0])
    j5 = int(value[1])
    
    if i5 != 0 and j5 != 0:
        # UP LEFT
        while i5 >= 0 and j5 >= 0:
            i5-=1
            j5-=1
        
            if empty_or_oppoent_piece(chess_board, i5, j5) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i5, j5) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i5][j5] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i6 = int(value[0])
    j6 = int(value[1])
    
    if i6 != 0 and j6 != 7:
        # UP RIGHT
        while i6 >= 0 and j6 <= 7:
            i6-=1
            j6+=1
        
            if empty_or_oppoent_piece(chess_board, i6, j6) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i6, j6) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i6][j6] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
        
                if valid == True:
                    break
                
    i7 = int(value[0])
    j7 = int(value[1])
    
    if i7 != 7 and j7 != 0:
        # DOWN LEFT
        while i7 <= 7 and j7 >= 0:
            i7+=1
            j7-=1
        
            if empty_or_oppoent_piece(chess_board, i7, j7) == False:
                break
            else:
                valid = False
                
                if oppoent_piece(chess_board, i7, j7) == True:
                    valid = True
                
                temp = copy.deepcopy(chess_board)
                temp[i7][j7] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)
    
                if valid == True:
                    break
                
    i8 = int(value[0])
    j8 = int(value[1])
    
    if i8 != 7 and j8 != 7:
    # DOWN RIGHT
        while i8 <= 7 and j8 <= 7:
            i8+=1
            j8+=1
        
            if empty_or_oppoent_piece(chess_board, i8, j8) == False:
                break
            else:
                valid = False
            
                if oppoent_piece(chess_board, i8, j8) == True:
                    valid = True
            
                temp = copy.deepcopy(chess_board)
                temp[i8][j8] = temp[queen_current_i][queen_current_j]
                temp[queen_current_i][queen_current_j] = 0
                STACK.append(temp)

                if valid == True:
                    break

def AI_King_Possible_Moves(chess_board, king, value, STACK):
    king_current_i = int(value[0])
    king_current_j = int(value[1])
    
    # UP
    if king_current_i != 0:
        if empty_or_oppoent_piece(chess_board, (king_current_i - 1), king_current_j) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i - 1][king_current_j] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
    
    # DOWN
    if king_current_i != 7:
        if empty_or_oppoent_piece(chess_board, (king_current_i + 1), king_current_j) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i + 1][king_current_j] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # LEFT
    if king_current_j != 0:
        if empty_or_oppoent_piece(chess_board, king_current_i, (king_current_j - 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i][king_current_j - 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # RIGHT
    if king_current_j != 7:
        if empty_or_oppoent_piece(chess_board, king_current_i, (king_current_j + 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i][king_current_j + 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # UP LEFT
    if king_current_i != 0 and king_current_j != 0:
        if empty_or_oppoent_piece(chess_board, (king_current_i - 1), (king_current_j - 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i - 1][king_current_j - 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # UP RIGHT
    if king_current_i != 0 and king_current_j != 7:
        if empty_or_oppoent_piece(chess_board, (king_current_i - 1), (king_current_j + 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i - 1][king_current_j + 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # DOWN LEFT
    if king_current_i != 7 and king_current_j != 0:
        if empty_or_oppoent_piece(chess_board, (king_current_i + 1), (king_current_j - 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i + 1][king_current_j - 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)
        
    # DOWN RIGHT
    if king_current_i != 7 and king_current_j != 7:
        if empty_or_oppoent_piece(chess_board, (king_current_i + 1), (king_current_j + 1)) == True:
            temp = copy.deepcopy(chess_board)
            temp[king_current_i + 1][king_current_j + 1] = temp[king_current_i][king_current_j]
            temp[king_current_i][king_current_j] = 0
            STACK.append(temp)

def heuristic(AIScore, PlayerScore, who):
    if who == 'player':
        return PlayerScore - AIScore
    else:
        return AIScore - PlayerScore

def FIND_MIN_Level_Heuristics(chess_board):
    MIN = [0 for i in range(len(chess_board))]
    
    for i in range(len(chess_board)):
        chess_pieces = finding_present_chess_pieces(chess_board[i])
    
        sumPlayer = 0
        sumAI = 0
        
        for key, value in chess_pieces.items():
            if key == 'KK1':
                sumAI+=1000
                
            if key == 'Q1' or key == 'Q2' or key == 'Q3' or key == 'Q4' or key == 'Q5' or key == 'Q6' or key == 'Q7' or key == 'Q8' or key == 'Q9':
                sumAI+=9
                
            if key == 'R1' or key == 'R2' or key == 'R3' or key == 'R4' or key == 'R5' or key == 'R6' or key == 'R7' or key == 'R8' or key == 'R9' or key == 'R10':
                sumAI+=5
                
            if key == 'B1' or key == 'B2' or key == 'B3' or key == 'B4' or key == 'B5' or key == 'B6' or key == 'B7' or key == 'B8' or key == 'B9' or key == 'B10':
                sumAI+=3
                
            if key == 'K1' or key == 'K2' or key == 'K3' or key == 'K4' or key == 'K5' or key == 'K6' or key == 'K7' or key == 'K8' or key == 'K9' or key == 'K10':
                sumAI+=3
                
            if key == 'P1' or key == 'P2' or key == 'P3' or key == 'P4' or key == 'P5' or key == 'P6' or key == 'P7' or key == 'P8':
                sumAI+=1
                
            if key == 'kk1':
                sumAI+=1000
                
            if key == 'q1' or key == 'q2' or key == 'q3' or key == 'q4' or key == 'q5' or key == 'q6' or key == 'q7' or key == 'q8' or key == 'q9':
                sumAI+=9
                
            if key == 'r1' or key == 'r2' or key == 'r3' or key == 'r4' or key == 'r5' or key == 'r6' or key == 'r7' or key == 'r8' or key == 'r9' or key == 'r10':
                sumAI+=5
                
            if key == 'b1' or key == 'b2' or key == 'b3' or key == 'b4' or key == 'b5' or key == 'b6' or key == 'b7' or key == 'b8' or key == 'b9' or key == 'b10':
                sumAI+=3
                
            if key == 'k1' or key == 'k2' or key == 'k3' or key == 'k4' or key == 'k5' or key == 'k6' or key == 'k7' or key == 'k8' or key == 'k9' or key == 'k10':
                sumAI+=3
                
            if key == 'p1' or key == 'p2' or key == 'p3' or key == 'p4' or key == 'p5' or key == 'p6' or key == 'p7' or key == 'p8':
                sumAI+=1
        
        value = heuristic(sumAI, sumPlayer, 'AI')
        
        MIN[i] = value
    
    minimum = 1000000000
    
    for k in range(len(chess_board)):
        if MIN[i] < minimum:
            minimum = MIN[i]
            
    return minimum
        
def AI_Move(chess_board):    
    present_chess_pieces = dict()
    
    present_chess_pieces = finding_present_chess_pieces_of_AI(chess_board)
   
    MAX_STACK = [] # 3D
    
    #TEMP_MIN_STACK = [] # 3D
    
    for key, value in present_chess_pieces.items():
        if key[0] == 'K' and key[1] == 'K':
            AI_King_Possible_Moves(chess_board, key, value, MAX_STACK)
        
        if key[0] == 'P':
            AI_Pawn_Possible_Moves(chess_board, key, value, MAX_STACK)
            
        if key[0] == 'R':
            AI_Rook_Possible_Moves(chess_board, key, value, MAX_STACK)
        
        if key[0] == 'B':
            AI_Bishop_Possible_Moves(chess_board, key, value, MAX_STACK)
        
        if key[0] == 'K':
            AI_Knight_Possible_Moves(chess_board, key, value, MAX_STACK)
        
        if key[0] == 'Q':
            AI_Queen_Possible_Moves(chess_board, key, value, MAX_STACK)

    MIN_STACK = [] # 4D
    
    for i in range(len(MAX_STACK)):
        p_present_chess_pieces = finding_present_chess_pieces_of_player(MAX_STACK[i])
                   
        TEMP_MIN_STACK = []
        
        for key, value in p_present_chess_pieces.items():
            if key[0] == 'k' and key[1] == 'k':
                Player_King_Possible_Moves(chess_board, key, value, TEMP_MIN_STACK)
        
            if key[0] == 'p':
                Player_Pawn_Possible_Moves(chess_board, key, value, TEMP_MIN_STACK)
            
            if key[0] == 'r':
                Player_Rook_Possible_Moves(chess_board, key, value, TEMP_MIN_STACK)
        
            if key[0] == 'b':
                Player_Bishop_Possible_Moves(chess_board, key, value, TEMP_MIN_STACK)
        
            if key[0] == 'k':
                Player_Knight_Possible_Moves(chess_board, key, value, TEMP_MIN_STACK)
        
            if key[0] == 'q':
                Player_Queen_Possible_Moves(chess_board, key, value, TEMP_MIN_STACK)
           
        MIN_STACK.append(TEMP_MIN_STACK)
    
    MAX_Level_Heuristics = [0 for l in range(len(MAX_STACK))]
    
    for f in range(len(MIN_STACK)):
        MAX_Level_Heuristics[f] = FIND_MIN_Level_Heuristics(MIN_STACK[f])
        
    maximum = -1000000
    index = -10
    
    for h in range(len(MAX_STACK)):
        if MAX_Level_Heuristics[h] > maximum:
            maximum = MAX_Level_Heuristics[h]
            index = h
            
    return MAX_STACK[index]

def user_move(chess_board):
    move_validity = False
    
    while(move_validity != True):
        player_piece = input("\nEnter Piece Name which you want to move: ")
    
        position = input("Enter Position to where you want to move piece: ")
    
        p_piece_current_position_x, p_piece_current_position_y = find_current_cell_of_piece(player_piece)
        
        p_piece_next_position_x, p_piece_next_position_y = find_cell_to_where_piece_has_to_be_moved(position)
        
        if player_piece[0] == 'p':
            move_validity_1 = check_p_pawn_move_validity(player_piece, p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y)
            move_validity = move_validity_1[0]
            player_pawns_move_no[player_piece]+=1
        elif player_piece[0] == 'r':
            move_validity = check_p_rook_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y)
        elif player_piece[0] == 'k':
            move_validity = check_p_knight_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y)
        elif player_piece[0] == 'b':
            move_validity = check_p_bishop_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y)
        elif player_piece[0] == 'q':
            move_validity = check_p_queen_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y)
        elif player_piece[0] == 'k' and player_piece[1] == 'k':
            move_validity = check_p_king_move_validity(p_piece_current_position_x, p_piece_current_position_y, p_piece_next_position_x, p_piece_next_position_y)

        if move_validity == True:
            chess_board[p_piece_next_position_x][p_piece_next_position_y] = player_piece
        
            chess_board[p_piece_current_position_x][p_piece_current_position_y] = 0
        else:
            print("You can't move", player_piece, "to ", position)

    return chess_board

def check_checkmate_by_AI(chess_board):
    check_mate = True
    
    flag1 = False
    
    for a in range(0, 8):
        for b in range(0, 8):
            if chess_board[a][b] == 'kk1':
                check_mate = False
                flag1 = True
                break
        
        if flag1 == True:
            break
            
    return check_mate
            
def check_checkmate_by_player(chess_board):
    check_mate = True
    
    flag1 = False
    
    for a in range(0, 8):
        for b in range(0, 8):
            if chess_board[a][b] == 'KK1':
                check_mate = False
                flag1 = True
                break
        
        if flag1 == True:
            break
            
    return check_mate

#####################

check_mate = False

while checkmate != True:
    chess_board = AI_Move(chess_board)
    
    print('\nAI Move: --v')
    print(chess_board)
    
    check_mate = check_checkmate_by_AI(chess_board)
    
    if check_mate == True:
        break
    
    #sleep(1)
    
    chess_board = user_move(chess_board)
    
    print('\nPlayer Move: --v')
    print(chess_board)
    
    check_mate = check_checkmate_by_player(chess_board)
    
    if check_mate == True:
        break


# In[ ]:





# In[ ]:




