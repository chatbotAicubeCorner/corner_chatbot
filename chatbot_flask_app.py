from flask import Flask, request, redirect, render_template, jsonify

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    message = ""
    if request.method == 'POST':
        print(request.form)
        message = request.form
    return render_template('index.html', message = message)




if __name__  ==  '__main__':
    app.run(debug=True)