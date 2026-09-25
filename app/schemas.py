from pydantic import BaseModel, ConfigDict
from typing import Optional

class VideogameBase(BaseModel):
    name: str
    genre: str
    platform: str
    release_year: int
    rating: float
    developer: str

class VideogameCreate(VideogameBase):
    pass

class VideogameUpdate(BaseModel):
    name: Optional[str] = None
    genre: Optional[str] = None
    platform: Optional[str] = None
    release_year: Optional[int] = None
    rating: Optional[float] = None
    developer: Optional[str] = None

class VideogameResponse(VideogameBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
