import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import requests
import uvicorn

app = FastAPI()

FIBONACCI_API_URL = os.getenv("FIBONACCI_API_URL", "http://fibonacci_api:8001/fibonacci/")

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Fibonacci and Factorial</title>
        </head>
        <body style="background-color: #2d2d2d; color: white; font-family: Arial;">
            <h1>Enter the index for the Fibonacci number</h1>
            <form action="/calculate" method="post">
                <input type="number" name="index" min="0" required>
                <button type="submit">Calculate</button>
            </form>
        </body>
    </html>
    """

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(request: Request):
    data = await request.form()
    index = int(data.get("index"))

    try:
        response = requests.post(FIBONACCI_API_URL, json={"index": index})

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error calling Fibonacci API.")

        result = response.json()
        fibonacci_value = result["fibonacci"]
        factorial_value = result["factorial_response"]["factorial"]

        return f"""
        <html>
            <head>
                <title>Calculation Result</title>
            </head>
            <body style="background-color: #2d2d2d; color: white; font-family: Arial;">
                <h1>Result</h1>
                <p>Fibonacci number: <b>{fibonacci_value}</b></p>
                <p>Factorial of this number: <b>{factorial_value}</b></p>
                <a href="/">Back</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
            <body style="background-color: #2d2d2d; color: red; font-family: Arial;">
                <h1>Error</h1>
                <p>{str(e)}</p>
                <a href="/">Back</a>
            </body>
        </html>
        """

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8002
    uvicorn.run(app, host="0.0.0.0", port=port)
