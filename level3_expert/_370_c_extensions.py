"""
_370_c_extensions.py — C 확장과 FFI (Foreign Function Interface)

이 모듈에서 다루는 내용:
  1. ctypes 기본
  2. struct 모듈 (바이너리 데이터)
  3. array 모듈 (타입화된 배열)
  4. memoryview (메모리 뷰)
  5. buffer protocol
  6. 확장 라이브러리 개요

실행 방법:
    poetry run python 3_expert/_370_c_extensions.py
"""

import array
import ctypes
import struct
import sys


def demonstrate_ctypes() -> None:
    """ctypes 기본을 보여준다."""
    print("=" * 60)
    print("1. ctypes 기본")
    print("=" * 60)

    # C 타입 매핑
    print("ctypes C 타입 매핑:")
    c_types: list[tuple[str, str, int]] = [
        ("c_int", "int", ctypes.sizeof(ctypes.c_int)),
        ("c_long", "long", ctypes.sizeof(ctypes.c_long)),
        ("c_float", "float", ctypes.sizeof(ctypes.c_float)),
        ("c_double", "double", ctypes.sizeof(ctypes.c_double)),
        ("c_char", "char", ctypes.sizeof(ctypes.c_char)),
        ("c_bool", "_Bool", ctypes.sizeof(ctypes.c_bool)),
        ("c_void_p", "void*", ctypes.sizeof(ctypes.c_void_p)),
    ]
    print(f"  {'ctypes':<12} {'C 타입':<10} {'크기 (bytes)':>12}")
    for name, c_type, size in c_types:
        print(f"  {name:<12} {c_type:<10} {size:>12}")

    # c_int 사용
    x: ctypes.c_int = ctypes.c_int(42)
    print(f"\nc_int(42):")
    print(f"  value = {x.value}")  # →   value = 42
    print(f"  sizeof = {ctypes.sizeof(x)}")  # →   sizeof = 4

    # 포인터
    p: ctypes.pointer = ctypes.pointer(x)
    print(f"\npointer:")
    print(f"  *p = {p.contents.value}")  # →   *p = 42
    p.contents.value = 100
    print(f"  *p = {p.contents.value}")  # →   *p = 100

    # Structure
    class Point(ctypes.Structure):
        _fields_: list[tuple[str, type]] = [
            ("x", ctypes.c_double),
            ("y", ctypes.c_double),
        ]

    pt: Point = Point(3.0, 4.0)
    print(f"\nStructure:")
    print(f"  Point({pt.x}, {pt.y})")  # →   Point(3.0, 4.0)
    print(f"  sizeof = {ctypes.sizeof(pt)}")  # →   sizeof = 16

    # 시스템 라이브러리 로드 (macOS)
    if sys.platform == "darwin":
        libc = ctypes.CDLL("libSystem.B.dylib")
        print(f"\nlibc.time(None) = {libc.time(None)}")


