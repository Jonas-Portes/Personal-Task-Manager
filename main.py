from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# JSON file for storing tasks
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from JSON file"""
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                # Migrate existing tasks to include end_until field
                for task in tasks:
                    if 'end_until' not in task:
                        task['end_until'] = ''
                return tasks
        else:
            # Create initial tasks if file doesn't exist
            initial_tasks = [
                {
                    'id': 1,
                    'title': 'Complete Flask project',
                    'description': 'Build a complete Flask application',
                    'completed': False,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'end_until': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                },
                {
                    'id': 2,
                    'title': 'Learn Python',
                    'description': 'Study Python programming language',
                    'completed': True,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'end_until': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
                }
            ]
            save_tasks(initial_tasks)
            return initial_tasks
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks_list):
    """Save tasks to JSON file"""
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks_list, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving tasks: {e}")

# Load tasks from JSON file
tasks = load_tasks()

# Routes
@app.route('/')
def index():
    """Home page route"""
    # Reload tasks from JSON file to get latest data
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """Add task route - handles both GET and POST requests"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description', '')
        
        # Validate required fields
        if not title:
            flash('Title is required!', 'error')
            return redirect(url_for('index'))
        
        # Load current tasks
        current_tasks = load_tasks()
        
        # Get end date from form
        end_until = request.form.get('end_until', '')
        
        # Create new task
        new_task = {
            'id': len(current_tasks) + 1,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'end_until': end_until
        }
        
        # Add task to list and save to JSON
        current_tasks.append(new_task)
        save_tasks(current_tasks)
        
        # Flash success message
        flash('Task added successfully!', 'success')
        
        # Redirect to home page
        return redirect(url_for('index'))
    
    # GET request - show add task form
    return render_template('add_task.html')

@app.route('/api/tasks')
def get_tasks():
    """API endpoint to get all tasks"""
    current_tasks = load_tasks()
    return jsonify(current_tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """API endpoint to create a new task"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Load current tasks
    current_tasks = load_tasks()
    
    new_task = {
        'id': len(current_tasks) + 1,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'end_until': data.get('end_until', '')
    }
    
    # Add task and save to JSON
    current_tasks.append(new_task)
    save_tasks(current_tasks)
    
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """API endpoint to update a task"""
    current_tasks = load_tasks()
    task = next((t for t in current_tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    if 'end_until' in data:
        task['end_until'] = data['end_until']
    
    # Save updated tasks to JSON
    save_tasks(current_tasks)
    
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """API endpoint to delete a task"""
    current_tasks = load_tasks()
    task = next((t for t in current_tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Remove task and save to JSON
    current_tasks = [t for t in current_tasks if t['id'] != task_id]
    save_tasks(current_tasks)
    
    return jsonify({'message': 'Task deleted successfully'})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# Template filters
@app.template_filter('datetime')
def format_datetime(value):
    """Format datetime for templates"""
    if isinstance(value, str):
        return value
    return value.strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('is_overdue')
def is_overdue(end_date):
    """Check if task is overdue"""
    if not end_date:
        return False
    try:
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        return end_datetime.date() < datetime.now().date()
    except ValueError:
        return False

@app.template_filter('days_remaining')
def days_remaining(end_date):
    """Calculate days remaining until deadline"""
    if not end_date:
        return None
    try:
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        remaining = (end_datetime.date() - datetime.now().date()).days
        return remaining
    except ValueError:
        return None

# Context processors
@app.context_processor
def inject_now():
    """Inject current datetime into all templates"""
    return {'now': datetime.now()}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
