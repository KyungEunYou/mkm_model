from pathlib import Path

EXAMPLE = Path(__file__).parent.parent.joinpath("example").as_posix()

from .elementary_reaction_step import *