"""
Input Handler for Buttons, Joysticks, and Touch
"""

import pygame
from config import gpio_pins

class InputHandler:
    def __init__(self):
        self.button_states = {}
        self.joystick_states = {'left_x': 0, 'left_y': 0, 'right_x': 0, 'right_y': 0}
        
        for button in gpio_pins.BUTTONS:
            self.button_states[button] = False
        
        for dpad in gpio_pins.DPAD:
            self.button_states[dpad] = False
        
        self.touch_pos = None
        self.touch_pressed = False
        
        self._init_pygame_input()
    
    def _init_pygame_input(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self._map_keyboard_to_button(event.key, True)
        elif event.type == pygame.KEYUP:
            self._map_keyboard_to_button(event.key, False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.touch_pos = event.pos
            self.touch_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.touch_pressed = False
        elif event.type == pygame.MOUSEMOTION and self.touch_pressed:
            self.touch_pos = event.pos
        
        if event.type == pygame.JOYBUTTONDOWN and self.joystick:
            self._map_joystick_button(event.button, True)
        elif event.type == pygame.JOYBUTTONUP and self.joystick:
            self._map_joystick_button(event.button, False)
    
    def _map_keyboard_to_button(self, key, pressed):
        key_map = {
            pygame.K_ESCAPE: 'HOME',
            pygame.K_RETURN: 'START',
            pygame.K_BACKSPACE: 'SELECT',
            pygame.K_a: 'A',
            pygame.K_s: 'B',
            pygame.K_d: 'X',
            pygame.K_w: 'Y',
            pygame.K_q: 'L',
            pygame.K_e: 'R',
            pygame.K_UP: 'UP',
            pygame.K_DOWN: 'DOWN',
            pygame.K_LEFT: 'LEFT',
            pygame.K_RIGHT: 'RIGHT',
            pygame.K_f: 'FRIENDS',
            pygame.K_p: 'POWER',
        }
        if key in key_map:
            self.button_states[key_map[key]] = pressed
    
    def _map_joystick_button(self, button, pressed):
        button_map = {
            0: 'A',
            1: 'B',
            2: 'X',
            3: 'Y',
            4: 'L',
            5: 'R',
            6: 'SELECT',
            7: 'START',
            8: 'HOME',
        }
        if button in button_map:
            self.button_states[button_map[button]] = pressed
    
    def get_button_states(self):
        return self.button_states.copy()
    
    def get_touch_pos(self):
        return self.touch_pos
    
    def is_touch_pressed(self):
        return self.touch_pressed
