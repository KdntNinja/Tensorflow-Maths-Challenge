from fastapi import FastAPI, HTTPException
import torch

app = FastAPI()

operations = {
    "+": torch.add,
    "-": torch.sub,
    "*": torch.mul,
    "/": torch.div
}

def closest_combination(target, total, index, numbers, operation="", closest=(float("inf"), "")):
    if abs(target - total) < abs(target - closest[0]):
        closest = (total, operation)
    if index == len(numbers) or abs(target - total) < 0.5:
        return closest
    for op, func in operations.items():
        new_operation = f"({operation} {op} {numbers[index].item()})" if operation else str(numbers[index].item())
        new_total = func(total, numbers[index]) if operation else numbers[index]
        closest = closest_combination(target, new_total, index + 1, numbers, new_operation, closest)
    return closest

numbers = torch.tensor([50, 10, 5, 4, 2, 1])

@app.get("/calculate/{user_input}/{api_key}")
def calculate(user_input: int, api_key: str):
    if api_key != "9521383":
        raise HTTPException(status_code=400, detail="Invalid API key")
    closest_total, operation = closest_combination(user_input, 0, 0, numbers)
    return {"Closest total": closest_total.item(), "Operation used": operation}