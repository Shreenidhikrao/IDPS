from scapy.all import *
import multiprocessing


SERVICES = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS"}

def get_service_name(port):
    return SERVICES.get(port, "Unknown")

def packet_handler(packet, results_queue):
    result = []
    if packet.haslayer(TCP):
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        flags = packet[TCP].flags
        protocol = "TCP"
    elif packet.haslayer(UDP):
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        flags = None  # UDP doesn't have flags
        protocol = "UDP"
    else:
        src_port = None
        dst_port = None
        flags = None
        protocol = "Unknown"

    result.append(f"{protocol}")
    if src_port:
        result.append(f"{get_service_name(src_port)}")
    else:
        result.append("Unknown")
    if flags is not None and protocol == "TCP":
        tcp_flags = []
        if flags & 0x01:
            tcp_flags.append("FIN")
        if flags & 0x02:
            tcp_flags.append("SYN")
        if flags & 0x04:
            tcp_flags.append("RST")
        if flags & 0x08:
            tcp_flags.append("PSH")
        if flags & 0x10:
            tcp_flags.append("ACK")
        if flags & 0x20:
            tcp_flags.append("URG")
        result.append(f"{','.join(tcp_flags)}")
    else:
        result.append("N/A")

    results_queue.put(result)

def packet_sniffer(iface, results_queue, stop_event, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        conn, addr = server_socket.accept()
        with conn:
            while not stop_event.is_set():
                packet = sniff(iface=iface, count=1)
                packet_handler(packet[0], results_queue)

def main():
    results_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()

    # Set the host and port for socket communication
    host = '127.0.0.1'
    port = 12346

    # Start the packet sniffer in a separate process
    packet_sniffer_process = multiprocessing.Process(target=packet_sniffer, args=('wlo1', results_queue, stop_event, host, port))
    packet_sniffer_process.start()

    try:
        packet_sniffer_process.join()  # Wait for the packet sniffer process to finish
    except KeyboardInterrupt:
        # Terminate the packet sniffer process when the user interrupts (Ctrl+C)
        stop_event.set()
        packet_sniffer_process.join()

if __name__ == "__main__":
    main()

