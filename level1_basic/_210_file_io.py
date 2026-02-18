"""
_210_file_io.py — 파일 입출력 (File I/O)

이 모듈에서 다루는 내용:
  1. 파일 열기와 닫기 (with 문)
  2. 텍스트 파일 읽기/쓰기
  3. pathlib.Path (현대적 파일 경로 처리)
  4. CSV 파일 처리
  5. JSON 파일 처리
  6. 바이너리 파일 기초
  7. 실용적인 파일 패턴

실행 방법:
    poetry run python 1_basic/_210_file_io.py
"""

import csv
import json
import tempfile
from pathlib import Path


def demonstrate_with_statement() -> None:
    """with 문을 이용한 파일 열기/닫기를 보여준다."""
    print("=" * 60)
    print("1. 파일 열기/닫기 (with 문)")
    print("=" * 60)

    # 임시 디렉토리에서 작업
    tmp: Path = Path(tempfile.mkdtemp())
    filepath: Path = tmp / "example.txt"

    # ✅ 권장: with 문 (자동으로 close)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Hello, Python!\n")
        f.write("파일 입출력 학습\n")
    print(f"✅ with 문으로 파일 작성: {filepath.name}")

    # 파일 모드
    print(f"\n파일 모드:")
    print(f"  'r'  — 읽기 (기본값)")
    print(f"  'w'  — 쓰기 (덮어쓰기)")
    print(f"  'a'  — 추가 (append)")
    print(f"  'x'  — 배타적 생성 (이미 있으면 에러)")
    print(f"  'b'  — 바이너리 모드 (rb, wb)")
    print(f"  '+'  — 읽기+쓰기 (r+, w+)")

    # ❌ 비권장: 수동 close (예외 시 닫히지 않을 수 있음)
    # f = open(filepath, 'r')
    # data = f.read()
    # f.close()


