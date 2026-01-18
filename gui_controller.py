#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI Controller for Dockling Document Converter
Handles business logic, threading, and coordination between GUI and conversion
"""

import tkinter as tk
from tkinter import messagebox
import threading
import queue
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

from config_manager import ConfigManager
from logger_adapter import LogCapture
from i18n import I18n


class ConversionController:
    """Controller for managing document conversion process"""

    def __init__(self, root: tk.Tk, initial_config: Dict[str, Any]):
        """
        Initialize conversion controller

        Args:
            root: Tk root window
            initial_config: Initial configuration dictionary
        """
        self.root = root
        self.config = initial_config

        # Threading components
        self.worker_thread: Optional[threading.Thread] = None
        self.message_queue = queue.Queue()
        self.is_running = False
        self.stop_requested = False

        # UI components (will be set by MainWindow)
        self.config_panel = None
        self.control_panel = None
        self.progress_panel = None
        self.stats_panel = None
        self.log_panel = None

        # Logging setup
        self.log_capture = LogCapture()
        self.log_capture.setup_gui_logging(self._on_log_message)

    def set_ui_components(self, config_panel, control_panel, progress_panel, stats_panel, log_panel):
        """
        Set references to UI components

        Args:
            config_panel: Configuration panel instance
            control_panel: Control panel instance
            progress_panel: Progress panel instance
            stats_panel: Statistics panel instance
            log_panel: Log panel instance
        """
        self.config_panel = config_panel
        self.control_panel = control_panel
        self.progress_panel = progress_panel
        self.stats_panel = stats_panel
        self.log_panel = log_panel

    def start_conversion(self):
        """Start document conversion process"""
        if self.is_running:
            messagebox.showwarning(
                I18n.get('msg_conversion_started'),
                I18n.get('msg_conversion_in_progress')
            )
            return

        # Get current configuration
        self.config = self.config_panel.get_config()

        # Normalize OCR languages to list for conversion pipeline
        ocr_langs = self.config.get("OCR_LANGUAGES")
        if isinstance(ocr_langs, str):
            parsed_langs = [lang.strip() for lang in ocr_langs.split(",") if lang.strip()]
            self.config["OCR_LANGUAGES"] = parsed_langs if parsed_langs else ["eng"]

        # Validate configuration
        errors = ConfigManager.validate_config(self.config)
        if errors:
            error_msg = I18n.get('msg_validation_error') + ":\n" + "\n".join(f"- {err}" for err in errors)
            messagebox.showerror(I18n.get('msg_validation_error'), error_msg)
            return

        # Get files to process
        processing_mode = self.config.get('processing_mode', 'folder')
        if processing_mode == 'folder':
            input_dir = Path(self.config.get('INPUT_DIR', 'input'))
            if not input_dir.exists():
                messagebox.showerror(
                    I18n.get('msg_validation_error'),
                    I18n.get('msg_input_dir_not_exist', path=str(input_dir))
                )
                return

            # Scan for files
            files = self._scan_directory(input_dir)
            if not files:
                messagebox.showwarning(
                    I18n.get('msg_no_files'),
                    I18n.get('msg_no_files_in_dir', path=str(input_dir))
                )
                return
        else:
            # Use selected files
            files = self.config.get('selected_files', [])
            if not files:
                messagebox.showwarning(
                    I18n.get('msg_no_files'),
                    I18n.get('msg_select_files_please')
                )
                return
            files = [Path(f) for f in files]

        # Reset UI
        self.progress_panel.reset()
        self.stats_panel.reset()

        # Update state
        self.is_running = True
        self.stop_requested = False
        self.control_panel.set_running_state(True)

        # Log start
        self.log_panel.append_log('ℹ', I18n.get('msg_starting_conversion', count=len(files)), 'INFO')

        # Start worker thread
        self.worker_thread = threading.Thread(
            target=self._conversion_worker,
            args=(files,),
            daemon=True
        )
        self.worker_thread.start()

        # Start queue checking
        self._check_queue()

    def stop_conversion(self):
        """Stop document conversion process"""
        if not self.is_running:
            return

        self.stop_requested = True
        self.log_panel.append_log('⚠', I18n.get('msg_stop_requested'), 'WARNING')

    def clear_log(self):
        """Clear log display"""
        if self.is_running:
            if not messagebox.askyesno(I18n.get('log_clear_confirm'), I18n.get('msg_clear_log_confirm')):
                return

        self.log_panel.clear()

    def save_settings(self):
        """Save current settings to .env file"""
        # Get current configuration from UI
        self.config = self.config_panel.get_config()

        # Validate before saving
        errors = ConfigManager.validate_config(self.config)
        if errors:
            error_msg = I18n.get('msg_validation_error') + ":\n" + "\n".join(f"- {err}" for err in errors)
            messagebox.showerror(I18n.get('msg_validation_error'), error_msg)
            return

        # Save to .env
        success, error = ConfigManager.save_config(self.config)
        if success:
            messagebox.showinfo(
                I18n.get('msg_settings_saved'),
                I18n.get('msg_settings_saved')
            )
            self.log_panel.append_log('✓', I18n.get('msg_settings_saved'), 'INFO')
        else:
            messagebox.showerror(
                I18n.get('msg_settings_error'),
                f"{I18n.get('msg_settings_error')}: {error}"
            )

    def _scan_directory(self, input_dir: Path) -> List[Path]:
        """
        Scan directory for supported document files

        Args:
            input_dir: Directory to scan

        Returns:
            List of file paths
        """
        supported_extensions = [
            '.pdf', '.docx', '.doc', '.pptx', '.ppt',
            '.xlsx', '.xls', '.html', '.htm', '.xml',
            '.md', '.asciidoc', '.adoc'
        ]

        files = []
        for ext in supported_extensions:
            files.extend(input_dir.rglob(f'*{ext}'))

        # Filter by size if limit is set
        max_size = self.config.get('MAX_FILE_SIZE', 0)
        if max_size > 0:
            files = [f for f in files if f.stat().st_size <= max_size]

        return sorted(files)

    def _conversion_worker(self, files: List[Path]):
        """
        Worker thread for document conversion

        Args:
            files: List of files to convert
        """
        try:
            # Import here to avoid GUI thread blocking
            from convert_to_markdown import (
                setup_document_converter,
                convert_documents,
                DocumentConversionStats
            )
            from config import Config

            # Update config module with current settings
            for key, value in self.config.items():
                if hasattr(Config, key):
                    setattr(Config, key, value)

            # Setup output directory
            output_dir = Path(self.config.get('OUTPUT_DIR', 'output'))
            output_dir.mkdir(parents=True, exist_ok=True)

            # Setup converter
            self.message_queue.put({
                'type': 'log',
                'emoji': 'ℹ',
                'message': 'Setting up document converter...',
                'level': 'INFO'
            })

            converter = setup_document_converter(Config)

            # Create stats tracker
            stats = DocumentConversionStats()

            # Convert documents with progress callback
            convert_documents(
                files=files,
                converter=converter,
                output_dir=output_dir,
                config=Config,
                stats=stats,
                progress_callback=self._progress_callback,
                stop_check=lambda: self.stop_requested
            )

            # Send completion message
            self.message_queue.put({
                'type': 'complete',
                'stats': {
                    'success': stats.successful,
                    'partial': stats.partial_success,
                    'failed': stats.failed,
                    'skipped': stats.skipped
                }
            })

        except Exception as e:
            logging.exception("Error in conversion worker")
            self.message_queue.put({
                'type': 'error',
                'message': str(e)
            })

    def _progress_callback(self, message: Dict[str, Any]):
        """
        Callback for progress updates from conversion

        Args:
            message: Progress message dictionary
        """
        self.message_queue.put(message)

    def _on_log_message(self, emoji: str, message: str, level: str):
        """
        Callback for log messages

        Args:
            emoji: Emoji indicator
            message: Log message
            level: Log level
        """
        self.message_queue.put({
            'type': 'log',
            'emoji': emoji,
            'message': message,
            'level': level
        })

    def _check_queue(self):
        """Check message queue and update UI"""
        try:
            while True:
                try:
                    message = self.message_queue.get_nowait()
                    self._handle_message(message)
                except queue.Empty:
                    break
        except Exception as e:
            logging.exception("Error handling queue message")

        # Schedule next check if still running
        if self.is_running:
            self.root.after(100, self._check_queue)

    def _handle_message(self, message: Dict[str, Any]):
        """
        Handle message from worker thread

        Args:
            message: Message dictionary
        """
        msg_type = message.get('type')

        if msg_type == 'progress':
            self.progress_panel.update_progress(message)

        elif msg_type == 'stats':
            self.stats_panel.update_stats(message)

        elif msg_type == 'log':
            emoji = message.get('emoji', 'ℹ')
            text = message.get('message', '')
            level = message.get('level', 'INFO')
            self.log_panel.append_log(emoji, text, level)

        elif msg_type == 'complete':
            self._on_conversion_complete(message)

        elif msg_type == 'error':
            self._on_conversion_error(message)

    def _on_conversion_complete(self, message: Dict[str, Any]):
        """
        Handle conversion completion

        Args:
            message: Completion message
        """
        self.is_running = False
        self.control_panel.set_running_state(False)

        stats = message.get('stats', {})
        total = sum(stats.values())

        self.log_panel.append_log(
            '✓',
            I18n.get('msg_conversion_completed_log',
                     total=total,
                     success=stats.get('success', 0),
                     partial=stats.get('partial', 0),
                     failed=stats.get('failed', 0),
                     skipped=stats.get('skipped', 0)),
            'INFO'
        )

        messagebox.showinfo(
            I18n.get('msg_conversion_completed'),
            I18n.get('msg_conversion_completed_body',
                     success=stats.get('success', 0),
                     partial=stats.get('partial', 0),
                     failed=stats.get('failed', 0),
                     skipped=stats.get('skipped', 0))
        )

    def _on_conversion_error(self, message: Dict[str, Any]):
        """
        Handle conversion error

        Args:
            message: Error message
        """
        self.is_running = False
        self.control_panel.set_running_state(False)

        error = message.get('message', 'Unknown error')
        self.log_panel.append_log('✗', f"Conversion error: {error}", 'ERROR')

        messagebox.showerror(
            I18n.get('msg_conversion_error'),
            I18n.get('msg_conversion_error_body', error=error)
        )
