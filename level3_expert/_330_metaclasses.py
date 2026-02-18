"""
_330_metaclasses.py — 메타클래스 (Metaclasses)

이 모듈에서 다루는 내용:
  1. type()으로 클래스 생성
  2. 메타클래스 프로토콜 (__new__, __init__)
  3. __init_subclass__ (간단한 대안)
  4. __class_getitem__
  5. 메타클래스 실용 패턴 (싱글턴, 레지스트리)
  6. 메타클래스 vs 대안

실행 방법:
    poetry run python 3_expert/_330_metaclasses.py
"""


def demonstrate_type_as_metaclass() -> None:
    """type()으로 클래스를 생성한다."""
    print("=" * 60)
    print("1. type()으로 클래스 생성")
    print("=" * 60)

    # 일반적인 클래스 정의
    class Dog:
        sound: str = "Woof"

        def speak(self) -> str:
            return self.sound

    # type()으로 동일한 클래스 생성
    def speak(self) -> str:
        return self.sound

    DogDynamic = type("DogDynamic", (), {"sound": "Woof", "speak": speak})

    d1: Dog = Dog()
    d2 = DogDynamic()
    print(f"class Dog:     {d1.speak()} (type: {type(d1).__name__})")  # → class Dog:     Woof (type: Dog)
    print(f"type('Dog'):   {d2.speak()} (type: {type(d2).__name__})")  # → type('Dog'):   Woof (type: DogDynamic)

    # 메타클래스 체인
    print(f"\n메타클래스 체인:")
    print(f"  type(Dog)       = {type(Dog)}")       # →   type(Dog)       = <class 'type'>
    print(f"  type(type)      = {type(type)}")       # →   type(type)      = <class 'type'>
    print(f"  isinstance(Dog, type) = {isinstance(Dog, type)}")  # →   isinstance(Dog, type) = True

    # 상속 포함
    CatDynamic = type("CatDynamic", (DogDynamic,), {"sound": "Meow"})
    c = CatDynamic()
    print(f"\n상속: {c.speak()} (bases: {CatDynamic.__bases__})")


