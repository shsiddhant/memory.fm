"""Module: _typing
Define typing classes
"""
from typing import TypeAlias
from pathlib import Path

PathLike: TypeAlias = str | Path
