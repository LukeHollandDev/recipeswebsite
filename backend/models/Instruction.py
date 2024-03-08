from typing import List, Optional
from sqlmodel import SQLModel, Field


class Instruction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    index: int
    text: str
    image: Optional[str]


class InstructionGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    # add list of instructions