def demonstrate_metaclass_protocol() -> None:
    """메타클래스 프로토콜을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 메타클래스 프로토콜")
    print("=" * 60)

    class Meta(type):
        """커스텀 메타클래스."""

        def __new__(
            mcs,
            name: str,
            bases: tuple[type, ...],
            namespace: dict[str, object],
            **kwargs: object,
        ) -> type:
            print(f"  Meta.__new__: 클래스 '{name}' 생성")
            cls = super().__new__(mcs, name, bases, namespace, **kwargs)
            return cls

        def __init__(
            cls,
            name: str,
            bases: tuple[type, ...],
            namespace: dict[str, object],
            **kwargs: object,
        ) -> None:
            print(f"  Meta.__init__: 클래스 '{name}' 초기화")
            super().__init__(name, bases, namespace, **kwargs)

        def __call__(cls, *args: object, **kwargs: object) -> object:
            print(f"  Meta.__call__: '{cls.__name__}' 인스턴스 생성")
            instance = super().__call__(*args, **kwargs)
            return instance

    print("메타클래스 동작 추적:")

    class MyClass(metaclass=Meta):
        def __init__(self, value: int) -> None:
            self.value: int = value

    print(f"\n인스턴스 생성:")
    obj: MyClass = MyClass(42)
    print(f"  obj.value = {obj.value}")  # →   obj.value = 42

    # 호출 순서
    print(f"\n📌 클래스 생성 순서:")
    print(f"  1. Meta.__new__  → cls 객체 생성")
    print(f"  2. Meta.__init__ → cls 초기화")
    print(f"  인스턴스 생성 순서:")
    print(f"  3. Meta.__call__ → cls() 호출 시")
    print(f"     → cls.__new__ → 인스턴스 생성")
    print(f"     → cls.__init__ → 인스턴스 초기화")


def demonstrate_init_subclass() -> None:
    """__init_subclass__를 보여준다."""
    print("\n" + "=" * 60)
    print("3. __init_subclass__ (메타클래스 대안)")
    print("=" * 60)

    # __init_subclass__ — 서브클래스 생성 훅
    class Plugin:
        """플러그인 기본 클래스."""

        _registry: dict[str, type] = {}

        def __init_subclass__(cls, *, plugin_name: str = "", **kwargs: object) -> None:
            super().__init_subclass__(**kwargs)
            name: str = plugin_name or cls.__name__.lower()
            Plugin._registry[name] = cls
            print(f"  등록됨: {name!r} → {cls.__name__}")

    class JSONPlugin(Plugin, plugin_name="json"):
        def process(self) -> str:
            return "JSON 처리"

    class XMLPlugin(Plugin, plugin_name="xml"):
        def process(self) -> str:
            return "XML 처리"

    class CSVPlugin(Plugin):  # plugin_name 생략 → 클래스명 사용
        def process(self) -> str:
            return "CSV 처리"

    print(f"\n등록된 플러그인: {list(Plugin._registry.keys())}")  # → 등록된 플러그인: ['json', 'xml', 'csvplugin']

    # 팩토리
    for name, cls in Plugin._registry.items():
        instance = cls()
        print(f"  {name}: {instance.process()}")

    print(f"\n📌 __init_subclass__ vs 메타클래스:")
    print(f"  __init_subclass__: 간단, 키워드 인수 지원")
    print(f"  메타클래스:        더 강력, 클래스 생성 자체를 제어")
    print(f"  💡 대부분의 경우 __init_subclass__로 충분!")


def demonstrate_class_getitem() -> None:
    """__class_getitem__을 보여준다."""
    print("\n" + "=" * 60)
    print("4. __class_getitem__")
    print("=" * 60)

    # __class_getitem__ — 제네릭 문법 지원
    class Response:
        """제네릭쉬 응답 타입."""

        def __init__(self, data: object, status: int = 200) -> None:
            self.data = data
            self.status: int = status

        def __class_getitem__(cls, item: type) -> str:
            return f"{cls.__name__}[{item.__name__}]"

        def __repr__(self) -> str:
            return f"Response(data={self.data!r}, status={self.status})"

    print(f"Response[str] = {Response[str]}")  # → Response[str] = Response[str]
    print(f"Response[int] = {Response[int]}")  # → Response[int] = Response[int]

    r = Response("hello", 200)
    print(f"인스턴스: {r}")  # → 인스턴스: Response(data='hello', status=200)

    # Python 3.12+ class Foo[T]: 문법
    class TypedResponse[T]:
        def __init__(self, data: T, status: int = 200) -> None:
            self.data: T = data
            self.status: int = status

        def __repr__(self) -> str:
            return f"TypedResponse(data={self.data!r})"

    tr: TypedResponse[str] = TypedResponse("hello")
    print(f"\nPython 3.12+ 문법: {tr}")


def demonstrate_practical_metaclasses() -> None:
    """메타클래스 실용 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 메타클래스 실용 패턴")
    print("=" * 60)

    # 싱글턴 메타클래스
    class SingletonMeta(type):
        """싱글턴 메타클래스."""

        _instances: dict[type, object] = {}

        def __call__(cls, *args: object, **kwargs: object) -> object:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]

    class Database(metaclass=SingletonMeta):
        def __init__(self) -> None:
            self.connection: str = "connected"

    db1: Database = Database()
    db2: Database = Database()
    print(f"싱글턴: db1 is db2 = {db1 is db2}")  # → 싱글턴: db1 is db2 = True

    # 인터페이스 강제 메타클래스
    class InterfaceMeta(type):
        """필수 메서드를 강제하는 메타클래스."""

        required_methods: list[str] = []

        def __init__(
            cls,
            name: str,
            bases: tuple[type, ...],
            namespace: dict[str, object],
            **kwargs: object,
        ) -> None:
            super().__init__(name, bases, namespace, **kwargs)
            if bases:  # 기본 클래스가 아닌 경우만
                for method in cls.required_methods:
                    if not callable(namespace.get(method)):
                        raise TypeError(
                            f"{name}은 {method!r} 메서드를 구현해야 합니다"
                        )

    class Serializer(metaclass=InterfaceMeta):
        required_methods = ["serialize", "deserialize"]

    try:
        class BadSerializer(Serializer):
            pass
    except TypeError as e:
        print(f"\n인터페이스 강제: {e}")

    class GoodSerializer(Serializer):
        def serialize(self, data: object) -> str:
            return str(data)
        def deserialize(self, text: str) -> object:
            return text

    print(f"구현 완료: {GoodSerializer().serialize({'key': 'value'})}")


def demonstrate_metaclass_alternatives() -> None:
    """메타클래스 대안을 비교한다."""
    print("\n" + "=" * 60)
    print("6. 메타클래스 vs 대안")
    print("=" * 60)

    print(f"📌 도구 선택 가이드:")
    print(f"")
    print(f"  {'목적':<20} {'도구':<25} 복잡도")
    print(f"  {'-'*20} {'-'*25} {'-'*10}")
    print(f"  {'서브클래스 훅':<20} {'__init_subclass__':<25} {'★☆☆'}")
    print(f"  {'속성 검증':<20} {'디스크립터':<25} {'★★☆'}")
    print(f"  {'인터페이스 강제':<20} {'ABC / Protocol':<25} {'★☆☆'}")
    print(f"  {'자동 등록':<20} {'__init_subclass__':<25} {'★☆☆'}")
    print(f"  {'클래스 데코레이터':<20} {'데코레이터':<25} {'★☆☆'}")
    print(f"  {'클래스 생성 제어':<20} {'메타클래스':<25} {'★★★'}")
    print(f"")
    print(f"  💡 메타클래스는 최후의 수단!")
    print(f"  💡 Python 3.12+ → class Foo[T]: 제네릭 문법")
    print(f"  💡 대부분의 경우 __init_subclass__ + 데코레이터로 충분")


if __name__ == "__main__":
    demonstrate_type_as_metaclass()
    demonstrate_metaclass_protocol()
    demonstrate_init_subclass()
    demonstrate_class_getitem()
    demonstrate_practical_metaclasses()
    demonstrate_metaclass_alternatives()

    print("\n" + "=" * 60)
    print("✅ _330_metaclasses.py 학습 완료!")
    print("=" * 60)
