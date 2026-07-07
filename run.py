#!/usr/bin/env python3
"""
run.py - Start the AI Timetable Scheduler application.
Run: python run.py
Then visit: http://localhost:5000
"""

import sys
import subprocess

def main():
    print("=" * 55)
    print("  AI Timetable Scheduler - MIC College of Technology")
    print("=" * 55)
    print()
    print("  Starting Flask server...")
    print("  URL  : http://localhost:5000")
    print("  Login: admin / admin123")
    print()
    print("  Press Ctrl+C to stop.")
    print("-" * 55)

    try:
        subprocess.run(
            [sys.executable, "app.py"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n  Server stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n  Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
