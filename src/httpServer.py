import http.server
import typing
import platform

Handler = http.server.BaseHTTPRequestHandler

OnRequestCallback = typing.Callable[[Handler],str]

def getRequestBody(handler: Handler) -> typing.Optional[bytes]:
    if handler.headers['Content-Length']:
        content_length = int(handler.headers['Content-Length'])
        body = handler.rfile.read(content_length)
        return body
    else:
        return None

def createServer(
    port:int=8722,
    host:str='',
    onRequest:typing.Optional[OnRequestCallback]=None,
):
    """create http server
    """
    class RequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.handleRequest()
        def do_OPTIONS(self):
            self.handleRequest()
        def do_POST(self):
            self.handleRequest()

        def handleRequest(self):
            if(onRequest):
                message = onRequest(self)
                self.handlerSendHeader()
                self.wfile.write(bytes(message, "utf8"))

        def handlerSendHeader(self):
            self.send_response(200)
            self.send_header('Server',f'My server Python/{platform.python_version()}')
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Access-Control-Allow-Headers','*')
            self.send_header('Cache-Control','public, max-age=0')
            self.send_header('Content-Type','text/plain; charset=UTF-8')
            self.end_headers()

        def log_request(self,code='-', size='-'):pass

    server_address = (host, port)
    print(f'server is running {host} {port} http://localhost:{port}')
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()
    return httpd
