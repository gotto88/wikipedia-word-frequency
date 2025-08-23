from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import structlog
import wikipediaapi

from src.models import RequestPost
from src.page_handler import PageHandler, RootPageNotFoundError
from src.wikipage_fetcher import WikiPageFetcher

logger = structlog.get_logger(__name__)

app = FastAPI(
    title="Word Frequency API",
    description="A REST API for calculating word frequencies from Wikipedia pages",
    version="1.0.0"
)

wiki_api = wikipediaapi.Wikipedia('Api-User-Agent', 'en')
wiki_fetcher = WikiPageFetcher(wiki_api=wiki_api)
page_handler = PageHandler(wiki_fetcher)


@app.get("/")
async def root():
    """
    Root endpoint that returns 200 OK
    """
    return {}


@app.head("/")
async def root_head():
    """
    HEAD endpoint that returns 200 OK
    """
    return {"status": "OK", "message": "Word Frequency API is running"}


@app.get("/word-frequency")
async def get_word_frequency(article: str, depth: int):
    """
    GET endpoint for calculating word frequencies

    Args:
        article: str, name of the article
        depth: int, depth of the look-up

    Returns:
        Dictionary containing word frequencies with count and percentage
    """
    try:
        logger.info("Processing word frequency request", article=article, depth=depth)

        result = page_handler.calculate_word_frequency(
            page_name=article,
            depth=depth
        )
        logger.info(
            "Word frequency calculation completed",
            article=article,
            word_count=len(result)
        )
        return JSONResponse(
            status_code=200,
            content=result
        )

    except RootPageNotFoundError as error:
        logger.error(
            "Root page not found",
            article=article,
            error=str(error)
        )
        raise HTTPException(status_code=404, detail=f"Article '{article}' not found")

    except Exception as error:
        logger.error(
            "Unexpected error while calculating word frequency",
            article=article,
            error=str(error)
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/keywords")
async def post_keywords(request: RequestPost):
    """
    POST endpoint for calculating word frequencies with additional parameters

    Args:
        request: RequestPost model containing article, depth, ignore_list, and percentile

    Returns:
        Dictionary containing word frequencies with count and percentage
    """
    try:
        logger.info(
            "Processing keywords request",
            article=request.article,
            depth=request.depth,
        )
        result: dict[str, dict[str, int | float]] = page_handler.calculate_word_frequency(
            page_name=request.article,
            depth=request.depth,
            ignore_list=request.ignore_list,
            percentile=request.percentile
        )
        logger.info(
            "Keywords calculation completed",
            article=request.article,
            word_count=len(result)
        )
        return JSONResponse(
            status_code=200,
            content=result
        )
    except RootPageNotFoundError as error:
        logger.error(
            "Root page not found",
            article=request.article,
            error=str(error)
        )
        raise HTTPException(status_code=404, detail=f"Article '{request.article}' not found")
    except Exception as error:
        logger.error(
            "Error calculating keywords",
            article=request.article,
            error=str(error)
        )
        raise HTTPException(status_code=500, detail="Internal server error")
