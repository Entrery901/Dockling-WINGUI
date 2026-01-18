#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI widgets for Dockling WINGUI.
Tabs, panels, and controls.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys
import webbrowser
from typing import Dict, Any, Callable, Optional
from i18n import I18n


class MainWindow:
    """Main application window container"""

    def __init__(self, root: tk.Tk, controller: Any, config: Dict[str, Any]):
        """
        Initialize main window

        Args:
            root: Tk root window
            controller: Application controller
            config: Configuration dictionary
        """
        self.root = root
        self.controller = controller
        self.config = config

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Create components
        self.language_switcher = LanguageSwitcher(self.main_frame, self.on_language_change)
        self.language_switcher.frame.grid(row=0, column=0, sticky=(tk.E), pady=(0, 10))

        self.config_panel = ConfigPanel(self.main_frame, config)
        self.config_panel.frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.main_frame.rowconfigure(1, weight=0)

        self.control_panel = ControlPanel(self.main_frame, controller)
        self.control_panel.frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        self.progress_panel = ProgressPanel(self.main_frame)
        self.progress_panel.frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        self.stats_panel = StatsPanel(self.main_frame)
        self.stats_panel.frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        self.log_panel = LogPanel(self.main_frame)
        self.log_panel.frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        self.main_frame.rowconfigure(5, weight=1, minsize=180)

        # Register for i18n updates
        I18n.register_callback(self.update_texts)

    def on_language_change(self, lang: str):
        """Handle language change"""
        I18n.set_language(lang)

    def update_texts(self):
        """Update all text labels to current language"""
        self.root.title(I18n.get('app_title'))
        self.config_panel.update_texts()
        self.control_panel.update_texts()
        self.progress_panel.update_texts()
        self.stats_panel.update_texts()
        self.log_panel.update_texts()


class LanguageSwitcher:
    """Language selection widget"""

    def __init__(self, parent: ttk.Frame, callback: Callable[[str], None]):
        self.frame = ttk.Frame(parent)
        self.callback = callback

        # Language buttons
        self.lang_var = tk.StringVar(value=I18n.current_language)

        self.btn_ru = ttk.Radiobutton(
            self.frame,
            text="РУ",
            variable=self.lang_var,
            value="ru",
            command=self._on_change
        )
        self.btn_ru.pack(side=tk.LEFT, padx=2)

        self.btn_en = ttk.Radiobutton(
            self.frame,
            text="EN",
            variable=self.lang_var,
            value="en",
            command=self._on_change
        )
        self.btn_en.pack(side=tk.LEFT, padx=2)

    def _on_change(self):
        """Handle language change"""
        self.callback(self.lang_var.get())


class ConfigPanel:
    """Configuration panel with tabs"""

    def __init__(self, parent: ttk.Frame, config: Dict[str, Any]):
        self.config = config
        self.frame = ttk.LabelFrame(parent, text=I18n.get('tab_api'), padding="10")

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.api_tab = ApiTab(self.notebook, config)
        self.paths_tab = PathsTab(self.notebook, config)
        self.processing_tab = ProcessingTab(self.notebook, config)
        self.hardware_tab = HardwareTab(self.notebook, config)
        self.limits_tab = LimitsTab(self.notebook, config)
        self.about_tab = AboutTab(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.api_tab.frame, text=I18n.get('tab_api'))
        self.notebook.add(self.paths_tab.frame, text=I18n.get('tab_paths'))
        self.notebook.add(self.processing_tab.frame, text=I18n.get('tab_processing'))
        self.notebook.add(self.hardware_tab.frame, text=I18n.get('tab_hardware'))
        self.notebook.add(self.limits_tab.frame, text=I18n.get('tab_limits'))
        self.notebook.add(self.about_tab.frame, text=I18n.get('tab_about'))

    def update_texts(self):
        """Update tab labels"""
        self.notebook.tab(0, text=I18n.get('tab_api'))
        self.notebook.tab(1, text=I18n.get('tab_paths'))
        self.notebook.tab(2, text=I18n.get('tab_processing'))
        self.notebook.tab(3, text=I18n.get('tab_hardware'))
        self.notebook.tab(4, text=I18n.get('tab_limits'))
        self.notebook.tab(5, text=I18n.get('tab_about'))
        self.api_tab.update_texts()
        self.paths_tab.update_texts()
        self.processing_tab.update_texts()
        self.hardware_tab.update_texts()
        self.limits_tab.update_texts()
        self.about_tab.update_texts()

    def get_config(self) -> Dict[str, Any]:
        """Get configuration from all tabs"""
        config = {}
        config.update(self.api_tab.get_values())
        config.update(self.paths_tab.get_values())
        config.update(self.processing_tab.get_values())
        config.update(self.hardware_tab.get_values())
        config.update(self.limits_tab.get_values())
        return config


