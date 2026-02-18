"""
_380_networking.py — 네트워킹 (Networking)

이 모듈에서 다루는 내용:
  1. socket 프로그래밍 기본
  2. TCP 에코 서버/클라이언트
  3. HTTP 요청 (urllib)
  4. 비동기 네트워킹 (asyncio)
  5. 네트워크 유틸리티

실행 방법:
    poetry run python 3_expert/_380_networking.py
"""

import asyncio
import json
import socket
import threading
import urllib.error
import urllib.parse
import urllib.request


def demonstrate_socket_basics() -> None:
    """socket 기본을 보여준다."""
    print("=" * 60)
    print("1. socket 프로그래밍 기본")
    print("=" * 60)

    hostname: str = socket.gethostname()
    print(f"호스트명: {hostname}")

    try:
        ip: str = socket.gethostbyname(hostname)
        print(f"IP: {ip}")
    except socket.gaierror:
        print(f"IP 확인 불가")

    print(f"\n📌 소켓 타입:")
    print(f"  SOCK_STREAM: TCP (신뢰성, 연결 지향)")
    print(f"  SOCK_DGRAM:  UDP (빠름, 비연결)")

    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0)
    print(f"\n소켓 생성: fd={sock.fileno()}")
    sock.close()


def demonstrate_tcp_echo() -> None:
    """TCP 에코 서버/클라이언트를 보여준다."""
    print("\n" + "=" * 60)
    print("2. TCP 에코 서버/클라이언트")
    print("=" * 60)

    host: str = "127.0.0.1"
    server_ready: threading.Event = threading.Event()
    actual_port: list[int] = []

    def echo_server() -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, 0))
            actual_port.append(s.getsockname()[1])
            s.listen(1)
            s.settimeout(5.0)
            server_ready.set()
            conn, addr = s.accept()
            with conn:
                data: bytes = conn.recv(1024)
                conn.sendall(data.upper())

    server_thread = threading.Thread(target=echo_server, daemon=True)
    server_thread.start()
    server_ready.wait()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, actual_port[0]))
        message: str = "Hello, Server!"
        s.sendall(message.encode())
        response: bytes = s.recv(1024)

    print(f"보낸 메시지: {message!r}")  # → 보낸 메시지: 'Hello, Server!'
    print(f"받은 응답: {response.decode()!r}")  # → 받은 응답: 'HELLO, SERVER!'
    server_thread.join(timeout=2)


def demonstrate_http_urllib() -> None:
    """HTTP 요청을 보여준다."""
    print("\n" + "=" * 60)
    print("3. HTTP 요청 (urllib)")
    print("=" * 60)

    print("GET 요청:")
    try:
        url: str = "https://httpbin.org/get?name=Python"
        req = urllib.request.Request(url, headers={"User-Agent": "PythonLearning/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data: dict = json.loads(resp.read().decode())
            print(f"  상태: {resp.status}")
            print(f"  args: {data.get('args', {})}")
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"  연결 실패: {e}")

    # URL 인코딩/파싱
    params: dict[str, str] = {"query": "파이썬", "page": "1"}
    encoded: str = urllib.parse.urlencode(params)
    print(f"\nURL 인코딩: {encoded}")  # → URL 인코딩: query=%ED%8C%8C%EC%9D%B4%EC%8D%AC&page=1

    parsed = urllib.parse.urlparse("https://example.com:8080/path?q=test#s")
    print(f"URL 파싱: scheme={parsed.scheme}, host={parsed.hostname}, port={parsed.port}")

    print(f"\n📌 HTTP 라이브러리:")
    print(f"  urllib:   표준 라이브러리, 저수준")
    print(f"  requests: 가장 인기, 간결한 API")
    print(f"  httpx:    async 지원, requests 호환")


async def demonstrate_async_networking() -> None:
    """비동기 네트워킹을 보여준다."""
    print("\n" + "=" * 60)
    print("4. 비동기 네트워킹")
    print("=" * 60)

    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        data: bytes = await reader.read(1024)
        writer.write(data.upper())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    server: asyncio.Server = await asyncio.start_server(handle_client, "127.0.0.1", 0)
    port: int = server.sockets[0].getsockname()[1]
    print(f"비동기 에코 서버 (port={port})")

    async def send_msg(msg: str) -> str:
        reader, writer = await asyncio.open_connection("127.0.0.1", port)
        writer.write(msg.encode())
        await writer.drain()
        data = await reader.read(1024)
        writer.close()
        await writer.wait_closed()
        return data.decode()

    async with server:
        results = await asyncio.gather(*[send_msg(m) for m in ["hello", "async", "python"]])

    for sent, received in zip(["hello", "async", "python"], results):
        print(f"  {sent!r} → {received!r}")


def demonstrate_network_utilities() -> None:
    """네트워크 유틸리티를 보여준다."""
    print("\n" + "=" * 60)
    print("5. 네트워크 유틸리티")
    print("=" * 60)

    import ipaddress

    ip4 = ipaddress.ip_address("192.168.1.1")
    print(f"IPv4: {ip4}, private={ip4.is_private}")  # → IPv4: 192.168.1.1, private=True

    net = ipaddress.ip_network("192.168.1.0/24")
    print(f"네트워크: {net}, 호스트={net.num_addresses - 2}")  # → 네트워크: 192.168.1.0/24, 호스트=254

    ports: list[tuple[str, int]] = [
        ("HTTP", 80), ("HTTPS", 443), ("SSH", 22), ("DNS", 53),
    ]
    print(f"\n주요 포트:")
    for name, port in ports:
        print(f"  {name:<6}: {port}")

    print(f"\n📌 네트워킹 모범 사례:")
    print(f"  ✅ 타임아웃 설정, 예외 처리, with 문")
    print(f"  ✅ HTTPS, 환경 변수로 API 키 관리")
    print(f"  ❌ 민감 데이터 평문 전송")


def main() -> None:
    demonstrate_socket_basics()
    demonstrate_tcp_echo()
    demonstrate_http_urllib()
    asyncio.run(demonstrate_async_networking())
    demonstrate_network_utilities()
    print("\n" + "=" * 60)
    print("✅ _380_networking.py 학습 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
