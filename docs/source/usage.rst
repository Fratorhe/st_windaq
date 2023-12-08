======
Usage
======

Start by importing the module

.. code-block:: python

    from st_windaq import Parabola

Then, we can create an object as:

.. code-block:: python

    a = 1
    b = 4
    c = 20
    x = np.linspace(-10, 10, num=50)
    parabola_obj = Parabola(a, b, c, x)

    parabola_obj.plot_y()
