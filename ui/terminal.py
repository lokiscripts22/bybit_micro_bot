"""
terminal.py

A GUI terminal/log panel for the Spot Bot using Tkinter.

Features:
- Scrollable log area with color-coded messages
- Filters for INFO, TRADE, ERROR, and REASON logs
- Thread-safe logging
- Redirects stdout and stderr to the terminal
"""

import tkinter as tk
from tkinter import scrolledtext
import sys
import threading


class Terminal:
    def __init__(self, master):
        """
        Initialize the terminal GUI panel.

        Args:
            master: Parent Tkinter frame
        """
        self.frame = tk.Frame(master, bg="#1E1E1E", bd=2, relief=tk.RIDGE)
        self.frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollable text area
        self.text_area = scrolledtext.ScrolledText(
            self.frame, bg="#121212", fg="white",
            insertbackground="white", height=10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.tag_config("INFO", foreground="cyan")
        self.text_area.tag_config("TRADE", foreground="lime")
        self.text_area.tag_config("ERROR", foreground="red")
        self.text_area.tag_config("REASON", foreground="yellow")

        # Filter controls
        filter_frame = tk.Frame(self.frame, bg="#1E1E1E")
        filter_frame.pack(fill=tk.X)

        tk.Label(filter_frame, text="Show Logs:", bg="#1E1E1E", fg="white").pack(side=tk.LEFT, padx=5)

        self.show_info = tk.BooleanVar(value=True)
        self.show_trade = tk.BooleanVar(value=True)
        self.show_error = tk.BooleanVar(value=True)
        self.show_reason = tk.BooleanVar(value=True)

        tk.Checkbutton(filter_frame, text="INFO", bg="#1E1E1E", fg="cyan", variable=self.show_info,
                       command=self.refresh).pack(side=tk.LEFT)
        tk.Checkbutton(filter_frame, text="TRADE", bg="#1E1E1E", fg="lime", variable=self.show_trade,
                       command=self.refresh).pack(side=tk.LEFT)
        tk.Checkbutton(filter_frame, text="ERROR", bg="#1E1E1E", fg="red", variable=self.show_error,
                       command=self.refresh).pack(side=tk.LEFT)
        tk.Checkbutton(filter_frame, text="REASON", bg="#1E1E1E", fg="yellow", variable=self.show_reason,
                       command=self.refresh).pack(side=tk.LEFT)

        # Internal log storage
        self.logs = []  # list of tuples: (type, message)
        self.lock = threading.Lock()

        # Redirect stdout & stderr
        sys.stdout = self
        sys.stderr = self

    # ── Logging interface ──
    def write(self, message):
        """Write message to terminal, determining type by prefix."""
        if message.strip() == "":
            return

        if message.startswith("[ERROR]"):
            log_type = "ERROR"
            msg = message[len("[ERROR] "):]
        elif message.startswith("[TRADE]"):
            log_type = "TRADE"
            msg = message[len("[TRADE] "):]
        elif message.startswith("[REASON]"):
            log_type = "REASON"
            msg = message[len("[REASON] "):]
        else:
            log_type = "INFO"
            msg = message

        with self.lock:
            self.logs.append((log_type, msg))
            self.display(log_type, msg)

    def flush(self):
        """Needed for stdout/stderr redirect."""
        pass

    # ── Display message in text area ──
    def display(self, log_type, msg):
        """Display a message in the terminal if its filter is active."""
        show = {
            "INFO": self.show_info.get(),
            "TRADE": self.show_trade.get(),
            "ERROR": self.show_error.get(),
            "REASON": self.show_reason.get()
        }.get(log_type, True)

        if show:
            self.text_area.configure(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"[{log_type}] {msg}\n", log_type)
            self.text_area.see(tk.END)
            self.text_area.configure(state=tk.DISABLED)

    # ── Refresh display based on filters ──
    def refresh(self):
        """Refresh displayed logs based on filter settings."""
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        with self.lock:
            for log_type, msg in self.logs:
                self.display(log_type, msg)
        self.text_area.configure(state=tk.DISABLED)

    # ── Add log manually (optional) ──
    def log(self, msg, log_type="INFO"):
        """Manually log a message."""
        with self.lock:
            self.logs.append((log_type, msg))
            self.display(log_type, msg)
