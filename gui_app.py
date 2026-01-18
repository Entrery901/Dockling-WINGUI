#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dockling WINGUI — приложение, работающее из коробки.
Конвертация документов в Markdown для RAG и ИИ.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui_widgets import MainWindow
from gui_controller import ConversionController
from config_manager import ConfigManager
from i18n import I18n


class DocklingGUIApp:
    """Main Dockling GUI application"""

    def __init__(self):
        """Initialize the application"""
        # Create root window
        self.root = tk.Tk()
        self.root.title(I18n.get('app_title'))
        self.root.geometry("850x950")
        self.root.minsize(700, 700)
        self.set_window_icon()

        # Setup styles
        self.setup_styles()

        # Load configuration
        self.config = ConfigManager.load_config()

        # Create controller
        self.controller = ConversionController(self.root, self.config)

        # Create main window
        self.main_window = MainWindow(self.root, self.controller, self.config)

        # Connect controller to UI components
        self.controller.set_ui_components(
            self.main_window.config_panel,
            self.main_window.control_panel,
            self.main_window.progress_panel,
            self.main_window.stats_panel,
            self.main_window.log_panel
        )

        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Развернуть окно на весь экран при первом запуске — все элементы видны без ручного разворачивания
        self.root.update_idletasks()
        try:
            self.root.state('zoomed')  # Windows: максимизация
        except tk.TclError:
            # На некоторых платформах 'zoomed' недоступен — центрируем с большим размером
            self.center_window()

        # Log welcome message
        self.main_window.log_panel.append_log(
            'ℹ',
            f"Dockling WINGUI {I18n.get('status_ready')}",
            'INFO'
        )

        # Close splash screen if running from PyInstaller
        try:
            import pyi_splash
            pyi_splash.close()
        except:
            pass  # Not running from PyInstaller or splash not available

    def setup_styles(self):
        """Setup ttk styles for better appearance"""
        style = ttk.Style()

        # Try to use a modern theme
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')

        # Configure colors
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        style.configure('TLabelframe', background='#f0f0f0')
        style.configure('TLabelframe.Label', background='#f0f0f0')

        # Configure button styles
        style.configure('TButton', padding=6)

        # Configure progressbar
        style.configure('TProgressbar', thickness=20)

    def set_window_icon(self):
        """Set application window icon"""
        try:
            icon_path = self._resource_path(os.path.join("images", "icon.png"))
            if os.path.exists(icon_path):
                icon_image = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon_image)
                self._icon_image = icon_image
        except Exception:
            pass

    @staticmethod
    def _resource_path(relative_path: str) -> str:
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, relative_path)

    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()

        # Get window dimensions
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set position
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def on_closing(self):
        """Handle window close event"""
        if self.controller.is_running:
            response = messagebox.askokcancel(
                I18n.get('quit'),
                I18n.get('quit_confirmation')
            )
            if response:
                self.controller.stop_conversion()
                self.root.after(500, self.root.destroy)  # Give time for cleanup
        else:
            self.root.destroy()

    def run(self):
        """Start the application main loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror(
                I18n.get('msg_error'),
                I18n.get('msg_unexpected_error', error=str(e))
            )
            raise


def main():
    """Main function"""
    try:
        # Create and run application
        app = DocklingGUIApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
