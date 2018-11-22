import SimpleHTTPServer
import BaseHTTPServer
import sys

class reqhand(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self,node_dict):
        self.nodes=node_dict

    def do_GET(self):
        print 'Hello GET'
        for value in self.nodes.itervalues():
            if value[2]==True:
                print value


        
    def do_POST(self):
        print 'Hello POST'
        pass

    def do_HEAD(self):
        pass


def ak(my_port,node_dict):

    print 'Hello'
    abc = BaseHTTPServer.HTTPServer(('',int(my_port)),reqhand(node_dict))
    abc.serve_forever()