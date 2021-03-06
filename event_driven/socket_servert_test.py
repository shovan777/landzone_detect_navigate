# Copyright (c) Prokura Innovations. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from aiohttp import web
import socketio

# creates a new Async Socket IO Server
sio = socketio.Server()
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

# we can define aiohttp endpoints just as we normally
# would with no change
def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect',namespace='/')
def connect(sid, environ):
    print('connect',sid)

@sio.on('disconnect',namespace='/')
def disconnect(sid):
    print('disconnect',sid)


# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the
# event we wish to listen out for
@sio.on('message',namespace='/')
def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)
    sio.emit('reply',room=sid)

# We bind our aiohttp endpoint to our app
# router
app.router.add_get('/', index)

# We kick off our server
if __name__ == '__main__':
    web.run_app(app)
