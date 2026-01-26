import socket

def check_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print(f"Успешное подключение к {host}:{port}")
        return True
    except socket.error as ex:
        print(f"Ошибка подключения: {ex}")
        return False

if __name__ == "__main__":
    print("Запуск тестового скрипта...")
    check_connection()
