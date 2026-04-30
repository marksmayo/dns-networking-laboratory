#!/usr/bin/env python3
"""
DNS Benchmark Laboratory - A modern, cross-platform DNS benchmarking application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import DNSBenchmarkApp

def main():
    app = DNSBenchmarkApp()
    app.run()

if __name__ == "__main__":
    main()