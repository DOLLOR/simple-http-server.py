from .httpServer import createServer,Handler,getRequestBody,OnRequestCallbackResult
import typing

count = 0

def onRequest(handler:Handler) -> OnRequestCallbackResult:
    """http handler
        ```js
        fetch('http://localhost:8722/path/name?a=b',{
        method:'POST',
        body: JSON.stringify({
            a: 1,
            b: 'a',
        }),
        })
        .then(i=>i.text())
        .then(i=>console.log(i))
        ```
    """
    data = getRequestBody(handler)
    ip,port = handler.client_address

    body:typing.Union[bytes,str,None] = data
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
    return {
        'data':f"server ok!\r\n{count}\r\n{body}",
        'headers':None,
        'statusCode':None
    }
    

createServer(
    onRequest=onRequest,
    # certfile='cert.pem',
    # keyfile='key.pem',
)
