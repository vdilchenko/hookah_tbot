from pydantic import BaseModel
from typing import List, Dict, Any

class BrandResponse(BaseModel):
    Бренд: str
    Рейтинг: float
    Вкус: str
    Название_вкуса: str
    Количество_оценок: int
    Отзывы: str

class FlavorResponse(BaseModel):
    Вкус: str
    Рейтинг: float
    Бренд: str
    Название_вкуса: str
    Количество_оценок: int
    Отзывы: str