class ApiTab:
    """API settings tab"""

    def __init__(self, parent: ttk.Notebook, config: Dict[str, Any]):
        self.frame = ttk.Frame(parent, padding="10")
        self.default_max_tokens = int(config.get('OPENAI_MAX_TOKENS', 400))

        row = 0

        # API Key
        self.api_key_label = ttk.Label(self.frame, text=I18n.get('api_key_label'))
        self.api_key_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar(value=config.get('OPENAI_API_KEY', ''))
        self.api_key_entry = ttk.Entry(self.frame, textvariable=self.api_key_var, width=50, show='*')
        self.api_key_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        row += 1

        # Model Name
        self.api_model_label = ttk.Label(self.frame, text=I18n.get('api_model_label'))
        self.api_model_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value=config.get('OPENAI_MODEL_NAME', 'x-ai/grok-4-fast'))
        self.model_entry = ttk.Entry(self.frame, textvariable=self.model_var, width=50)
        self.model_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        row += 1

        # Max tokens
        self.api_max_tokens_label = ttk.Label(self.frame, text=I18n.get('api_max_tokens_label'))
        self.api_max_tokens_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.max_tokens_var = tk.StringVar(value=str(self.default_max_tokens))
        self.max_tokens_entry = ttk.Entry(self.frame, textvariable=self.max_tokens_var, width=10)
        self.max_tokens_entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        row += 1

        # Base URL
        self.api_base_url_label = ttk.Label(self.frame, text=I18n.get('api_base_url_label'))
        self.api_base_url_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.base_url_var = tk.StringVar(value=config.get('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1'))
        self.base_url_entry = ttk.Entry(self.frame, textvariable=self.base_url_var, width=50)
        self.base_url_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        row += 1

        # Enable Picture Description (single toggle)
        desc_enabled = bool(
            config.get('ENABLE_PICTURE_DESCRIPTION', False)
            or config.get('USE_OPENAI_API', False)
        )
        self.pic_desc_var = tk.BooleanVar(value=desc_enabled)
        self.pic_desc_cb = ttk.Checkbutton(
            self.frame,
            text=I18n.get('api_enable_desc'),
            variable=self.pic_desc_var
        )
        self.pic_desc_cb.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        # Description Prompt
        self.api_prompt_label = ttk.Label(self.frame, text=I18n.get('api_prompt_label'))
        self.api_prompt_label.grid(row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        self.prompt_var = tk.StringVar(value=config.get('PICTURE_DESCRIPTION_PROMPT', I18n.get('api_prompt_default')))
        self.prompt_text = tk.Text(self.frame, width=50, height=3)
        self.prompt_text.insert('1.0', self.prompt_var.get())
        self.prompt_text.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        row += 1

        # Подсказка внизу вкладки
        ttk.Separator(self.frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 6))
        row += 1
        self.hint_label = ttk.Label(self.frame, text=I18n.get('hint_api'), wraplength=700, justify=tk.LEFT)
        self.hint_label.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.N), pady=(0, 5))
        self.frame.rowconfigure(row, weight=1)

        # Configure column weights
        self.frame.columnconfigure(1, weight=1)

    def update_texts(self):
        """Update text labels"""
        self.api_key_label.config(text=I18n.get('api_key_label'))
        self.api_model_label.config(text=I18n.get('api_model_label'))
        self.api_max_tokens_label.config(text=I18n.get('api_max_tokens_label'))
        self.api_base_url_label.config(text=I18n.get('api_base_url_label'))
        self.pic_desc_cb.config(text=I18n.get('api_enable_desc'))
        self.api_prompt_label.config(text=I18n.get('api_prompt_label'))
        if hasattr(self, 'hint_label'):
            self.hint_label.config(text=I18n.get('hint_api'))

    def get_values(self) -> Dict[str, Any]:
        """Get values from all fields"""
        max_tokens = self._parse_int(self.max_tokens_var.get(), self.default_max_tokens)
        use_api = self.pic_desc_var.get()
        return {
            'OPENAI_API_KEY': self.api_key_var.get(),
            'OPENAI_MODEL_NAME': self.model_var.get(),
            'OPENAI_BASE_URL': self.base_url_var.get(),
            'OPENAI_MAX_TOKENS': max_tokens,
            'USE_OPENAI_API': use_api,
            'ENABLE_PICTURE_DESCRIPTION': use_api,
            'PICTURE_DESCRIPTION_PROMPT': self.prompt_text.get('1.0', tk.END).strip(),
            'ENABLE_REMOTE_SERVICES': use_api
        }

    @staticmethod
    def _parse_int(value: str, fallback: int) -> int:
        try:
            parsed = int(str(value).strip())
            return parsed if parsed > 0 else fallback
        except Exception:
            return fallback


