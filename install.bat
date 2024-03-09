@echo off
REM Install dependencies
pip install discord.py
pip install openai

REM Run the Python script
python SLLM.py

REM Pause to keep the console window open (optional)
pause
