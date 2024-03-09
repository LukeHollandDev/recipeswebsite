from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Instruction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    index: int
    text: str
    image: Optional[str]
    group_id: int = Field(foreign_key="instructiongroup.id")
    group: "InstructionGroup" = Relationship(back_populates="instructions")


class InstructionGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    instructions: List[Instruction] = Relationship(back_populates="group")
    recipe_id: int = Field(foreign_key="recipe.id")
