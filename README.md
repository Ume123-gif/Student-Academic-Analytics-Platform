# Student Academic Analytics Platform 📊

An enterprise-ready, full-stack student record management and performance analytics engine. This project refactors legacy structural data code into a robust, web-based application utilizing a modern Model-View-Controller (MVC) architecture.

## 🚀 Core Features
- **Full Ingestion Pipeline (CRUD):** Users can securely register new records, fetch current profiles, and modify performance marks on-the-fly via interactive forms.
- **Relational Integrity Schema:** Powered by SQLite3 with strict table-level constraints (`PRIMARY KEY`, `NOT NULL`, `CHECK BETWEEN 0 AND 100`) to guarantee absolute data consistency.
- **Real-Time Data Analytics:** Leverages optimized SQL aggregate pipelines (`AVG()`, `MAX()`, `MIN()`) to instantly compute subject-level trends and performance insights.
- **Dynamic Ranked Merit List:** Automatically tracks, computes, and updates a live scoreboard ordering students dynamically by their weighted aggregate percentages.
- **Secure Architecture:** Built using Flask parameterized SQL queries to protect the internal data pipelines against SQL injection attacks.

## 🛠️ Technical Stack
- **Backend Infrastructure:** Python 3, Flask Web Framework
- **Data Engine:** SQLite3, SQL Relational Query Language
- **Frontend Template UI:** HTML5, CSS3 Grid Layouts, Jinja2 Templating Engine
- **Version Control:** Git, GitHub

## 📂 Architecture Structure
```text
├── templates/
│   ├── dashboard.html        # Main analytics control center view
│   ├── add_student.html      # Transactional record ingestion form
│   └── update_student.html   # Dynamically pre-populated editing panel
├── app.py                    # Core Flask engine and SQL routing logic
├── STUDENT.db                # Local transactional SQLite database file
└── .gitignore                # Production pipeline exclusion map