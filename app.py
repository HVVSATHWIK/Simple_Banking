# app.py

import os
from flask import Flask, render_template, request, redirect, url_for, abort
import BANKING

app = Flask(__name__)
banking_system = BANKING.banking_system  # Initialize banking system

# Helper function to check if a template file exists
def render_if_exists(template_name, **context):
    template_path = os.path.join(app.template_folder, template_name)
    if not os.path.exists(template_path):
        abort(404)  # Render a 404 error if the template is missing
    return render_template(template_name, **context)

@app.route('/')
def home():
    return render_if_exists('index.html')

@app.route('/about')
def about():
    info = banking_system.about()
    return render_if_exists('about.html', info=info)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        result = banking_system.admin_panel()
        return render_if_exists('admin.html', result=result)
    return render_if_exists('admin.html')

@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        try:
            initial_balance = float(request.form['initial_balance'])
            message = banking_system.create_account(name, initial_balance)
        except ValueError:
            message = "Invalid initial balance. Please enter a numeric value."
        return render_if_exists('create_account.html', message=message)
    return render_if_exists('create_account.html')

@app.route('/deposit', methods=['POST', 'GET'])
def deposit():
    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
            amount = float(request.form['amount'])
            message = banking_system.deposit(user_id, amount)
        except ValueError:
            message = "Invalid input. Please ensure user ID and amount are numeric."
        return render_if_exists('deposit.html', message=message)
    return render_if_exists('deposit.html')

@app.route('/withdraw', methods=['POST', 'GET'])
def withdraw():
    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
            amount = float(request.form['amount'])
            message = banking_system.withdraw(user_id, amount)
        except ValueError:
            message = "Invalid input. Please ensure user ID and amount are numeric."
        return render_if_exists('withdraw.html', message=message)
    return render_if_exists('withdraw.html')

@app.route('/balance', methods=['POST', 'GET'])
def balance():
    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
            message = banking_system.get_balance(user_id)
        except ValueError:
            message = "Invalid user ID. Please enter a numeric value."
        return render_if_exists('balance.html', message=message)
    return render_if_exists('balance.html')

@app.route('/set_budget', methods=['POST', 'GET'])
def set_budget():
    if request.method == 'POST':
        category = request.form['category']
        try:
            amount = float(request.form['amount'])
            banking_system.set_budget(category, amount)
            return redirect(url_for('home'))
        except ValueError:
            message = "Invalid budget amount. Please enter a numeric value."
            return render_if_exists('set_budget.html', message=message)
    return render_if_exists('set_budget.html')

@app.route('/check_budget', methods=['GET'])
def check_budget():
    budget_status = banking_system.check_budget()
    return render_if_exists('check_budget.html', budget_status=budget_status)

@app.route('/generate_report', methods=['GET'])
def generate_report():
    report = banking_system.generate_report()
    return render_if_exists('generate_report.html', report=report)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404  # Optional: create a 404.html template for user-friendly errors

if __name__ == '__main__':
    app.run(debug=True)

@app.teardown_appcontext
def close_db(error):
    banking_system.close()