class PathsTab:
    """Paths and file selection tab"""

    def __init__(self, parent: ttk.Notebook, config: Dict[str, Any]):
        self.frame = ttk.Frame(parent, padding="10")
        self.selected_files = []

        row = 0

        # Title section
        self.title_label = ttk.Label(self.frame, text=I18n.get('paths_title'),
                                     font=('TkDefaultFont', 10, 'bold'))
        self.title_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0,10))
        row += 1

        # === INPUT SECTION ===
        self.input_frame = ttk.LabelFrame(self.frame, text="📂 " + I18n.get('paths_input_section'), padding="10")
        self.input_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1

        # Processing mode (inside input frame)
        mode_row = 0
        self.mode_var = tk.StringVar(value="folder")

        self.mode_folder_rb = ttk.Radiobutton(
            self.input_frame,
            text="📁 " + I18n.get('paths_mode_folder'),
            variable=self.mode_var,
            value="folder",
            command=self.on_mode_change
        )
        self.mode_folder_rb.grid(row=mode_row, column=0, columnspan=3, sticky=tk.W, pady=2)
        mode_row += 1

        # Input directory (for folder mode)
        self.input_dir_frame = ttk.Frame(self.input_frame)
        self.input_dir_frame.grid(row=mode_row, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=20, pady=2)
        mode_row += 1

        self.input_label = ttk.Label(self.input_dir_frame, text=I18n.get('paths_input_label'))
        self.input_label.grid(row=0, column=0, sticky=tk.W, padx=(0,5))
        self.input_dir_var = tk.StringVar(value=config.get('INPUT_DIR', 'input'))
        self.input_dir_var.trace_add('write', self.validate_input_path)
        self.input_dir_entry = ttk.Entry(self.input_dir_frame, textvariable=self.input_dir_var, width=50)
        self.input_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.input_browse_btn = ttk.Button(self.input_dir_frame, text="📁 " + I18n.get('paths_browse_button'),
                                          command=self.browse_input, width=12)
        self.input_browse_btn.grid(row=0, column=2, padx=5)
        self.input_dir_frame.columnconfigure(1, weight=1)

        # Input status label
        self.input_status_var = tk.StringVar(value="")
        self.input_status_label = ttk.Label(self.input_dir_frame, textvariable=self.input_status_var, foreground='gray')
        self.input_status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(2,0))

        # File selection mode
        self.mode_files_rb = ttk.Radiobutton(
            self.input_frame,
            text="📄 " + I18n.get('paths_mode_files'),
            variable=self.mode_var,
            value="files",
            command=self.on_mode_change
        )
        self.mode_files_rb.grid(row=mode_row, column=0, columnspan=3, sticky=tk.W, pady=2)
        mode_row += 1

        # File selection controls (for files mode)
        self.files_frame = ttk.Frame(self.input_frame)
        self.files_frame.grid(row=mode_row, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=20, pady=2)
        mode_row += 1

        self.select_files_btn = ttk.Button(
            self.files_frame,
            text="📄 " + I18n.get('paths_select_files_button'),
            command=self.select_files,
            state=tk.DISABLED,
            width=20
        )
        self.select_files_btn.grid(row=0, column=0, sticky=tk.W, pady=2)

        self.clear_files_btn = ttk.Button(
            self.files_frame,
            text="🗑 " + I18n.get('paths_clear_files'),
            command=self.clear_selected_files,
            state=tk.DISABLED,
            width=12
        )
        self.clear_files_btn.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        # Selected files count
        self.files_label_var = tk.StringVar(value=I18n.get('paths_selected_files', count=0))
        self.files_label = ttk.Label(self.files_frame, textvariable=self.files_label_var, foreground='blue')
        self.files_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(2,0))

        # Selected files listbox
        self.files_list_frame = ttk.Frame(self.files_frame)
        self.files_list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.files_listbox = tk.Listbox(self.files_list_frame, height=5, width=70)
        files_scrollbar = ttk.Scrollbar(self.files_list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        files_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.files_list_frame.columnconfigure(0, weight=1)
        self.files_list_frame.rowconfigure(0, weight=1)

        # === OUTPUT SECTION ===
        self.output_frame = ttk.LabelFrame(self.frame, text="💾 " + I18n.get('paths_output_section'), padding="10")
        self.output_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1

        # Output directory
        self.output_label = ttk.Label(self.output_frame, text=I18n.get('paths_output_label'))
        self.output_label.grid(row=0, column=0, sticky=tk.W, padx=(0,5), pady=5)
        self.output_dir_var = tk.StringVar(value=config.get('OUTPUT_DIR', 'output'))
        self.output_dir_var.trace_add('write', self.validate_output_path)
        self.output_dir_entry = ttk.Entry(self.output_frame, textvariable=self.output_dir_var, width=50)
        self.output_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.output_browse_btn = ttk.Button(self.output_frame, text="📁 " + I18n.get('paths_browse_button'),
                                           command=self.browse_output, width=12)
        self.output_browse_btn.grid(row=0, column=2, padx=5, pady=5)
        self.output_frame.columnconfigure(1, weight=1)

        # Output status label
        self.output_status_var = tk.StringVar(value="")
        self.output_status_label = ttk.Label(self.output_frame, textvariable=self.output_status_var, foreground='gray')
        self.output_status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0,5))

        # Auto-create output folder checkbox
        self.auto_create_var = tk.BooleanVar(value=True)
        self.auto_create_cb = ttk.Checkbutton(
            self.output_frame,
            text="✓ " + I18n.get('paths_auto_create'),
            variable=self.auto_create_var
        )
        self.auto_create_cb.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Подсказка внизу вкладки (row уже увеличен после output_frame)
        ttk.Separator(self.frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 6))
        row += 1
        self.hint_label = ttk.Label(self.frame, text=I18n.get('hint_paths'), wraplength=700, justify=tk.LEFT)
        self.hint_label.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.N), pady=(0, 5))
        self.frame.rowconfigure(row, weight=1)

        # Configure column weights
        self.frame.columnconfigure(1, weight=1)

    def validate_input_path(self, *args):
        """Validate input path and show status"""
        import os
        path = self.input_dir_var.get()
        if not path:
            self.input_status_var.set("")
            return

        if os.path.exists(path) and os.path.isdir(path):
            # Count files in directory
            try:
                supported_extensions = ('.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.html', '.htm', '.xml')
                file_count = sum(1 for f in os.listdir(path) if f.lower().endswith(supported_extensions))
                self.input_status_var.set(I18n.get('paths_status_folder_ok_files', count=file_count))
                self.input_status_label.config(foreground='green')
            except Exception as e:
                self.input_status_var.set(I18n.get('paths_status_read_error', err=str(e)))
                self.input_status_label.config(foreground='orange')
        else:
            self.input_status_var.set(I18n.get('paths_status_folder_missing'))
            self.input_status_label.config(foreground='red')

    def validate_output_path(self, *args):
        """Validate output path and show status"""
        import os
        path = self.output_dir_var.get()
        if not path:
            self.output_status_var.set("")
            return

        if os.path.exists(path) and os.path.isdir(path):
            self.output_status_var.set(I18n.get('paths_status_folder_ok'))
            self.output_status_label.config(foreground='green')
        else:
            if self.auto_create_var.get():
                self.output_status_var.set(I18n.get('paths_status_folder_auto'))
                self.output_status_label.config(foreground='orange')
            else:
                self.output_status_var.set(I18n.get('paths_status_folder_missing'))
                self.output_status_label.config(foreground='red')

    def browse_input(self):
        """Browse for input directory"""
        import os
        initial_dir = self.input_dir_var.get()
        if not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")

        directory = filedialog.askdirectory(
            title=I18n.get('msg_select_input_folder'),
            initialdir=initial_dir
        )
        if directory:
            self.input_dir_var.set(directory)

    def browse_output(self):
        """Browse for output directory"""
        import os
        initial_dir = self.output_dir_var.get()
        if not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")

        directory = filedialog.askdirectory(
            title=I18n.get('msg_select_output_folder'),
            initialdir=initial_dir
        )
        if directory:
            self.output_dir_var.set(directory)

    def select_files(self):
        """Select individual files"""
        import os
        filetypes = [
            (I18n.get('file_types_all'), '*.pdf *.docx *.doc *.pptx *.ppt *.xlsx *.xls *.html *.htm *.xml'),
            (I18n.get('file_types_pdf'), '*.pdf'),
            (I18n.get('file_types_word'), '*.docx *.doc'),
            (I18n.get('file_types_powerpoint'), '*.pptx *.ppt'),
            (I18n.get('file_types_excel'), '*.xlsx *.xls'),
            (I18n.get('file_types_html'), '*.html *.htm'),
            (I18n.get('file_types_all_files'), '*.*'),
        ]

        initial_dir = os.path.expanduser("~")
        if self.selected_files:
            initial_dir = os.path.dirname(self.selected_files[0])

        files = filedialog.askopenfilenames(
            title=I18n.get('msg_select_files'),
            filetypes=filetypes,
            initialdir=initial_dir
        )

        if files:
            self.selected_files = list(files)
            self.update_files_list()

    def clear_selected_files(self):
        """Clear selected files"""
        self.selected_files = []
        self.update_files_list()

    def update_files_list(self):
        """Update files listbox"""
        import os
        self.files_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            filename = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, f"📄 {filename}")

        count = len(self.selected_files)
        self.files_label_var.set(I18n.get('paths_selected_files', count=count))

        # Enable/disable clear button
        if count > 0:
            self.clear_files_btn.config(state=tk.NORMAL)
        else:
            self.clear_files_btn.config(state=tk.DISABLED)

    def on_mode_change(self):
        """Handle mode change"""
        if self.mode_var.get() == "files":
            self.select_files_btn.config(state=tk.NORMAL)
            self.input_dir_entry.config(state=tk.DISABLED)
            self.input_browse_btn.config(state=tk.DISABLED)
        else:
            self.select_files_btn.config(state=tk.DISABLED)
            self.clear_files_btn.config(state=tk.DISABLED)
            self.input_dir_entry.config(state=tk.NORMAL)
            self.input_browse_btn.config(state=tk.NORMAL)
            self.selected_files = []
            self.update_files_list()

        # Trigger initial validation
        self.validate_input_path()

    def update_texts(self):
        """Update text labels"""
        count = len(self.selected_files)
        self.files_label_var.set(I18n.get('paths_selected_files', count=count))
        self.title_label.config(text=I18n.get('paths_title'))
        self.input_frame.config(text="📂 " + I18n.get('paths_input_section'))
        self.output_frame.config(text="💾 " + I18n.get('paths_output_section'))
        self.mode_folder_rb.config(text="📁 " + I18n.get('paths_mode_folder'))
        self.mode_files_rb.config(text="📄 " + I18n.get('paths_mode_files'))
        self.input_label.config(text=I18n.get('paths_input_label'))
        self.output_label.config(text=I18n.get('paths_output_label'))
        self.input_browse_btn.config(text="📁 " + I18n.get('paths_browse_button'))
        self.output_browse_btn.config(text="📁 " + I18n.get('paths_browse_button'))
        self.select_files_btn.config(text="📄 " + I18n.get('paths_select_files_button'))
        self.clear_files_btn.config(text="🗑 " + I18n.get('paths_clear_files'))
        self.auto_create_cb.config(text="✓ " + I18n.get('paths_auto_create'))
        self.validate_input_path()
        self.validate_output_path()
        if hasattr(self, 'hint_label'):
            self.hint_label.config(text=I18n.get('hint_paths'))

    def get_values(self) -> Dict[str, Any]:
        """Get values from all fields"""
        return {
            'INPUT_DIR': self.input_dir_var.get(),
            'OUTPUT_DIR': self.output_dir_var.get(),
            'processing_mode': self.mode_var.get(),
            'selected_files': self.selected_files,
            'auto_create_output': self.auto_create_var.get()
        }


