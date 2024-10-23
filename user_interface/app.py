import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import uvicorn

app = FastAPI()

FIBONACCI_API_URL = os.getenv("FIBONACCI_API_URL", "http://fibonacci_api:8001/fibonacci/")
MAX_INDEX = 1480  # Set the maximum index limit

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Fibonacci and Factorial</title>
        </head>
        <body style="background-color: #2d2d2d; color: white; font-family: Arial;">
            <h1>Enter the index for the Fibonacci number</h1>
            <form id="fibonacciForm">
                <input type="number" name="index" id="indexInput" min="0" max="1480" required>
                <label>
                    <input type="checkbox" id="noLimit" onclick="toggleInputType()"> Remove input restrictions
                </label>
                <button type="submit">Calculate</button>
            </form>
            <div id="result"></div>
            <script>
                function toggleInputType() {
                    const indexInput = document.getElementById('indexInput');
                    if (document.getElementById('noLimit').checked) {
                        indexInput.type = 'text';
                        indexInput.setAttribute('placeholder', 'Any input allowed');
                        indexInput.value = ''; 
                    } else {
                        indexInput.type = 'number';
                        indexInput.setAttribute('min', '0');
                        indexInput.setAttribute('max', '1480');
                        indexInput.setAttribute('placeholder', 'Only non-negative numbers (max 1480)');
                    }
                }

                document.getElementById('fibonacciForm').onsubmit = async function(event) {
                    event.preventDefault();
                    const indexInput = document.getElementById('indexInput').value;
                    const resultDiv = document.getElementById('result');

                    try {
                        const response = await fetch('/calculate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: new URLSearchParams({ 'index': indexInput })
                        });

                        if (response.ok) {
                            const data = await response.json();
                            resultDiv.innerHTML = `
                                <p>Fibonacci number: <b>${data.fibonacci}</b></p>
                                <p>Factorial of this number: <b>${data.factorial}</b></p>
                            `;
                        } else {
                            const errorData = await response.text();
                            resultDiv.innerHTML = `<p style="color: red;">${errorData}</p>`;
                        }
                    } catch (error) {
                        resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
                    }
                }
            </script>
        </body>
    </html>
    """

@app.post("/calculate", response_class=JSONResponse)
async def calculate(request: Request):
    data = await request.form()
    index_input = data.get("index")

    try:
        if index_input.isdigit() or (index_input.startswith('-') and index_input[1:].isdigit()):
            index = int(index_input)
        else:
            raise ValueError("Invalid input: Please enter a valid non-negative integer.")
        
        if index > MAX_INDEX:
            raise ValueError(f"Input exceeds maximum limit. Please enter a number less than or equal to {MAX_INDEX}.")

        response = requests.post(FIBONACCI_API_URL, json={"index": index})

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error calling Fibonacci API.")

        result = response.json()
        fibonacci_value = result["fibonacci"]
        factorial_value = result["factorial_response"]["factorial"]

        return {"fibonacci": fibonacci_value, "factorial": factorial_value}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8002
    uvicorn.run(app, host="0.0.0.0", port=port)
