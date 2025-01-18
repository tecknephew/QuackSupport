import base64
import io

import pyautogui
from PIL import Image


class ComputerControl:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.PAUSE = 0.5  # Add a small delay between actions for stability
        self.position_callback = None  # Add callback for position updates

    def set_position_callback(self, callback):
        """Set the callback for position updates"""
        self.position_callback = callback

    def perform_action(self, action):
        action_type = action["type"]

        if action_type == "mouse_move":
            x, y = self.map_from_ai_space(action["x"], action["y"])
            print(f"Nicolas {x}")
            print(f"Nicolas{y}")
            pyautogui.moveTo(x, y)
            self.position_callback(int(x), int(y))
        elif action_type == "left_click":
            return
        elif action_type == "right_click":
            return
        elif action_type == "middle_click":
            return
        elif action_type == "double_click":
            return
        elif action_type == "left_click_drag":
            return
        elif action_type == "type":
            return
        elif action_type == "key":
            return
        elif action_type == "screenshot":
            return
        elif action_type == "cursor_position":
            x, y = self.map_from_ai_space(action["x"], action["y"])
            self.position_callback(int(x), int(y))
        else:
            raise ValueError(f"Unsupported action: {action_type}")

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        ai_screenshot = self.resize_for_ai(screenshot)
        buffered = io.BytesIO()
        ai_screenshot.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def map_from_ai_space(self, x, y):
        ai_width, ai_height = 1280, 800
        return (x * self.screen_width / ai_width, y * self.screen_height / ai_height)

    def map_to_ai_space(self, x, y):
        ai_width, ai_height = 1280, 800
        return (x * ai_width / self.screen_width, y * ai_height / self.screen_height)

    def resize_for_ai(self, screenshot):
        return screenshot.resize((1280, 800), Image.LANCZOS)
