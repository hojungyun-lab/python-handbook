"""
_300_async_await.py — 비동기 프로그래밍 (Async/Await)

이 모듈에서 다루는 내용:
  1. asyncio 기본 (async/await)
  2. Task와 동시 실행
  3. asyncio.gather와 as_completed
  4. 비동기 제너레이터와 async for
  5. async with (비동기 컨텍스트 매니저)
  6. 동기화 프리미티브 (Lock, Semaphore, Event)

실행 방법:
    poetry run python 3_expert/_300_async_await.py
"""

import asyncio
import time


async def demonstrate_basic_async() -> None:
    """asyncio 기본을 보여준다."""
    print("=" * 60)
    print("1. asyncio 기본 (async/await)")
    print("=" * 60)

    # 코루틴 정의
    async def say_hello(name: str, delay: float) -> str:
        """비동기로 인사한다."""
        print(f"  {name}: 시작 (대기 {delay}초)")
        await asyncio.sleep(delay)  # 비동기 대기
        print(f"  {name}: 완료!")
        return f"Hello, {name}!"

    # 단일 코루틴 실행
    result: str = await say_hello("Python", 0.1)
    print(f"  결과: {result}")  # →   결과: Hello, Python!

    # 코루틴 vs 일반 함수
    print(f"\n📌 핵심 개념:")
    print(f"  async def → 코루틴 함수 정의")
    print(f"  await     → 코루틴 실행 대기")
    print(f"  asyncio.run() → 이벤트 루프 시작")
    print(f"  💡 await는 async 함수 안에서만 사용 가능!")


async def demonstrate_tasks() -> None:
    """Task와 동시 실행을 보여준다."""
    print("\n" + "=" * 60)
    print("2. Task와 동시 실행")
    print("=" * 60)

    async def fetch_data(source: str, delay: float) -> dict[str, str | float]:
        """데이터를 가져오는 시뮬레이션."""
        await asyncio.sleep(delay)
        return {"source": source, "delay": delay}

    # 순차 실행
    start: float = time.perf_counter()
    r1 = await fetch_data("DB", 0.1)
    r2 = await fetch_data("API", 0.15)
    r3 = await fetch_data("Cache", 0.05)
    sequential: float = time.perf_counter() - start
    print(f"순차 실행: {sequential:.3f}초")

    # 동시 실행 (Task)
    start = time.perf_counter()
    task1: asyncio.Task[dict] = asyncio.create_task(fetch_data("DB", 0.1))
    task2: asyncio.Task[dict] = asyncio.create_task(fetch_data("API", 0.15))
    task3: asyncio.Task[dict] = asyncio.create_task(fetch_data("Cache", 0.05))

    results: list[dict] = [await task1, await task2, await task3]
    concurrent: float = time.perf_counter() - start
    print(f"동시 실행: {concurrent:.3f}초")
    print(f"  속도 향상: {sequential/concurrent:.1f}배")

    # Task 상태
    task: asyncio.Task[dict] = asyncio.create_task(fetch_data("test", 0.01))
    print(f"\nTask 상태:")
    print(f"  done: {task.done()}")
    await task
    print(f"  done: {task.done()}")
    print(f"  result: {task.result()}")


async def demonstrate_gather() -> None:
    """asyncio.gather와 as_completed를 보여준다."""
    print("\n" + "=" * 60)
    print("3. gather와 as_completed")
    print("=" * 60)

    async def process(name: str, delay: float) -> str:
        await asyncio.sleep(delay)
        return f"{name}({delay}s)"

    # gather — 여러 코루틴을 한번에 실행
    start: float = time.perf_counter()
    results: list[str] = await asyncio.gather(
        process("A", 0.1),
        process("B", 0.15),
        process("C", 0.05),
    )
    elapsed: float = time.perf_counter() - start
    print(f"gather: {results} ({elapsed:.3f}초)")

    # gather + return_exceptions
    async def might_fail(n: int) -> int:
        if n == 2:
            raise ValueError("에러!")
        await asyncio.sleep(0.01)
        return n * 10

    results_with_errors = await asyncio.gather(
        might_fail(1), might_fail(2), might_fail(3),
        return_exceptions=True,
    )
    print(f"\nreturn_exceptions: {results_with_errors}")

    # as_completed — 완료 순서대로 처리
    print(f"\nas_completed (완료 순서):")
    coros = [process("A", 0.15), process("B", 0.05), process("C", 0.1)]
    for coro in asyncio.as_completed(coros):
        result: str = await coro
        print(f"  완료: {result}")

    # TaskGroup (Python 3.11+)
    print(f"\nTaskGroup (Python 3.11+):")
    results_tg: list[str] = []
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(process("X", 0.05)),
            tg.create_task(process("Y", 0.1)),
        ]
    results_tg = [t.result() for t in tasks]
    print(f"  결과: {results_tg}")


