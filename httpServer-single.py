import socket

port = 8722
server = socket.socket()
server.bind(("", port))

server.listen(5)

count = 0

while True:
    connect,addr = server.accept()
    print('connect--------------------\n',connect,addr)
    data = connect.recv(1024)
    text = data.decode()
    # 两个换行符分隔header和body
    header,body = text.split('\r\n\r\n',1)
    print('header-----------------------\n',header)
    print('body-----------------------\n',body)

    # response header
    responseText = ""
    responseText += "HTTP/1.1 200 OK\r\n"
    responseText += "Server: My server\r\n"
    responseText += "Cache-Control: public, max-age=0\r\n"
    responseText += "Content-Type: text/plain; charset=UTF-8\r\n"
    responseText += "Access-Control-Allow-Origin: *\r\n"
    responseText += "\r\n"
    # response body
    responseText += "server ok!\r\n"
    count += 1
    responseText += "%d\r\n" % (count)

    connect.send(bytes(responseText,"utf-8"))
    connect.close()


'''
fetch('http://192.168.72.244:8722/action',{
	body:new Date().toLocaleString(),
	method: 'POST',
	referrerPolicy: 'no-referrer',
}).then(r=>r.text()).then(console.log)

fetch('http://192.168.72.244:8722/action',{
	method: 'GET',
	referrerPolicy: 'no-referrer',
}).then(r=>r.text()).then(console.log)
'''
