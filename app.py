from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from agent import conversational_agent

app = Flask(__name__, static_folder='./build')
CORS(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/handle_message', methods=['POST'])
def handle_message():
    

    data = request.json
    print('data: ', data)
    if (data['message'][-1]['user'] == "me"):
        # get latest msg
        message = data['message'][-1]['message']
        print('usr-msg', message)

        max_attempts = 3
        for attempt in range(1, max_attempts):
            try:
                response = conversational_agent(message)
                break 
            except:
                if attempt==max_attempts:
                    response = {'output': "Something went wrong. Just try again."}


        print('response: ', response)
        return jsonify({'message': response['output']}) #['output']
    else:
        return jsonify({'message': "Oups! Something went wrong, check again!"})


if __name__ == '__main__':
    app.run()
