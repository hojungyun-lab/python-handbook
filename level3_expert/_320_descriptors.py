"""
_320_descriptors.py — 디스크립터 (Descriptors)

이 모듈에서 다루는 내용:
  1. 디스크립터 프로토콜 (__get__, __set__, __delete__)
  2. 데이터 디스크립터 vs 비데이터 디스크립터
  3. property의 내부 구현
  4. __set_name__ (Python 3.6+)
  5. 검증 디스크립터
  6. 디스크립터 실용 패턴

실행 방법:
    poetry run python 3_expert/_320_descriptors.py
"""


def demonstrate_descriptor_protocol() -> None:
    """디스크립터 프로토콜을 보여준다."""
    print("=" * 60)
    print("1. 디스크립터 프로토콜")
    print("=" * 60)

    # 디스크립터 = __get__, __set__, __delete__ 중 하나 이상 정의한 객체

    class Verbose:
        """모든 접근을 로깅하는 디스크립터."""

        def __set_name__(self, owner: type, name: str) -> None:
            self.name: str = name
            self.storage_name: str = f"_desc_{name}"

        def __get__(self, obj: object, objtype: type | None = None) -> object:
            if obj is None:
                return self
            value = getattr(obj, self.storage_name, "미설정")
            print(f"  __get__: {self.name} = {value!r}")
            return value

        def __set__(self, obj: object, value: object) -> None:
            print(f"  __set__: {self.name} = {value!r}")
            setattr(obj, self.storage_name, value)

        def __delete__(self, obj: object) -> None:
            print(f"  __delete__: {self.name}")
            delattr(obj, self.storage_name)

    class MyClass:
        attr: object = Verbose()

    print("디스크립터 동작:")
    m: MyClass = MyClass()
    m.attr = 42       # __set__
    _ = m.attr         # __get__
    del m.attr         # __delete__

    # 클래스에서 접근 시
    print(f"\n클래스 접근: {MyClass.attr}")


def demonstrate_data_vs_nondata() -> None:
    """데이터 vs 비데이터 디스크립터를 보여준다."""
    print("\n" + "=" * 60)
    print("2. 데이터 vs 비데이터 디스크립터")
    print("=" * 60)

    # 비데이터 디스크립터 — __get__만
    class NonDataDescriptor:
        def __get__(self, obj: object, objtype: type | None = None) -> str:
            return "non-data descriptor"

    # 데이터 디스크립터 — __get__ + __set__
    class DataDescriptor:
        def __get__(self, obj: object, objtype: type | None = None) -> str:
            if obj is None:
                return self  # type: ignore[return-value]
            return getattr(obj, "_data_val", "data descriptor default")

        def __set__(self, obj: object, value: str) -> None:
            setattr(obj, "_data_val", value)

    class Demo:
        non_data = NonDataDescriptor()
        data = DataDescriptor()

    d: Demo = Demo()

    # 비데이터: 인스턴스 __dict__가 우선
    print("비데이터 디스크립터:")
    print(f"  d.non_data = {d.non_data!r}")  # →   d.non_data = 'non-data descriptor'
    d.__dict__["non_data"] = "instance value"
    print(f"  인스턴스 dict 추가 후: {d.non_data!r}")  # →   인스턴스 dict 추가 후: 'instance value'
    print(f"  💡 인스턴스 __dict__가 비데이터 디스크립터보다 우선!")

    # 데이터: 디스크립터가 우선
    print(f"\n데이터 디스크립터:")
    print(f"  d.data = {d.data!r}")  # →   d.data = 'data descriptor default'
    d.__dict__["data"] = "should be ignored"
    print(f"  인스턴스 dict 추가 후: {d.data!r}")  # →   인스턴스 dict 추가 후: 'data descriptor default'
    print(f"  💡 데이터 디스크립터가 인스턴스 __dict__보다 우선!")

    # 우선순위
    print(f"\n📌 속성 검색 우선순위:")
    print(f"  1. 데이터 디스크립터 (클래스)")
    print(f"  2. 인스턴스 __dict__")
    print(f"  3. 비데이터 디스크립터 / 클래스 변수")


def demonstrate_property_internals() -> None:
    """property의 내부 구현을 보여준다."""
    print("\n" + "=" * 60)
    print("3. property의 내부 구현")
    print("=" * 60)

    # property는 사실 데이터 디스크립터!
    class Property:
        """property의 간략한 구현."""

        def __init__(
            self,
            fget: callable = None,
            fset: callable = None,
            fdel: callable = None,
            doc: str | None = None,
        ) -> None:
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            self.__doc__ = doc or (fget.__doc__ if fget else None)

        def __get__(self, obj: object, objtype: type | None = None) -> object:
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("읽기 불가")
            return self.fget(obj)

        def __set__(self, obj: object, value: object) -> None:
            if self.fset is None:
                raise AttributeError("쓰기 불가")
            self.fset(obj, value)

        def __delete__(self, obj: object) -> None:
            if self.fdel is None:
                raise AttributeError("삭제 불가")
            self.fdel(obj)

        def setter(self, fset: callable) -> "Property":
            return Property(self.fget, fset, self.fdel, self.__doc__)

        def deleter(self, fdel: callable) -> "Property":
            return Property(self.fget, self.fset, fdel, self.__doc__)

    class Circle:
        def __init__(self, radius: float) -> None:
            self._radius: float = radius

        @Property  # 커스텀 프로퍼티!
        def radius(self) -> float:
            return self._radius

        @radius.setter
        def radius(self, value: float) -> None:
            if value < 0:
                raise ValueError("음수 불가")
            self._radius = value

    c: Circle = Circle(5)
    print(f"커스텀 Property: radius = {c.radius}")  # → 커스텀 Property: radius = 5
    c.radius = 10
    print(f"setter 후: radius = {c.radius}")  # → setter 후: radius = 10
    print(f"💡 @property는 데이터 디스크립터의 문법적 설탕!")


