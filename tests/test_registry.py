import pytest

from src.core.registry import Registry


def test_registry_basic():
    registry = Registry[int]("Test")
    
    @registry.register("one")
    class One:
        val = 1
        
    assert registry.get("one") == One
    assert registry.list_all() == ["one"]
    
    instance = registry.create("one")
    assert isinstance(instance, One)

def test_registry_overwrite():
    registry = Registry[int]("Test")
    
    @registry.register("item")
    class Item1:
        pass
        
    @registry.register("item")
    class Item2:
        pass
        
    assert registry.get("item") == Item2

def test_registry_missing():
    registry = Registry[int]("Test")
    with pytest.raises(ValueError):
        registry.create("missing")
