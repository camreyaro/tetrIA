import numpy
import Coordinate
import copy
import math

class Piece():
    
    # Constructor
    def __init__(self,coordinates, pieceType):
        self.coordinates = coordinates
        self.pieceType = pieceType
        
    ## Definimos los distintos movimientos que puede realizar la pieza ##
        
    def moveLeft(self):
        for coord in self.coordinates:
            y = coord.getY()
            coord.setY(y-1)
        
    def moveRight(self):
        for coord in self.coordinates:
            y = coord.getY()
            coord.setY(y+1)
        
    def moveDown(self):
        for coord in self.coordinates:
            x = coord.getX()
            coord.setX(x+1)
        
    def rotateLeft(self, boardWidth):
        px = self.coordinates[0].x
        py = self.coordinates[0].y
        
        for coord in self.coordinates:
            x = coord.getX()
            y = coord.getY()
            
            coord.setX(px + py - y)
            coord.setY(x + py - px)
            
    def rotateRight(self, boardWidth):
        px = self.coordinates[0].x
        py = self.coordinates[0].y
        
        for coord in self.coordinates:
            x = coord.getX()
            y = coord.getY()
            
            coord.setX(y + px - py)
            coord.setY(px + py - x)
        
    def canMoveDown(self,board):
        pieceCopy = copy.deepcopy(self)
        pieceCopy.moveDown()
        
        for coord in pieceCopy.coordinates:
            if coord.getX() > board.height-1:
                return False
        return True
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
    
    def __str__(self):
        cadena = ""
        for i in self.coordinates:
            cadena += str(i) + ", "
            
        return cadena
    
    def __hash__(self):
        return hash(self.pieceType)
