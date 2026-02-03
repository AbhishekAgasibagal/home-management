from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "ngo_secret_key"


site_data = {
    "mission": "Our Mission text here...",
    "vision": "Our Vision text here...",
}

@app.route('/')
def index():
    return render_template('index.html', data=site_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      
        username = request.form.get('user')
        password = request.form.get('pass')
   
        if username == 'admin' and password == '123':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Credentials. Use admin and 123."
            
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', data=site_data)

@app.route('/update', methods=['POST'])
def update():
    if session.get('logged_in'):
        site_data['mission'] = request.form.get('mission')
        site_data['vision'] = request.form.get('vision')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':

    app.run(debug=True)
