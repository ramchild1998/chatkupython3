"""Server untuk aplikasi obrolan multithread(asynchronous)."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """ Mengatur penanganan untuk klien yang masuk."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s telah terhubung." % client_address)
        client.send(bytes("Salam dari saya! Sekarang ketikkan nama Anda dan tekan enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  #  Mengambil socket klien sebagai argumen.
    """Menangani satu koneksi klien."""

    nama = client.recv(BUFSIZ).decode("utf8")
    ucpnslmt = 'Selamat datang %s! Jika Anda ingin berhenti, ketik {quit} untuk keluar.' % nama
    client.send(bytes(ucpnslmt, "utf8"))
    pesan = "%s telah bergabung dengan obrolan!" % nama
    broadcast(bytes(pesan, "utf8"))
    clients[client] = nama

    while True:
        pesan = client.recv(BUFSIZ)
        if pesan != bytes("{keluar}", "utf8"):
            broadcast(pesan, nama + ": ")
        else:
            client.send(bytes("{keluar}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s telah meninggalkan obrolan." % nama, "utf8"))
            break


def broadcast(pesan, prefix=""):  # prefix adalah untuk identifikasi nama.
    """Siarkan pesan ke semua klien."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + pesan)


clients = {}
addresses = {}

HOST = ''
PORT = 6000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Menunggu Koneksi...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()