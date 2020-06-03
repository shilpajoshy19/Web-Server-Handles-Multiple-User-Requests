import errno
import os
import signal
import socket
import logging

class Server():
    def __init__(self):
        try:
            with open('text.txt', 'r') as fh:
                Conf = fh.read().split()
            p = int(Conf[5])
            
        except:
            logging.warning('File does not exist / Port not found ')
            p = 8888

        self.SERVER_ADDRESS = (self.HOST, self.PORT) = '', p
        self.REQUEST_QUEUE_SIZE = 1024
        self.Generator()

    def DeadPool(signum, frame, temp):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except OSError:
                return
                
            if pid == 0:  # no clients
                return
            
    # Request from the clients
    def WorkStation(self):
        request = self.client.recv(1024)
        
        try:
            with open('text.txt', 'r') as fh:
                Conf = fh.read().split()
            
            html = Conf[21]
            htm = Conf[24]
            txt = Conf[27]
            png = Conf[30]
            gif = Conf[33]
            jpg = Conf[36]
            jpeg = Conf[39]
            css = Conf[42]
            js = Conf[45]


            Keepalive = int(Conf[-1])
            Root = Conf[10][4:-1]

            try:
                if request:

                    string_list = request.decode().split(' ')
                    self.client.settimeout(Keepalive)
                    requesting_file = string_list[1]
                    version = string_list[2]
                    v = version[5:8]
                    myfile = requesting_file.split('?')
                    file = myfile[0][1:]
                    if file == 'index':
                        file += html
                    else:
                        file = file

                    # HTTP version
                    if (v == '1.1' or v == '1.0'): 

                        if (string_list[0] == 'GET'):
                            
                            # Handling the get request
                            if os.path.isfile(Root + file):

                                with open(Root + file, 'rb') as fh:
                                    response = fh.read()
                                header = 'HTTP/' + v + ' 200 OK\n'
                                header += 'Content-Type: ' + file + '<Content_Length: ' + str(os.path.getsize(Root + file)) + '\n\n'
                                http_response = header.encode()
                                http_response += response

                            elif (file == ''):

                                myfile = Root + 'index.html'
                                with open(myfile) as fh:
                                    hresponse = 'HTTP/' + v + ' 200 OK\n' + fh.read()
                                http_response = hresponse.encode()

                            else:
                                # the file is not exist : 404 Not Found
                                header = 'HTTP/' + v + ' 404 Not Found\n\n'
                                response = '<html><body><center><h3>Error 404: Not Found Reason URL does not Exist</h3><p>Shjo</p></center></body></html>'.encode()
                                http_response = header.encode()
                                http_response += response


                        elif (string_list[0] == 'POST'):
                            # Handling The post request
                            header = 'HTTP/' + v + ' 200 OK\n\n'
                            response = '<html><body><h1>Post Data</h1><pre>\n'.encode() + request + '</pre> </body></html>'.encode()
                            http_response = header.encode()
                            http_response += response

                        else:
                            # Handling other kind of request
                            header = 'HTTP/1.1 400 Bad Request\n\n'
                            response = '<html><body><center><h3>400 Bad Request: Invalid Request.</h3>\n<p>Shjo</p></center></body></html>'.encode()
                            http_response = header.encode()
                            http_response += response

                    else:
                        # Handling the 501 error
                        header = 'HTTP/' + v + ' 501 Not Implemented\n\n'
                        response = '<html><body><center><h3>Error 501: Not Implemented</h3>\n<p>Shjo</p></center></body></html>'.encode()
                        http_response = header.encode()
                        http_response += response

            except:
                # Handling other kind of request error
                header = 'HTTP/1.1 400 Bad Request\n\n'
                response = '<html><body><center><h3>Error 400: Invalid Request </h3><p>Shjo</p></center></body></html>'.encode()
                http_response = header.encode()
                http_response += response
        except:
            # Handling server error
            header = 'HTTP/1.1 500 Internal Server Error\n\n'
            response = '<html><body><center><h3>Error 500: Server Error </h3><p>Shjo</p></center></body></html>'.encode()
            http_response = header.encode()
            http_response += response

        try:
            self.client.sendall(http_response)
        except:
            logging.warning('Unexpected Error: Empty Packet / Empty Address')

    def Generator(self):
        # generate new socket
        self.listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen.bind(self.SERVER_ADDRESS)
        self.listen.listen(self.REQUEST_QUEUE_SIZE)
        print('The HTTP Server is running on port {port} ...'.format(port=self.PORT))

        while True:
            signal.signal(signal.SIGCHLD, self.DeadPool)
            # Accept Request
            try:
                self.client, self.client_address = self.listen.accept()
            except IOError as e:
                logging.warning('Connection was interrupted')
                code, msg = e.args
                if code == errno.EINTR:
                    continue
                else:
                    raise
                
            
            pid = os.fork()
            if pid == 0:
                self.listen.close()  # close the listen request 
                self.WorkStation()   # handle the client request 
                os._exit(0)
            else:  
                self.client.close()  # close the request


if __name__ == '__main__':
    server = Server()
