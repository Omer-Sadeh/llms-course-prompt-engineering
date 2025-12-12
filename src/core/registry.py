import logging
from typing import Dict, Generic, List, Optional, Type, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar('T')

class Registry(Generic[T]):
    """Generic registry for plugins."""
    
    def __init__(self, name: str):
        self._registry: Dict[str, Type[T]] = {}
        self.name = name

    def register(self, name: str):
        """Decorator to register a class."""
        def decorator(cls: Type[T]):
            if name in self._registry:
                logger.warning(f"{name} already registered in {self.name} registry. Overwriting.")
            self._registry[name] = cls
            return cls
        return decorator

    def get(self, name: str) -> Optional[Type[T]]:
        """Get a registered class by name."""
        return self._registry.get(name)

    def list_all(self) -> List[str]:
        """List all registered names."""
        return list(self._registry.keys())

    def create(self, name: str, *args, **kwargs) -> T:
        """Instantiate a registered class."""
        cls = self.get(name)
        if not cls:
            raise ValueError(f"'{name}' not found in {self.name} registry.")
        return cls(*args, **kwargs)

# Global registries
strategy_registry = Registry("Strategy")
metric_registry = Registry("Metric")