class ProcessingTab:
    """Processing options tab"""

    def __init__(self, parent: ttk.Notebook, config: Dict[str, Any]):
        self.frame = ttk.Frame(parent, padding="10")

        row = 0

        # OCR section
        self.ocr_var = tk.BooleanVar(value=config.get('ENABLE_OCR', True))
        self.ocr_cb = ttk.Checkbutton(
            self.frame,
            text=I18n.get('proc_ocr_enable'),
            variable=self.ocr_var,
            command=self.on_ocr_toggle
        )
        self.ocr_cb.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        # OCR Engine
        self.ocr_engine_label = ttk.Label(self.frame, text=I18n.get('proc_ocr_engine_label'))
        self.ocr_engine_label.grid(row=row, column=0, sticky=tk.W, padx=20, pady=5)
        self.ocr_engine_var = tk.StringVar(value=config.get('OCR_ENGINE', 'easyocr'))
        ocr_frame = ttk.Frame(self.frame)
        ocr_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.ocr_easy_rb = ttk.Radiobutton(ocr_frame, text=I18n.get('proc_ocr_engine_easyocr'), variable=self.ocr_engine_var, value="easyocr")
        self.ocr_easy_rb.pack(side=tk.LEFT, padx=5)
        self.ocr_tesseract_rb = ttk.Radiobutton(ocr_frame, text=I18n.get('proc_ocr_engine_tesseract'), variable=self.ocr_engine_var, value="tesseract")
        self.ocr_tesseract_rb.pack(side=tk.LEFT, padx=5)
        self.ocr_install_tesseract_btn = ttk.Button(ocr_frame, text=I18n.get('proc_tesseract_install_btn'), command=self._on_install_tesseract, width=16)
        self.ocr_install_tesseract_btn.pack(side=tk.LEFT, padx=5)
        row += 1

        # OCR Languages
        self.ocr_lang_label = ttk.Label(self.frame, text=I18n.get('proc_ocr_languages_label'))
        self.ocr_lang_label.grid(row=row, column=0, sticky=tk.W, padx=20, pady=5)
        self.ocr_lang_var = tk.StringVar(value=config.get('OCR_LANGUAGES', 'rus,eng'))
        self.ocr_lang_entry = ttk.Entry(self.frame, textvariable=self.ocr_lang_var, width=30)
        self.ocr_lang_entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        row += 1

        # Table recognition
        self.table_var = tk.BooleanVar(value=config.get('ENABLE_TABLE_STRUCTURE', True))
        self.table_cb = ttk.Checkbutton(
            self.frame,
            text=I18n.get('proc_table_enable'),
            variable=self.table_var,
            command=self.on_table_toggle
        )
        self.table_cb.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        # Table mode
        self.table_mode_label = ttk.Label(self.frame, text=I18n.get('proc_table_mode_label'))
        self.table_mode_label.grid(row=row, column=0, sticky=tk.W, padx=20, pady=5)
        self.table_mode_var = tk.StringVar(value=config.get('TABLE_STRUCTURE_MODE', 'accurate'))
        table_frame = ttk.Frame(self.frame)
        table_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.table_accurate_rb = ttk.Radiobutton(table_frame, text=I18n.get('proc_table_mode_accurate'), variable=self.table_mode_var, value="accurate")
        self.table_accurate_rb.pack(side=tk.LEFT, padx=5)
        self.table_fast_rb = ttk.Radiobutton(table_frame, text=I18n.get('proc_table_mode_fast'), variable=self.table_mode_var, value="fast")
        self.table_fast_rb.pack(side=tk.LEFT, padx=5)
        row += 1

        # Image extraction
        self.images_var = tk.BooleanVar(value=config.get('GENERATE_PICTURE_IMAGES', True))
        self.images_cb = ttk.Checkbutton(
            self.frame,
            text=I18n.get('proc_images_enable'),
            variable=self.images_var,
            command=self.on_images_toggle
        )
        self.images_cb.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        # Image scale
        self.images_scale_label = ttk.Label(self.frame, text=I18n.get('proc_images_scale_label'))
        self.images_scale_label.grid(row=row, column=0, sticky=tk.W, padx=20, pady=5)
        self.scale_var = tk.DoubleVar(value=config.get('IMAGES_SCALE', 2.0))
        self.scale_spin = ttk.Spinbox(self.frame, from_=0.5, to=5.0, increment=0.5, textvariable=self.scale_var, width=10)
        self.scale_spin.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        row += 1

        # Подсказка внизу вкладки
        ttk.Separator(self.frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 6))
        row += 1
        self.hint_label = ttk.Label(self.frame, text=I18n.get('hint_processing'), wraplength=700, justify=tk.LEFT)
        self.hint_label.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.N), pady=(0, 5))
        self.frame.rowconfigure(row, weight=1)

        # Initialize states
        self.on_ocr_toggle()
        self.on_table_toggle()
        self.on_images_toggle()

    def on_ocr_toggle(self):
        """Handle OCR enable/disable"""
        state = tk.NORMAL if self.ocr_var.get() else tk.DISABLED
        self.ocr_lang_entry.config(state=state)

    def on_table_toggle(self):
        """Handle table recognition enable/disable"""
        # Future: disable table mode selection when disabled
        pass

    def on_images_toggle(self):
        """Handle image extraction enable/disable"""
        state = tk.NORMAL if self.images_var.get() else tk.DISABLED
        self.scale_spin.config(state=state)

    def _on_install_tesseract(self):
        """Check Tesseract or open download page with instructions"""
        import shutil
        import webbrowser
        path = shutil.which('tesseract')
        if path:
            messagebox.showinfo(
                I18n.get('proc_tesseract_already_installed'),
                f"Tesseract: {path}"
            )
            return
        url = "https://github.com/UB-Mannheim/tesseract/wiki"
        messagebox.showinfo(
            I18n.get('proc_tesseract_download_page'),
            I18n.get('proc_tesseract_install_instructions')
        )
        webbrowser.open(url)

    def update_texts(self):
        """Update text labels"""
        self.ocr_cb.config(text=I18n.get('proc_ocr_enable'))
        self.ocr_engine_label.config(text=I18n.get('proc_ocr_engine_label'))
        self.ocr_easy_rb.config(text=I18n.get('proc_ocr_engine_easyocr'))
        self.ocr_tesseract_rb.config(text=I18n.get('proc_ocr_engine_tesseract'))
        self.ocr_install_tesseract_btn.config(text=I18n.get('proc_tesseract_install_btn'))
        self.ocr_lang_label.config(text=I18n.get('proc_ocr_languages_label'))
        self.table_cb.config(text=I18n.get('proc_table_enable'))
        self.table_mode_label.config(text=I18n.get('proc_table_mode_label'))
        self.table_accurate_rb.config(text=I18n.get('proc_table_mode_accurate'))
        self.table_fast_rb.config(text=I18n.get('proc_table_mode_fast'))
        self.images_cb.config(text=I18n.get('proc_images_enable'))
        self.images_scale_label.config(text=I18n.get('proc_images_scale_label'))
        if hasattr(self, 'hint_label'):
            self.hint_label.config(text=I18n.get('hint_processing'))

    def get_values(self) -> Dict[str, Any]:
        """Get values from all fields"""
        return {
            'ENABLE_OCR': self.ocr_var.get(),
            'OCR_ENGINE': self.ocr_engine_var.get(),
            'OCR_LANGUAGES': self.ocr_lang_var.get(),
            'ENABLE_TABLE_STRUCTURE': self.table_var.get(),
            'TABLE_STRUCTURE_MODE': self.table_mode_var.get(),
            'GENERATE_PICTURE_IMAGES': self.images_var.get(),
            'IMAGES_SCALE': self.scale_var.get()
        }


