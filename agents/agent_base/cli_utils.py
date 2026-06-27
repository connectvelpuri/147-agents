import builtins


def sanitize(text: str) -> str:
    """Strip non-ASCII characters for Windows console compatibility."""
    if isinstance(text, str):
        return text.encode("ascii", errors="replace").decode()
    return text


def patch_print():
    """Monkey-patch builtins.print to sanitize non-ASCII output."""
    _orig_print = builtins.print
    def _safe_print(*args, **kwargs):
        _orig_print(*(sanitize(str(a)) for a in args), **kwargs)
    builtins.print = _safe_print