async def demonstrate_async_generators() -> None:
    """비동기 제너레이터를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 비동기 제너레이터와 async for")
    print("=" * 60)

    # async 제너레이터
    async def async_range(start: int, stop: int, delay: float = 0.01):
        """비동기 범위 제너레이터."""
        for i in range(start, stop):
            await asyncio.sleep(delay)
            yield i

    # async for
    print("async for:")
    values: list[int] = []
    async for n in async_range(1, 6):
        values.append(n)
    print(f"  결과: {values}")  # →   결과: [1, 2, 3, 4, 5]

    # 비동기 컴프리헨션
    results: list[int] = [n async for n in async_range(1, 6)]
    print(f"  async 컴프리헨션: {results}")  # →   async 컴프리헨션: [1, 2, 3, 4, 5]

    # 필터링
    evens: list[int] = [n async for n in async_range(1, 11) if n % 2 == 0]
    print(f"  짝수 필터: {evens}")  # →   짝수 필터: [2, 4, 6, 8, 10]

    # 실용: 스트림 처리
    async def data_stream() -> None:
        """데이터 스트림 시뮬레이션."""
        data: list[str] = ["chunk1", "chunk2", "chunk3"]
        for chunk in data:
            await asyncio.sleep(0.01)
            yield chunk

    print(f"\n스트림 처리:")
    async for chunk in data_stream():
        print(f"  수신: {chunk!r}")


async def demonstrate_async_context_manager() -> None:
    """async with를 보여준다."""
    print("\n" + "=" * 60)
    print("5. async with (비동기 컨텍스트 매니저)")
    print("=" * 60)

    # __aenter__ / __aexit__
    class AsyncTimer:
        """비동기 타이머."""

        def __init__(self, label: str) -> None:
            self.label: str = label
            self.start: float = 0

        async def __aenter__(self) -> "AsyncTimer":
            self.start = time.perf_counter()
            print(f"  [{self.label}] 시작")
            return self

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: object | None,
        ) -> None:
            elapsed: float = time.perf_counter() - self.start
            print(f"  [{self.label}] 완료: {elapsed:.4f}초")

    async with AsyncTimer("작업"):
        await asyncio.sleep(0.05)

    # asynccontextmanager
    import contextlib

    @contextlib.asynccontextmanager
    async def async_resource(name: str):
        """비동기 리소스 관리자."""
        print(f"\n  리소스 '{name}' 획득")
        try:
            yield name
        finally:
            print(f"  리소스 '{name}' 해제")

    async with async_resource("DB Connection") as conn:
        print(f"  사용 중: {conn}")


async def demonstrate_synchronization() -> None:
    """동기화 프리미티브를 보여준다."""
    print("\n" + "=" * 60)
    print("6. 동기화 프리미티브")
    print("=" * 60)

    # Lock — 상호 배제
    lock: asyncio.Lock = asyncio.Lock()
    shared: list[str] = []

    async def worker(name: str) -> None:
        async with lock:
            shared.append(f"{name}-start")
            await asyncio.sleep(0.01)
            shared.append(f"{name}-end")

    await asyncio.gather(worker("A"), worker("B"), worker("C"))
    print(f"Lock (순서 보장): {shared}")

    # Semaphore — 동시 접근 제한
    sem: asyncio.Semaphore = asyncio.Semaphore(2)  # 최대 2개 동시

    async def limited_task(n: int) -> str:
        async with sem:
            print(f"  Task {n}: 시작 (세마포어 획득)")
            await asyncio.sleep(0.05)
            return f"Task-{n}"

    print(f"\nSemaphore (동시 2개 제한):")
    results: list[str] = await asyncio.gather(
        limited_task(1), limited_task(2),
        limited_task(3), limited_task(4),
    )
    print(f"  결과: {results}")

    # Event — 이벤트 통지
    event: asyncio.Event = asyncio.Event()

    async def waiter(name: str) -> str:
        await event.wait()
        return f"{name} received event"

    async def setter() -> None:
        await asyncio.sleep(0.05)
        event.set()
        print(f"\nEvent: set!")

    results2 = await asyncio.gather(
        waiter("W1"), waiter("W2"), setter(),
    )
    print(f"  대기자 결과: {results2[:2]}")

    # Queue — 비동기 큐
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=5)

    async def producer() -> None:
        for i in range(3):
            await queue.put(f"item-{i}")

    async def consumer() -> list[str]:
        items: list[str] = []
        for _ in range(3):
            item: str = await queue.get()
            items.append(item)
            queue.task_done()
        return items

    await producer()
    consumed: list[str] = await consumer()
    print(f"\nQueue: {consumed}")  # → Queue: ['item-0', 'item-1', 'item-2']

    print(f"\n📌 async/await 모범 사례:")
    print(f"  ✅ I/O-bound 작업에 사용 (네트워크, 파일)")
    print(f"  ✅ asyncio.gather()로 동시 실행")
    print(f"  ✅ TaskGroup (3.11+)으로 구조적 동시성")
    print(f"  ❌ CPU-bound 작업 → multiprocessing 사용")
    print(f"  ❌ 동기 코드와 혼합 시 주의 (블로킹 방지)")


async def main() -> None:
    """메인 비동기 함수."""
    await demonstrate_basic_async()
    await demonstrate_tasks()
    await demonstrate_gather()
    await demonstrate_async_generators()
    await demonstrate_async_context_manager()
    await demonstrate_synchronization()

    print("\n" + "=" * 60)
    print("✅ _300_async_await.py 학습 완료!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
