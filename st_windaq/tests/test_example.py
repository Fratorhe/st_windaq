import numpy as np
import pytest

from ..code import Parabola


def test_check_default_values():
    """
    Test to check if the values a, b, c for the parabola are stored properly
    """
    parabola_object = Parabola(a=1, b=1, c=1, x=np.array([0]))
    assert parabola_object.a == 1
    assert parabola_object.b == 1
    assert parabola_object.c == 1


@pytest.mark.parametrize("a, b, c", [(1, 1, 1), (2, 3, 4), (5, 10, 12)])
def test_y_values(a, b, c):
    """
    This test evaluates the value of y at x=0 for different values of a, b, and c.
    """
    y = a * 0 + b * 0 + c
    parabola = Parabola(a, b, c, np.array([0]))
    assert parabola.y == y
