"""
_300_context_managers.py — 컨텍스트 매니저

이 모듈에서 다루는 내용:
  1. with 문 동작 원리
  2. __enter__/__exit__ 프로토콜
  3. contextlib.contextmanager
  4. contextlib.suppress
  5. contextlib.ExitStack
  6. 실용적인 컨텍스트 매니저 패턴

실행 방법:
    poetry run python 2_intermediate/_300_context_managers.py
"""

import contextlib
import tempfile
import time
from pathlib import Path


def demonstrate_with_statement() -> None:
    """with 문의 동작 원리를 보여준다."""
    print("=" * 60)
    print("1. with 문 동작 원리")
    print("=" * 60)

    print("""
with expression as var:
    body

위 코드는 내부적으로 다음과 동일:

  manager = expression
  var = manager.__enter__()
  try:
      body
  except:
      if not manager.__exit__(*sys.exc_info()):
          raise
  else:
      manager.__exit__(None, None, None)
""")

    # 파일 — 가장 흔한 컨텍스트 매니저
    tmp: Path = Path(tempfile.mkdtemp()) / "demo.txt"
    with open(tmp, "w") as f:
        f.write("컨텍스트 매니저!")
    # f.close()가 자동 호출됨

    with open(tmp) as f:
        print(f"파일 내용: {f.read()}")  # → 파일 내용: 컨텍스트 매니저!


def demonstrate_enter_exit() -> None:
    """__enter__/__exit__ 프로토콜을 보여준다."""
    print("\n" + "=" * 60)
    print("2. __enter__/__exit__ 프로토콜")
    print("=" * 60)

    class Timer:
        """실행 시간을 측정하는 컨텍스트 매니저."""

        def __init__(self, label: str = "Timer") -> None:
            self.label: str = label
            self.start: float = 0
            self.elapsed: float = 0

        def __enter__(self) -> "Timer":
            self.start = time.perf_counter()
            return self

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: object | None,
        ) -> bool:
            self.elapsed = time.perf_counter() - self.start
            print(f"  [{self.label}] {self.elapsed:.4f}초")
            return False  # 예외를 전파 (True면 예외 억제)

    with Timer("sum 계산"):
        total: int = sum(range(1_000_000))
    print(f"  결과: {total:,}")

    # 예외 처리 컨텍스트 매니저
    class ErrorHandler:
        """예외를 로깅하고 억제하는 컨텍스트 매니저."""

        def __init__(self, suppress: bool = False) -> None:
            self.suppress: bool = suppress

        def __enter__(self) -> "ErrorHandler":
            return self

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: object | None,
        ) -> bool:
            if exc_type is not None:
                print(f"  에러 발생: {exc_type.__name__}: {exc_val}")
            return self.suppress  # True → 예외 억제

    print(f"\n예외 억제:")
    with ErrorHandler(suppress=True):
        _ = 1 / 0  # ZeroDivisionError — 억제됨
    print(f"  계속 실행됨!")


def demonstrate_contextmanager() -> None:
    """contextlib.contextmanager를 보여준다."""
    print("\n" + "=" * 60)
    print("3. contextlib.contextmanager")
    print("=" * 60)

    # 제너레이터 기반 컨텍스트 매니저
    @contextlib.contextmanager
    def timer(label: str = "Timer"):
        """실행 시간 측정 (제너레이터 방식)."""
        start: float = time.perf_counter()
        try:
            yield  # with 블록 실행 지점
        finally:
            elapsed: float = time.perf_counter() - start
            print(f"  [{label}] {elapsed:.4f}초")

    with timer("range sum"):
        total: int = sum(range(500_000))
        print(f"  결과: {total:,}")

    # 값을 yield하는 경우
    @contextlib.contextmanager
    def temp_directory():
        """임시 디렉토리를 생성하고 정리한다."""
        tmp_dir: Path = Path(tempfile.mkdtemp())
        print(f"\n  임시 디렉토리 생성: {tmp_dir.name}")
        try:
            yield tmp_dir
        finally:
            import shutil
            shutil.rmtree(tmp_dir, ignore_errors=True)
            print(f"  임시 디렉토리 삭제됨")

    with temp_directory() as tmp:
        file_path: Path = tmp / "test.txt"
        file_path.write_text("Hello!")
        print(f"  파일 생성: {file_path.name}")

    # 리디렉션 예시
    @contextlib.contextmanager
    def log_section(title: str):
        """로그 섹션을 구분한다."""
        print(f"\n{'─' * 40}")
        print(f"📋 {title}")
        print(f"{'─' * 40}")
        yield
        print(f"{'─' * 40}")

    with log_section("데이터 처리"):
        print("  1단계: 데이터 로드")
        print("  2단계: 변환")
        print("  3단계: 저장")


