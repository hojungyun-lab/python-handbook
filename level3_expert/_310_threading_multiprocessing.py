"""
_310_threading_multiprocessing.py — 스레딩과 멀티프로세싱

이 모듈에서 다루는 내용:
  1. Thread 기본
  2. Lock과 동기화
  3. GIL의 이해
  4. concurrent.futures (ThreadPoolExecutor)
  5. multiprocessing (ProcessPoolExecutor)
  6. 실용적인 병렬 패턴

실행 방법:
    poetry run python 3_expert/_310_threading_multiprocessing.py
"""

import os
import threading
import time
from concurrent.futures import (
    Future,
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    as_completed,
)


def demonstrate_thread_basics() -> None:
    """Thread 기본을 보여준다."""
    print("=" * 60)
    print("1. Thread 기본")
    print("=" * 60)

    # 기본 스레드 생성
    results: list[str] = []

    def worker(name: str, delay: float) -> None:
        """작업자 스레드."""
        tid: int = threading.get_ident()
        print(f"  [{name}] 시작 (tid={tid})")
        time.sleep(delay)
        results.append(f"{name}-done")
        print(f"  [{name}] 완료")

    threads: list[threading.Thread] = []
    for name, delay in [("A", 0.1), ("B", 0.05), ("C", 0.08)]:
        t: threading.Thread = threading.Thread(
            target=worker, args=(name, delay)
        )
        threads.append(t)
        t.start()

    # 모든 스레드 완료 대기
    for t in threads:
        t.join()

    print(f"  결과: {results}")
    print(f"  메인 스레드: {threading.current_thread().name}")
    print(f"  활성 스레드 수: {threading.active_count()}")

    # 데몬 스레드
    def background_task() -> None:
        while True:
            time.sleep(0.1)

    daemon: threading.Thread = threading.Thread(
        target=background_task, daemon=True
    )
    daemon.start()
    print(f"\n  데몬 스레드: 메인 종료 시 자동 종료됨")


