from Vector import Vector
import random
from Complex import Complex


def StandardInnerProduct(a: Vector, b: Vector) -> float:
    if not isinstance(a, Vector):
        raise TypeError("a must be a Vector")
    if not isinstance(b, Vector):
        raise TypeError("b must be a Vector")
    if a.length != b.length:
        raise ValueError("Vectors must have the same length")
    return sum([a[i] * b[i] for i in range(a.length)])


def isInnerProduct(func, generator_func) -> bool:
    MIN_VAL = -100
    MAX_VAL = 100
    REPETITIONS = 1000
    THRESHOLD = 0.000000001

    def check_linearity(func, generator_func) -> bool:
        for _ in range(REPETITIONS):
            a: Vector = generator_func()
            b: Vector = generator_func()
            c: Vector = generator_func()
            s1 = random.randint(MIN_VAL, MAX_VAL)
            s2 = random.randint(MIN_VAL, MAX_VAL)
            original = func(a, s1*b+s2*c)
            decomp = s1*func(a, b)+s2*func(a, c)
            if original - decomp > THRESHOLD:
                return False
        return True

    def check_symmetry(func, generator_func) -> bool:
        for _ in range(REPETITIONS):
            a: Vector = generator_func()
            b: Vector = generator_func()
            # TODO complex
            original = func(a, b)
            adj = func(b, a)
            if original-adj > THRESHOLD:
                return False
        return True

    def check_norm(func, generator_func) -> bool:
        for _ in range(REPETITIONS):
            v: Vector = generator_func()
            if not func(v, v) > 0:
                return False
        v = generator_func(True)
        if func(v, v) != 0:
            return False
        return True

    linearity_result = check_linearity(func, generator_func)
    symmetry_result = check_symmetry(func, generator_func)
    norm_result = check_norm(func, generator_func)
    return [linearity_result, symmetry_result, norm_result]