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
import tkinter as tk

import utils
from utils import *

from slitherlink_gui import SlitherlinkGUI

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
        self.n_lines = len(matrixValues)
        self.n_columns = len(matrixValues[0]) if self.n_lines > 0 else 0
        matrix_dict = {}
        matrix_edges = {}
        for i, row in enumerate(matrixValues):
            for j, cell in enumerate(row):
                matrix_dict[(i+1, j+1)] = cell
                matrix_edges[(i+1, j+1)] = ("0000")
                
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
    
    def get_inactive_edges(self, row:int, column:int) -> list:
        """Devolve o número de arestas inativas"""
        edgeNum = self.matrixEdges.get((row, column))
        return edgeNum.count('0')
    
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
    def __str__(self):
        """Devolve uma representação em string do tabuleiro com arestas visíveis.
        Usa: == para arestas horizontais marcadas, -- para não marcadas
             || para arestas verticais marcadas, | para não marcadas
        Retorna erro se houver incompatibilidade entre células vizinhas."""
        
        def formatCell(value):
            return "." if value == -1 else str(value)
        
        # Validar consistência das arestas
        errors = []
        for r in range(1, self.n_lines + 1):
            for c in range(1, self.n_columns + 1):
                _, right, bottom, _ = self.matrixEdges[(r, c)]
                # Verificar bottom vs top da célula abaixo
                if r < self.n_lines:
                    if bottom != self.matrixEdges[(r+1, c)][0]:
                        errors.append(f"Aresta horizontal entre ({r},{c}) e ({r+1},{c}): incompatível ({bottom} vs {self.matrixEdges[(r+1, c)][0]})")
                # Verificar right vs left da célula à direita
                if c < self.n_columns:
                    if right != self.matrixEdges[(r, c+1)][3]:
                        errors.append(f"Aresta vertical entre ({r},{c}) e ({r},{c+1}): incompatível ({right} vs {self.matrixEdges[(r, c+1)][3]})")
        
        if errors:
            return "ERRO: Arestas com incompatibilidade:\n" + "\n".join(errors)
        
        # Construir representação visual
        lines = []
        
        for i in range(1, self.n_lines + 1):
            # Linha superior com arestas horizontais
            h_line = "+"
            for j in range(1, self.n_columns + 1):
                top_edge = self.matrixEdges[(i, j)][0]
                h_symbol = "=" if top_edge == '1' else "-"
                h_line += h_symbol * 4 + "+"
            lines.append(h_line)
            
            # Linha com células e arestas verticais
            cell_line = ""
            for j in range(1, self.n_columns + 1):
                left_edge = self.matrixEdges[(i, j)][3]
                v_symbol = "||" if left_edge == '1' else " |"
                cell = formatCell(self.matrixValues[(i, j)]).center(3)
                cell_line += v_symbol + cell
            
            # Aresta vertical direita da última coluna
            right_edge = self.matrixEdges[(i, self.n_columns)][1]
            v_symbol = "||" if right_edge == '1' else " |"
            cell_line += v_symbol
            lines.append(cell_line)
        
        # Linha final com arestas horizontais inferiores
        h_line = "+"
        for j in range(1, self.n_columns + 1):
            bottom_edge = self.matrixEdges[(self.n_lines, j)][2]
            h_symbol = "=" if bottom_edge == '1' else "-"
            h_line += h_symbol * 4 + "+"
        lines.append(h_line)
        
        return "\n".join(lines)
    
    def boardToList(self):
        """Devolve uma representação em lista do tabuleiro, onde cada célula é representada por um número de 0 a 3 ou None, e as arestas são representadas por '1' para ativas e '0' para inativas."""
        board_list = []
        for r in range(1, self.n_lines + 1):
            row = []
            for c in range(1, self.n_columns + 1):
                cell_value = self.matrixValues[(r, c)]
                row.append(cell_value)
            board_list.append(row)
        return board_list

class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        """O construtor especifica o estado inicial."""
        # TODO
        self.initial_state = SlitherlinkState(board)
        self.gui = gui


    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        #eu acho que da pra fazer com 1/4 do tempo
        matrix  =  state.board.matrixEdges
        seen = set()
        for key, value in matrix.items():
            edges = state.board.get_cell_edges(key[0], key[1])
            for idx, active in enumerate(value):
                if active == '0':
                    seen.add(edges[idx])

        return list(seen)


    def result(self, state: SlitherlinkState, action:list[tuple]):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        new_board = copy.deepcopy(state.board)
        edge_type, line, column = action
        if edge_type == 'h':
        # edge is top of cell (line,column) and bottom of cell (line-1,column)
        # top index = 0, bottom index = 2
            if (line, column) in new_board.matrixEdges:
                new_board.matrixEdges[(line, column)] = '1' + new_board.matrixEdges[(line, column)][1:]
            if (line-1, column) in new_board.matrixEdges:
                new_board.matrixEdges[(line - 1, column)] = new_board.matrixEdges[(line-1, column)][:2] + '1' + new_board.matrixEdges[(line-1, column)][3]
        elif edge_type == 'v':
        # edge is left of cell (line,column) and right of cell (line,column-1)
        # right index = 1, left index = 3
            if (line, column) in new_board.matrixEdges: 
                new_board.matrixEdges[(line, column)] = new_board.matrixEdges[(line, column)][:3] + '1' 
            if (line, column-1) in new_board.matrixEdges:
                new_board.matrixEdges[(line, column-1)] = new_board.matrixEdges[(line, column-1)][0] + '1' + new_board.matrixEdges[(line, column-1)][2:] 

        return SlitherlinkState(new_board)


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
    board = Board.parse_instance()
    root = tk.Tk()
    app = SlitherlinkGUI(root, board.boardToList())
    
    problem = Slitherlink(board, gui=app)
    print(problem.actions(problem.initial_state))

    print(board)
    s0 = problem.result(problem.initial_state, ('v', 1, 1))
    s1 = problem.result(s0, ('v', 3, 5))
    s2 = problem.result(s1, ('h', 2, 3))
        
    print("\n\n\n")
    app.update_from_state(s2.board)

    print(s0.board)

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    root.mainloop()







