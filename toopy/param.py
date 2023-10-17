import numpy as np

class Param:
    def __init__(self, value, name="", min=None, max=None, step=None, 
                 prior=None):
            self.name = name
            self._type = type(value)
            self._type.__init__(value)
            self.min = self._type(self.minfunc(value, min))
            self.max = self._type(self.maxfunc(value, min))
            self.step = self._type(1 if step is None else step)
            self.prior = prior

    def minfunc(self, value, minimum):
        if minimum is not None:
            return minimum
        
        if value <= 1:
            minimum = value / 10
        else:
            minimum = value / 4
    
        return np.round(maximum, np.abs(np.min([0, self.scale])))
        
    def maxfunc(self, value, maximum):
        if maximum is not None:
            return maximum
        
        if value <= 1:
            maximum = value * 10
        else:
            maximum = value * 2
            
        return np.round(maximum, np.abs(np.min([0, self.scale])))
    
    @property
    def scale(self):
        return self._type(np.log10(np.abs(self)))
        
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
    
    def __pow__(self, other):
        return self.ParamClass(self._type(self) ** other)

    def __repr__(self):
        pcls = str(self._type).split("'")[1]
        return f"<Param[{pcls}] '{self.name}': {self._type(self)} [{self.min}-{self.max}] step={self.step}>"

    @property
    def value(self):
        return self._type(self)


class FloatParam(Param, float):
    def __new__(self, value, name="", min=None, max=None, step=None, prior=None) -> float:
        return float.__new__(self, value)

class IntParam(Param, int):
    def __new__(self, value, name="", min=None, max=None, step=None, prior=None) -> int:
        return int.__new__(self, value)
