import operator


class Condition:
    def __init__(self, operator=None, a=None, b=None) -> None:
        self.operator = operator
        self.a = a
        self.b = b

    def __repr__(self) -> str:
        return f'<Condition({self.operator.__name__, self.a, self.b})>'

    def __eq__(self, o: object) -> object:
        return Condition(operator.eq, a=self, b=o)

    def __ne__(self, o: object) -> object:
        return Condition(operator.ne, a=self, b=o)

    def is_(self, o: object) -> object:
        return Condition(operator.is_, a=self, b=o)

    def is_not(self, o: object) -> object:
        return Condition(operator.is_not, a=self, b=o)

    def is_in(self, o: object) -> object:
        return Condition(operator.contains, a=o, b=self)

    def __and__(self, o: object) -> object:
        return Condition(operator.and_, a=self, b=o)

    def __or__(self, o: object) -> object:
        return Condition(operator.or_, a=self, b=o)

    def __lt__(self, o: object) -> object:
        return Condition(operator.lt, a=self, b=o)

    def __le__(self, o: object) -> object:
        return Condition(operator.le, a=self, b=o)

    def __ge__(self, o: object) -> object:
        return Condition(operator.ge, a=self, b=o)

    def __gt__(self, o: object) -> object:
        return Condition(operator.gt, a=self, b=o)

    def __invert__(self) -> object:
        return Condition(operator.not_, a=self)