class HardwareTab:
    """Hardware acceleration tab"""

    def __init__(self, parent: ttk.Notebook, config: Dict[str, Any]):
        self.frame = ttk.Frame(parent, padding="10")

        row = 0

        # Accelerator selection
        self.hw_accelerator_label = ttk.Label(self.frame, text=I18n.get('hw_accelerator_label'))
        self.hw_accelerator_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.accelerator_var = tk.StringVar(value=config.get('ACCELERATOR_DEVICE', 'cuda').lower())
        self.accelerator_combo = ttk.Combobox(
            self.frame,
            textvariable=self.accelerator_var,
            values=['auto', 'cpu', 'cuda', 'gpu', 'mps'],
            state='readonly',
            width=20
        )
        self.accelerator_combo.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        row += 1

        # CPU threads
        self.hw_cpu_threads_label = ttk.Label(self.frame, text=I18n.get('hw_cpu_threads_label'))
        self.hw_cpu_threads_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.threads_var = tk.IntVar(value=config.get('ACCELERATOR_NUM_THREADS', 0))
        self.threads_spin = ttk.Spinbox(self.frame, from_=0, to=32, textvariable=self.threads_var, width=10)
        self.threads_spin.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        self.hw_cpu_threads_hint = ttk.Label(self.frame, text=I18n.get('hw_cpu_threads_hint'))
        self.hw_cpu_threads_hint.grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1

        # GPU status
        self.hw_gpu_status_label = ttk.Label(self.frame, text=I18n.get('hw_gpu_status_label'))
        self.hw_gpu_status_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.gpu_status_var = tk.StringVar(value=self.detect_gpu())
        self.gpu_status_label = ttk.Label(self.frame, textvariable=self.gpu_status_var)
        self.gpu_status_label.grid(row=row, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        row += 1

        # Подсказка внизу вкладки
        ttk.Separator(self.frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 6))
        row += 1
        self.hint_label = ttk.Label(self.frame, text=I18n.get('hint_hardware'), wraplength=700, justify=tk.LEFT)
        self.hint_label.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.N), pady=(0, 5))
        self.frame.rowconfigure(row, weight=1)

    def detect_gpu(self) -> str:
        """Detect GPU availability"""
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                return f"✓ {I18n.get('hw_gpu_detected', name=gpu_name)}"
            else:
                return f"⊝ {I18n.get('hw_gpu_not_detected')}"
        except ImportError:
            return f"⚠ {I18n.get('hw_pytorch_not_installed')}"
        except Exception as e:
            return f"⚠ {I18n.get('hw_cuda_not_available')}: {str(e)}"

    def update_texts(self):
        """Update text labels"""
        self.hw_accelerator_label.config(text=I18n.get('hw_accelerator_label'))
        self.hw_cpu_threads_label.config(text=I18n.get('hw_cpu_threads_label'))
        self.hw_cpu_threads_hint.config(text=I18n.get('hw_cpu_threads_hint'))
        self.hw_gpu_status_label.config(text=I18n.get('hw_gpu_status_label'))
        self.gpu_status_var.set(self.detect_gpu())
        if hasattr(self, 'hint_label'):
            self.hint_label.config(text=I18n.get('hint_hardware'))

    def get_values(self) -> Dict[str, Any]:
        """Get values from all fields"""
        return {
            'ACCELERATOR_DEVICE': self.accelerator_var.get(),
            'ACCELERATOR_NUM_THREADS': self.threads_var.get()
        }


