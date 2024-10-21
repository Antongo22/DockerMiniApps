from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI()

def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

class FibonacciRequest(BaseModel):
    index: int

@app.post("/fibonacci/")
async def get_fibonacci(request: FibonacciRequest):
    try:
        fib_value = fibonacci(request.index)
        FACTORIAL_API_URL = "http://localhost:8000/factorial/"

        response = requests.post(FACTORIAL_API_URL, json={"number": fib_value})

        if response.status_code == 200:
            return {
                "fibonacci": fib_value,
                "factorial_response": response.json()
            }
        else:
            return {"error": "Ошибка при обращении к API факториала.", "details": response.json()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    uvicorn.run(app, host="0.0.0.0", port=port)
