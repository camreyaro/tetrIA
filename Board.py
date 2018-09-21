import copy
import numpy
import Piece as pieceClass
import Coordinate as coordinateClass
import scipy
import re
from scipy.ndimage import label, binary_dilation


class Board:

    # Constructor de un objeto de tipo Board
    def __init__(self, height, width, currentPiece):
        self.height = height
        self.width = width
        self.currentPiece = currentPiece
        self.matrix = numpy.zeros((height, width), numpy.int8)

        for coord in self.getCurrentPiece().coordinates:
            if (self.getCurrentPiece().pieceType == "L"):
                self.matrix[coord.x, coord.y] = 1
            elif (self.getCurrentPiece().pieceType == "J"):
                self.matrix[coord.x, coord.y] = 2
            elif (self.getCurrentPiece().pieceType == "I"):
                self.matrix[coord.x, coord.y] = 3
            elif (self.getCurrentPiece().pieceType == "O"):
                self.matrix[coord.x, coord.y] = 4
            elif (self.getCurrentPiece().pieceType == "S"):
                self.matrix[coord.x, coord.y] = 5
            elif (self.getCurrentPiece().pieceType == "T"):
                self.matrix[coord.x, coord.y] = 6
            elif (self.getCurrentPiece().pieceType == "Z"):
                self.matrix[coord.x, coord.y] = 7
                
    ### GETTERS ###

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getCurrentPiece(self):
        return self.currentPiece
    
    ###
    
    # Determinamos si la pieza puede moverse abajo comprobando que no hay obstáculos
    def canMoveDown(self):
        boardCopy = copy.deepcopy(self)
        pieceCopy = copy.deepcopy(self.getCurrentPiece())
        pieceCopy.moveDown()

        for coord in self.getCurrentPiece().coordinates:
            if (coord.x < self.height and coord.y < self.width):
                boardCopy.matrix[coord.x, coord.y] = 0

        for coord in pieceCopy.coordinates:
            if (coord.getX() > self.height - 1 or coord.y > self.width - 1 or coord.y < 0):
                return False
            elif (boardCopy.matrix[coord.x, coord.y] >= 1):
                return False
        return True

    # Determinamos si la pieza puede moverse a la derecha comprobando que no hay obstáculos
    def canMoveRight(self):
        boardCopy = copy.deepcopy(self)
        pieceCopy = copy.deepcopy(self.getCurrentPiece())
        pieceCopy.moveRight()

        for coord in self.getCurrentPiece().coordinates:
            if (coord.x < self.height and coord.y < self.width):
                boardCopy.matrix[coord.x, coord.y] = 0

        for coord in pieceCopy.coordinates:
            if (coord.getY() > self.width - 1 or coord.getX() > self.height - 1 or coord.y < 0):
                return False
            elif (boardCopy.matrix[coord.x, coord.y] >= 1):
                return False
        return True

    # Determinamos si la pieza puede moverse a la izquierda comprobando que no hay obstáculos
    def canMoveLeft(self):
        boardCopy = copy.deepcopy(self)
        pieceCopy = copy.deepcopy(self.getCurrentPiece())
        pieceCopy.moveLeft()

        for coord in self.getCurrentPiece().coordinates:
            if (coord.x < self.height and coord.y < self.width and coord.y > 0):
                boardCopy.matrix[coord.x, coord.y] = 0

        for coord in pieceCopy.coordinates:
            if (coord.getY() < 0 or coord.getX() > self.height - 1 or coord.y < 0):
                return False
            elif (boardCopy.matrix[coord.x, coord.y] >= 1):
                return False
        return True
    
    
    # Determinamos si la pieza puede rotar a la izquierda comprobando que no hay obstáculos
    def canRotateLeft(self, originalBoard=None):
        boardCopy = copy.deepcopy(self)
        pieceCopy = copy.deepcopy(self.getCurrentPiece())
        pieceCopy.rotateLeft(self.width)

        for coord in self.getCurrentPiece().coordinates:
            if ((coord.y <= self.width - 1 and coord.y >= 0 and coord.x <= self.height - 1 and coord.x >= 0)
                    and ((originalBoard is not None and originalBoard.matrix[coord.x][
                        coord.y] == 0) or originalBoard is None)):
                boardCopy.matrix[coord.x][coord.y] = 0

        for coord in pieceCopy.coordinates:
            if (coord.getY() > self.width - 1):
                return False
            elif (coord.getY() < 0):
                return False
            elif (coord.getX() > self.height - 1):
                return False
            elif (coord.getX() < 0):
                return False
            elif (boardCopy.matrix[coord.x][coord.y] >= 1):
                return False
        return True

    # Comprobamos que al colocar una pieza no queda flotando en el tablero
    def checkFloatingPiece(self, piece):
        floating = True
        for coord in piece.coordinates:
            if ((coord.x + 1 < self.height and coord.y < self.width and self.matrix[coord.x + 1][
                coord.y] >= 1) or coord.x == self.height - 1):
                floating = False
        return floating

    # Determinamos si la pieza puede rotar a la derecha comprobando que no hay obstáculos
    def canRotateRight(self):
        boardCopy = copy.deepcopy(self)
        pieceCopy = copy.deepcopy(self.getCurrentPiece())
        pieceCopy.rotateRight(self.width)

        for coord in self.getCurrentPiece().coordinates:
            if (coord.x < self.height and coord.y < self.width):
                boardCopy.matrix[coord.x][coord.y] = 0

        for coord in pieceCopy.coordinates:
            if (coord.getY() > self.width - 1):
                return False
            elif (coord.getY() < 0):
                return False
            elif (coord.getX() > self.height - 1):
                return False
            elif (coord.getX() < 3):
                return False
            elif (boardCopy.matrix[coord.x][coord.y] >= 1):
                return False
        return True

    # Actualizamos el tablero: En primer lugar borramos la posición anterior de la pieza y después la colocamos en la nueva
    def updateBoard(self, piece):

        for coord in self.getCurrentPiece().coordinates:
            if (coord.x < self.height and coord.y < self.width):
                self.matrix[coord.x, coord.y] = 0

        self.currentPiece = piece
        for coord in self.getCurrentPiece().coordinates:
            if (coord.x < self.height and coord.y < self.width):
                if (self.getCurrentPiece().pieceType == "L"):
                    self.matrix[coord.x, coord.y] = 1
                elif (self.getCurrentPiece().pieceType == "J"):
                    self.matrix[coord.x, coord.y] = 2
                elif (self.getCurrentPiece().pieceType == "I"):
                    self.matrix[coord.x, coord.y] = 3
                elif (self.getCurrentPiece().pieceType == "O"):
                    self.matrix[coord.x, coord.y] = 4
                elif (self.getCurrentPiece().pieceType == "S"):
                    self.matrix[coord.x, coord.y] = 5
                elif (self.getCurrentPiece().pieceType == "T"):
                    self.matrix[coord.x, coord.y] = 6
                elif (self.getCurrentPiece().pieceType == "Z"):
                    self.matrix[coord.x, coord.y] = 7

    # Eliminamos las líneas que han sido completadas
    def cleanLines(self):
        if (self.countCompleteLines() > 0):
            i = self.height - 1
            while (numpy.sum(self.matrix.all(1))):
                if (numpy.all(self.matrix[i])):
                    for j in range(self.height - 1, 0, -1):
                        if (j <= i):
                            self.matrix[j] = self.matrix[j - 1]
                else:
                    i -= 1

    # Realizamos una copia del tablero
    def copyBoard(self, piece, cleanCurrentPiece=None):
        boardCopy = copy.deepcopy(self)

        if (cleanCurrentPiece):
            for coord in self.currentPiece.coordinates:
                boardCopy.matrix[coord.x, coord.y] = 0

        for coord in piece.coordinates:
            if (piece.pieceType == "L"):
                boardCopy.matrix[coord.x, coord.y] = 1
            elif (piece.pieceType == "J"):
                boardCopy.matrix[coord.x, coord.y] = 2
            elif (piece.pieceType == "I"):
                boardCopy.matrix[coord.x, coord.y] = 3
            elif (piece.pieceType == "O"):
                boardCopy.matrix[coord.x, coord.y] = 4
            elif (piece.pieceType == "S"):
                boardCopy.matrix[coord.x, coord.y] = 5
            elif (piece.pieceType == "T"):
                boardCopy.matrix[coord.x, coord.y] = 6
            elif (piece.pieceType == "Z"):
                boardCopy.matrix[coord.x, coord.y] = 7
            else:
                boardCopy.matrix[coord.x, coord.y] = 1
                print("ESTE ELSE NO SE TENDRÍA QUE DAR")

        boardCopy.currentPiece = piece

        return boardCopy

    # Devolvemos un diccionario con las posiciones posibles y su puntuación obtenida
    def calculatePosiblePositions(self, detailed=None):
        piecesByPuntuation = {}
        pieces = []

        for i in range(self.height - 1, 0, -1):
            for j in range(0, self.width):
                generatedPieces = self.generatePieces(i, j, self.currentPiece.pieceType)
                pieces.extend(generatedPieces)

        for piece in pieces:
            piecePuntuation = self.puntuatePosition(piece, detailed)
            piecesByPuntuation[piece] = piecePuntuation

        return piecesByPuntuation

    # Asignamos una puntuación a la posición
    def puntuatePosition(self, piece, detailed=None):
        boardCopy = copy.deepcopy(self)
        boardCopy.currentPiece = piece

        # Simulamos la situación de la pieza en dicha posición para poder evaluarla
        for coord in self.getCurrentPiece().coordinates:
            boardCopy.matrix[coord.x, coord.y] = 0

        for coord in piece.coordinates:
            if (piece.pieceType == "L"):
                boardCopy.matrix[coord.x, coord.y] = 1
            elif (piece.pieceType == "J"):
                boardCopy.matrix[coord.x, coord.y] = 2
            elif (piece.pieceType == "I"):
                boardCopy.matrix[coord.x, coord.y] = 3
            elif (piece.pieceType == "O"):
                boardCopy.matrix[coord.x, coord.y] = 4
            elif (piece.pieceType == "S"):
                boardCopy.matrix[coord.x, coord.y] = 5
            elif (piece.pieceType == "T"):
                boardCopy.matrix[coord.x, coord.y] = 6
            elif (piece.pieceType == "Z"):
                boardCopy.matrix[coord.x, coord.y] = 7
            else:
                boardCopy.matrix[coord.x, coord.y] = 1
                print("ESTE ELSE NO SE TENDRÍA QUE DAR")

        # Creamos un array donde cada valor representa el índice de la primera fila encontrada con un valor distinto de cero 
        # para cada columna
        nonZeroArray = (boardCopy.matrix != 0).argmax(axis=0) 
        
        # Restamos la altura total del tablero al índice de cada columna para obtener la altura 
        # Ej: Si hay una pieza en la columna 0 que tiene altura 2 (como una pieza de tipo 'O'), cuya parte superior está en la fila 18
        # entonces altura = 20 - 18 = 2
        heightArray = numpy.subtract(20, nonZeroArray[nonZeroArray != 0])
            
        # Contamos las filas completas (se quiere maximizar)
        completeLinesScore = numpy.sum(boardCopy.countCompleteLines())
        
        # Número de huecos que deja la pieza
        bricksScore = boardCopy.countBricks()
        
       # if completeLinesScore > bricksScore:
        #    completeLinesScore = completeLinesScore * 20
         #   bricksScore = bricksScore * 15
        #else:
         #   completeLinesScore = completeLinesScore * 15
          #  bricksScore = bricksScore * 20

        # Determinamos la altura máxima (se quiere minimizar) 
        if not numpy.any(boardCopy.matrix):
            maxHeightScore = numpy.max(heightArray) * 400 #Seleccionamos el valor máximo del array de alturas calculado antes
        else:
            maxHeightScore = 0

        holesCountScore = boardCopy.countBoardHoles()  # Determinamos el número de huecos que quedan al colocar la pieza (minimizar)
        lowerRowsFilledScore = boardCopy.sumRowCoordinates() * 0.1 # Intentamos que el algoritmo tienda a colocar las piezas abajo (max)
        lowerColsFilledScore = boardCopy.sumColCoordinates() * 0.001 # Intentamos que el algoritmo tienda a colocar las piezas abajo (max)

        if detailed is not None and detailed is True:
            print(
                "Pieza: {}, Líneas Completas: {}, Máxima altura: {}, Ceros: {}, Filas: {}, Bloques: {} - Puntuación: {}".format(
                    piece, completeLinesScore, maxHeightScore, holesCountScore, lowerRowsFilledScore, bricksScore,
                    completeLinesScore - maxHeightScore - holesCountScore + lowerRowsFilledScore - bricksScore))

        #return completeLinesScore - maxHeightScore - holesCountScore + lowerRowsFilledScore - bricksScore + lowerColsFilledScore - boardCopy.calculateColumnHeightVariation(
            #heightArray) * 0.01
        return numpy.sum(heightArray)*(-0.510066) + completeLinesScore*0.760666 + holesCountScore*(-0.35663) + boardCopy.calculateColumnHeightVariation(heightArray)*(-0.184483)

    def countCompleteLines(self):
        return numpy.sum(self.matrix.all(1)) # Sumamos el número de filas donde todos los valores son distintos de 0

    def calculateColumnHeightVariation(self, heightArray): # Calculamos la variación de altura de las columnas (se quiere minimizar)
        columnHeightVariation = 0

        for i in range(0, len(heightArray) - 1):
            columnHeightVariation += abs(heightArray[i] - heightArray[i + 1])
        return columnHeightVariation

    # Aplicamos una máscara para contabilizar el número de huecos existentes en el tablero
    def countBoardHoles(self):
        mask = numpy.ones((self.height, self.width)).astype(bool)
        labels, num_labels = scipy.ndimage.measurements.label(numpy.logical_and(mask, self.matrix == 0))

        return num_labels

    def countBricks(self):
        bricksCount = 0

        for coord in self.currentPiece.coordinates: # Contamos todos los huecos que deja la pieza viendo cada casilla debajo de ella
            if (coord.x < self.height - 1 and self.matrix[coord.x + 1, coord.y] == 0):
                for i in range (coord.x+1, self.height):
                    if(self.matrix[i, coord.y] == 0):
                        bricksCount += 1

        return bricksCount

    def sumRowCoordinates(self):
        rowCoordinates = numpy.where(self.matrix >= 1)

        return sum(rowCoordinates[0])

    def sumColCoordinates(self):
        rowCoordinates = numpy.where(self.matrix >= 1)

        return sum(rowCoordinates[1])

    # Generamos una pieza dadas las coordenadas de su centro de rotación y el tipo de pieza
    def generatePieces(self, i, j, pieceType):
        pieces = []

        if (pieceType == "L"):
            piece = pieceClass.Piece([coordinateClass.Coordinate(i, j), coordinateClass.Coordinate(i - 1, j),
                                      coordinateClass.Coordinate(i + 1, j), coordinateClass.Coordinate(i + 1, j + 1)],
                                     "L")

        elif (pieceType == "J"):
            piece = pieceClass.Piece([coordinateClass.Coordinate(i, j), coordinateClass.Coordinate(i - 1, j),
                                      coordinateClass.Coordinate(i - 1, j + 1), coordinateClass.Coordinate(i + 1, j)],
                                     "J")

        elif (pieceType == "I"):
            piece = pieceClass.Piece([coordinateClass.Coordinate(i, j), coordinateClass.Coordinate(i - 1, j),
                                      coordinateClass.Coordinate(i + 1, j), coordinateClass.Coordinate(i + 2, j)], "I")

        elif (pieceType == "O"):
            piece = pieceClass.Piece([coordinateClass.Coordinate(i, j), coordinateClass.Coordinate(i + 1, j),
                                      coordinateClass.Coordinate(i, j + 1), coordinateClass.Coordinate(i + 1, j + 1)],
                                     "O")

        elif (pieceType == "S"):
            piece = pieceClass.Piece([coordinateClass.Coordinate(i, j), coordinateClass.Coordinate(i - 1, j),
                                      coordinateClass.Coordinate(i, j + 1), coordinateClass.Coordinate(i + 1, j + 1)],
                                     "S")

        elif (pieceType == "T"):
            piece = pieceClass.Piece([coordinateClass.Coordinate(i, j), coordinateClass.Coordinate(i - 1, j),
                                      coordinateClass.Coordinate(i, j + 1), coordinateClass.Coordinate(i + 1, j)], "T")

        elif (pieceType == "Z"):
            piece = pieceClass.Piece([coordinateClass.Coordinate(i, j), coordinateClass.Coordinate(i, j + 1),
                                      coordinateClass.Coordinate(i - 1, j + 1), coordinateClass.Coordinate(i + 1, j)],
                                     "Z")

        else:
            return pieces

        boardCopy = copy.deepcopy(self)
        boardCopy.currentPiece = piece

        for coord in self.getCurrentPiece().coordinates:
            boardCopy.matrix[coord.x, coord.y] = 0

        if (self.checkPiece(boardCopy)):
            originalPiece = copy.deepcopy(piece)
            pieces.append(originalPiece)

        for i in range(0, 3):
            pieceToCheck = copy.deepcopy(piece)
            pieceToCheck.rotateLeft(self.width)
            boardToCheck = copy.deepcopy(boardCopy)
            boardToCheck.currentPiece = pieceToCheck
            if (boardCopy.canRotateLeft(self) and not boardToCheck.checkFloatingPiece(pieceToCheck) and boardToCheck.checkTopLines()):
                rotatedPiece = copy.deepcopy(piece)
                rotatedPiece.rotateLeft(self.width)
                pieces.append(rotatedPiece)
            piece.rotateLeft(self.width)
        return pieces

    # Comprobamos que no se llega a las líneas invisibles
    def checkTopLines(self):
        
        for coord in self.currentPiece.coordinates:
            if (coord.x <= 1):
                return False
        return True
            
    # Comprobamos que la posición es válida
    def checkPiece(self, boardCopy):

        for coord in boardCopy.currentPiece.coordinates:
            if (coord.getY() > self.width - 1):
                return False
            elif (coord.getY() < 0):
                return False
            elif (coord.getX() > self.height - 1):
                return False
            elif (coord.getX() < 2):
                return False
            elif (self.matrix[coord.x, coord.y] >= 1):
                return False
            elif (coord.x <= 1):
                return False
        return not boardCopy.checkFloatingPiece(boardCopy.currentPiece)

    # Formateamos la matriz
    def printBoard(self):
        #En esta función reemplazamos todos los digitos que representa a las distintas piezas por vocales (para evitar
        #reemplazos no debidos.
        x = numpy.char.mod('%d', self.matrix)
        x[x == '0'] = ' '
        x[x == '1'] = 'a'
        x[x == '2'] = 'b'
        x[x == '3'] = 'c'
        x[x == '4'] = 'd'
        x[x == '5'] = 'e'
        x[x == '6'] = 'f'
        x[x == '7'] = 'g'

        #Formateamos el tablero un poco más, añadiendo paredes y colores a cada tipo de pieza.
        boardString = str(x).replace("[[", " [")\
              .replace("]]", "]")\
              .replace("[", "\033[40m.\033[0m")\
              .replace("]", "\033[40m.\033[0m")\
              .replace("'", "")\
              .replace("a", "\033[36m■\033[0m")\
              .replace("b", "\033[31m■\033[0m")\
              .replace("c", "\033[32m■\033[0m")\
              .replace("d", "\033[33m■\033[0m")\
              .replace("e", "\033[34m■\033[0m")\
              .replace("f", "\033[35m■\033[0m")\
              .replace("g", "\033[30m■\033[0m")

        #Este código busca una línea completa (la cual se va a eliminar) y la marca en rojo para que el efecto sea
        #más visual.
        regexp = " \\u001b\[40m\.\\u001b\[0m\\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m \\u001b\[3[0-9]{1}m■\\u001b\[0m\\u001b\[40m\.\\u001b\[0m"
        rpl = " \033[40m.\033[0m\033[41m■ ■ ■ ■ ■ ■ ■ ■ ■ ■\033[0m\033[40m.\033[0m"
        imp = re.sub(regexp, rpl, boardString)
        imp = re.sub("\\u001b\[40m.\\u001b\[0m", "\033[0;37;47m.\033[0m", imp, 4)
        print(imp)
        #print(boardString)
        return imp

    def __eq__(self, other):
        return numpy.allclose(self.matrix, other.matrix)

    def __str__(self):
        return numpy.array2string(self.matrix)