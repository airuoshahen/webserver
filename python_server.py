#-*- coding:utf-8 -*-
import time
import threading
from socketserver import ThreadingMixIn
from http.server import ThreadingHTTPServer, CGIHTTPRequestHandler

# class RequestHandler(http.server.BaseHTTPRequestHandler):
class RequestHandler(CGIHTTPRequestHandler):
    '''处理请求并返回页面'''

    # 页面模板
    Page = '''\
        <html>
        <body>
        <ul>
        <li>
        <a href="test.txt">test.txt</a>
        </li>
        </ul>
        </body>
        </html>
    '''

    # 处理一个GET请求
    def do_GET(self):
        message = threading.currentThread().getName()
        print(message)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        if "test.txt" in self.requestline:
            with open('test.txt', 'a+') as f:
                f.write("test")
                read_buf = f.read()
                print(read_buf)
                f.close()
            f = open("test.txt","r")
            read_buf = f.read()
            print(read_buf)
            f.close()
            self.send_header("Content-Length", str(len(read_buf)))
            self.end_headers()
            self.wfile.write(read_buf.encode('utf-8'))
        else:
            self.send_header("Content-Length", str(len(self.Page)))
            self.end_headers()
            self.wfile.write(self.Page.encode('utf-8'))
        time.sleep(30)

    def do_POST(self):
        post_buf = self.rfile.read()
        print(post_buf.decode())
        with open("test.txt", "a+") as f:
            f.write(post_buf.decode())
            f.close()
        f = open("test.txt","r")
        read_buf = f.read()
        print(read_buf)
        f.close()
        self.send_response(200)


if __name__ == '__main__':
    serverAddress = ('', 9000)
    server = ThreadingHTTPServer(serverAddress, RequestHandler)
    server.serve_forever()