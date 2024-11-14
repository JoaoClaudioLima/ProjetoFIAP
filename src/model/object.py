from typing import List

from pydantic import BaseModel


class RecipeCreate(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str
    image: str = None
    category: str = None
