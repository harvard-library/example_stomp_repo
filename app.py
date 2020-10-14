from flask import Flask
import stomp

import os,time

def connect_and_subscribe(conn):
    conn.connect('guest', 'guest', wait=True)
    conn.subscribe(destination='/queue/test', id=1, ack='auto')

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, headers, body):
        print('received an error "%s"' % body)

    def on_message(self, headers, body):
        print('received a message "%s"' % body)
        for x in range(10):
            print(x)
        print('processed message')

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)


def create_app():
    app = Flask('myapp')
    app.conn = stomp.Connection([('localhost', 61613)], heartbeats=(4000, 4000))
    app.conn.set_listener('', MyListener(app.conn))
    app.conn.connect('guest', 'guest', wait=True)
    app.conn.subscribe('/queue/test', 24601)
    @app.route('/')
    def root():

        app.conn.send('/queue/test', 'test message')


        return "foo"

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
