#-*- coding:utf-8 -*-
import time
import threading
from socketserver import ThreadingMixIn
from http.server import ThreadingHTTPServer, CGIHTTPRequestHandler

txt_mu = threading.Lock()
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
        if "test.txt" in self.path:
            if txt_mu.acquire(True):
                f = open("test.txt","r")
                read_buf = f.read()
                print(read_buf)
                f.close()
                txt_mu.release()
            self.send_header("Content-Length", str(len(read_buf)))
            self.end_headers()
            try:
                self.wfile.write(read_buf.encode('utf-8'))
            except:
                self.send_error(404, "Page not Found!")
        else:
            self.send_header("Content-Length", str(len(self.Page)))
            self.end_headers()
            try:
                self.wfile.write(self.Page.encode('utf-8'))
            except:
                self.send_error(404, "Page not Found!")

    def do_POST(self):
        print(self.headers)
        print(self.command)
        read_buf = self.rfile.read(int(self.headers['content-length']))
        print(read_buf.decode())
        if txt_mu.acquire(True):
            with open("test.txt", "a+") as f:
                f.write(read_buf.decode())
                f.close()
            f = open("test.txt","r")
            read_buf = f.read()
            print(read_buf)
            f.close()
            txt_mu.release()
        # data = {
        #     'result_code': '2',
        #     'result_desc': 'Success',
        #     'timestamp': '',
        #     'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        # }
        self.send_response(200)
        # self.send_header('Content-type', 'application/json')
        # self.end_headers()
        # self.wfile.write(json.dumps(data).encode('utf-8'))

#----------------------------------------------------------------------

if __name__ == '__main__':
    serverAddress = ('', 70)
    server = ThreadingHTTPServer(serverAddress, RequestHandler)
    server.serve_forever()