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
    </body>
</html>
"""

@app.get("/")
def read_root():
    return HTMLResponse(content=html_template)
