#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logger Adapter for Dockling GUI
Captures logging output and forwards it to GUI with emoji indicators
"""

import logging
import sys
from typing import Callable, Optional
from datetime import datetime


class GuiLogHandler(logging.Handler):
    """Custom logging handler that sends log records to GUI"""

    def __init__(self, callback: Callable[[str, str, str], None]):
        """
        Initialize GUI log handler

        Args:
            callback: Function to call with (emoji, message, level)
        """
        super().__init__()
        self.callback = callback
        self.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        ))

    def emit(self, record: logging.LogRecord):
        """
        Emit a log record to the GUI

        Args:
            record: Log record to emit
        """
        try:
            msg = self.format(record)
            emoji = self._get_emoji(msg, record.levelname)
            self.callback(emoji, msg, record.levelname)
        except Exception:
            self.handleError(record)

    def _get_emoji(self, message: str, level: str) -> str:
        """
        Determine appropriate emoji for the message

        Args:
            message: Log message
            level: Log level name

        Returns:
            Emoji string
        """
        # Check message content first (more specific)
        msg_lower = message.lower()

        if '✓' in message or 'успешно' in msg_lower or 'success' in msg_lower or 'completed' in msg_lower:
            return '✓'
        elif '⚠' in message or 'частично' in msg_lower or 'partial' in msg_lower or 'warning' in msg_lower:
            return '⚠'
        elif '✗' in message or 'ошибка' in msg_lower or 'error' in msg_lower or 'failed' in msg_lower:
            return '✗'
        elif '⊝' in message or 'пропущен' in msg_lower or 'skipped' in msg_lower:
            return '⊝'

        # Fall back to log level
        if level == 'ERROR' or level == 'CRITICAL':
            return '✗'
        elif level == 'WARNING':
            return '⚠'
        elif level == 'INFO':
            return 'ℹ'
        elif level == 'DEBUG':
            return '🔍'
        else:
            return 'ℹ'


class LogCapture:
    """Manages log capture and formatting for GUI display"""

    def __init__(self):
        self.gui_handler: Optional[GuiLogHandler] = None
        self.original_handlers = {}

    def setup_gui_logging(self, log_callback: Callable[[str, str, str], None],
                         logger_name: Optional[str] = None):
        """
        Set up GUI logging by adding a custom handler

        Args:
            log_callback: Function to call with log messages (emoji, message, level)
            logger_name: Name of logger to capture (None for root logger)
        """
        # Create GUI handler
        self.gui_handler = GuiLogHandler(log_callback)
        self.gui_handler.setLevel(logging.DEBUG)

        # Get the target logger
        if logger_name:
            logger = logging.getLogger(logger_name)
        else:
            logger = logging.getLogger()

        # Store original handlers
        self.original_handlers[logger_name] = logger.handlers.copy()

        # Add GUI handler
        logger.addHandler(self.gui_handler)

    def teardown_gui_logging(self, logger_name: Optional[str] = None):
        """
        Remove GUI handler and restore original handlers

        Args:
            logger_name: Name of logger (None for root logger)
        """
        if not self.gui_handler:
            return

        # Get the target logger
        if logger_name:
            logger = logging.getLogger(logger_name)
        else:
            logger = logging.getLogger()

        # Remove GUI handler
        if self.gui_handler in logger.handlers:
            logger.removeHandler(self.gui_handler)

        self.gui_handler = None

    @staticmethod
    def format_time_elapsed(seconds: float) -> str:
        """
        Format elapsed time in HH:MM:SS format

        Args:
            seconds: Number of seconds

        Returns:
            Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    @staticmethod
    def format_file_size(bytes_size: int) -> str:
        """
        Format file size in human-readable format

        Args:
            bytes_size: Size in bytes

        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"

    @staticmethod
    def create_log_message(emoji: str, message: str, include_time: bool = True) -> str:
        """
        Create a formatted log message with emoji

        Args:
            emoji: Emoji to prepend
            message: Log message
            include_time: Whether to include timestamp

        Returns:
            Formatted log message
        """
        if include_time:
            timestamp = datetime.now().strftime('%H:%M:%S')
            return f"{emoji} {timestamp} - {message}"
        else:
            return f"{emoji} {message}"


class StdoutRedirector:
    """Redirects stdout/stderr to logging"""

    def __init__(self, logger: logging.Logger, level: int = logging.INFO):
        """
        Initialize stdout redirector

        Args:
            logger: Logger to send output to
            level: Log level to use
        """
        self.logger = logger
        self.level = level
        self.buffer = ''

    def write(self, message: str):
        """
        Write message to logger

        Args:
            message: Message to write
        """
        # Buffer messages until newline
        self.buffer += message
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            for line in lines[:-1]:
                if line.strip():  # Skip empty lines
                    self.logger.log(self.level, line.strip())
            self.buffer = lines[-1]

    def flush(self):
        """Flush remaining buffer"""
        if self.buffer.strip():
            self.logger.log(self.level, self.buffer.strip())
            self.buffer = ''


def setup_stdout_redirect(logger: Optional[logging.Logger] = None):
    """
    Redirect stdout and stderr to logging

    Args:
        logger: Logger to use (None for root logger)
    """
    if logger is None:
        logger = logging.getLogger()

    sys.stdout = StdoutRedirector(logger, logging.INFO)
    sys.stderr = StdoutRedirector(logger, logging.ERROR)


def restore_stdout():
    """Restore original stdout and stderr"""
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


if __name__ == '__main__':
    # Test logger adapter
    print("Testing LogCapture...")

    # Create a test callback
    captured_logs = []

    def test_callback(emoji, message, level):
        captured_logs.append((emoji, message, level))
        print(f"Captured: {emoji} [{level}] {message}")

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Create log capture
    capture = LogCapture()
    capture.setup_gui_logging(test_callback, __name__)

    # Test various log levels and messages
    print("\nTesting log messages:")
    logger.info("✓ Успешно сохранено: document.pdf")
    logger.warning("⚠ Частично успешно: file.docx - некоторые таблицы пропущены")
    logger.error("✗ Ошибка конвертации: invalid_file.pdf")
    logger.info("⊝ Пропущен файл: too_large.pdf (превышен размер)")
    logger.info("ℹ Начинается обработка файлов...")
    logger.debug("🔍 Debug информация")

    # Test time formatting
    print("\nTesting time formatting:")
    print(f"3665 seconds = {LogCapture.format_time_elapsed(3665)}")
    print(f"150 seconds = {LogCapture.format_time_elapsed(150)}")

    # Test file size formatting
    print("\nTesting file size formatting:")
    print(f"1024 bytes = {LogCapture.format_file_size(1024)}")
    print(f"1048576 bytes = {LogCapture.format_file_size(1048576)}")
    print(f"52428800 bytes = {LogCapture.format_file_size(52428800)}")

    # Test log message creation
    print("\nTesting log message creation:")
    msg1 = LogCapture.create_log_message('✓', 'Document converted successfully')
    msg2 = LogCapture.create_log_message('⚠', 'Partial conversion', include_time=False)
    print(msg1)
    print(msg2)

    # Teardown
    capture.teardown_gui_logging(__name__)

    print(f"\nCaptured {len(captured_logs)} log messages")
    print("Test completed!")
