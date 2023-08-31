def update_dataclass(obj, **kwargs):
    for key, value in kwargs.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
        else:
            raise AttributeError(f"{type(obj).__name__} object has no attribute '{key}'")
