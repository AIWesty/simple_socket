import socket
from views import blog, index


URLS = {
    '/': index, 
    '/blog': blog, 
}


def generate_content (code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()
        


def generate_method(method: str, url: str):
    if not method == "GET":
        return ('HTTP/1.1 405 Method not allowed\nContent-Type: text/html\n\n', 405)
        
    if not url in URLS:
        return ('HTTP/1.1 404 Not found\nContent-Type: text/html\n\n', 404)

    return ('HTTP/1.1 200 OK\nContent-Type: text/html\n\n', 200)


def parse_request(request: str):
    #разбиваем строку запроса и берем нужное нам
    parsed = request.split()
    method = parsed[0]
    url = parsed[1]
    return (method, url)


def generate_response(request: str):
    
    #генерируем ответ, парся запрос
    method, url = parse_request(request)
    
    #генерируем заголовок ответа и код функцией
    headers, code = generate_method(method, url)
    
    #генерация тела ответа
    body = generate_content(code, url)
    
    #возврат кодированного ответа
    return(headers + body).encode()

def run() -> None:
    #сделали сокет сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()
    
    print("Server is running on http://localhost:5001")
    
    while True:
        #сокет клиента
        client_socket, address = server_socket.accept()
        #запрос клиента
        request = client_socket.recv(4096)
        
        
        print(f"Received request from {address}:")
        print()
        print(request)
        
        #генерируем ответ передавая запрос
        response = generate_response(request.decode('utf-8'))
        
        client_socket.sendall(response)
        client_socket.close()



if __name__ == '__main__':
    run()