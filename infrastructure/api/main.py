import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()


async def number_stream(limit: int):
    for i in range(1, limit):
        yield json.dumps({"number": i}) + "\n"
        await asyncio.sleep(1)


@app.get("/numbers")
async def get_numbers(limit: int = 10):
    return StreamingResponse(
        number_stream(limit + 1), media_type="application/x-json-stream"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