def demonstrate_set_name() -> None:
    """__set_name__을 보여준다."""
    print("\n" + "=" * 60)
    print("4. __set_name__ (Python 3.6+)")
    print("=" * 60)

    class Named:
        """자동으로 속성 이름을 알아내는 디스크립터."""

        def __set_name__(self, owner: type, name: str) -> None:
            self.public_name: str = name
            self.private_name: str = f"_{name}"
            print(f"  __set_name__: owner={owner.__name__}, name={name!r}")

        def __get__(self, obj: object, objtype: type | None = None) -> object:
            if obj is None:
                return self
            return getattr(obj, self.private_name, None)

        def __set__(self, obj: object, value: object) -> None:
            setattr(obj, self.private_name, value)

    print("__set_name__ 호출 시점 (클래스 생성 시):")

    class Config:
        host = Named()
        port = Named()

    cfg: Config = Config()
    cfg.host = "localhost"
    cfg.port = 8080
    print(f"\n  cfg.host = {cfg.host!r}")  # →   cfg.host = 'localhost'
    print(f"  cfg.port = {cfg.port}")  # →   cfg.port = 8080
    print(f"  __dict__ = {cfg.__dict__}")


def demonstrate_validation_descriptor() -> None:
    """검증 디스크립터를 보여준다."""
    print("\n" + "=" * 60)
    print("5. 검증 디스크립터")
    print("=" * 60)

    class Validated:
        """타입과 조건을 검증하는 디스크립터."""

        def __init__(
            self,
            expected_type: type,
            min_value: float | None = None,
            max_value: float | None = None,
        ) -> None:
            self.expected_type: type = expected_type
            self.min_value: float | None = min_value
            self.max_value: float | None = max_value

        def __set_name__(self, owner: type, name: str) -> None:
            self.name: str = name
            self.storage: str = f"_{name}"

        def __get__(self, obj: object, objtype: type | None = None) -> object:
            if obj is None:
                return self
            return getattr(obj, self.storage, None)

        def __set__(self, obj: object, value: object) -> None:
            if not isinstance(value, self.expected_type):
                raise TypeError(
                    f"{self.name}: expected {self.expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
            if self.min_value is not None and value < self.min_value:
                raise ValueError(
                    f"{self.name}: {value} < min({self.min_value})"
                )
            if self.max_value is not None and value > self.max_value:
                raise ValueError(
                    f"{self.name}: {value} > max({self.max_value})"
                )
            setattr(obj, self.storage, value)

    class Product:
        """상품 (검증 디스크립터 사용)."""
        name = Validated(str)
        price = Validated(int | float, min_value=0)
        quantity = Validated(int, min_value=0, max_value=9999)

        def __init__(self, name: str, price: float, quantity: int) -> None:
            self.name = name
            self.price = price
            self.quantity = quantity

        def __repr__(self) -> str:
            return f"Product({self.name!r}, ${self.price}, qty={self.quantity})"

    p: Product = Product("Python Book", 35.99, 100)
    print(f"유효: {p}")  # → 유효: Product('Python Book', $35.99, qty=100)

    errors: list[tuple[str, object, str]] = [
        ("price", -10, "음수 가격"),
        ("quantity", 10000, "최대 초과"),
        ("quantity", "abc", "타입 오류"),
    ]
    print(f"\n검증 실패:")
    for attr, value, msg in errors:
        try:
            setattr(p, attr, value)
        except (TypeError, ValueError) as e:
            print(f"  {msg}: {e}")


def demonstrate_practical_patterns() -> None:
    """디스크립터 실용 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 실용 패턴")
    print("=" * 60)

    # Lazy 속성 (비데이터 디스크립터)
    class Lazy:
        """처음 접근 시에만 계산하는 디스크립터."""

        def __init__(self, func: callable) -> None:
            self.func = func
            self.name: str = func.__name__

        def __get__(self, obj: object, objtype: type | None = None) -> object:
            if obj is None:
                return self
            value = self.func(obj)
            # 인스턴스 __dict__에 저장 → 다음 접근 시 디스크립터 우회
            setattr(obj, self.name, value)
            return value

    class DataSet:
        def __init__(self, data: list[int]) -> None:
            self.data: list[int] = data

        @Lazy
        def statistics(self) -> dict[str, float]:
            print("  [통계 계산 중...]")
            n: int = len(self.data)
            mean: float = sum(self.data) / n
            return {"mean": round(mean, 2), "count": n}

    ds: DataSet = DataSet([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print("Lazy 디스크립터:")
    print(f"  첫 접근: {ds.statistics}")
    print(f"  두 번째: {ds.statistics}")
    print(f"  '계산 중' 메시지가 한 번만 출력!")

    # 캐시된 속성 (functools.cached_property와 유사)
    print(f"\n📌 디스크립터 활용 요약:")
    print(f"  검증:      타입/범위 자동 검증")
    print(f"  지연 로딩:  Lazy 패턴")
    print(f"  로깅:      속성 접근 추적")
    print(f"  변환:      단위 변환, 직렬화")
    print(f"  💡 @property, @classmethod, @staticmethod 모두 디스크립터!")


if __name__ == "__main__":
    demonstrate_descriptor_protocol()
    demonstrate_data_vs_nondata()
    demonstrate_property_internals()
    demonstrate_set_name()
    demonstrate_validation_descriptor()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ _320_descriptors.py 학습 완료!")
    print("=" * 60)
