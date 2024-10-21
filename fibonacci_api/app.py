from fastapi import FastAPI, HTTPException, Path
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

@app.get("/fibonacci/{index}")
async def get_fibonacci(index: int = Path(..., description="Индекс числа Фибоначчи")):
    try:
        fib_value = fibonacci(index)
        FACTORIAL_API_URL = f"http://factorial_api:8000/factorial/{fib_value}"

        response = requests.get(FACTORIAL_API_URL)

        if response.status_code == 200:
            factorial_response = response.json()
            return {
                "fibonacci": fib_value,
                "factorial_response": factorial_response
            }
        else:
            return {"error": "Ошибка при обращении к API факториала.", "details": response.json()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    uvicorn.run(app, host="0.0.0.0", port=port)