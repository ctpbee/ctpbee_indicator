from .plot import ShowLine


class Cerebro(ShowLine):
    """
        调度中心类
    """
    def __init__(self):
        super().__init__()

    def compute(self):
        pass

    def plots(self, width=8, height=6, color="k", lw=0.5):
        ShowLine.plot(width=width, height=height, color=color, lw=lw)