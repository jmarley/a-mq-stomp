# Simple script that tests whether a message server is functioning correctly

import stomp
import time
import getpass

class HornetqListener(object):
    def on_connecting(self, host_and_port):
        print('on_connecting %s %s' % host_and_port)
    def on_error(self, headers, message):
        print('received an error %s' % (headers, message))
    def on_message(self, headers, body):
        print('on_message %s %s' % (headers, body))
    def on_heartbeat(self):
        print('on_heartbeat')
    def on_send(self, frame):
        print('on_send %s %s %s' % (frame.cmd, frame.headers, frame.body))
    def on_connected(self, headers, body):
        print('on_connected %s %s' % (headers, body))
    def on_disconnected(self):
        print('on_disconnected')
    def on_heartbeat_timeout(self):
        print('on_heartbeat_timeout')
    def on_before_message(self, headers, body):
        print('on_before_message %s %s' % (headers, body))
        return (headers, body)

#dest='jms.queue.testQueue'
dest= raw_input('enter topic name, e.g. jms.topic.spin :')
user=raw_input('enter MQ user')
passwd= getpass.getpass()
server=raw_input('Enter server ip, e.g. 192.168.122.170 :')
port=61613

# make STOMP server connection
conn = stomp.Connection(host_and_ports=[(server, port)], prefer_localhost=False,keepalive=True,vhost='example.com')

# instantiate listener
conn.set_listener('',HornetqListener())

conn.start()

#TODO write test for bad username/password , not configured in jboss
conn.connect(username=user,passcode=passwd,wait=True)


# subscribe to queue
conn.subscribe(destination=dest,id=1)

# send message to queue
conn.send(body='the current time is:  ' + str(time.strftime('%X')) , destination=dest)

time.sleep(4)
conn.disconnect()



