#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Progress Tracker for Dockling GUI
Tracks conversion progress, statistics, and estimates time remaining
"""

import time
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class ConversionStats:
    """Statistics for document conversion"""
    success: int = 0
    partial: int = 0
    failed: int = 0
    skipped: int = 0

    def total_processed(self) -> int:
        """Get total number of files processed"""
        return self.success + self.partial + self.failed + self.skipped

    def success_rate(self) -> float:
        """Calculate success rate (including partial successes)"""
        total = self.total_processed()
        if total == 0:
            return 0.0
        return (self.success + self.partial) / total * 100

    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary"""
        return {
            'success': self.success,
            'partial': self.partial,
            'failed': self.failed,
            'skipped': self.skipped
        }


class ProgressTracker:
    """Tracks progress of document conversion with ETA calculation"""

    def __init__(self, total_files: int):
        """
        Initialize progress tracker

        Args:
            total_files: Total number of files to process
        """
        self.total_files = total_files
        self.current_file_index = 0
        self.current_filename = ""
        self.start_time = time.time()
        self.stats = ConversionStats()
        self.file_start_times: Dict[int, float] = {}
        self.file_end_times: Dict[int, float] = {}

    def start_file(self, filename: str, index: int):
        """
        Mark the start of processing a file

        Args:
            filename: Name of the file being processed
            index: Index of the file (1-based)
        """
        self.current_file_index = index
        self.current_filename = filename
        self.file_start_times[index] = time.time()

    def end_file(self, index: int):
        """
        Mark the end of processing a file

        Args:
            index: Index of the file (1-based)
        """
        self.file_end_times[index] = time.time()

    def update_stats(self, status: str):
        """
        Update statistics based on conversion status

        Args:
            status: Status string ('success', 'partial', 'failed', 'skipped')
        """
        status_lower = status.lower()
        if status_lower == 'success':
            self.stats.success += 1
        elif status_lower in ('partial', 'partial_success'):
            self.stats.partial += 1
        elif status_lower in ('failed', 'failure', 'error'):
            self.stats.failed += 1
        elif status_lower == 'skipped':
            self.stats.skipped += 1

    def get_progress_percentage(self) -> int:
        """
        Calculate overall progress percentage

        Returns:
            Progress percentage (0-100)
        """
        if self.total_files == 0:
            return 0
        return int((self.stats.total_processed() / self.total_files) * 100)

    def get_current_file_percentage(self) -> int:
        """
        Calculate current file progress (placeholder for future enhancement)

        Returns:
            Current file progress percentage (0-100)
        """
        # File-level progress is unknown without page callbacks
        return None

    def get_elapsed_time(self) -> float:
        """
        Get total elapsed time since start

        Returns:
            Elapsed time in seconds
        """
        return time.time() - self.start_time

    def get_average_time_per_file(self) -> float:
        """
        Calculate average time per file

        Returns:
            Average time in seconds
        """
        completed = self.stats.total_processed()
        if completed == 0:
            return 0.0
        return self.get_elapsed_time() / completed

    def get_eta(self) -> Tuple[float, str]:
        """
        Estimate time remaining

        Returns:
            Tuple of (seconds_remaining, formatted_string)
        """
        processed = self.stats.total_processed()

        if processed == 0:
            return 0.0, "Расчет..."

        remaining_files = self.total_files - processed
        if remaining_files <= 0:
            return 0.0, "00:00:00"

        avg_time = self.get_average_time_per_file()
        eta_seconds = remaining_files * avg_time

        return eta_seconds, self._format_time(eta_seconds)

    def get_elapsed_formatted(self) -> str:
        """
        Get formatted elapsed time

        Returns:
            Formatted time string (HH:MM:SS)
        """
        return self._format_time(self.get_elapsed_time())

    def _format_time(self, seconds: float) -> str:
        """
        Format time in HH:MM:SS format

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def to_progress_message(self) -> Dict[str, any]:
        """
        Create a progress message dictionary for queue

        Returns:
            Dictionary with progress information
        """
        eta_seconds, eta_formatted = self.get_eta()

        return {
            'type': 'progress',
            'current': self.current_file_index,
            'total': self.total_files,
            'filename': self.current_filename,
            'percentage': self.get_progress_percentage(),
            'current_file_percentage': self.get_current_file_percentage(),
            'elapsed': self.get_elapsed_formatted(),
            'eta': eta_formatted,
            'eta_seconds': eta_seconds
        }

    def to_stats_message(self) -> Dict[str, any]:
        """
        Create a statistics message dictionary for queue

        Returns:
            Dictionary with statistics information
        """
        return {
            'type': 'stats',
            'stats': self.stats.to_dict(),
            'total_processed': self.stats.total_processed(),
            'success_rate': self.stats.success_rate()
        }

    def to_complete_message(self) -> Dict[str, any]:
        """
        Create a completion message dictionary

        Returns:
            Dictionary with completion information
        """
        return {
            'type': 'complete',
            'stats': self.stats.to_dict(),
            'total_processed': self.stats.total_processed(),
            'elapsed': self.get_elapsed_formatted(),
            'success_rate': self.stats.success_rate()
        }

    def reset(self):
        """Reset tracker for new conversion session"""
        self.current_file_index = 0
        self.current_filename = ""
        self.start_time = time.time()
        self.stats = ConversionStats()
        self.file_start_times.clear()
        self.file_end_times.clear()

    def is_complete(self) -> bool:
        """Check if all files have been processed"""
        return self.stats.total_processed() >= self.total_files

    def get_status_summary(self) -> str:
        """
        Get a human-readable status summary

        Returns:
            Status summary string
        """
        if self.stats.total_processed() == 0:
            return f"Обработка 0 из {self.total_files} файлов"

        return (f"Обработано {self.stats.total_processed()} из {self.total_files} | "
                f"Успешно: {self.stats.success} | Частично: {self.stats.partial} | "
                f"Ошибок: {self.stats.failed} | Пропущено: {self.stats.skipped}")


if __name__ == '__main__':
    # Test ProgressTracker
    print("Testing ProgressTracker...")

    # Create tracker for 10 files
    tracker = ProgressTracker(total_files=10)

    print(f"\nInitial state:")
    print(f"  Progress: {tracker.get_progress_percentage()}%")
    print(f"  Elapsed: {tracker.get_elapsed_formatted()}")
    print(f"  ETA: {tracker.get_eta()[1]}")
    print(f"  Status: {tracker.get_status_summary()}")

    # Simulate processing files
    print("\nSimulating file processing...")
    for i in range(1, 11):
        tracker.start_file(f"document{i}.pdf", i)
        print(f"\nProcessing file {i}/10: {tracker.current_filename}")

        # Simulate processing time
        time.sleep(0.1)

        # Randomly assign status
        if i <= 7:
            tracker.update_stats('success')
        elif i == 8:
            tracker.update_stats('partial')
        elif i == 9:
            tracker.update_stats('skipped')
        else:
            tracker.update_stats('failed')

        tracker.end_file(i)

        # Show progress
        progress_msg = tracker.to_progress_message()
        stats_msg = tracker.to_stats_message()

        print(f"  Progress: {progress_msg['percentage']}%")
        print(f"  Elapsed: {progress_msg['elapsed']}")
        print(f"  ETA: {progress_msg['eta']}")
        print(f"  Stats: ✓{stats_msg['stats']['success']} "
              f"⚠{stats_msg['stats']['partial']} "
              f"✗{stats_msg['stats']['failed']} "
              f"⊝{stats_msg['stats']['skipped']}")

    # Final summary
    print("\nConversion complete!")
    complete_msg = tracker.to_complete_message()
    print(f"  Total processed: {complete_msg['total_processed']}")
    print(f"  Success rate: {complete_msg['success_rate']:.1f}%")
    print(f"  Total time: {complete_msg['elapsed']}")
    print(f"  Final stats: {complete_msg['stats']}")

    print("\nTest completed!")
