from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class FactorialRequest(BaseModel):
    number: int

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is defined only for non-negative integers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

@app.post("/factorial/")
async def get_factorial(factorial_request: FactorialRequest):
    try:
        result = factorial(factorial_request.number)
        return {"factorial": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
