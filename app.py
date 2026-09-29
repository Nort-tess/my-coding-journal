from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Temporary in-memory list to store entries (instead of a complex database for now)
journal_entries = [
    {"date": "2026-09-29", "task": "Learned HTML/CSS basics", "hours": 2},
    {"date": "2026-09-30", "task": "Built my first Python Flask app!", "hours": 3}
]

@app.route('/')
def index():
    return render_template('index.html', entries=journal_entries)

@app.route('/add', methods=['POST'])
def add_entry():
    task = request.form.get('task')
    hours = request.form.get('hours')
    
    if task and hours:
        new_entry = {
            "date": datetime.today().strftime('%Y-%m-%d'),
            "task": task,
            "hours": int(hours)
        }
        journal_entries.insert(0, new_entry) # Put newest entries at the top
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
