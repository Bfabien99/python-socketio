import eventlet
import eventlet.wsgi
import socketio

# mise en marche du serveur socketio
sio = socketio.Server(cors_allowed_origins='*')

# connected
connected = 0

# création d'une app wsgi qui relie socketio au fichier static
app = socketio.WSGIApp(sio, static_files={
    '/': {"content_type": "text/html", 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    global connected
    connected = connected + 1
    print('client with session ', sid, ' connected')
    sio.emit('private', sid, room=sid)
    sio.emit('notification_connected', connected)

# ajout d'évenement my_message pour gérer auqnd un client envoie un message au serveur
@sio.event
def my_message(sid, data):
    # affichage du message reçu
    print("Message reçu de ", sid, " : ", data)
    data = {"message": data, "sid": sid}
    sio.emit('message', data)


@sio.event
def disconnect(sid):
    global connected
    connected = connected - 1
    print("disconnect from ", sid)
    sio.emit('notification_connected', connected)

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('', 3000)), app)