import logging
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class ProductType(str, Enum):
    NEW = 'new'
    USED = 'used'


class Manufacturer(BaseModel):
    name: str
    city: Optional[str] = None


class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description='Название продукта')
    price: float = Field(..., gt=0, description='Цена продукта')
    in_stock: bool = Field(default=False)
    color: str = 'black'
    year: Optional[int] = None
    product_type: ProductType
    manufacturer: Manufacturer

def test_product():
    product = Product(
        name='Laptop',
        price='999.99',
        product_type=ProductType.NEW,
        manufacturer={'name': 'MSI'}
    )
    logger.info(f'{product=}')


class User(BaseModel):
    name: str
    age: int
    adult: bool

def get_user():
    return {
        'name': 'Alice',
        'age': 25,
        'adult': 'true'
    }

def test_user_data():
    user = User(**get_user())
    assert user.name == 'Alice'
    logger.info(f"{user.name=} {user.age=} {user.adult=}")