def demonstrate_lock() -> None:
    """Lock과 동기화를 보여준다."""
    print("\n" + "=" * 60)
    print("2. Lock과 동기화")
    print("=" * 60)

    # Lock 없이 — 경쟁 조건 (Race Condition)
    counter_unsafe: int = 0

    def increment_unsafe() -> None:
        nonlocal counter_unsafe
        for _ in range(100_000):
            counter_unsafe += 1

    threads = [
        threading.Thread(target=increment_unsafe) for _ in range(4)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Lock 없이 (4×100K): {counter_unsafe:,} (예상: 400,000)")

    # Lock 사용
    counter_safe: int = 0
    lock: threading.Lock = threading.Lock()

    def increment_safe() -> None:
        nonlocal counter_safe
        for _ in range(100_000):
            with lock:  # 자동 acquire/release
                counter_safe += 1

    threads = [
        threading.Thread(target=increment_safe) for _ in range(4)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Lock 사용 (4×100K): {counter_safe:,}")  # → Lock 사용 (4×100K): 400,000

    # RLock (재진입 가능)
    rlock: threading.RLock = threading.RLock()
    print(f"\nRLock: 같은 스레드에서 여러 번 acquire 가능")

    # Condition — 조건 변수
    print(f"Condition: wait()/notify()로 스레드 간 통신")

    # Event — 일회성 신호
    event: threading.Event = threading.Event()

    def waiter() -> None:
        event.wait()
        print(f"  Event 수신!")

    t = threading.Thread(target=waiter)
    t.start()
    time.sleep(0.01)
    event.set()
    t.join()


def demonstrate_gil() -> None:
    """GIL을 설명한다."""
    print("\n" + "=" * 60)
    print("3. GIL (Global Interpreter Lock)")
    print("=" * 60)

    # CPU-bound 작업 (GIL 제한)
    def cpu_work(n: int) -> int:
        """CPU 집약 작업."""
        return sum(i * i for i in range(n))

    size: int = 5_000_000

    # 순차 실행
    start: float = time.perf_counter()
    cpu_work(size)
    cpu_work(size)
    sequential: float = time.perf_counter() - start
    print(f"CPU-bound 순차 (×2): {sequential:.3f}초")

    # 스레드 실행 (GIL → 속도 향상 없음)
    start = time.perf_counter()
    t1 = threading.Thread(target=cpu_work, args=(size,))
    t2 = threading.Thread(target=cpu_work, args=(size,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    threaded: float = time.perf_counter() - start
    print(f"CPU-bound 스레드 (×2): {threaded:.3f}초")
    print(f"  속도 비율: {sequential/threaded:.2f}x")

    # I/O-bound 작업 (GIL 해제됨 → 스레드 유효)
    def io_work(delay: float) -> None:
        time.sleep(delay)

    start = time.perf_counter()
    io_work(0.1)
    io_work(0.1)
    sequential_io: float = time.perf_counter() - start

    start = time.perf_counter()
    t1 = threading.Thread(target=io_work, args=(0.1,))
    t2 = threading.Thread(target=io_work, args=(0.1,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    threaded_io: float = time.perf_counter() - start

    print(f"\nI/O-bound 순차: {sequential_io:.3f}초")
    print(f"I/O-bound 스레드: {threaded_io:.3f}초")
    print(f"  속도 향상: {sequential_io/threaded_io:.1f}x")

    print(f"\n📌 GIL 요약:")
    print(f"  CPU-bound → threading 비효율 → multiprocessing 사용")
    print(f"  I/O-bound → threading 유효 (GIL 해제)")
    print(f"  Python 3.13+ → PEP 703 free-threading 실험적 지원")


def demonstrate_thread_pool() -> None:
    """ThreadPoolExecutor를 보여준다."""
    print("\n" + "=" * 60)
    print("4. concurrent.futures (ThreadPoolExecutor)")
    print("=" * 60)

    def download(url: str) -> dict[str, str | float]:
        """다운로드 시뮬레이션."""
        delay: float = len(url) * 0.005
        time.sleep(delay)
        return {"url": url, "size": len(url) * 100}

    urls: list[str] = [
        "https://python.org",
        "https://docs.python.org",
        "https://pypi.org",
        "https://github.com",
    ]

    # submit + as_completed
    print("ThreadPoolExecutor:")
    start: float = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures: dict[Future[dict], str] = {
            executor.submit(download, url): url for url in urls
        }
        for future in as_completed(futures):
            url: str = futures[future]
            result: dict = future.result()
            print(f"  ✅ {url}: {result['size']} bytes")

    elapsed: float = time.perf_counter() - start
    print(f"  총 시간: {elapsed:.3f}초")

    # map — 간단한 병렬 매핑
    with ThreadPoolExecutor(max_workers=4) as executor:
        results: list[dict] = list(executor.map(download, urls))
    print(f"\nmap: {len(results)}개 완료")

    # 예외 처리
    def risky_task(n: int) -> int:
        if n == 3:
            raise ValueError(f"Error on {n}")
        time.sleep(0.01)
        return n * 10

    print(f"\n예외 처리:")
    with ThreadPoolExecutor() as executor:
        futures_list: list[Future[int]] = [
            executor.submit(risky_task, i) for i in range(5)
        ]
        for f in as_completed(futures_list):
            try:
                print(f"  결과: {f.result()}")
            except ValueError as e:
                print(f"  에러: {e}")


def _cpu_task(n: int) -> int:
    """CPU 작업 (프로세스풀용, 모듈 레벨 필수)."""
    return sum(i * i for i in range(n))


def demonstrate_process_pool() -> None:
    """ProcessPoolExecutor를 보여준다."""
    print("\n" + "=" * 60)
    print("5. multiprocessing (ProcessPoolExecutor)")
    print("=" * 60)

    size: int = 2_000_000
    count: int = 4

    # 순차
    start: float = time.perf_counter()
    for _ in range(count):
        _cpu_task(size)
    sequential: float = time.perf_counter() - start
    print(f"순차 ({count}×): {sequential:.3f}초")

    # ProcessPoolExecutor
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=count) as executor:
        results: list[int] = list(
            executor.map(_cpu_task, [size] * count)
        )
    parallel: float = time.perf_counter() - start
    print(f"프로세스풀 ({count}×): {parallel:.3f}초")
    print(f"  속도 향상: {sequential/parallel:.1f}x")
    print(f"  CPU 코어 수: {os.cpu_count()}")




def demonstrate_practical_patterns() -> None:
    """실용적인 병렬 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 실용적인 패턴")
    print("=" * 60)

    # 프로듀서-컨슈머 패턴
    import queue

    task_queue: queue.Queue[int | None] = queue.Queue(maxsize=10)
    results: list[int] = []

    def producer() -> None:
        for i in range(10):
            task_queue.put(i)
            time.sleep(0.001)
        task_queue.put(None)  # 종료 신호

    def consumer() -> None:
        while True:
            item: int | None = task_queue.get()
            if item is None:
                break
            results.append(item * 2)
            task_queue.task_done()

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(f"프로듀서-컨슈머: {results}")  # → 프로듀서-컨슈머: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

    # 올바른 도구 선택
    print(f"\n📌 동시성 도구 선택:")
    print(f"  {'작업 유형':<15} {'도구':<30} 비고")
    print(f"  {'-'*15} {'-'*30} {'-'*20}")
    print(f"  {'I/O-bound':<15} {'asyncio':<30} 높은 동시성, 단일 스레드")
    print(f"  {'I/O-bound':<15} {'ThreadPoolExecutor':<30} 간단, 블로킹 라이브러리")
    print(f"  {'CPU-bound':<15} {'ProcessPoolExecutor':<30} GIL 우회")
    print(f"  {'혼합':<15} {'asyncio + ProcessPool':<30} I/O + CPU 조합")


if __name__ == "__main__":
    demonstrate_thread_basics()
    demonstrate_lock()
    demonstrate_gil()
    demonstrate_thread_pool()
    demonstrate_process_pool()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ _310_threading_multiprocessing.py 학습 완료!")
    print("=" * 60)
