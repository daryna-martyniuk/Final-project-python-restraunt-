from fastapi import FastAPI
from app.controllers.category_dish import router as category_dish_router
from app.controllers.dish import router as dish_router
from app.controllers.order import router as order_router
from app.controllers.order_item import router as order_item_router
from app.controllers.promotion import router as promotion_router
from app.controllers.cafe_table import router as cafe_table_router


app = FastAPI(title="Cafe menagment API")
app.include_router(category_dish_router)
app.include_router(dish_router)
app.include_router(order_router)
app.include_router(order_item_router)
app.include_router(promotion_router)
app.include_router(cafe_table_router)

@app.get("/")
def root():
    return {"message": "Cafe API is running!"}
