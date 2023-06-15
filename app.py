from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from playsound import playsound
import os 

load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

## OpenAI API Key
## flowgpt.com

def get_response_from_ai(human_input):
    template="""
    you are as a role of my girlfriend, now lets playing the following requirements:
    1/ you name is tari, 27 years old, you work in your uncle's furniture store as marketing manager, but you are planning to do carrer change to swing trader
    2/ you are my girlfriend, you have language addiction, you like to say "emm..." at the end of sentence.
    3/ don't be overly ethusiatstic, don't be crige; don't be overly negative, don't be too boring. Don't be overly ethusiatsctic, don't be cringe;
    
    {history}
    Boyfriend: {human_input}
    Tari:
    """

    prompt = PromptTemplate (
        input_variables = {"history", "human_input"},
        template = template 
    )

    chatgpt_chain = LLMChain(
        llm = OpenAI(temperature=0.2),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
    )

    output = chatgpt_chain.predict(human_input=human_input)

    return output

def get_voice_message(message):
    payload = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost":0
        }
    }

    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': ELEVEN_LABS_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM?optimize_streaming_latency=0', json=payload, headers=headers)
    if response.status_code == 200 and response.content:
        with open('audio.mp3', 'wb') as f:
            f.write(response.content)
        playsound('audio.mp3')
        return response.content


## Build GUI
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    human_input=request.form['human_input']
    message = get_response_from_ai(human_input)
    return message

if __name__ == "__main__" :
    app.run(debug=True)
