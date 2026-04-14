from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str  # Note: mapping 'image' from JSON to 'image_url' or just accept what comes
    rating: Optional[float] = 0.0
    category: Optional[str] = "All"
    image: Optional[str] = ""

class CartItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    id: Optional[int] = None
    items: List[CartItem]
    total_price: float
