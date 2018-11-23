import SimpleHTTPServer
import BaseHTTPServer
import sys
import copy

class reqhand(BaseHTTPServer.BaseHTTPRequestHandler):
    nodes={}

    def do_GET(self):
        print 'Hello GET'
        print 'Reqhand is ',reqhand.nodes
        for value in self.nodes.itervalues():
            if value[2]==True:
                print 'Master',value


    
    
    def do_POST(self):
        print 'Hello POST'
        pass

    def do_HEAD(self):
        pass


def ak(my_port,obj):

    print 'Hello'
    reqhand.nodes=copy.copy(obj.my.node_dict)
    
    abc = BaseHTTPServer.HTTPServer(('',int(my_port)),reqhand)
    import pdb
    # pdb.set_trace()
    print("running")
    abc.serve_forever()
