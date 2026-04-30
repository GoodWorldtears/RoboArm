import socket
import struct

from config import load_config


def recv_some(host, port, timeout=3):
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        try:
            return sock.recv(256)
        except socket.timeout:
            return b""


def check_dashboard(name, host, port):
    print(f"\n{name}: dashboard {host}:{port}")
    try:
        with socket.create_connection((host, port), timeout=3) as sock:
            sock.settimeout(3)
            try:
                banner = sock.recv(256)
                if banner:
                    print("  banner:", banner[:120])
            except socket.timeout:
                print("  banner: timeout")
            sock.sendall(b"robotmode\n")
            response = sock.recv(256)
            print("  robotmode:", response[:120])
    except Exception as exc:
        print(f"  ERROR: {type(exc).__name__}: {exc}")


def check_secondary(name, host, port=30002):
    print(f"\n{name}: secondary {host}:{port}")
    try:
        data = recv_some(host, port)
        print("  first bytes:", data[:80])
        if len(data) >= 4:
            packet_size = struct.unpack("!i", data[:4])[0]
            print("  packet size:", packet_size)
            if packet_size <= 0 or packet_size > 100000:
                print("  WARNING: это не похоже на UR secondary stream")
        else:
            print("  WARNING: данных слишком мало")
    except Exception as exc:
        print(f"  ERROR: {type(exc).__name__}: {exc}")


def main():
    cfg = load_config()
    robots = [
        ("diagnost", cfg.diagnost_ip),
        ("surgeon", cfg.surgeon_ip),
    ]
    for name, host in robots:
        check_dashboard(name, host, cfg.dashboard_port)
        check_secondary(name, host)


if __name__ == "__main__":
    main()