def demonstrate_struct() -> None:
    """struct 모듈을 보여준다."""
    print("\n" + "=" * 60)
    print("2. struct 모듈 (바이너리 데이터)")
    print("=" * 60)

    # pack — Python → 바이너리
    packed: bytes = struct.pack("!ifd", 42, 3.14, 2.718)
    print(f"pack('!ifd', 42, 3.14, 2.718):")
    print(f"  bytes = {packed.hex()}")
    print(f"  크기 = {len(packed)} bytes")

    # unpack — 바이너리 → Python
    values: tuple = struct.unpack("!ifd", packed)
    print(f"\nunpack: {values}")  # → unpack: (42, 3.140000104904175, 2.718)

    # 포맷 코드
    print(f"\n포맷 코드:")
    codes: list[tuple[str, str, int]] = [
        ("b/B", "signed/unsigned byte", 1),
        ("h/H", "short (2 bytes)", 2),
        ("i/I", "int (4 bytes)", 4),
        ("q/Q", "long long (8 bytes)", 8),
        ("f", "float (4 bytes)", 4),
        ("d", "double (8 bytes)", 8),
        ("?", "bool (1 byte)", 1),
        ("s", "bytes (n bytes)", -1),
    ]
    for code, desc, size in codes:
        size_str: str = str(size) if size > 0 else "가변"
        print(f"  {code:<5} {desc:<25} {size_str}")

    # 바이트 순서
    print(f"\n바이트 순서 접두어:")
    print(f"  !  네트워크 (빅 엔디언)")
    print(f"  <  리틀 엔디언")
    print(f"  >  빅 엔디언")
    print(f"  =  네이티브")

    # 실용: 네트워크 패킷 시뮬레이션
    header_fmt: str = "!BBH"  # version(1), type(1), length(2)
    header: bytes = struct.pack(header_fmt, 1, 3, 1024)
    ver, msg_type, length = struct.unpack(header_fmt, header)
    print(f"\n네트워크 헤더:")
    print(f"  version={ver}, type={msg_type}, length={length}")  # →   version=1, type=3, length=1024

    # calcsize
    print(f"  header 크기: {struct.calcsize(header_fmt)} bytes")  # →   header 크기: 4 bytes

    # 이미지 헤더 읽기 (BMP 시뮬레이션)
    bmp_header: bytes = struct.pack("<2sIHHI", b"BM", 1024, 0, 0, 54)
    sig, size, _, _, offset = struct.unpack("<2sIHHI", bmp_header)
    print(f"\nBMP 헤더:")
    print(f"  시그니처={sig}, 크기={size}, 오프셋={offset}")  # →   시그니처=b'BM', 크기=1024, 오프셋=54


def demonstrate_array_module() -> None:
    """array 모듈을 보여준다."""
    print("\n" + "=" * 60)
    print("3. array 모듈 (타입화된 배열)")
    print("=" * 60)

    # array vs list (메모리)
    py_list: list[int] = list(range(10_000))
    c_array: array.array[int] = array.array("i", range(10_000))

    list_size: int = sys.getsizeof(py_list) + sum(
        sys.getsizeof(x) for x in py_list[:100]
    ) * 100
    array_size: int = sys.getsizeof(c_array)

    print(f"10,000개 정수:")
    print(f"  list:  ~{list_size:,} bytes")
    print(f"  array: ~{array_size:,} bytes")
    print(f"  절약: ~{(list_size-array_size)/list_size*100:.0f}%")

    # 타입 코드
    print(f"\narray 타입 코드:")
    type_codes: list[tuple[str, str, int]] = [
        ("b", "signed char", 1),
        ("B", "unsigned char", 1),
        ("h", "signed short", 2),
        ("H", "unsigned short", 2),
        ("i", "signed int", 4),
        ("I", "unsigned int", 4),
        ("f", "float", 4),
        ("d", "double", 8),
    ]
    for code, desc, size in type_codes:
        print(f"  {code}  {desc:<16}  {size} byte(s)")

    # 기본 연산
    arr: array.array[float] = array.array("d", [1.0, 2.0, 3.0])
    arr.append(4.0)
    arr.extend([5.0, 6.0])
    print(f"\n연산: {arr}")

    # 바이너리 변환
    raw: bytes = arr.tobytes()
    print(f"tobytes: {len(raw)} bytes")  # → tobytes: 48 bytes

    restored: array.array[float] = array.array("d")
    restored.frombytes(raw)
    print(f"frombytes: {restored}")


def demonstrate_memoryview() -> None:
    """memoryview를 보여준다."""
    print("\n" + "=" * 60)
    print("4. memoryview (메모리 뷰)")
    print("=" * 60)

    # 복사 없이 데이터 접근
    data: bytearray = bytearray(b"Hello, World!")
    view: memoryview = memoryview(data)

    print(f"원본: {data}")
    print(f"뷰 [0:5]: {bytes(view[0:5])}")

    # 뷰를 통한 수정 (원본도 변경!)
    view[0:5] = b"HELLO"
    print(f"수정 후 원본: {data}")

    # 슬라이싱 (복사 없음!)
    large: bytearray = bytearray(1_000_000)
    chunk: memoryview = memoryview(large)[100:200]
    print(f"\n대용량 슬라이스:")
    print(f"  원본: {len(large):,} bytes")
    print(f"  뷰:   {len(chunk)} bytes (복사 없음!)")

    # array와 함께
    arr: array.array[int] = array.array("i", [1, 2, 3, 4, 5])
    mv: memoryview = memoryview(arr)
    print(f"\narray memoryview:")
    print(f"  format: {mv.format}")
    print(f"  itemsize: {mv.itemsize}")
    print(f"  shape: {mv.shape}")
    print(f"  리스트 변환: {mv.tolist()}")  # →   리스트 변환: [1, 2, 3, 4, 5]

    # struct와 조합
    header_data: bytes = struct.pack("!HH4s", 1, 1024, b"DATA")
    mv_header: memoryview = memoryview(header_data)
    version: int = struct.unpack("!H", mv_header[0:2])[0]
    print(f"\nstruct + memoryview:")
    print(f"  version: {version}")


