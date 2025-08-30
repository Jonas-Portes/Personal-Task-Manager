# Flask Task Manager

A simple and elegant task management application built with Flask, featuring a RESTful API and a modern responsive web interface.

## About This Project

This project was developed as part of the **"Python and Cursor: Smarter development with AI"** course offered by **Santander**. The course focuses on leveraging AI-powered development tools to enhance the coding experience and productivity.

### Course Details
- **Institution**: Santander
- **Course**: Python and Cursor: Smarter development with AI
- **Focus**: AI-assisted development with Cursor IDE
- **Technology**: Python, Flask, HTML/CSS/JavaScript

## Features

- ✅ Create, read, update, and delete tasks
- 📅 Deadline management with overdue highlighting
- 📊 Real-time task statistics and progress tracking
- 🎨 Modern, responsive UI with Bootstrap 5
- 🌙 Dark mode and light mode toggle
- 🔄 RESTful API for backend operations
- 📱 Mobile-friendly design
- ⚡ Fast and lightweight

## Technology Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons**: Font Awesome
- **Styling**: Custom CSS with hover effects and animations

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone https://github.com/Jonas-Portes/Personal-Task-Manager
   cd Personal-Task-Manager
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### Web Interface

- **Home Page**: View all tasks, add new tasks, and see statistics
- **Add Task**: Click the "Add Task" button to create a new task with optional deadline
- **Complete Task**: Click the checkmark icon to mark a task as complete
- **Delete Task**: Click the trash icon to delete a task
- **Deadline Management**: Set deadlines for tasks with visual overdue indicators
- **Theme Toggle**: Switch between light and dark modes using the moon/sun icon
- **About Page**: Learn more about the application and API endpoints

### API Endpoints

The application provides a RESTful API for programmatic access:

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/tasks` | Get all tasks | - |
| POST | `/api/tasks` | Create a new task | `{"title": "Task title", "description": "Optional description", "end_until": "YYYY-MM-DD"}` |
| PUT | `/api/tasks/{id}` | Update a task | `{"title": "New title", "description": "New description", "completed": true, "end_until": "YYYY-MM-DD"}` |
| DELETE | `/api/tasks/{id}` | Delete a task | - |

### Example API Usage

```bash
# Get all tasks
curl http://localhost:5000/api/tasks

# Create a new task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "description": "Study Flask framework", "end_until": "2025-09-15"}'

# Update a task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a task
curl -X DELETE http://localhost:5000/api/tasks/1
```

## Project Structure

```
Personal Task Manager/
├── main.py              # Main Flask application
├── tasks.json           # JSON file storing all tasks
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── templates/          # HTML templates
    ├── base.html       # Base template with navigation
    ├── index.html      # Home page with task list
    ├── add_task.html   # Add task form page
    ├── about.html      # About page
    ├── 404.html        # 404 error page
    └── 500.html        # 500 error page
```

## Configuration

The application uses the following configuration:

- **Debug Mode**: Enabled for development
- **Secret Key**: Set via environment variable `SECRET_KEY` or defaults to development key
- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: `5000`

To set a custom secret key:
```bash
export SECRET_KEY="your-secret-key-here"
```

## Development

### Adding New Features

1. **New Routes**: Add route handlers in `main.py`
2. **New Templates**: Create HTML files in the `templates/` directory
3. **Styling**: Modify CSS in `templates/base.html` or add new stylesheets
4. **JavaScript**: Add custom scripts in template files or create separate JS files

### Data Storage

The application uses JSON file storage (`tasks.json`) for persistence. All tasks are automatically saved to and loaded from this file. The JSON format makes it easy to:

- View and edit tasks manually
- Backup and restore data
- Migrate to other storage systems
- Debug and inspect data

### Database Integration

To upgrade to a database system:

1. Install a database driver (e.g., `pip install flask-sqlalchemy`)
2. Configure database connection in `main.py`
3. Replace the JSON file functions with database models
4. Update CRUD operations to use database queries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/Personal-Task-Manager/issues) page
2. Create a new issue with detailed information
3. Include your Python version, Flask version, and error messages

---

**Happy Task Managing!** 🎉
