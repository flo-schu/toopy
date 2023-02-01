
class Param:
    def __init__(self, value, min=None, max=None, step=None):
            self._type = type(value)
            self._type.__init__(value)
            self.min = self._type(value / 4 if min is None else min)
            self.max = self._type(value * 2 if max is None else max)
            self.step = self._type(1 if step is None else step)

    def ParamClass(self, value):
        kwargs = self.__dict__.copy()
        _type = kwargs.pop("_type")
        ParamClass = type(self)
        return ParamClass(_type(value), **kwargs)

    def __mul__(self, other):
        return self.ParamClass(self._type(self) * other)

    def __div__(self, other):
        return self.ParamClass(self._type(self) / other)

    def __truediv__(self, other):
        return self.ParamClass(self._type(self) / other)

    def __add__(self, other):
        return self.ParamClass(self._type(self) + other)

    def __sub__(self, other):
        return self.ParamClass(self._type(self) - other)

    def __repr__(self):
        pcls = str(self._type).split("'")[1]
        return f"<Param[{pcls}]: {self._type(self)} [{self.min}-{self.max}] step={self.step}>"


class FloatParam(Param, float):
    def __new__(self, value, min=None, max=None, step=None) -> float:
        return float.__new__(self, value)

class IntParam(Param, int):
    def __new__(self, value, min=None, max=None, step=None) -> int:
        return int.__new__(self, value)
