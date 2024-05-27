from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def home():
    # Render an HTML template instead of returning plain text
    return render_template('home.html')

@app.route('/about')
def about():
    # Render a different HTML template for the about page
    return render_template('about.html')

@app.route('/hello/<name>')
def hello_name(name):
    # Pass the 'name' variable to the template to personalize the response
    return render_template('hello.html', name=name)

@app.route('/submit', methods=['POST'])
def submit():
    # Example for handling form submission
    name = request.form['name']
    return redirect(url_for('hello_name', name=name))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002 , debug=True)
