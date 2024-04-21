from fastapi import FastAPI, HTTPException
import torch

app = FastAPI()

numbers = torch.tensor([50, 10, 5, 4, 2, 1])

operations = {
    "+": torch.add,
    "-": torch.sub,
    "*": torch.mul,
    "/": torch.div
}

def closest_combination(target, total, index, numbers_list, operation="", closest=(float("inf"), "")):
    if abs(target - total) < abs(target - closest[0]):
        closest = (total, operation)
    if index == len(numbers_list) or abs(target - total) < 0.5:
        return closest
    for op, func in operations.items():
        new_operation = f"({operation} {op} {numbers_list[index].item()})" if operation else str(numbers_list[index].item())
        new_total = func(total, numbers_list[index]) if operation else numbers_list[index]
        closest = closest_combination(target, new_total, index + 1, numbers_list, new_operation, closest)
    return closest

@app.get("/maths/{user_input}/{api_key}")
def calculate(user_input: int, api_key: str):
    if api_key != "9521383":
        raise HTTPException(status_code=400, detail="Invalid API key")
    closest_total, operation = closest_combination(user_input, 0, 0, numbers)
    return {"Closest total": closest_total.item(), "Operation used": operation}
