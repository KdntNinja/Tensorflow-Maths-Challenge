from fastapi import FastAPI, HTTPException
from collections import deque
import torch

app = FastAPI()

numbers = torch.tensor([50, 10, 5, 4, 2, 1])
operations = {"+": torch.add, "-": torch.sub, "*": torch.mul, "/": torch.div}

def closest_combination(target, numbers_list):
    memo = {}
    queue = deque([(0, "")])

    while queue:
        total, path = queue.popleft()

        if (total, path) in memo:
            continue

        memo[(total, path)] = True

        if abs(target - total) < abs(target - closest[0]):
            closest = (total, path)

        for num in numbers_list:
            for op, func in operations.items():
                new_total = func(total, num.item())
                new_path = f"{path} {op} {num.item()}"
                queue.append((new_total, new_path))

    return closest

@app.get("/maths/{user_input}")
def calculate(user_input: int, api_key: str):
    if api_key != "9521383":
        raise HTTPException(status_code=400, detail="Invalid API key")

    closest_total, operation = closest_combination(user_input, 0, 0, numbers)
    return {"Closest total": closest_total.item(), "Operation used": operation}
