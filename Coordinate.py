class Coordinate():
    
    # Constructor
    def __init__(self,x,y):
        self.x = x
        self.y = y

    ## GETTERS ##
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    ## SETTERS ##
    
    def setX(self,x):
        self.x = x
        
    def setY(self,y):
        self.y = y
    
    ##
    
    def __eq__(self, other):
        return self.y == other.y and self.x == other.x
    
    def __str__(self):
        return '(' + str(self.getX()) + ',' + str(self.getY()) + ')'
