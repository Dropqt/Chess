pieceScore={"K":0,"Q":10,'R':5,'B':3,"N":3,'p':1}
knightScores= [
    [-10, -10,  -8,  -8,  -8,  -8, -10, -10],
    [-10,  -2,   0,   0,   0,   0,  -2, -10],
    [ -8,   0,   4,   6,   6,   4,   0,  -8],
    [ -8,   2,   6,   8,   8,   6,   2,  -8],
    [ -8,   0,   6,   8,   8,   6,   0,  -8],
    [ -8,   2,   4,   6,   6,   4,   2,  -8],
    [-10,  -2,   0,   2,   2,   0,  -2, -10],
    [-10, -10,  -8,  -8,  -8,  -8, -10, -10]
]
pawnScoresw=[
    [ 10, 10,  10,  10,  10,  10,  10,  10],
    [ 8,   8,   8,   8,   8,   8,   8,   8],
    [ 3,   4,   5,   6,   6,   5,   4,   3],
    [ 2,   2,   4,  10,  10,   4,   2,   2],
    [-1,  -2,  -3,   0,   0,  -3,  -2,  -1],
    [1,  -5,  -6,  -8,  -8,  -6,  -5,  1],
    [-5,  -7,  -8, -10, -10,  -8,  -7,  -5],
    [ 0,   0,   0,   0,   0,   0,   0,   0]
]

"""pawnScoresw=[
[ 60,   60,   60,   60,   60,   60,   60,   60 ],
[ 50,  50,  50,  50,  50,  50,  50,  50 ],
[ 10,  10,  20,  30,  30,  20,  10,  10 ],
[ 5,   5,  10,  25,  25,  10,   5,   5 ],
[ 0,   0,   0,  20,  20,   0,   0,   0 ],
[ 5,  -5, -10,   1,   1, -10,  -5,   5 ],
[ 5,  10,  10, 0.5, 0.5,  10,  10,   5 ],
[ 0,   0,   0,   0,   0,   0,   0,   0 ]
]"""
#Just reversing the order of weight elements for black pieces
pawnScoresb=[pawnScoresw[x] for x in range(len(pawnScoresw)-1,-1,-1)]
bishopsScoresw =[ 
[ -20, -10, -10, -10, -10, -10, -10, -20 ],
[ -10,   0,   0,   0,   0,   0,   0, -10 ],
[ -10,   0,   5,  10,  10,   5,   0, -10 ],
[ -10,   5,   5,  10,  10,   5,   5, -10 ],
[ -10,   0,  10,  10,  10,  10,   0, -10 ],
[ -10,  10,  10,  5,  5,  10,  10, -10 ],
[ -10,   5,   0,   0,   0,   0,   5, -10 ],
[ -20, -10, -10, -10, -10, -10, -10, -20 ]
]
bishopsScoresb=[bishopsScoresw[x] for x in range(len(bishopsScoresw)-1,-1,-1)]

