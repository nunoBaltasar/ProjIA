#!/usr/bin/env python3
# slitherlink.py: Template para implementação do projeto de Inteligência Artificial 2025/2026.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import random, copy
from sys import stdin
from collections import defaultdict

import utils
from utils import *

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class SlitherlinkState:
    state_id = 0


    def __init__(self, board):
        self.board = board
        self.id = SlitherlinkState.state_id
        SlitherlinkState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Slitherlink."""

    def __init__(self, matrixValues: list):
        '''
        n_lines = len(matrix)
        n_columns = len(matrix[0]) if n_lines > 0 else 0
        matrix_dict = {}
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                #if cell not in [0, 1, 2, 3, None]:
                #    raise ValueError("Invalid cell value: {}".format(cell))
                matrix_dict[(i, j)] = cell
        self.matrix = matrix_dict'''
        rows = len(matrixValues)
        cols = len(matrixValues[0])
        matrix_dict = {}
        matrix_edges = {}
        for i in range(1,rows+1):
            for j in range(1, cols+1):
                matrix_dict[(i, j)] = matrixValues[i-1][j-1]
                matrix_edges[(i, j)] = ("0000")
                
        self.matrixValues = matrix_dict
        self.matrixEdges = matrix_edges

    def adjacent_cell(self, cell:tuple) -> list:
        """Devolve uma lista das células que fazem
        fronteira com a célula enviada no argumento"""
        row = cell[1]
        col = cell[2]
        lastCell = next(reversed(self.matrixValues))
    
        leftCell = (self.matrixValues.get((row, col-1)) if col-1 > 0 else None, row, col-1)
        rightCell = (self.matrixValues.get((row, col+1)) if col+1 <= lastCell[1] else None, row, col+1)
        upCell = (self.matrixValues.get((row-1, col)) if row-1 > 0 else None, row-1, col)
        downCell = (self.matrixValues.get((row+1, col)) if row+1 <= lastCell[0] else None, row+1, col)

        return [cell for cell in [leftCell, rightCell, upCell, downCell] if cell[0].isdigit()]

    def get_cell_edges(self, row:int, column:int) -> list:
        """Devolve os arestas da célula enviada no argumento"""
        return [('h', row, column), ('h', row+1, column),
                ('v', row, column), ('v', row, column+1)]

    def get_active_edges(self, row:int, column:int) -> list:
        """Devolve o número de arestas ativas"""
        edgeNum = self.matrixEdges.get((row, column))
        return edgeNum.count('1')
    
    def print_instance(self):
        l = len(self.matrixValues)
        m = 1
        for _, val in self.matrixEdges.items():
            if m == l:
                print(val, end="\n")
                m =1
            print(val, end=' ')




    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        matrix = []
        for i in stdin:
            line = i.split()
            for j in line:
                if j.isdigit():
                    line[line.index(j)] = int(j)
                else:
                    line[line.index(j)] = -1
            matrix.append(line)

        return Board(matrix)

    # TODO: outros metodos da classe

class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        """O construtor especifica o estado inicial."""
        # TODO
        pass


    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass


    def result(self, state: SlitherlinkState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: SlitherlinkState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass







