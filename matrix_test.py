from Matrix import Matrix
from Field import RealField, Fields

COUNT = 100
N = 50
Fn = RealField(N)


def test_from_vector():
    for _ in range(COUNT):
        v = Fn.random()
        m = Matrix.fromVector(v)
        for i in range(v.length):
            assert v[i] == m[i][0]


def test_from_vectors():
    for _ in range(int(COUNT/10)+1):
        vecs = [Fn.random() for _ in range(10)]
        m = Matrix.fromVectors(vecs)
        for i in range(len(vecs[0])):
            for j in range(len(vecs)):
                assert vecs[j][i] == m[i][j]


def test_determinant():
    assert Matrix([[1, 1], [1, 1]]).determinant == 0


def test_id():
    assert Matrix.id_matrix(2) == Matrix([[1, 0], [0, 1]])


def test_guassian_elimination():
    assert Matrix([[1, 1], [1, 1]]).guassian_elimination(
    ) == Matrix([[1, 1], [0, 0]])
    assert Matrix.id_matrix(5).guassian_elimination(
    ) == Matrix.id_matrix(5)


def test_solve():
    from Span import Span
    from Vector import Vector
    assert Matrix([[1, 1], [1, 1]]).solve(Vector([1, 2])) == None
    assert Matrix.id_matrix(2).solve() == Vector([0, 0])
    # FIXME
    # assert Matrix([[1, 1], [1, 1]]).solve() == Span([Vector([0, 1])])


# def test_kernel():
#     from Span import Span
#     from Vector import Vector
#     assert Matrix([[1, 0], [0, 0]]).kernel == Span([Vector([0, 1])])


# test_kernel()


def test_with_polynomial():
    from SimplePolynomial import SimplePolynomial
    assert SimplePolynomial.fromString("x^2")(
        Matrix([[1, 0], [0, 1]])) == Matrix([[1, 0], [0, 1]])
