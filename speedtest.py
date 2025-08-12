import socket
import threading
import time
import argparse

def format_speed(bits_per_second):
    units = ['bit/s', 'Kbit/s', 'Mbit/s', 'Gbit/s']
    unit_index = 0
    while bits_per_second >= 1000 and unit_index < len(units) - 1:
        bits_per_second /= 1000
        unit_index += 1
    return f"{bits_per_second:,.2f} {units[unit_index]}".replace(',', '.')

def print_elapsed_time(start_time, last_printed_time):
    elapsed_time = int(time.time() - start_time) 
    if elapsed_time > last_printed_time:
        print(f"Tempo decorrido: {elapsed_time} segundos")
        return elapsed_time
    return last_printed_time

def sender(protocol, host, port):
    message = "teste de rede *2024*"
    message = message.ljust(500, '*')
    message_bytes = message.encode('utf-8')

    packets_sent = 0
    bytes_sent = 0

    start_time = time.time()
    end_time = start_time + 20 
    last_printed_time = 0 

    if protocol == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"Conexão TCP estabelecida com {host}:{port}")
        while time.time() < end_time:
            sock.sendall(message_bytes)
            packets_sent += 1
            bytes_sent += len(message_bytes)
            last_printed_time = print_elapsed_time(start_time, last_printed_time)
        sock.close()
    elif protocol == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Pronto para enviar pacotes UDP para {host}:{port}")
        while time.time() < end_time:
            sock.sendto(message_bytes, (host, port))
            packets_sent += 1
            bytes_sent += len(message_bytes)
            last_printed_time = print_elapsed_time(start_time, last_printed_time)
        sock.close()
    else:
        print("Protocolo desconhecido")
        return

    duration = time.time() - start_time
    bits_sent = bytes_sent * 8
    bits_per_second = bits_sent / duration
    packets_per_second = packets_sent / duration

    print(f"Pacotes enviados: {packets_sent}")
    print(f"Bytes enviados: {bytes_sent}")
    print(f"Velocidade: {format_speed(bits_per_second)}")
    print(f"Velocidade em pacotes por segundo: {packets_per_second:,.2f}".replace(',', '.'))

def receiver(protocol, port):
    packets_received = 0
    bytes_received = 0

    if protocol == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', port))
        sock.listen(1)
        print(f"Aguardando conexão TCP na porta {port}...")
        conn, addr = sock.accept()
        print(f"Conexão estabelecida com {addr[0]}:{addr[1]}")
        start_time = time.time()
        end_time = start_time + 20
        last_printed_time = 0 
        conn.settimeout(end_time - start_time)
        try:
            while time.time() < end_time:
                data = conn.recv(500)
                if not data:
                    break
                packets_received += 1
                bytes_received += len(data)
                last_printed_time = print_elapsed_time(start_time, last_printed_time)
        except socket.timeout:
            pass
        sock.settimeout(1)
        conn.close()
        sock.close()
    elif protocol == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        print(f"Aguardando pacotes UDP na porta {port}...")
        start_time = time.time()
        end_time = start_time + 20
        last_printed_time = 0 
        sock.settimeout(end_time - start_time)
        try:
            while time.time() < end_time:
                data, addr = sock.recvfrom(500)
                if not data:
                    break
                if packets_received == 0:
                    print(f"Recebendo pacotes de {addr[0]}:{addr[1]}")
                packets_received += 1
                bytes_received += len(data)
                last_printed_time = print_elapsed_time(start_time, last_printed_time)
        except socket.timeout:
            pass
        sock.settimeout(1)
        sock.close()
    else:
        print("Protocolo desconhecido")
        return

    duration = time.time() - start_time
    bits_received = bytes_received * 8
    bits_per_second = bits_received / duration
    packets_per_second = packets_received / duration

    print(f"Pacotes recebidos: {packets_received}")
    print(f"Bytes recebidos: {bytes_received}")
    print(f"Velocidade: {format_speed(bits_per_second)}")
    print(f"Velocidade em pacotes por segundo: {packets_per_second:,.2f}".replace(',', '.'))

if __name__ == "__main__":
    print("Speedtest - Redes 2024")
    print("Ana Paula Pereira, Cristiano Kenji Nacayama, Leonardo Daiki Fuzikawa")

    parser = argparse.ArgumentParser(description="Ferramenta de teste de rede")
    parser.add_argument('--protocol', choices=['tcp', 'udp'], required=True, help='Protocolo (tcp ou udp)')
    parser.add_argument('--role', choices=['sender', 'receiver'], required=True, help='Função (sender ou receiver)')
    parser.add_argument('--host', help='Endereço IP do receptor (necessário para o sender)')
    parser.add_argument('--port', type=int, default=5000, help='Porta a ser utilizada')

    args = parser.parse_args()

    if args.role == 'sender':
        if not args.host:
            print("Para o sender, é necessário especificar o host.")
        else:
            print("Enviando pacotes para " + args.host + "...")
            sender(args.protocol, args.host, args.port)
    elif args.role == 'receiver':
        print("Recebendo pacotes...")
        receiver(args.protocol, args.port)
    else:
        print("Função desconhecida.")
