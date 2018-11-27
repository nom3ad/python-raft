import SimpleHTTPServer
import BaseHTTPServer
import sys
import copy
from wire import *
import socket 

class reqhand(BaseHTTPServer.BaseHTTPRequestHandler):
    nodes={}

    def do_GET(self):
        #print 'Hello GET'
        print 'Node Status is ',reqhand.nodes
        for value in self.nodes.itervalues():
            if value[2]==True:
                file_path = "127.0.0.1:/home/jones/Desktop/td-agent" + str(reqhand.port)
                h = pack_dgram_header(
                    TYPE_WB_DATA,'13',reqhand.rt_obj.my.term)
                b = pack_wb_struct(
                    file_path)
                reqhand.rt_obj.write( h+b, (value[0],value[1]))
                

                print 'Master',reqhand.rt_obj.my.term
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write('Master is '+value[0]+':'+str(value[1]))
        return


    
    
    def do_POST(self):
        print 'Hello POST'
        pass

    def do_HEAD(self):
        pass


def ak(my_port,obj):

    print 'Hello'
    reqhand.rt_obj = obj
    reqhand.nodes=copy.copy(obj.my.node_dict)
    reqhand.port = my_port
    abc = BaseHTTPServer.HTTPServer(('',int(my_port)),reqhand)
    import pdb
    # pdb.set_trace()
    print("running")
    abc.serve_forever()
