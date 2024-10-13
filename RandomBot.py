import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move
import random

# Initialize the game
myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")

# Main loop
while True:
    game_map.get_frame()
    moves = []
    
    # Go and take the sqaures with the highest production
    for square in game_map:
        if square.owner == myID:
            for direction in (NORTH, EAST, SOUTH, WEST):
                neighbor = game_map.get_target(square, direction)
                if neighbor.owner != myID and neighbor.strength < square.strength:
                    moves.append(Move(square, direction))
                    break
                else:    
                    if square.strength > 50:
                        
                        # Check if the current game_map row we are is full of our squares
                        row_full = True
                        for i in range(game_map.width):
                            if game_map.contents[square.y][i].owner != myID:
                                row_full = False
                                break
                        if row_full:
                            moves.append(Move(square, NORTH))                            
                        # Check if the current game_map column we are is full of our squares
                        col_full = True
                        for i in range(game_map.height):
                            if game_map.contents[i][square.x].owner != myID:
                                col_full = False
                                break
                            
                        if col_full:
                            moves.append(Move(square, EAST))
                        
                        moves.append(Move(square, random.choice((NORTH, EAST))))
                    else:
                        moves.append(Move(square, STILL))
                    
    hlt.send_frame(moves)
