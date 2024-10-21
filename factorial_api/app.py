from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError
import uvicorn

app = FastAPI()

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

class NumberRequest(BaseModel):
    number: int

@app.post("/factorial/")
async def get_factorial(request: NumberRequest):
    try:
        result = factorial(request.number)
        return {"number": request.number, "factorial": result}
    except ValueError as e:
        return {"error": str(e), "number": request.number}

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return {"error": "Неверные данные. Убедитесь, что передано целое число."}

if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
