from fastapi import FastAPI, Request, Response

from api.v1 import users_router, tasks_router

app = FastAPI()
app.include_router(tasks_router)
app.include_router(users_router)

@app.get("/")
def health():
    return {"message": "I'am alive"}

@app.post("/debug")
async def debug(request: Request):
    body = await request.body()
    body = body.decode("utf-8")
    json_data = await request.json()
    query_params = dict(request.query_params)
    headers = dict(request.headers)
    ip = request.client.host

    return {"ip": ip, "body": body, "query_params": query_params, "headers": headers, "json_data": json_data}

