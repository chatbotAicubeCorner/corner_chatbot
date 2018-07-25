from flask import Flask, request, redirect, render_template, jsonify
import requests
from algo_corner import classify
from answer import answer_dict
app = Flask(__name__)


luis_api_link = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/30b0505a-38d8-4cfa-9a66-ebec34db7b97?subscription-key=358d6c53b3b740f79d30410c720a7f95&verbose=true&timezoneOffset=0&q="


@app.route('/', methods=["GET","POST"])
def index():
    message = ""
    answer = ""
    if request.method == 'POST':

        message = request.form['chatbot_message']
        query = str(luis_api_link + message)
        api_callback = requests.get(query).json()
        print(api_callback)
        top_scoring_intent = api_callback['topScoringIntent']['intent']
        print(top_scoring_intent)
        answer = answer_dict[top_scoring_intent]()
        #algo_corner
        #classification = classify(message)[0]
        #answer = answer_dict[classification]()

        print(message)
        print(answer)

    return render_template('index.html', message = message, answer=answer)




if __name__  ==  '__main__':
    app.run(debug=True)