Google Sheets To-Do List App (Python + CustomTkinter)
====================================================

Author: Khuzaima Amir
GitHub: https://github.com/xkhuzaima

Description:
------------
A Python-based To-Do List application with a sleek CustomTkinter UI 
that stores tasks in real-time using Google Sheets.

Features:
---------
- Add new tasks
- Mark tasks as done
- Delete tasks
- Persistent storage via Google Sheets API
- Dark/Light mode toggle

Setup Instructions:
-------------------
1. Create a Google Cloud project and enable the Google Sheets API.
2. Create a Google Sheet named "TodoTasks" with the columns:
       Task | Done
3. Download your Google service account credentials JSON file and 
   save it as `sheet_credentials.json` in the project root.
4. Install required Python packages:
       pip install gspread oauth2client customtkinter tkinter
5. Run the application:
       python todo_app.py

Controls:
---------
- Type a task in the entry field and click "Add Task" to create it.
- Select a task and click "Mark Done" to complete it.
- Select a task and click "Delete" to remove it.
- Use the Dark/Light button to switch UI themes.

Notes:
------
- Make sure your Google Sheet is shared with the service account email 
  found in your credentials file.
