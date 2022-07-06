from __future__ import annotations
from typing import Any, Union
from Complex import Complex
from Vector import Vector, t_vector
from Span import Span
from Field import Field, DefaultRealField
import copy
import functools
t_matrix = list[list[Union[float, Complex]]]


class Matrix:
    def __init__(self, mat: t_matrix, sol_vec: t_vector = None, field: Field = DefaultRealField) -> None:
        self.__matrix = mat
        self.__rows = len(mat)
        self.__cols = len(mat[0])
        self.__solution_vector = sol_vec if sol_vec else [
            0 for _ in range(self.__rows)]
        self.__field = field

    @property
    def rank(self) -> int:
        self.reorgenize_rows()
        rank = 0
        for row in self.__matrix:
            if all([i == 0 for i in row]):
                continue
            rank += 1
        return rank

    @property
    def determinant(self) -> float:
        if self.__rows != self.__cols:
            raise ValueError("Matrix must be square")
        if self.__rows == 1:
            return self.__matrix[0][0]
        if self.__rows == 2:
            return self.__matrix[0][0] * self.__matrix[1][1] - self.__matrix[0][1] * self.__matrix[1][0]
        return sum([self.__matrix[i][0] * ((-1)**i) * self.minor(i, 0) for i in range(self.__rows)])

    @property
    def is_invertiable(self) -> bool:
        return self.determinant != 0

    @property
    def is_square(self) -> bool:
        return self.__rows == self.__cols

    @property
    def kernel(self) -> Span:
        pass

    @property
    def image(self) -> Span:
        pass

    def inverse(self) -> Matrix:
        if not self.is_invertiable:
            raise ValueError("Matrix must be invertible")
        return Matrix([[self.minor(i, j) / self.determinant for j in range(self.__cols)]
                       for i in range(self.__rows)])

    def cofactor(self, row_to_ignore: int, col_to_ignore: int) -> Matrix:
        if(row_to_ignore >= self.__rows or col_to_ignore >= self.__cols):
            raise ValueError("Row or column index out of range")
        res: t_matrix = []
        for i, row in enumerate(self.__matrix):
            if i == row_to_ignore:
                continue
            res.append([])
            for j, col in enumerate(self.__matrix[i]):
                if j == col_to_ignore:
                    continue
                res[i if i < row_to_ignore else i -
                    1].append(self.__matrix[i][j])
        return Matrix(res)

    def minor(self, row_to_ignore: int, col_to_ignore: int) -> float:
        return self.cofactor(row_to_ignore, col_to_ignore).determinant

    def transpose(self) -> Matrix:
        return Matrix([[self.__matrix[j][i] for j in range(self.__cols)]
                       for i in range(self.__rows)])

    def reorgenize_rows(self):
        def comparer(a: list[float], b: list[float]) -> bool:
            def first_not_zero_index(row: list[float]) -> int:
                for i in range(len(row)):
                    if row[i] != 0:
                        break
                return i
            return -1 if first_not_zero_index(a) > first_not_zero_index(b) else 1
        self.__matrix = sorted(
            self.__matrix, key=functools.cmp_to_key(comparer), reverse=True)

    def solve(self) -> Matrix:
        """
        Solve the system of equations
        """
        if self.__rows != self.__cols:
            raise ValueError("Matrix must be square")
        # if self.rows != self.solution_vector.length:
        #     raise ValueError(
        #         "Matrix and solution vector must have the same number of rows")

        def first_not_zero_index(row: list[float]) -> int:
            for i in range(len(row)):
                if row[i] != 0:
                    break
            return i
        res = copy.deepcopy(self)
        res.reorgenize_rows()
        for r in range(res.__rows):
            lead_index = first_not_zero_index(res[r])
            lead_value = res[r][lead_index]
            if lead_value == 0:
                continue
            if lead_value != 1:
                for c in range(res.__cols):
                    res[r][c] /= lead_value
                res.__solution_vector[r] /= lead_value
                lead_value = res[r][lead_index]
            for r2 in range(res.__rows):
                if r == r2:
                    continue
                row_divider = res[r2][lead_index]/lead_value
                if row_divider == 0:
                    continue
                for c in range(res.__cols):
                    res[r2][c] -= row_divider * res[r][c]
                res.__solution_vector[r2] -= row_divider * \
                    res.__solution_vector[r]
        if res.rank != res.__rows:
            return "nullity rank was atleast 1, not yet implemented"  # TODO

        return res

    def __getitem__(self, index: int):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
        return self.__matrix[index]

    def __str__(self) -> str:
        result = ""
        for i, row in enumerate(self.__matrix):
            result += str(row)
            result += " | "+str(self.__solution_vector[i]) + "\n"
        return result

    def __add__(self, other: Matrix) -> Matrix:
        if not Matrix.isInstance(other):
            raise TypeError("Matrix can only be added to another Matrix")
        if self.__rows != other.__rows or self.__cols != other.__cols:
            raise ValueError("Matrices must have the same dimensions")
        return Matrix([[self.__matrix[i][j] + other.__matrix[i][j] for j in range(self.__cols)]
                       for i in range(self.__rows)])

    def __neg__(self) -> Matrix:
        return Matrix([[-self.__matrix[i][j] for j in range(self.__cols)]
                       for i in range(self.__rows)])

    def __sub__(self, other: Matrix) -> Matrix:
        if not Matrix.isInstance(other):
            raise TypeError(
                "Matrix can only be subtracted from another Matrix")
        if self.__rows != other.__rows or self.__cols != other.__cols:
            raise ValueError("Matrices must have the same dimensions")
        return Matrix([[self.__matrix[i][j] - other.__matrix[i][j] for j in range(self.__cols)]
                       for i in range(self.__rows)])

    def __mul__(self, other: Union[float, Complex, Vector, Matrix]) -> Union[float, Complex, Vector, Matrix]:
        """
        self * other
        """
        if isinstance(other, float) or isinstance(other, Complex) or isinstance(other, int):
            return Matrix([[other * self.__matrix[i][j] for j in range(self.__cols)]
                           for i in range(self.__rows)])
        if isinstance(other, Vector):
            if self.__cols != other.length:
                raise ValueError(
                    "Matrix and Vector must have the same number of rows")
            return Vector([sum([self.__matrix[i][j] * other[j] for j in range(self.__cols)])
                           for i in range(self.__rows)])
        if isinstance(other, Matrix):
            if self.__cols != other.__rows:
                raise ValueError(
                    "Matrix and Matrix must have matching sizes: self.cols == other.rows")
            return Matrix([[sum([self.__matrix[i][j] * other.__matrix[j][k] for j in range(self.__cols)])
                            for k in range(other.__cols)] for i in range(self.__rows)])
        raise TypeError(
            "Matrix can only be multiplied by a number, Vector, or Matrix")

    def __rmul__(self, other: Union[int, float, Complex, Vector, Matrix]) -> Union[float, Complex, Vector, Matrix]:
        """
        other * self
        """
        if isinstance(other, float) or isinstance(other, Complex) or isinstance(other, int):
            return self.__mul__(other)
        if isinstance(other, Vector):
            raise TypeError(
                "Matrix can only be multiplied by a vector from the right")
        if isinstance(other, Matrix):
            if self.__cols != other.__rows:
                raise ValueError(
                    "Matrix and Matrix must have the same number of columns")
            return Matrix([[sum([self.__matrix[i][j] * other.__matrix[j][k] for j in range(self.__cols)])
                            for k in range(other.__cols)] for i in range(self.__rows)])
        raise TypeError(
            "Matrix can only be multiplied by a number, Vector, or Matrix")

    def __eq__(self, other: Matrix) -> bool:
        if not isinstance(other, Matrix):
            raise TypeError("Matrix can only be compared to another Matrix")
        if self.__rows != other.__rows or self.__cols != other.__cols:
            return False
        if any([self.__matrix[i][j] != other.__matrix[i][j] for i in range(self.__rows) for j in range(self.__cols)]):
            return False
        return True

    @staticmethod
    def fromVector(vec: Vector) -> Matrix:
        return Matrix([[vec.__values[i] for i in range(vec.length)]])

    @staticmethod
    def fromString(matrix_string: str) -> Matrix:
        return Matrix([[int(num) for num in row.split()]
                       for row in matrix_string.split("\n")])

    @staticmethod
    def random(f: Field = DefaultRealField, min: float = -10, max: float = 10, degree: int = 10,  def_value=None) -> Matrix:
        # TODO how to check that defualt value is inside 'f'? what if 'f' is ratinals and has no __contains__ implemented?
        return Matrix([f.random(min, max) if def_value is None else def_value for _ in range(degree)], field=f)