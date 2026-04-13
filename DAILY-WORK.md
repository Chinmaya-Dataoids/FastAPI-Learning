# FastAPI Learning Journal

### PLaylist like - https://www.youtube.com/playlist?list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI
## 📅 Day 1 - 2026-04-10

### Topics Covered
- **Setting up Git Repo and Syncing it to local folder**
  - Create a markdown file for documenting task and what learned 
  - Created a git repo first
  - Initialised git in local folder which created a master branch by default
  - Deleted master branch and configured main as *Upstream Tracking* for pull and push to work 

- **UV as package manager**
  - Installed UV as replacement for pip
  - Initalised uv in local folder using 'uv init' without this packages cant be install as it uses a 'pyproject.toml' file
  - Install packages using 'uv add <package_name>'
  - To run using uv we need 'uv run <command>' like 'uv run fastapi dev main.py'

- **Install FastAPI using uv**
  - run command 'uv add "fastapi[standard]"'
  - Include FastAPI framework , Uvicorn which is a ASGI server , FastAPI CLI command
  - FastAPI gives 2 mode dev for development server and run for production server
  - DEV mode - has auto reload which is helpful while developing , more helpful in debuging
  - /docs - route to SWAGGER UI and has automatic documentation based on our code
  - /redoc - routes to another SWAGGER UI that also provide documentation based on our code just in a different way
  - Using Jinja Templating we can render HTML content and can pass variable values that can be used in HTML file

## 📅 Day 2 - 2026-04-13
### Topics Covered
- **Path parameters**
  - in decorator we can define variable in url that can be accessed in python 
  - HTTPException is used to return HTTP error responses
  - status - gives constants for error. Make code for readable
  - we might work with return JSON response , make sure to include status_code parameter else it will show success
---

### 🛠️ What I Built / Practiced
- **<Task/Project Name>**
  - Description: (What you implemented)
  - Key Learnings: (Important insights or challenges)

---

### 💡 Key Concepts Learned
- **<Concept 1>**
  - Explanation: (Short explanation)
  
- **<Concept 2>**
  - Explanation:

---

### ❓ Doubts / Questions
- (Things you didn’t understand or want to revisit)

