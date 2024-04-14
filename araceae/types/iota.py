class iota:
    """Auto incrementing value, similar to iota in Golang.

    Normal usage::

        _iota = iota()
        a = _iota()     # a = 0
        b = _iota()     # b = 1

    Custom values::

        _iota = iota(100, 10)
        a = _iota()     # a = 100
        b = _iota()     # b = 110
    """

    x: int

    def __init__(self, s: int = 0, i: int = 1) -> None:
        """
        Args:
            s (int, optional): Start value. Defaults to 0.
            i (int, optional): Step value. Defaults to 1.
        """
        self.x = s

    def __call__(self) -> int:
        self.x += 1
        return self.x


auto = iota()