class LimitsTab:
    """Conversion limits tab"""

    def __init__(self, parent: ttk.Notebook, config: Dict[str, Any]):
        self.frame = ttk.Frame(parent, padding="10")

        row = 0

        # Max file size
        self.limits_max_size_label = ttk.Label(self.frame, text=I18n.get('limits_max_size_label'))
        self.limits_max_size_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        max_size_mb = config.get('MAX_FILE_SIZE', 52428800) // (1024 * 1024)
        self.max_size_var = tk.IntVar(value=max_size_mb)
        self.max_size_spin = ttk.Spinbox(self.frame, from_=0, to=1000, textvariable=self.max_size_var, width=10)
        self.max_size_spin.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        self.limits_max_size_hint = ttk.Label(self.frame, text=I18n.get('limits_max_size_hint'))
        self.limits_max_size_hint.grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1

        # Max pages
        self.limits_max_pages_label = ttk.Label(self.frame, text=I18n.get('limits_max_pages_label'))
        self.limits_max_pages_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.max_pages_var = tk.IntVar(value=config.get('MAX_NUM_PAGES', 0))
        self.max_pages_spin = ttk.Spinbox(self.frame, from_=0, to=10000, textvariable=self.max_pages_var, width=10)
        self.max_pages_spin.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        self.limits_max_pages_hint = ttk.Label(self.frame, text=I18n.get('limits_max_pages_hint'))
        self.limits_max_pages_hint.grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1

        # Continue on error
        self.continue_error_var = tk.BooleanVar(value=config.get('CONTINUE_ON_ERROR', True))
        self.continue_error_cb = ttk.Checkbutton(
            self.frame,
            text=I18n.get('limits_continue_error'),
            variable=self.continue_error_var
        )
        self.continue_error_cb.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1

        # Подсказка внизу вкладки
        ttk.Separator(self.frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 6))
        row += 1
        self.hint_label = ttk.Label(self.frame, text=I18n.get('hint_limits'), wraplength=700, justify=tk.LEFT)
        self.hint_label.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.N), pady=(0, 5))
        self.frame.rowconfigure(row, weight=1)

    def update_texts(self):
        """Update text labels"""
        self.limits_max_size_label.config(text=I18n.get('limits_max_size_label'))
        self.limits_max_size_hint.config(text=I18n.get('limits_max_size_hint'))
        self.limits_max_pages_label.config(text=I18n.get('limits_max_pages_label'))
        self.limits_max_pages_hint.config(text=I18n.get('limits_max_pages_hint'))
        self.continue_error_cb.config(text=I18n.get('limits_continue_error'))
        if hasattr(self, 'hint_label'):
            self.hint_label.config(text=I18n.get('hint_limits'))

    def get_values(self) -> Dict[str, Any]:
        """Get values from all fields"""
        return {
            'MAX_FILE_SIZE': self.max_size_var.get() * 1024 * 1024,  # Convert MB to bytes
            'MAX_NUM_PAGES': self.max_pages_var.get(),
            'CONTINUE_ON_ERROR': self.continue_error_var.get()
        }


