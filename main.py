from fastapi import FastAPI, HTTPException
import torch

app = FastAPI()

numbers = torch.tensor([50, 10, 5, 4, 2, 1])
operations = {"+": torch.add, "-": torch.sub, "*": torch.mul, "/": torch.div}

def closest_combination(target, numbers_list):
    closest = [None] * (target + 1)
    closest[0] = (0, "")

    for i in range(target + 1):
        if closest[i] is not None:
            for num in numbers_list:
                for op, func in operations.items():
                    if op == "/" and i < num.item():
                        continue
                    new_total = int(func(i, num.item()))
                    if new_total <= target:
                        new_path = f"{closest[i][1]} {op} {num.item()}"
                        if closest[new_total] is None or abs(target - new_total) < abs(target - closest[new_total][0]):
                            closest[new_total] = (new_total, new_path)

    closest_total, operation = min(((total, operation) for total, operation in closest if total is not None), key=lambda x: abs(target - x[0]))
    return closest_total

@app.get("/maths/{user_input}")
def calculate(user_input: int, api_key: str):
    if api_key != "9521383":
        raise HTTPException(status_code=400, detail="Invalid API key")

    closest_total, operation = closest_combination(user_input, numbers)
    return {"Closest total": closest_total.item(), "Operation used": operation}
