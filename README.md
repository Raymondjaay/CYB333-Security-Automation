# Automated Password Strength Checker

A lightweight, terminal-based Python utility designed to evaluate user-submitted passwords in real-time. The script checks structural complexity and cross-references inputs against a blocklist of commonly used credentials to enforce strong password hygiene.

## Features
* **Length Validation:** Verifies structural stability.
* **Character Diversity Analysis:** Checks for uppercase, lowercase, numbers, and special characters.
* **Dictionary Blocklist Filtering:** Rejects common weak entries (e.g., "123456", "qwerty").
* **Granular User Feedback:** Outlines exactly what structural components are missing.

## Prerequisites & Installation
* **Python 3.x** must be installed on your operating system.
* No external dependencies or pip installations are required.

## How to Run the Script
1. Clone this repository or download `hello.py`.
2. Open your terminal window and navigate to the project directory.
3. Execute the script using the following command:
   ```bash
   python3 hello.py