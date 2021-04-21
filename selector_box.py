
class SelectorBox():
    def __init__(self):
        self.draw_new_selection_box = False
        self.selection_completed = False

    def draw_selection(self):
        if unit_selector.draw_new_selection_box:
            selection_box_x = current_mouse_location[0] - leftclick_down_location[0]
            selection_box_y = current_mouse_location[1] - leftclick_down_location[1]
            selection_box = pygame.Rect((leftclick_down_location), (selection_box_x, selection_box_y))
            return selection_box