def demonstrate_text_read_write() -> None:
    """텍스트 파일 읽기/쓰기를 보여준다."""
    print("\n" + "=" * 60)
    print("2. 텍스트 파일 읽기/쓰기")
    print("=" * 60)

    tmp: Path = Path(tempfile.mkdtemp())
    filepath: Path = tmp / "sample.txt"

    # 쓰기
    lines: list[str] = [
        "첫 번째 줄\n",
        "두 번째 줄\n",
        "세 번째 줄\n",
        "네 번째 줄\n",
        "다섯 번째 줄\n",
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"5줄 작성 완료")

    # 전체 읽기: read()
    with open(filepath, encoding="utf-8") as f:
        content: str = f.read()
    print(f"\nread() 전체 읽기:")
    print(f"  {content!r}")

    # 줄 단위 읽기: readlines()
    with open(filepath, encoding="utf-8") as f:
        all_lines: list[str] = f.readlines()
    print(f"readlines(): {all_lines}")

    # 한 줄씩 읽기 (메모리 효율적)
    print(f"\n한 줄씩 순회 (권장):")
    with open(filepath, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            print(f"  {i}: {line.rstrip()}")

    # readline()
    with open(filepath, encoding="utf-8") as f:
        first: str = f.readline()
        second: str = f.readline()
    print(f"\nreadline(): 첫째={first.rstrip()!r}, 둘째={second.rstrip()!r}")

    # 추가 모드 (append)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("추가된 줄\n")
    print(f"\nappend 후:")
    with open(filepath, encoding="utf-8") as f:
        print(f"  총 줄 수: {len(f.readlines())}")

    # print()로 파일 쓰기
    output_path: Path = tmp / "print_output.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        print("print()로 씁니다", file=f)
        print(f"값: {42}", file=f)
    with open(output_path, encoding="utf-8") as f:
        print(f"\nprint() → 파일:\n  {f.read().rstrip()}")


def demonstrate_pathlib() -> None:
    """pathlib.Path를 보여준다."""
    print("\n" + "=" * 60)
    print("3. pathlib.Path (현대적 파일 경로)")
    print("=" * 60)

    # Path 생성
    current: Path = Path(".")
    home: Path = Path.home()
    cwd: Path = Path.cwd()

    print(f"현재 디렉토리: {cwd}")
    print(f"홈 디렉토리: {home}")

    # 경로 조합 (/ 연산자)
    filepath: Path = Path("/usr") / "local" / "bin" / "python3"
    print(f"\n경로 조합: {filepath}")  # → 경로 조합: /usr/local/bin/python3

    # 경로 분해
    sample: Path = Path("/home/user/documents/report.tar.gz")
    print(f"\n경로 분해:")
    print(f"  name:     {sample.name}")  # →   name:     report.tar.gz
    print(f"  stem:     {sample.stem}")  # →   stem:     report.tar
    print(f"  suffix:   {sample.suffix}")  # →   suffix:   .gz
    print(f"  suffixes: {sample.suffixes}")  # →   suffixes: ['.tar', '.gz']
    print(f"  parent:   {sample.parent}")  # →   parent:   /home/user/documents
    print(f"  parts:    {sample.parts}")  # →   parts:    ('/', 'home', 'user', 'documents', 'report.tar.gz')

    # 파일 읽기/쓰기 (간편 메서드)
    tmp: Path = Path(tempfile.mkdtemp())
    text_file: Path = tmp / "pathlib_demo.txt"
    text_file.write_text("Path로 쓰기!", encoding="utf-8")
    content: str = text_file.read_text(encoding="utf-8")
    print(f"\nPath.write_text / read_text: {content!r}")

    # 파일 정보
    print(f"\n파일 정보:")
    print(f"  exists: {text_file.exists()}")
    print(f"  is_file: {text_file.is_file()}")
    print(f"  is_dir: {text_file.is_dir()}")
    print(f"  stat().st_size: {text_file.stat().st_size} bytes")

    # 디렉토리 순회
    print(f"\n현재 디렉토리 .py 파일:")
    py_files: list[Path] = sorted(Path(".").glob("**/*.py"))
    for p in py_files[:5]:
        print(f"  {p}")
    if len(py_files) > 5:
        print(f"  ... 외 {len(py_files) - 5}개")

    # 유용한 메서드들
    print(f"\n유용한 Path 메서드:")
    print(f"  .resolve()   — 절대 경로로 변환")
    print(f"  .glob('*')   — 패턴 매칭")
    print(f"  .rglob('*')  — 재귀 패턴 매칭")
    print(f"  .mkdir()     — 디렉토리 생성")
    print(f"  .rename()    — 이름 변경")
    print(f"  .unlink()    — 파일 삭제")
    print(f"  .with_suffix('.txt') — 확장자 변경")


def demonstrate_csv() -> None:
    """CSV 파일 처리를 보여준다."""
    print("\n" + "=" * 60)
    print("4. CSV 파일 처리")
    print("=" * 60)

    tmp: Path = Path(tempfile.mkdtemp())
    csv_path: Path = tmp / "data.csv"

    # CSV 쓰기
    header: list[str] = ["이름", "나이", "도시"]
    rows: list[list[str | int]] = [
        ["Alice", 30, "Seoul"],
        ["Bob", 25, "Busan"],
        ["Charlie", 35, "Incheon"],
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer: csv.writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"CSV 작성 완료")

    # CSV 읽기
    print(f"\ncsv.reader:")
    with open(csv_path, encoding="utf-8") as f:
        reader: csv.reader = csv.reader(f)
        for row in reader:
            print(f"  {row}")

    # DictReader / DictWriter
    print(f"\ncsv.DictReader:")
    with open(csv_path, encoding="utf-8") as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            print(f"  {dict(row)}")

    # DictWriter 예시
    dict_csv_path: Path = tmp / "dict_data.csv"
    people: list[dict[str, str | int]] = [
        {"name": "Diana", "age": 28, "role": "Dev"},
        {"name": "Eve", "age": 32, "role": "PM"},
    ]
    with open(dict_csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames: list[str] = ["name", "age", "role"]
        writer_d = csv.DictWriter(f, fieldnames=fieldnames)
        writer_d.writeheader()
        writer_d.writerows(people)

    print(f"\nDictWriter 결과:")
    print(f"  {dict_csv_path.read_text(encoding='utf-8').rstrip()}")


def demonstrate_json() -> None:
    """JSON 파일 처리를 보여준다."""
    print("\n" + "=" * 60)
    print("5. JSON 파일 처리")
    print("=" * 60)

    tmp: Path = Path(tempfile.mkdtemp())
    json_path: Path = tmp / "data.json"

    # Python 객체 → JSON 문자열
    data: dict[str, str | int | list[str] | dict[str, str]] = {
        "name": "Python",
        "version": 313,
        "features": ["dynamic", "interpreted", "object-oriented"],
        "creator": {"name": "Guido van Rossum", "country": "Netherlands"},
    }

    # JSON 파일 쓰기
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON 파일 작성 완료")

    # JSON 파일 읽기
    with open(json_path, encoding="utf-8") as f:
        loaded: dict = json.load(f)
    print(f"\njson.load():")
    print(f"  name: {loaded['name']}")  # →   name: Python
    print(f"  features: {loaded['features']}")  # →   features: ['dynamic', 'interpreted', 'object-oriented']

    # 문자열 변환
    json_str: str = json.dumps(data, ensure_ascii=False, indent=2)
    print(f"\njson.dumps() (문자열):")
    print(f"  {json_str[:80]}...")

    # JSON → Python 타입 매핑
    print(f"\nJSON ↔ Python 타입 매핑:")
    print(f"  object  → dict")
    print(f"  array   → list")
    print(f"  string  → str")
    print(f"  number  → int / float")
    print(f"  true    → True")
    print(f"  false   → False")
    print(f"  null    → None")

    # 문자열 파싱
    json_text: str = '{"key": "value", "number": 42}'
    parsed: dict[str, str | int] = json.loads(json_text)
    print(f"\njson.loads(): {parsed}")  # → json.loads(): {'key': 'value', 'number': 42}


def demonstrate_binary_files() -> None:
    """바이너리 파일 기초를 보여준다."""
    print("\n" + "=" * 60)
    print("6. 바이너리 파일 기초")
    print("=" * 60)

    tmp: Path = Path(tempfile.mkdtemp())
    bin_path: Path = tmp / "data.bin"

    # 바이너리 쓰기
    data: bytes = b"\x48\x65\x6c\x6c\x6f"  # "Hello"
    with open(bin_path, "wb") as f:
        f.write(data)
        f.write(b"\x00\xFF")

    # 바이너리 읽기
    with open(bin_path, "rb") as f:
        content: bytes = f.read()
    print(f"바이너리 읽기: {content}")
    print(f"  hex: {content.hex()}")  # →   hex: 48656c6c6f00ff
    print(f"  텍스트 부분: {content[:5].decode('ascii')}")  # →   텍스트 부분: Hello

    # 텍스트 vs 바이너리 모드
    print(f"\n텍스트 모드 vs 바이너리 모드:")
    print(f"  텍스트: 줄바꿈 자동 변환, 인코딩 처리")
    print(f"  바이너리: 원시 바이트 그대로 처리")


def demonstrate_practical_patterns() -> None:
    """실용적인 파일 처리 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("7. 실용적인 파일 패턴")
    print("=" * 60)

    tmp: Path = Path(tempfile.mkdtemp())

    # 파일 존재 확인 후 처리
    config_path: Path = tmp / "config.json"
    if not config_path.exists():
        default_config: dict[str, str | int | bool] = {
            "debug": False, "port": 8080, "host": "localhost"
        }
        config_path.write_text(
            json.dumps(default_config, indent=2), encoding="utf-8"
        )
        print(f"기본 설정 파일 생성")

    # 안전한 파일 쓰기 (임시 파일 → 리네임)
    import os
    safe_path: Path = tmp / "important.txt"
    temp_path: Path = tmp / "important.txt.tmp"
    temp_path.write_text("중요 데이터", encoding="utf-8")
    os.replace(str(temp_path), str(safe_path))
    print(f"안전한 쓰기 (atomic replace) 완료")

    # 줄 단위 처리 (대용량 파일에 적합)
    large_file: Path = tmp / "large.txt"
    with open(large_file, "w", encoding="utf-8") as f:
        for i in range(100):
            f.write(f"Line {i:03d}: data\n")

    # 조건에 맞는 줄 찾기
    matches: list[str] = []
    with open(large_file, encoding="utf-8") as f:
        for line in f:
            if "05" in line:
                matches.append(line.rstrip())

    print(f"\n줄 검색 결과: {matches[:3]}...")

    # 여러 파일 동시 열기
    source: Path = tmp / "source.txt"
    dest: Path = tmp / "dest.txt"
    source.write_text("원본 데이터\n입니다!", encoding="utf-8")

    with (
        open(source, encoding="utf-8") as src,
        open(dest, "w", encoding="utf-8") as dst,
    ):
        for line in src:
            dst.write(line.upper())

    result: str = dest.read_text(encoding="utf-8")
    print(f"\n동시 열기 (대문자 변환): {result.rstrip()!r}")

    # tempfile 모듈 활용
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as tmp_f:
        tmp_f.write("임시 데이터")
        print(f"\n임시 파일: {tmp_f.name}")

    print(f"\n📌 파일 I/O 모범 사례:")
    print(f"  ✅ 항상 with 문 사용")
    print(f"  ✅ encoding='utf-8' 명시")
    print(f"  ✅ pathlib.Path 사용 권장")
    print(f"  ✅ 대용량 파일은 줄 단위 처리")
    print(f"  ❌ 수동 f.close() 사용 금지")


if __name__ == "__main__":
    demonstrate_with_statement()
    demonstrate_text_read_write()
    demonstrate_pathlib()
    demonstrate_csv()
    demonstrate_json()
    demonstrate_binary_files()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ _210_file_io.py 학습 완료!")
    print("=" * 60)
