from dataclasses import is_dataclass, fields, dataclass
from typing import get_origin, get_args, List, Dict, Optional, Union
import random
import string


class BaseSimulator:
    """
    Provides most intuitive implementation of mock data.
    """
    def invoke(self, item_class, n=1):
        return [self._generate_mock_instance(item_class) for i in range(n)]

    def _generate_mock_instance(self, cls):
        if not is_dataclass(cls):
            raise ValueError("Only dataclass types are supported.")

        kwargs = {}
        for field in fields(cls):
            field_type = field.type
            kwargs[field.name] = self._generate_value_for_type(field_type)
        return cls(**kwargs)

    def _generate_value_for_type(self, tp):
        origin = get_origin(tp)
        args = get_args(tp)

        if origin is Union and type(None) in args:  # Optional[X]
            non_none_type = [a for a in args if a is not type(None)][0]
            return None  # or generate value: _generate_value_for_type(non_none_type)

        if origin is list or origin is List:
            elem_type = args[0] if args else str
            return [self._generate_value_for_type(elem_type) for _ in range(2)]

        if origin is dict or origin is Dict:
            key_type = args[0] if args else str
            val_type = args[1] if len(args) > 1 else str
            return {
                self._generate_value_for_type(key_type): self._generate_value_for_type(val_type)
                for _ in range(2)
            }

        if is_dataclass(tp):
            return self._generate_mock_instance(tp)

        # Primitive types
        if tp is int:
            return random.randint(1, 100)
        elif tp is float:
            return round(random.uniform(1.0, 100.0), 2)
        elif tp is str:
            return ''.join(random.choices(string.ascii_letters, k=8))
        elif tp is bool:
            return random.choice([True, False])

        # Fallback
        return None