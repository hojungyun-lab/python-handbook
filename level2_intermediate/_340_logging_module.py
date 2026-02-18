"""
_340_logging_module.py — logging 모듈

이 모듈에서 다루는 내용:
  1. logging 기본
  2. 로그 레벨
  3. 핸들러와 포맷터
  4. 로거 계층
  5. 파일 로깅
  6. logging.config 설정

실행 방법:
    poetry run python 2_intermediate/_340_logging_module.py
"""

import logging
import logging.config
import sys
import tempfile
from pathlib import Path


def demonstrate_logging_basics() -> None:
    """logging 기본을 보여준다."""
    print("=" * 60)
    print("1. logging 기본")
    print("=" * 60)

    # 모듈 수준 로깅 (비권장 — 루트 로거 사용)
    # logging.warning("루트 로거 경고!")  # 이렇게 쓰지 마세요

    # 올바른 방법: 모듈별 로거 생성
    logger: logging.Logger = logging.getLogger(__name__)

    print(f"로거 이름: {logger.name!r}")  # → 로거 이름: '__main__'
    print(f"유효 레벨: {logger.getEffectiveLevel()}")  # → 유효 레벨: 30
    print(f"  (WARNING = {logging.WARNING})")  # →   (WARNING = 30)

    # print vs logging
    print(f"\n📌 print vs logging:")
    print(f"  print:   개발 디버깅용, 제거 필요")
    print(f"  logging: 프로덕션용, 레벨 제어 가능")
    print(f"  💡 프로덕션 코드에서는 항상 logging 사용!")


def demonstrate_log_levels() -> None:
    """로그 레벨을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 로그 레벨")
    print("=" * 60)

    levels: list[tuple[str, int, str]] = [
        ("DEBUG", logging.DEBUG, "상세 디버깅 정보"),
        ("INFO", logging.INFO, "일반 정보"),
        ("WARNING", logging.WARNING, "잠재적 문제 (기본)"),
        ("ERROR", logging.ERROR, "에러 발생"),
        ("CRITICAL", logging.CRITICAL, "심각한 에러"),
    ]

    print(f"{'레벨':<10} {'값':>3}  설명")
    print(f"{'-'*10} {'-'*3}  {'-'*20}")
    for name, value, desc in levels:
        print(f"{name:<10} {value:>3}  {desc}")

    # 레벨 필터링 동작
    logger: logging.Logger = logging.getLogger("demo.levels")
    logger.setLevel(logging.DEBUG)

    # 콘솔 핸들러 추가
    handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter: logging.Formatter = logging.Formatter(
        "  %(levelname)-8s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False  # 루트 로거로 전파 방지

    print(f"\n모든 레벨 출력:")
    logger.debug("디버깅 정보")
    logger.info("일반 정보")
    logger.warning("경고!")
    logger.error("에러 발생!")
    logger.critical("심각한 에러!")

    # 핸들러 정리
    logger.removeHandler(handler)


def demonstrate_handlers_formatters() -> None:
    """핸들러와 포맷터를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 핸들러와 포맷터")
    print("=" * 60)

    logger: logging.Logger = logging.getLogger("demo.handlers")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # 커스텀 포맷터
    detailed_fmt: logging.Formatter = logging.Formatter(
        "  %(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    simple_fmt: logging.Formatter = logging.Formatter(
        "  %(levelname)s: %(message)s"
    )

    # 콘솔 핸들러 (WARNING 이상)
    console: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.WARNING)
    console.setFormatter(simple_fmt)
    logger.addHandler(console)

    # 파일 핸들러 (DEBUG 이상)
    tmp_log: Path = Path(tempfile.mkdtemp()) / "app.log"
    file_handler: logging.FileHandler = logging.FileHandler(tmp_log)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_fmt)
    logger.addHandler(file_handler)

    print("핸들러별 출력 (콘솔=WARNING+, 파일=DEBUG+):")
    logger.debug("디버깅 (파일만)")
    logger.info("정보 (파일만)")
    logger.warning("경고 (둘 다)")
    logger.error("에러 (둘 다)")

    # 파일 내용 확인
    print(f"\n파일 로그 내용:")
    for line in tmp_log.read_text().splitlines():
        print(f"  📄 {line}")

    # 핸들러 정리
    logger.removeHandler(console)
    logger.removeHandler(file_handler)
    file_handler.close()

    # 주요 핸들러 타입
    print(f"\n📌 주요 핸들러:")
    print(f"  StreamHandler:        콘솔/스트림 출력")
    print(f"  FileHandler:          파일 출력")
    print(f"  RotatingFileHandler:  크기 기반 로테이션")
    print(f"  TimedRotatingFileHandler: 시간 기반 로테이션")
    print(f"  SMTPHandler:          이메일 전송")
    print(f"  SocketHandler:        네트워크 전송")


