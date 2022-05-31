import http.server
import typing

Handler = http.server.BaseHTTPRequestHandler

def createServer(
    port:int=8722,
    host:str='',
    onRequest:typing.Callable[[Handler,bytes|None],str]|None=None
):
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

        def handleRequest(self,body:bytes|None):
            if(onRequest):
                message = onRequest(self,body)
                self.handlerSendHeader()
                self.wfile.write(bytes(message, "utf8"))

        def handlerSendHeader(self):
            self.send_response(200)
            self.send_header('Server','My server')
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Access-Control-Allow-Headers','*')
            self.send_header('Cache-Control','public, max-age=0')
            self.send_header('Content-Type','text/plain; charset=UTF-8')
            self.end_headers()

        def log_request(self,code='-', size='-'):pass

    server_address = (host, port)
    print(f'server is running {host} {port}')
    httpd = http.server.HTTPServer(server_address, Handler)
    httpd.serve_forever()
    return httpd

count = 0
def onReq(handler:Handler,data:bytes|None):
    ip,port = handler.client_address

    body:bytes|str|None = data
    if data and data.decode:
        body = data.decode('utf8')

    print(
f'''
from {ip}:{port}
{handler.command} {handler.path}
{handler.headers}
data:
{body}
-----------
'''
    )
    global count
    count = count + 1
    return f"server ok!\r\n{count}\r\n{body}"

createServer(onRequest=onReq)
