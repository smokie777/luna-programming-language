# data_structures.py

from pydantic.dataclasses import dataclass
from pydantic import Field
from .luna_types import EvalExpr
from .utils import luna_throw

@dataclass
class LunaMap():
  aa: list[list[EvalExpr]] = Field(default_factory=list)
  def __post_init__(self):
    if any([len(l) != 2 for l in self.aa]):
      luna_throw(f'Every item in a LunaMap associative array must be a list of size 2. Got: {self.aa}')
      