class AboutTab:
    """About/Donation tab"""

    def __init__(self, parent: ttk.Notebook):
        self.frame = ttk.Frame(parent, padding="10")
        self.site_url = "https://ipnikpv40.ru/"
        self.email = "Console3@yandex.ru"
        self.wallet_address = "TJuFvcnLcYrnTJcesFTQQFwYvPXsvz61Mb"

        self.icon_image = self._load_image(os.path.join("images", "icon.png"), max_width=320)
        self.icon_label = ttk.Label(self.frame, image=self.icon_image)
        self.icon_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        self.title_label = ttk.Label(
            self.frame,
            text=I18n.get('about_title'),
            font=('TkDefaultFont', 10, 'bold')
        )
        self.title_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))

        self.info_label = ttk.Label(
            self.frame,
            text=I18n.get('about_info'),
            wraplength=700,
            justify=tk.LEFT
        )
        self.info_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 6))

        self.site_label = ttk.Label(self.frame, text=I18n.get('about_site_label'))
        self.site_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 6))

        self.site_link = tk.Label(
            self.frame,
            text=self.site_url,
            fg='blue',
            cursor='hand2'
        )
        self.site_link.bind('<Button-1>', lambda _: webbrowser.open(self.site_url))
        self.site_link.grid(row=3, column=1, sticky=tk.W, pady=(0, 6))

        self.email_label = ttk.Label(self.frame, text=I18n.get('about_email_label'))
        self.email_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 6))

        self.email_value = ttk.Label(self.frame, text=self.email)
        self.email_value.grid(row=4, column=1, sticky=tk.W, pady=(0, 6))

        self.donation_title = ttk.Label(
            self.frame,
            text=I18n.get('about_donation_title'),
            font=('TkDefaultFont', 9, 'bold')
        )
        self.donation_title.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(10, 4))

        self.donation_phrase = ttk.Label(
            self.frame,
            text=I18n.get('about_donation_phrase'),
            wraplength=700,
            justify=tk.LEFT
        )
        self.donation_phrase.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))

        self.wallet_label = ttk.Label(self.frame, text=I18n.get('about_wallet_label'))
        self.wallet_label.grid(row=7, column=0, sticky=tk.W, pady=(0, 4))

        self.wallet_value = ttk.Label(self.frame, text=self.wallet_address)
        self.wallet_value.grid(row=7, column=1, sticky=tk.W, pady=(0, 4))

        self.wallet_button = ttk.Button(
            self.frame,
            text=I18n.get('about_wallet_copy'),
            command=self._copy_wallet
        )
        self.wallet_button.grid(row=8, column=1, sticky=tk.W, pady=(0, 10))

        self.wallet_status = ttk.Label(self.frame, text="", foreground='green')
        self.wallet_status.grid(row=8, column=0, sticky=tk.W, pady=(0, 10))

        self.crypto_label = ttk.Label(self.frame, text=I18n.get('about_qr_crypto'))
        self.crypto_label.grid(row=9, column=0, sticky=tk.W)

        self.rub_label = ttk.Label(self.frame, text=I18n.get('about_qr_rub'))
        self.rub_label.grid(row=9, column=1, sticky=tk.W)

        self.crypto_image = self._load_image(os.path.join("images", "Донат В Крипте.png"))
        self.rub_image = self._load_image(os.path.join("images", "Донат рубли.PNG"))

        self.crypto_image_label = ttk.Label(self.frame, image=self.crypto_image)
        self.crypto_image_label.grid(row=10, column=0, sticky=tk.W, padx=(0, 10), pady=(4, 0))

        self.rub_image_label = ttk.Label(self.frame, image=self.rub_image)
        self.rub_image_label.grid(row=10, column=1, sticky=tk.W, pady=(4, 0))

        # Лицензии / сторонние компоненты
        self.license_title = ttk.Label(self.frame, text=I18n.get('about_license_title'), font=('TkDefaultFont', 9, 'bold'))
        self.license_title.grid(row=11, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))
        self.license_label = ttk.Label(self.frame, text=I18n.get('about_license_docling'), wraplength=700, justify=tk.LEFT)
        self.license_label.grid(row=12, column=0, columnspan=2, sticky=tk.W, pady=(0, 6))

        # Подсказка внизу вкладки
        ttk.Separator(self.frame, orient='horizontal').grid(row=13, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 6))
        self.hint_label = ttk.Label(self.frame, text=I18n.get('hint_about'), wraplength=700, justify=tk.LEFT)
        self.hint_label.grid(row=14, column=0, columnspan=2, sticky=(tk.W, tk.N), pady=(0, 5))
        self.frame.rowconfigure(14, weight=1)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def update_texts(self):
        self.title_label.config(text=I18n.get('about_title'))
        self.info_label.config(text=I18n.get('about_info'))
        self.site_label.config(text=I18n.get('about_site_label'))
        self.email_label.config(text=I18n.get('about_email_label'))
        self.donation_title.config(text=I18n.get('about_donation_title'))
        self.donation_phrase.config(text=I18n.get('about_donation_phrase'))
        self.wallet_label.config(text=I18n.get('about_wallet_label'))
        self.wallet_button.config(text=I18n.get('about_wallet_copy'))
        self.crypto_label.config(text=I18n.get('about_qr_crypto'))
        self.rub_label.config(text=I18n.get('about_qr_rub'))
        self.license_title.config(text=I18n.get('about_license_title'))
        self.license_label.config(text=I18n.get('about_license_docling'))
        if hasattr(self, 'hint_label'):
            self.hint_label.config(text=I18n.get('hint_about'))

    def _copy_wallet(self):
        self.frame.clipboard_clear()
        self.frame.clipboard_append(self.wallet_address)
        self.wallet_status.config(text=I18n.get('about_wallet_copied'))
        self.frame.after(2000, lambda: self.wallet_status.config(text=""))

    def _load_image(self, relative_path: str, max_width: int = 260) -> tk.PhotoImage:
        image_path = self._resource_path(relative_path)
        image = tk.PhotoImage(file=image_path)
        if image.width() > max_width:
            factor = max(1, int(image.width() / max_width))
            image = image.subsample(factor, factor)
        return image

    @staticmethod
    def _resource_path(relative_path: str) -> str:
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, relative_path)


