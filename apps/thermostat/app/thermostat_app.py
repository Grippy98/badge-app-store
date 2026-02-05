"""Thermostat - Smart thermostat control and monitoring demo.

Control temperature settings and monitor your home climate.
"""

import sys
if "core" not in sys.path: sys.path.append("core")
from core import app
import lvgl as lv

class ThermostatApp(app.App):
    def __init__(self):
        super().__init__("Thermostat")
        self.screen = None
        self.current_temp = 72  # Current temperature
        self.target_temp = 72   # Target temperature
        self.mode = "auto"      # auto, heat, cool, off
        self.fan = "auto"       # auto, on

        # UI elements
        self.temp_label = None
        self.target_label = None
        self.mode_label = None
        self.status_label = None

    def enter(self, on_exit=None):
        self.on_exit = on_exit

        # Create screen
        self.screen = lv.obj()
        self.screen.set_style_bg_color(lv.color_white(), 0)
        lv.screen_load(self.screen)

        # Title
        title = lv.label(self.screen)
        title.set_text("Thermostat")
        title.set_style_text_color(lv.color_black(), 0)
        title.align(lv.ALIGN.TOP_MID, 0, 10)
        try:
            title.set_style_text_font(lv.font_montserrat_18, 0)
        except:
            pass

        # Current temperature display (MAXIMUM SIZE)
        # Create a container for better layout
        temp_cont = lv.obj(self.screen)
        temp_cont.set_size(300, 150)
        temp_cont.align(lv.ALIGN.CENTER, 0, -20)
        temp_cont.set_style_bg_opa(0, 0)
        temp_cont.set_style_border_width(0, 0)
        temp_cont.set_style_pad_all(0, 0)

        self.temp_label = lv.label(temp_cont)
        self.temp_label.set_text(f"{self.current_temp}")
        self.temp_label.set_style_text_color(lv.color_black(), 0)
        # Try to find and use the largest available font
        font_found = False
        for font_size in [48, 42, 38, 32, 28, 24, 20, 18, 16, 14]:
            try:
                font = getattr(lv, f'font_montserrat_{font_size}')
                self.temp_label.set_style_text_font(font, 0)
                font_found = True
                break
            except AttributeError:
                continue
        if not font_found:
            # Use default font if nothing else works
            pass
        self.temp_label.set_style_text_line_space(0, 0)
        self.temp_label.set_style_pad_all(0, 0)
        self.temp_label.align(lv.ALIGN.CENTER, -20, 0)

        # Degree label - positioned right next to the temperature
        degree_label = lv.label(temp_cont)
        degree_label.set_text("°F")
        degree_label.set_style_text_color(lv.color_black(), 0)
        try:
            degree_label.set_style_text_font(lv.font_montserrat_28, 0)
        except AttributeError:
            try:
                degree_label.set_style_text_font(lv.font_montserrat_24, 0)
            except AttributeError:
                pass
        degree_label.align_to(self.temp_label, lv.ALIGN.OUT_RIGHT_TOP, 5, 0)

        # Target temperature
        self.target_label = lv.label(self.screen)
        self.target_label.set_text(f"Target: {self.target_temp}°F")
        self.target_label.set_style_text_color(lv.color_black(), 0)
        try:
            self.target_label.set_style_text_font(lv.font_montserrat_16, 0)
        except:
            pass
        self.target_label.align(lv.ALIGN.CENTER, 0, 30)

        # Mode display
        self.mode_label = lv.label(self.screen)
        self.mode_label.set_text(f"Mode: {self.mode.upper()}")
        self.mode_label.set_style_text_color(lv.color_black(), 0)
        try:
            self.mode_label.set_style_text_font(lv.font_montserrat_14, 0)
        except:
            pass
        self.mode_label.align(lv.ALIGN.CENTER, 0, 60)

        # Status
        self.status_label = lv.label(self.screen)
        self.update_status()
        self.status_label.set_style_text_color(lv.color_black(), 0)
        try:
            self.status_label.set_style_text_font(lv.font_montserrat_12, 0)
        except:
            pass
        self.status_label.align(lv.ALIGN.CENTER, 0, 85)

        # Instructions
        info_label = lv.label(self.screen)
        info_label.set_text("UP/DN: Temp | L/R: Mode | ESC: Exit")
        info_label.set_style_text_color(lv.color_black(), 0)
        info_label.align(lv.ALIGN.BOTTOM_MID, 0, -5)
        try:
            info_label.set_style_text_font(lv.font_montserrat_10, 0)
        except:
            pass

        # Setup input
        import input
        if input.driver and input.driver.group:
            input.driver.group.remove_all_objs()
            input.driver.group.add_obj(self.screen)
            lv.group_focus_obj(self.screen)

        self.screen.add_event_cb(self.on_key, lv.EVENT.KEY, None)

    def update_status(self):
        """Update status label based on current vs target temp."""
        if self.mode == "off":
            status = "System OFF"
        elif self.current_temp < self.target_temp - 1:
            status = "HEATING" if self.mode in ["auto", "heat"] else "Idle"
        elif self.current_temp > self.target_temp + 1:
            status = "COOLING" if self.mode in ["auto", "cool"] else "Idle"
        else:
            status = "At target"

        self.status_label.set_text(f"Status: {status}")

    def on_key(self, e):
        key = e.get_key()

        if key == lv.KEY.ESC:
            self.exit()
            if self.on_exit:
                self.on_exit()

        elif key == lv.KEY.UP:
            # Increase target temperature
            self.target_temp = min(90, self.target_temp + 1)
            self.target_label.set_text(f"Target: {self.target_temp}°F")
            self.update_status()
            lv.refr_now(None)

        elif key == lv.KEY.DOWN:
            # Decrease target temperature
            self.target_temp = max(60, self.target_temp - 1)
            self.target_label.set_text(f"Target: {self.target_temp}°F")
            self.update_status()
            lv.refr_now(None)

        elif key == lv.KEY.RIGHT:
            # Cycle mode forward: auto -> heat -> cool -> off -> auto
            modes = ["auto", "heat", "cool", "off"]
            current_idx = modes.index(self.mode)
            self.mode = modes[(current_idx + 1) % len(modes)]
            self.mode_label.set_text(f"Mode: {self.mode.upper()}")
            self.update_status()
            lv.refr_now(None)

        elif key == lv.KEY.LEFT:
            # Cycle mode backward
            modes = ["auto", "heat", "cool", "off"]
            current_idx = modes.index(self.mode)
            self.mode = modes[(current_idx - 1) % len(modes)]
            self.mode_label.set_text(f"Mode: {self.mode.upper()}")
            self.update_status()
            lv.refr_now(None)

    def exit(self):
        if self.screen:
            self.screen.delete()
            self.screen = None
        self.temp_label = None
        self.target_label = None
        self.mode_label = None
        self.status_label = None
