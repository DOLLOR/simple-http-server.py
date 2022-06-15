from .httpServer import createServer,Handler

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