class ControlPanel:
    """Control buttons panel"""

    def __init__(self, parent: ttk.Frame, controller: Any):
        self.controller = controller
        self.frame = ttk.Frame(parent, padding="5")

        # Start button
        self.start_btn = ttk.Button(
            self.frame,
            text=I18n.get('control_start'),
            command=controller.start_conversion
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        # Stop button
        self.stop_btn = ttk.Button(
            self.frame,
            text=I18n.get('control_stop'),
            command=controller.stop_conversion,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Clear log button
        self.clear_btn = ttk.Button(
            self.frame,
            text=I18n.get('control_clear_log'),
            command=controller.clear_log
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Save settings button
        self.save_btn = ttk.Button(
            self.frame,
            text=I18n.get('control_save_settings'),
            command=controller.save_settings
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

    def update_texts(self):
        """Update button labels"""
        self.start_btn.config(text=I18n.get('control_start'))
        self.stop_btn.config(text=I18n.get('control_stop'))
        self.clear_btn.config(text=I18n.get('control_clear_log'))
        self.save_btn.config(text=I18n.get('control_save_settings'))

    def set_running_state(self, is_running: bool):
        """Update button states based on running status"""
        if is_running:
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.DISABLED)
        else:
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.save_btn.config(state=tk.NORMAL)


class ProgressPanel:
    """Progress display panel"""

    def __init__(self, parent: ttk.Frame):
        self.frame = ttk.LabelFrame(parent, text=I18n.get('progress_current'), padding="10")
        self._last_progress = None

        # Current file label
        self.current_file_var = tk.StringVar(value=I18n.get('progress_idle'))
        self.current_file_label = ttk.Label(self.frame, textvariable=self.current_file_var)
        self.current_file_label.pack(fill=tk.X, pady=(0, 5))

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self.frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        # Activity label (honest status during long files)
        self.activity_var = tk.StringVar(value="")
        self.activity_label = ttk.Label(self.frame, textvariable=self.activity_var, foreground='gray')
        self.activity_label.pack(fill=tk.X, pady=(0, 5))

        # Time labels
        time_frame = ttk.Frame(self.frame)
        time_frame.pack(fill=tk.X)

        self.elapsed_var = tk.StringVar(value=f"{I18n.get('progress_elapsed')} 00:00:00")
        ttk.Label(time_frame, textvariable=self.elapsed_var).pack(side=tk.LEFT, padx=(0, 20))

        self.eta_var = tk.StringVar(value=f"{I18n.get('progress_remaining')} {I18n.get('progress_calculating')}")
        ttk.Label(time_frame, textvariable=self.eta_var).pack(side=tk.LEFT)

    def update_texts(self):
        """Update text labels"""
        self.frame.config(text=I18n.get('progress_current'))
        # Keep time/eta values, refresh translated prefixes
        ev = self.elapsed_var.get()
        ep = ev.split(" ", 1)
        self.elapsed_var.set(f"{I18n.get('progress_elapsed')} {ep[1] if len(ep) > 1 else '00:00:00'}")
        et = self.eta_var.get()
        tp = et.split(" ", 1)
        self.eta_var.set(f"{I18n.get('progress_remaining')} {tp[1] if len(tp) > 1 else I18n.get('progress_calculating')}")
        if self._last_progress is not None:
            self.update_progress(self._last_progress)

    def update_progress(self, message: Dict[str, Any]):
        """Update progress display"""
        self._last_progress = message
        current = message.get('current', 0)
        total = message.get('total', 0)
        filename = message.get('filename', '')
        percentage = message.get('percentage')
        elapsed = message.get('elapsed', '00:00:00')
        eta = message.get('eta', I18n.get('progress_calculating'))

        if filename:
            self.current_file_var.set(f"{I18n.get('progress_current')} {filename} ({current}/{total})")
        else:
            self.current_file_var.set(I18n.get('progress_idle'))

        is_processing = bool(filename) and (percentage is None or percentage < 100)
        if is_processing:
            self.activity_var.set(I18n.get('status_processing'))
        else:
            self.activity_var.set("")

        if percentage is not None:
            self.progress_var.set(percentage)
        self.elapsed_var.set(f"{I18n.get('progress_elapsed')} {elapsed}")
        self.eta_var.set(f"{I18n.get('progress_remaining')} {eta}")

    def reset(self):
        """Reset progress display"""
        self._last_progress = None
        self.current_file_var.set(I18n.get('progress_idle'))
        self.progress_var.set(0)
        self.elapsed_var.set(f"{I18n.get('progress_elapsed')} 00:00:00")
        self.eta_var.set(f"{I18n.get('progress_remaining')} {I18n.get('progress_calculating')}")


class StatsPanel:
    """Statistics display panel"""

    def __init__(self, parent: ttk.Frame):
        self.frame = ttk.Frame(parent, padding="5")
        self._last_stats = {}

        # Statistics labels
        self.success_var = tk.StringVar(value=f"✓ {I18n.get('stats_success')} 0")
        ttk.Label(self.frame, textvariable=self.success_var, foreground='green').pack(side=tk.LEFT, padx=10)

        self.partial_var = tk.StringVar(value=f"⚠ {I18n.get('stats_partial')} 0")
        ttk.Label(self.frame, textvariable=self.partial_var, foreground='orange').pack(side=tk.LEFT, padx=10)

        self.failed_var = tk.StringVar(value=f"✗ {I18n.get('stats_failed')} 0")
        ttk.Label(self.frame, textvariable=self.failed_var, foreground='red').pack(side=tk.LEFT, padx=10)

        self.skipped_var = tk.StringVar(value=f"⊝ {I18n.get('stats_skipped')} 0")
        ttk.Label(self.frame, textvariable=self.skipped_var).pack(side=tk.LEFT, padx=10)

    def update_texts(self):
        """Update text labels"""
        if self._last_stats:
            self.update_stats({'stats': self._last_stats})

    def update_stats(self, message: Dict[str, Any]):
        """Update statistics display"""
        stats = message.get('stats', {})
        self._last_stats = stats
        self.success_var.set(f"✓ {I18n.get('stats_success')} {stats.get('success', 0)}")
        self.partial_var.set(f"⚠ {I18n.get('stats_partial')} {stats.get('partial', 0)}")
        self.failed_var.set(f"✗ {I18n.get('stats_failed')} {stats.get('failed', 0)}")
        self.skipped_var.set(f"⊝ {I18n.get('stats_skipped')} {stats.get('skipped', 0)}")

    def reset(self):
        """Reset statistics display"""
        self.success_var.set(f"✓ {I18n.get('stats_success')} 0")
        self.partial_var.set(f"⚠ {I18n.get('stats_partial')} 0")
        self.failed_var.set(f"✗ {I18n.get('stats_failed')} 0")
        self.skipped_var.set(f"⊝ {I18n.get('stats_skipped')} 0")


class LogPanel:
    """Log display panel"""

    def __init__(self, parent: ttk.Frame):
        self.frame = ttk.LabelFrame(parent, text=I18n.get('log_title'), padding="10")

        # Scrolled text widget
        self.log_text = scrolledtext.ScrolledText(
            self.frame,
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Consolas', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Configure tags for color coding
        self.log_text.tag_config('INFO', foreground='black')
        self.log_text.tag_config('WARNING', foreground='orange')
        self.log_text.tag_config('ERROR', foreground='red')
        self.log_text.tag_config('DEBUG', foreground='gray')

    def update_texts(self):
        """Update text labels"""
        self.frame.config(text=I18n.get('log_title'))

    def append_log(self, emoji: str, message: str, level: str):
        """Append log message"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{emoji} {message}\n", level)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def clear(self):
        """Clear log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
