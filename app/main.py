from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="TicketBox API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}

html_template = """
<!DOCTYPE html>
<html>
    <head>
        <title>TicketBox API</title>
    </head>
    <body>
        <h1>TicketBox API</h1>
        <p>Welcome to the TicketBox API</p>
        <p>This is the root endpoint of the API</p>
        <p>Use the following endpoints to interact with the API:</p>
        <ul>
            <li><a href="/health">/health</a> - Check the health of the API</li>
            <li><a href="/docs">/docs</a> - OpenAPI documentation</li>
            <li><a href="/">Home</a> - This page</li>
        </ul>
    </body>
    
</html>
"""

@app.get("/")
def read_root():
    return HTMLResponse(content=html_template)