def demonstrate_suppress() -> None:
    """contextlib.suppress를 보여준다."""
    print("\n" + "=" * 60)
    print("4. contextlib.suppress")
    print("=" * 60)

    # suppress — 특정 예외 무시
    with contextlib.suppress(FileNotFoundError):
        Path("/nonexistent/file.txt").unlink()
    print("파일을 찾을 수 없음 (FileNotFoundError 억제됨)")  # → 파일을 찾을 수 없음 (FileNotFoundError 억제됨)

    # 위 코드는 아래와 동일
    try:
        Path("/nonexistent/file.txt").unlink()
    except FileNotFoundError:
        pass

    # 여러 예외 타입 suppress
    with contextlib.suppress(KeyError, IndexError):
        d: dict[str, int] = {}
        _ = d["missing"]
    print("KeyError 억제됨")  # → KeyError 억제됨

    # closing — close() 호출 보장
    import io
    with contextlib.closing(io.StringIO("hello")) as f:
        content: str = f.read()
        print(f"\nclosing: {content!r}")  # → closing: 'hello'

    # redirect_stdout — stdout 리디렉트
    import io as _io

    captured = _io.StringIO()
    with contextlib.redirect_stdout(captured):
        print("이 출력은 캡처됨")
    print(f"캡처된 내용: {captured.getvalue().rstrip()!r}")  # → 캡처된 내용: '이 출력은 캡처됨'


def demonstrate_exitstack() -> None:
    """contextlib.ExitStack을 보여준다."""
    print("\n" + "=" * 60)
    print("5. contextlib.ExitStack")
    print("=" * 60)

    # ExitStack — 동적으로 컨텍스트 매니저 관리
    tmp: Path = Path(tempfile.mkdtemp())

    file_paths: list[Path] = [
        tmp / f"file_{i}.txt" for i in range(3)
    ]
    for fp in file_paths:
        fp.write_text(f"내용: {fp.name}")

    with contextlib.ExitStack() as stack:
        files = [
            stack.enter_context(open(fp, encoding="utf-8"))
            for fp in file_paths
        ]
        print("ExitStack (동적 파일 열기):")
        for f in files:
            print(f"  {f.name}: {f.read().rstrip()}")
    # 모든 파일 자동으로 닫힘

    # 콜백 등록
    with contextlib.ExitStack() as stack:
        stack.callback(print, "  3. 마지막 등록")
        stack.callback(print, "  2. 두 번째 등록")
        stack.callback(print, "  1. 첫 번째 등록")
        print("\nExitStack 콜백 (LIFO 순서):")
    # 콜백은 등록 역순으로 실행됨


def demonstrate_practical_patterns() -> None:
    """실용적인 컨텍스트 매니저 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 실용적인 패턴")
    print("=" * 60)

    # 트랜잭션 패턴
    @contextlib.contextmanager
    def transaction(data: dict):
        """딕셔너리 트랜잭션 — 실패 시 롤백."""
        backup: dict = data.copy()
        try:
            yield data
        except Exception:
            data.clear()
            data.update(backup)
            print("  ⚠️ 트랜잭션 롤백!")
            raise

    config: dict[str, int | str] = {"host": "localhost", "port": 8080}
    print("트랜잭션 패턴:")
    print(f"  변경 전: {config}")

    try:
        with transaction(config) as cfg:
            cfg["port"] = 3000
            cfg["debug"] = True  # type: ignore[assignment]
            raise ValueError("설정 오류!")
    except ValueError:
        pass
    print(f"  롤백 후: {config}")

    # 다중 with 문 (Python 3.10+)
    tmp: Path = Path(tempfile.mkdtemp())
    f1: Path = tmp / "a.txt"
    f2: Path = tmp / "b.txt"
    f1.write_text("AAA")
    f2.write_text("BBB")

    with (
        open(f1) as a,
        open(f2) as b,
    ):
        print(f"\n다중 with: {a.read()}, {b.read()}")  # → 다중 with: AAA, BBB

    # 비동기 컨텍스트 매니저 (개념 소개)
    print(f"\n📌 async with (비동기 컨텍스트 매니저):")
    print(f"  __aenter__ / __aexit__ 사용")
    print(f"  → 3_expert/async_await.py에서 상세 다룸")


if __name__ == "__main__":
    demonstrate_with_statement()
    demonstrate_enter_exit()
    demonstrate_contextmanager()
    demonstrate_suppress()
    demonstrate_exitstack()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ _300_context_managers.py 학습 완료!")
    print("=" * 60)
