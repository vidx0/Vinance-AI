from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/stocks')
def stocks():
    return render_template('stocks.html')

if __name__ == '__main__':
    app.run(debug=True)
