@REM run.bat

@echo off

cd /d %~dp0

.venv\Scripts\activate & python x-market.py & deactivate
