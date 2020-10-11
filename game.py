import pygame

from engine.display import Display
from engine.event_handler import EventHandler
from engine.vector2 import Vector2

# import path_finder as PathFinder
from path_finder import PathFinder
from board import Board
from test_tower import TestTower


class Game:
    board = None
    mouse_cell = None   # What cell is the mouse over?
    path = None     # What path will the enemies take?

    def start(self):
        self.board = Board()
        EventHandler.add_listener(pygame.MOUSEMOTION, self.mouse_motion_listener)
        EventHandler.add_listener(pygame.MOUSEBUTTONUP, self.mouse_up_listener)

        self.path = []
        self.update_path()

    def run_frame(self):
        EventHandler.run()

        Display.surface.fill((255, 255, 255))
        self.board.show_background()
        self.show_mouse_over_cell()
        self.board.show_towers()

        self.show_path()

        pygame.display.update()

    def update_path(self):
        """ Run the path finder and update self.path """
        self.path = PathFinder.find_path(self.board)

    def show_path(self):
        """ Show the path line
        As a bunch of dots """
        for i, cell in enumerate(self.path):
            color = (0, (i / len(self.path)) * 255, 0)
            pygame.draw.circle(Display.surface, color, self.board.get_cell_center(cell).get_pygame_tuple(), 3)

    def show_mouse_over_cell(self, color=(255, 255, 0)):
        """ Highlight the mouse_cell if it exists. """
        if self.mouse_cell:
            pygame.draw.rect(Display.surface, color, self.board.get_cell_rect(self.mouse_cell).get_pygame_tuple())

    def mouse_motion_listener(self, event):
        """ When there's a mouse motion event, set the mouse cell. """
        mouse_pos = Vector2(event.pos[0], event.pos[1])
        mouse_pos -= self.board.get_board_rect().get_top_left()
        mouse_pos /= self.board.get_cell_size()
        if 0 < mouse_pos.x < self.board.size.x and 0 < mouse_pos.y < self.board.size.y:
            self.mouse_cell = Vector2(int(mouse_pos.x), int(mouse_pos.y))
        else:
            self.mouse_cell = None

    def mouse_up_listener(self, event):
        """ When mouse 1 (left) is released, try make a tower.
        When mouse 3 (right) is released, try remove a tower. """
        board_change = False
        if event.button == 1:
            board_change = self.try_make_tower("HOES", self.mouse_cell)
        elif event.button == 3:
            board_change = self.sell_cell(self.mouse_cell)

        if board_change:
            self.update_path()

    def sell_cell(self, cell):
        """ Clears the cell. Refunding the player the towers refund amount.
        Returns true if cell contents was sold. """
        # TODO sell once money is in
        if self.board.get_cell_contents(cell):
            contains = True
        else:
            contains = False
        self.board.set_cell_contents(None, cell)
        return contains

    def try_make_tower(self, tower, cell):
        """ Try to make a tower at the position.
        Checks:
          - position (anything there? on board?)
          - is the tower valid (not None?)

        Returns true if new tower was made
        """
        # TODO buy once money is in
        # Is this a valid position? (Anything there already?)
        # Can the player afford this?
        if self.board.get_cell_contents(cell) is None:
            self.board.set_cell_contents(TestTower(cell), cell)
            return True
        else:
            return False
