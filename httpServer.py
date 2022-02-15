import http.server

def createServer(port=8722,host='',onRequest=None):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.handleRequest(None)
        def do_OPTIONS(self):
            self.handleRequest(None)

        def do_POST(self):
            # post body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            self.handleRequest(body)

        def handleRequest(self,body):
            message = onRequest(self,body)
            self.handlerSendHeader()
            self.wfile.write(bytes(message, "utf8"))

        def handlerSendHeader(self):
            self.send_response(200)
            self.send_header('Server','My server')
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Access-Control-Allow-Headers','*')
            self.send_header('Cache-Control','public, max-age=0')
            self.end_headers()

        def log_request(code='-', size='-'):pass

    server_address = (host, port)
    print('server is running')
    httpd = http.server.HTTPServer(server_address, Handler)
    httpd.serve_forever()
    return httpd

count = 0
def onReq(handler,data):
    ip,port = handler.client_address
    if data and data.decode:
        data = data.decode('utf8')

    print(
        f'from {ip}:{port}',
        handler.command,
        handler.path,
        '\n{',
        handler.headers,
        '}\n',
        'Data: ',
        data,
        '\n-----------',
    )
    global count
    count = count + 1
    return "server ok!\r\n%d" % (count)

createServer(onRequest=onReq)
