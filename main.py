import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.get_kyiv import Kyiv
from api.cfr import Cfr
from api.bbc import BBC
from ratelimit import limits

app = FastAPI(
    title="Get Kyiv",
    description="Scrapes news about Ukraine Invasion",
    version="1.0.1",
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

# init classes
kyiv = Kyiv()
cfr = Cfr()
bbc = BBC()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/tweets/kyivindependent", tags=["Twitter"])
def kyiv_independent():
    return kyiv.get_kyiv()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/news/kyivindependent", tags=["News"])
def kyiv_independent_news():
    return kyiv.kyiv_news()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/news/cfr/ukraine", tags=["News"])
def global_conflict_tracker():
    return cfr.cfr_conflict_news()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/news/cfr/status", tags=["News"])
def global_conflict_tracker_status():
    return cfr.cfr_status()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/news/bbc/latest", tags=["News"])
def bbc_ukraine_latest_updates():
    return bbc.bbc_ukraine_news()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
