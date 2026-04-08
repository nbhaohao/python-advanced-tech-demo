import socket
from urllib.parse import urlparse


def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"
    port = url.port if url.port else 80
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    client.send("GET {} HTTP/1.1\r\nHost: {}\r\nConnection:close\r\n\r\n".format(path, host).encode('utf8'))

    data = b""
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break
    data = data.decode('utf8')
    html_data = data.split("\r\n\r\n")[1]
    print(html_data)
    client.close()


if __name__ == "__main__":
    get_url("http://www.baidu.com")
