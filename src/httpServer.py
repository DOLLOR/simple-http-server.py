import http.server
import typing
import platform
import ssl
# from _typeshed import StrOrBytesPath

Handler = http.server.BaseHTTPRequestHandler
StrOrBytesPath = typing.Union[str,bytes]

class OnRequestCallbackResult(typing.TypedDict):
    data: typing.Union[str,bytes]
    headers: typing.Optional[typing.Dict[str, str]]
    statusCode: typing.Optional[int]

OnRequestCallback = typing.Callable[[Handler], OnRequestCallbackResult]


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
    certfile:typing.Optional[StrOrBytesPath]=None,
    keyfile:typing.Optional[StrOrBytesPath]=None,
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
                result = onRequest(self)
                self.handlerSendHeader(result)
                if type(result['data']) == str:
                    text = typing.cast(str,result['data'])
                    data = bytes(text, "utf8")
                else:
                    data = typing.cast(bytes,result['data'])
                self.wfile.write(data)

        def handlerSendHeader(self, result: OnRequestCallbackResult):
            if result['statusCode']: pass
            else:
                result['statusCode'] = 200

            self.send_response(result['statusCode'])
            self.send_header('Dollor-Server',f'My server Python/{platform.python_version()}')

            if result['headers']:
                for (key, value,) in result['headers'].items():
                    self.send_header(key,value)
            else:
                self.send_header('Access-Control-Allow-Origin','*')
                self.send_header('Access-Control-Allow-Headers','*')
                self.send_header('Cache-Control','public, max-age=0')
                self.send_header('Content-Type','text/plain; charset=UTF-8')

            self.end_headers()

        def log_request(self,code='-', size='-'):pass

    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, RequestHandler)

    if certfile and keyfile:
        httpd.socket = ssl.wrap_socket(
            httpd.socket,
            server_side=True,
            certfile=certfile,
            keyfile=keyfile,
        )
        print(f'server is running {host} {port} https://localhost:{port}')
    else:
        print(f'server is running {host} {port} http://localhost:{port}')

    httpd.serve_forever()
    return httpd
