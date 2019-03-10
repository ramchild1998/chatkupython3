"""Skrip untuk klien obrolan GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Menangani penerimaan pesan."""
    while True:
        try:
            pasan = client_socket.recv(BUFSIZ).decode("utf8")
            daftar_pesan.insert(tkinter.END, pasan)
        except OSError:  # Kemungkinan klien telah meninggalkan obrolan.
            break


def send(event=None):  # event dilewati oleh binder.
    """Menangani pengiriman pesan."""
    pesan = pesan_ku.get()
    pesan_ku.set("")  # Menghapus bidang input.
    client_socket.send(bytes(pesan, "utf8"))
    if pesan == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """Fungsi ini dipanggil ketika jendela ditutup."""
    pesan_ku.set("{Keluar")
    send()

top = tkinter.Tk()
top.title("Obrolan")

frame_pesan = tkinter.Frame(top)
pesan_ku = tkinter.StringVar()  # Agar pesan dapat dikirim.
pesan_ku.set("Ketikkan pesan Anda di sini.")
scrollbar = tkinter.Scrollbar(frame_pesan)  # Untuk menavigasi pesan yang lalu.
# Mengikuti akan berisi pesan-pesan.
daftar_pesan = tkinter.Listbox(frame_pesan, height=25, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
daftar_pesan.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
daftar_pesan.pack()
frame_pesan.pack()

entry_field = tkinter.Entry(top, textvariable=pesan_ku)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Kirim", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#---- Sekarang sampai pada bagian soket ----
HOST = input('Masukkan host: ')
PORT = input('Masukkan port: ')
if not PORT:
    PORT = 6000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Mulai eksekusi GUI.