def demonstrate_logger_hierarchy() -> None:
    """로거 계층을 보여준다."""
    print("\n" + "=" * 60)
    print("4. 로거 계층")
    print("=" * 60)

    # 로거 이름은 점(.)으로 계층 구조를 형성
    root: logging.Logger = logging.getLogger()
    parent: logging.Logger = logging.getLogger("myapp")
    child: logging.Logger = logging.getLogger("myapp.db")
    grandchild: logging.Logger = logging.getLogger("myapp.db.query")

    print(f"로거 계층:")
    print(f"  root → {root.name!r}")
    print(f"    └─ myapp → {parent.name!r}")
    print(f"        └─ myapp.db → {child.name!r}")
    print(f"            └─ myapp.db.query → {grandchild.name!r}")

    # 전파 (propagation)
    print(f"\n전파 (propagate):")
    print(f"  자식 로거가 처리하지 못한 메시지는 부모로 전파")
    print(f"  propagate=False로 전파 중단 가능")
    print(f"  💡 __name__으로 로거 생성 → 자동 계층화")


def demonstrate_structured_logging() -> None:
    """구조화된 로깅을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 구조화된 로깅")
    print("=" * 60)

    logger: logging.Logger = logging.getLogger("demo.structured")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("  %(message)s"))
    logger.addHandler(handler)

    # 예외 로깅 — exc_info
    print("예외 로깅:")
    try:
        result: float = 1 / 0
    except ZeroDivisionError:
        logger.error("계산 오류", exc_info=True)

    # 추가 데이터
    print(f"\nextra 데이터:")
    extra_fmt: logging.Formatter = logging.Formatter(
        "  %(levelname)s: %(message)s [%(user)s]"
    )
    handler.setFormatter(extra_fmt)
    logger.info("로그인 성공", extra={"user": "alice"})
    logger.warning("권한 부족", extra={"user": "bob"})

    # 핸들러 정리
    logger.removeHandler(handler)


def demonstrate_dict_config() -> None:
    """dictConfig 설정을 보여준다."""
    print("\n" + "=" * 60)
    print("6. dictConfig 설정")
    print("=" * 60)

    config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "  %(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "brief": {
                "format": "  %(levelname)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "brief",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "demo.config": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(config)
    logger: logging.Logger = logging.getLogger("demo.config")

    print("dictConfig 로거:")
    logger.debug("보이지 않음 (핸들러 레벨=INFO)")
    logger.info("정보 메시지")
    logger.warning("경고 메시지")
    logger.error("에러 메시지")

    print(f"\n📌 로깅 모범 사례:")
    print(f"  ✅ __name__으로 로거 생성")
    print(f"  ✅ 루트 로거 직접 사용 금지")
    print(f"  ✅ 적절한 로그 레벨 사용")
    print(f"  ✅ 프로덕션: dictConfig/fileConfig 사용")
    print(f"  ✅ 예외: logger.exception() 또는 exc_info=True")
    print(f"  ❌ print() 디버깅 → logging.debug() 사용")


if __name__ == "__main__":
    demonstrate_logging_basics()
    demonstrate_log_levels()
    demonstrate_handlers_formatters()
    demonstrate_logger_hierarchy()
    demonstrate_structured_logging()
    demonstrate_dict_config()

    print("\n" + "=" * 60)
    print("✅ _340_logging_module.py 학습 완료!")
    print("=" * 60)
