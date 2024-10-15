from fastapi import FastAPI
from enum import Enum
app = FastAPI()

food_items = {
    'indian': ["Panipuri", "Chole Bhature", "Lassi"],
    'bangladeshi': ["Morog polao", "Dhakai Kacchi", "Chom chom"],
    'american': ["Hot dog", "Stake", "Apple Pie"],
    'italian' : ["Pizza", "Pasta", "Cold Coffee"]
}

valid_cuisines = food_items.keys()
class AvailableCuisines(str, Enum):
    indian = "indian"
    american = "american"
    italian = "italian"
    bangladeshi = "bangladeshi"

@app.get("/{name}")
async def hello(name):
    return f"welcome to server, {name}"

@app.get("/hi/{name}")
async def hello(name):
    return f"Hi, {name}. Welcome to fastapi tutorial"

@app.get("/get_items/{cuisine}")
async def get_items(cuisine):
    if cuisine not in valid_cuisines:
        return f"{cuisine} is not available. {valid_cuisines} are available now"
    return food_items.get(cuisine)

@app.get("/new_get_items/{cuisine}")
async def get_items(cuisine : AvailableCuisines):
    # if cuisine not in valid_cuisines:
    #     return f"{cuisine} is not available. {valid_cuisines} are available now"
    return food_items.get(cuisine)

coupon = {
    1 : "10%",
    2: "20%",
    3: "30%"
}
@app.get("/coupon_code/{code}")
async def coupon_code(code: int):
    return f"We got {coupon[code]} discount"