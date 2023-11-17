import utils
from utils import creational

@creational.singleton
class X: 
    def __init__(self, a: int = 5):
        self.a = a
        

def test_singleton():
    x = X()
    y = X(a=10)
    assert x == y
    assert x.a == y.a