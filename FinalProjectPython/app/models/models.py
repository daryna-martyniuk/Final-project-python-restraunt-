from datetime import date, datetime, time
from typing import List, Optional

from sqlalchemy import String, ForeignKey, Date, Integer, Time, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class DishCategory(Base):
    __tablename__ = "dish_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    dishes: Mapped[List["Dish"]] = relationship("Dish", back_populates="category", cascade="all, delete")

class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey("dish_categories.id"))
    category: Mapped["DishCategory"] = relationship("DishCategory", back_populates="dishes")

    promotions: Mapped[List["Promotion"]] = relationship(
        secondary="promotion_dish_association",
        back_populates="dishes"
    )

class Promotion(Base):
    __tablename__ = "promotions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    discount_percent: Mapped[int] = mapped_column(Integer, nullable=False)  # Наприклад, 10%
    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
    valid_to: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=True)
    end_time: Mapped[time] = mapped_column(Time, nullable=True)

    dishes: Mapped[List["Dish"]] = relationship(
        secondary="promotion_dish_association",
        back_populates="promotions"
    )

class PromotionDishAssociation(Base):
    __tablename__ = "promotion_dish_association"

    promotion_id: Mapped[int] = mapped_column(ForeignKey("promotions.id"), primary_key=True)
    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id"), primary_key=True)

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_id: Mapped[int] = mapped_column(ForeignKey("cafe_tables.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete")
    table: Mapped["CafeTable"] = relationship("CafeTable")  # <-- об'єкт тут

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id"))
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    price_at_order: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    dish: Mapped["Dish"] = relationship("Dish")

class CafeTable(Base):
    __tablename__ = "cafe_tables"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number:Mapped[int] = mapped_column(Integer, unique=True, nullable=False)  # Номер столу
    location:Mapped[str] = mapped_column(String(255), nullable=True)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="table")

