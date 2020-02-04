from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

result = {}

@socketio.on('quiz', namespace='/test')
def test_message(json):
    global result
    try:
        if result[json[q_id]]:
            json[q_id][a_id] += json[q_id][a_id]
            json[q_id][b_id] += json[q_id][b_id]
            json[q_id][c_id] += json[q_id][c_id]
            json[q_id][d_id] += json[q_id][d_id]-

    except:
        result[json[q_id]] = {
            json[a_id]:1.0,
            json[b_id]:1.0,
            json[c_id]:1.0,
            json[d_id]:1.0
        }
    
    emit('my response', {'data': json}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)