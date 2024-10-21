from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import requests
import uvicorn

app = FastAPI()

FIBONACCI_API_URL = "http://fibonacci_api:8001/fibonacci/"

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Число Фибоначчи и Факториал</title>
        </head>
        <body style="background-color: #2d2d2d; color: white; font-family: Arial;">
            <h1>Введите индекс для числа Фибоначчи</h1>
            <form action="/calculate" method="get">
                <input type="number" name="index" min="0" required>
                <button type="submit">Вычислить</button>
            </form>
        </body>
    </html>
    """

@app.get("/calculate", response_class=HTMLResponse)
async def calculate(index: int):
    try:
        response = requests.get(f"{FIBONACCI_API_URL}{index}")
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ошибка при вызове API Фибоначчи.")

        result = response.json()

        fibonacci_value = result["fibonacci"]
        factorial_value = result["factorial_response"]["factorial"]

        return f"""
        <html>
            <head>
                <title>Результат вычислений</title>
            </head>
            <body style="background-color: #2d2d2d; color: white; font-family: Arial;">
                <h1>Результат</h1>
                <p>Число Фибоначчи: <b>{fibonacci_value}</b></p>
                <p>Факториал этого числа: <b>{factorial_value}</b></p>
                <a href="/">Назад</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
            <body style="background-color: #2d2d2d; color: red; font-family: Arial;">
                <h1>Ошибка</h1>
                <p>{str(e)}</p>
                <a href="/">Назад</a>
            </body>
        </html>
        """

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8002
    uvicorn.run(app, host="0.0.0.0", port=port)