@echo off

7z.exe a -t7z program.7z setup.bat
7z.exe a -t7z program.7z requirements.txt
7z.exe a -t7z program.7z main.py
7z.exe a -t7z program.7z configs.json
7z.exe a -t7z program.7z cogs_handler
7z.exe a -t7z program.7z core_cogs
7z.exe a -t7z program.7z "DO NOT OPEN ON CAM" -x!"DO NOT OPEN ON CAM/.env.account_details"
7z.exe a -t7z program.7z geckodriver-0.32.2
7z.exe a -t7z program.7z helper_functions
7z.exe a -t7z program.7z resources
7z.exe a -t7z program.7z .gitignore
7z.exe a -t7z program.7z geckodriver.exe