def demonstrate_buffer_protocol() -> None:
    """buffer protocol을 보여준다."""
    print("\n" + "=" * 60)
    print("5. Buffer Protocol")
    print("=" * 60)

    # Buffer Protocol 지원 타입
    buffer_types: list[tuple[str, object]] = [
        ("bytes", b"hello"),
        ("bytearray", bytearray(b"hello")),
        ("array.array", array.array("i", [1, 2, 3])),
        ("memoryview", memoryview(b"hello")),
    ]

    print("Buffer Protocol 지원 타입:")
    for name, obj in buffer_types:
        mv: memoryview = memoryview(obj)
        print(f"  {name:<15} format={mv.format!r:>4}  "
              f"itemsize={mv.itemsize}  readonly={mv.readonly}")

    # 커스텀 Buffer Protocol (Python 3.12+)
    print(f"\nPython 3.12+ __buffer__ 프로토콜:")
    print(f"  class MyBuffer:")
    print(f"      def __buffer__(self, flags):")
    print(f"          return memoryview(self._data)")

    # 바이너리 파일 I/O
    import tempfile
    from pathlib import Path

    tmp: Path = Path(tempfile.mkdtemp()) / "binary.dat"

    # 바이너리 쓰기
    arr: array.array[int] = array.array("i", [100, 200, 300, 400])
    with open(tmp, "wb") as f:
        f.write(arr.tobytes())

    # 바이너리 읽기
    read_arr: array.array[int] = array.array("i")
    with open(tmp, "rb") as f:
        raw: bytes = f.read()
        read_arr.frombytes(raw)

    print(f"\n바이너리 I/O:")
    print(f"  쓰기: {arr}")
    print(f"  읽기: {read_arr}")


def demonstrate_extension_overview() -> None:
    """확장 라이브러리 개요를 보여준다."""
    print("\n" + "=" * 60)
    print("6. 확장 라이브러리 개요")
    print("=" * 60)

    print(f"📌 Python 확장 도구:")
    print(f"")
    print(f"  {'도구':<18} {'언어':<8} {'특징'}")
    print(f"  {'-'*18} {'-'*8} {'-'*35}")
    print(f"  {'ctypes':<18} {'C':<8} 표준 라이브러리, DLL/SO 호출")
    print(f"  {'cffi':<18} {'C':<8} ctypes 대안, 외부 라이브러리")
    print(f"  {'Cython':<18} {'C/Python':<8} Python 문법으로 C 속도")
    print(f"  {'pybind11':<18} {'C++':<8} C++ 바인딩, 현대적")
    print(f"  {'PyO3/maturin':<18} {'Rust':<8} Rust 바인딩, 안전성")
    print(f"  {'SWIG':<18} {'다양':<8} 범용, 레거시")
    print(f"  {'numpy C API':<18} {'C':<8} NumPy 확장 전용")
    print(f"")
    print(f"  💡 성능 필요 시: numpy → Cython → PyO3")
    print(f"  💡 기존 C 라이브러리: ctypes/cffi")
    print(f"  💡 새 확장: PyO3 (Rust) 권장")


if __name__ == "__main__":
    demonstrate_ctypes()
    demonstrate_struct()
    demonstrate_array_module()
    demonstrate_memoryview()
    demonstrate_buffer_protocol()
    demonstrate_extension_overview()

    print("\n" + "=" * 60)
    print("✅ _370_c_extensions.py 학습 완료!")
    print("=" * 60)