rooksScorew =[
[  0,   0,   0,   0,   0,   0,   0,   0 ],
[  5,  10,  10,  10,  10,  10,  10,   5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[ -5,   0,   0,   0,   0,   0,   0,  -5 ],
[  -10,   -15,   2,   5,   5,   2,   -15,   -10 ]
]
rooksScoreb=[rooksScorew[x] for x in range(len(rooksScorew)-1,-1,-1)]

queensScorew=[
[ -20, -10, -10,  -5,  -5, -10, -10, -20 ],
[ -10,   0,   0,   0,   0,   0,   0, -10 ],
[ -10,   0,   5,   5,   5,   5,   0, -10 ],
[  -5,   0,   5,   5,   5,   5,   0,  -5 ],
[   0,   0,   5,   5,   5,   5,   0,  -5 ],
[ -10,   5,   5,   5,   5,   5,   0, -10 ],
[ -10,   0,   5,   0,   0,   0,   0, -10 ],
[ -20, -10, -10,  -5,  -5, -10, -10, -20 ]
]
queensScoreb=[queensScorew[x] for x in range(len(queensScorew)-1,-1,-1)]

kingsScorew=[
[-30, -40, -40, -50, -50, -40, -40, -30], 
[-30, -40, -40, -50, -50, -40, -40, -30], 
[-30, -40, -40, -50, -50, -40, -40, -30], 
[-30, -40, -40, -50, -50, -40, -40, -30], 
[-20, -30, -30, -40, -40, -30, -30, -20], 
[-10, -20, -20, -20, -20, -20, -20, -10], 
[20, 20, 0, 0, 0, 0, 20, 20], 
[20, 30, 10, -1, 0, -4, 30, 20]]
kingsScoreb=[kingsScorew[x] for x in range(len(kingsScorew)-1,-1,-1)]
"""
    
    
    
    
    
    
    
    
    Midgame Scores
    
    
    
    
    
    
    
    
    
    
    
"""
rookTableMidGamew = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5,  7,  7,  7,  7,  7,  7,  5],
    [5,  8,  8,  8,  8,  8,  8,  5],
    [5,  8,  8,  8,  8,  8,  8,  5],
    [5,  8,  8,  8,  8,  8,  8,  5],
    [5,  7,  7,  7,  7,  7,  7,  5],
    [0,  0,  0, 10, 10,  0,  0,  0],
    [-5, 0,  0,  0,  0,  0,  0, -5]
]
rookTableMidGameb=[rookTableMidGamew[x] for x in range(len(rookTableMidGamew)-1,-1,-1)]
pawnTableMidGamew = [
    [0,   0,   0,   0,   0,   0,   0,   0],
    [5,   5,   5,  -5,  -5,   5,   5,   5],
    [1,   1,   2,   6,   6,   2,   1,   1],
    [1,   2,   3,  10,  10,   3,   2,   1],
    [1,   1,   2,   8,   8,   2,   1,   1],
    [2,   3,   4,   5,   5,   4,   3,   2],
    [10, 10, 10, -10, -10, 10, 10, 10],
    [0,   0,   0,   0,   0,   0,   0,   0]
]
pawnTableMidGameb=[pawnTableMidGamew[x] for x in range(len(pawnTableMidGamew)-1,-1,-1)]
bishopTableMidGamew = [
    [-10, -10, -10, -10, -10, -10, -10, -10],
    [-10,   0,   0,   2,   2,   0,   0, -10],
    [-10,   0,   5,  5,  5,   5,   0, -10],
    [-10,   2,  10,  12,  12,  10,   2, -10],
    [-10,   2,  10,  12,  12,  10,   2, -10],
    [-10,   0,   5,  5,  5,   5,   0, -10],
    [-10,   0,   0,   2,   2,   0,   0, -10],
    [-10, -10, -10, -10, -10, -10, -10, -10]
]
bishopTableMidGameb=[bishopTableMidGamew[x] for x in range(len(bishopTableMidGamew)-1,-1,-1)]
knightTableMidGamew = [
    [-10, -10,  -8,  -8,  -8,  -8, -10, -10],
    [-10,  -2,   0,   0,   0,   0,  -2, -10],
    [ -8,   0,   4,   6,   6,   4,   0,  -8],
    [ -8,   2,   6,   8,   8,   6,   2,  -8],
    [ -8,   0,   6,   8,   8,   6,   0,  -8],
    [ -8,   2,   4,   6,   6,   4,   2,  -8],
    [-10,  -2,   0,   2,   2,   0,  -2, -10],
    [-10, -10,  -8,  -8,  -8,  -8, -10, -10]
]
knightTableMidGameb=[knightTableMidGamew[x] for x in range(len(knightTableMidGamew)-1,-1,-1)]
"""queenTableMidGamew = [
    [-10, -8, -8, -7, -7, -8, -8, -10],
    [ -8, -2, -2, -1, -1, -2, -2,  -8],
    [ -8, -2,  1,  0,  0,  1, -2,  -8],
    [ -7, -1,  0,  3,  3,  0, -1,  -7],
    [ -7, -1,  0,  3,  3,  0, -1,  -7],
    [ -8, -2,  1,  0,  0,  1, -2,  -8],
    [ -8, -2, -2, -1, -1, -2, -2,  -8],
    [-10, -8, -8, -7, -7, -8, -8, -10]
]
Maybe tighter positioning?
"""
queenTableMidGamew = [
    [-10, -10,  -8,  -8,  -8,  -8, -10, -10],
    [-10,  -2,   0,   0,   0,   0,  -2, -10],
    [ -8,   0,   4,   6,   6,   4,   0,  -8],
    [ -8,   2,   6,   8,   8,   6,   2,  -8],
    [ -8,   0,   6,   8,   8,   6,   0,  -8],
    [ -8,   2,   4,   6,   6,   4,   2,  -8],
    [-10,  -2,   0,   2,   2,   0,  -2, -10],
    [-10, -10,  -8,  -8,  -8,  -8, -10, -10]
]
queenTableMidGameb=[queenTableMidGamew[x] for x in range(len(queenTableMidGamew)-1,-1,-1)]

"""kingTableMidGamew = [
    [  2,   3,  -1,  -3,  -3,  -1,   3,   2],
    [  3,   2,  -2,  -4,  -4,  -2,   2,   3],
    [ -1,  -2,  -5,  -7,  -7,  -5,  -2,  -1],
    [ -3,  -4,  -7,  -9,  -9,  -7,  -4,  -3],
    [ -3,  -4,  -7,  -9,  -9,  -7,  -4,  -3],
    [ -1,  -2,  -5,  -7,  -7,  -5,  -2,  -1],
    [  3,   2,  -2,  -4,  -4,  -2,   2,   3],
    [  2,   3,  -1,  -3,  -3,  -1,   3,   2]
]
More protective
"""

kingTableMidGamew = [
[-6, -7, -7, -8, -8, -7, -7, -6],
[-5, -6, -6, -7, -7, -6, -6, -5],
[-4, -5, -5, -6, -6, -5, -5, -4],
[-3, -4, -4, -5, -5, -4, -4, -3], 
[-2, -3, -3, -4, -4, -3, -3, -2],
[-1, -2, -2, -3, -3, -2, -2, -1],
[2, 2, 0, 0, 0, 0, 2, 2],
[2, 3, 1, 0, 0, 1, 3, 2]]
kingTableMidGameb=[kingTableMidGamew[x] for x in range(len(kingTableMidGamew)-1,-1,-1)]