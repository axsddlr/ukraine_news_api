import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.tweets_scrape import get_kyiv
from ratelimit import limits

app = FastAPI(
    title="Get Kyiv",
    description="Scrapes news about Ukraine Invasion",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TWO_MINUTES = 150


@limits(calls=250, period=TWO_MINUTES)
@app.get("/tweets/KyivIndependent", tags=["News"])
def ukraine_news():
    return get_kyiv()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
