from __future__ import annotations
import utils
from utils import almost_equal
from typing import Union, Any
import Field
import Complex
t_vector = list[Union[float, Complex.Complex]]


class Vector:

    @staticmethod
    def random(min: float = -10, max: float = 10, degree: int = 10,  def_value=None, f: Field.Field = Field.DefaultRealField) -> Vector:
        return Vector([f.random(min, max) if def_value is None else def_value for _ in range(degree)])

    @staticmethod
    def fromSize(size: int, default_value: Any = 0) -> Vector:
        return Vector([default_value for _ in range(size)])

    def __init__(self, values: t_vector, field: Field.Field = None) -> None:
        self.__values = values
        self.field = Field.RealField(len(values)) if not field else field

    @property
    def length(self):
        return len(self.__values)

    @property
    def adjoint(self) -> Vector:
        # TODO implement adjoint for complex vector
        return self.copy()

    @property
    def has_no_zero(self) -> bool:
        for v in self:
            if v != 0:
                return True
        return False

    def __str__(self) -> str:
        return str(self.__values)

    def __add__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            raise TypeError("Vector can only be added to another Vector")
        if self.field != other.field:
            raise ValueError("Vectors must have the same field")
        if len(self.__values) != len(other.__values):
            raise ValueError("Vectors must have the same length")
        return Vector([self[i] + other[i] for i in range(len(self))], self.field)

    def __radd__(self, other) -> Vector:
        return self.__add__(other)

    def __sub__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            raise TypeError(
                "Vector can only be subtracted from another Vector")
        if self.field != other.field:
            raise ValueError("Vectors must have the same field")
        if len(self.__values) != len(other.__values):
            raise ValueError("Vectors must have the same length")
        return Vector([self.__values[i] - other.__values[i] for i in range(len(self.__values))], self.field)

    def __rsub__(self, other) -> Vector:
        return (-self) + other

    def __neg__(self) -> Vector:
        return Vector([-self.__values[i] for i in range(len(self.__values))], self.field)

    def __mul__(self, num: float) -> Vector:
        return Vector([num * self.__values[i] for i in range(len(self.__values))], self.field)

    def __rmul__(self, num: float) -> Vector:
        return self.__mul__(num)

    def __truediv__(self, other) -> Vector:
        if utils.isoneof(other, [int, float, Complex]):
            return self.__mul__(1/other)
        raise ValueError("cant divide vector")

    def __rtruediv__(self, num: float) -> Vector:
        raise ValueError("cant divide by vector")

    def __getitem__(self, index: int) -> Union[float, Complex.Complex]:
        return self.__values[index]

    def __iter__(self):
        return iter(self.__values)

    def __eq__(self, other: Vector) -> bool:
        if not utils.isoneof(other, [Vector, list]):
            return False
        if isinstance(other, Vector):
            other = other.__values
        if len(self) != len(other):
            return False
        return self.__values == other

    def __ne__(self, other: Vector) -> bool:
        return not (self == other)

    def __len__(self) -> int:
        return self.length

    def almost_equal(self, other: Vector) -> bool:
        if not isinstance(other, Vector):
            raise TypeError("Vector can only be compared to another Vector")
        if not self.field == other.field:
            raise ValueError("Vectors must have the same field")
        return all([almost_equal(self[i], other[i]) for i in range(len(self))])

    def set(self, index, value) -> None:
        self.__values[index] = value

    def norm(self) -> float:
        return sum([x ** 2 for x in self]) ** 0.5

    def dot(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            raise TypeError("Vector can only be multiplied by another Vector")
        if self.field != other.field:
            raise ValueError("Vectors must have the same field")
        if len(self.__values) != len(other.__values):
            raise ValueError("Vectors must have the same length")
        return Vector([self.__values[i] * other.__values[i] for i in range(len(self.__values))])

    def toOrthonormal(self) -> Vector:
        # TODO change name to Normalize?
        return self / self.norm()

    def projection_onto(self, value) -> Vector:
        """
        return the projection of self onto value which can be another vector or a Span
        """
        from .Span import Span
        if not isinstance(value, Vector) and not isinstance(value, Span):
            raise TypeError("v must be of type Vector or Span")
        is_span = isinstance(value, Span)
        if not is_span and value.length != self.length:
            raise ValueError("value must have the same length as self")
        if is_span and value[0].length != self.length:
            raise ValueError(
                "the span's vectors must have the same length as self")
        from .InnerProduct import StandardInnerProduct as sip
        if not is_span:
            return sip(self, value)/sip(value, value)*value
        else:
            return value.projection_of(self)

    def copy(self) -> Vector:
        return Vector(self.__values, self.field)
