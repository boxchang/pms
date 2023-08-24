from django.shortcuts import render
import socket
from monitor.models import Config


def index(request):
    configs = Config.objects.all()
    for config in configs:
        HOST = config.ip_addr
        PORT = int(config.port)
        server_addr = (HOST, PORT)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(config.command.encode(), server_addr)
        indata, addr = s.recvfrom(1024)
        print('recvfrom ' + str(addr) + ': ' + indata.decode())
    return render(request, 'monitor/index.html', locals())