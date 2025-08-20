import asyncio
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import main as scraper_main
from utils.logger import Logger


app = FastAPI(title="Upwork Job Scraper API", version="1.0.0")


class KeywordRequest(BaseModel):
    query: str = Field(..., description="Search keyword to query on Upwork")
    limit: int = Field(50, ge=1, le=200, description="Maximum number of jobs to return")
    username: Optional[str] = Field(None, description="Upwork username/email for login (optional)")
    password: Optional[str] = Field(None, description="Upwork password for login (optional)")


class AdvancedSearchRequest(BaseModel):
    query: str = Field(..., description="Search keyword to query on Upwork")
    limit: int = Field(50, ge=1, le=200, description="Maximum number of jobs to return")
    
    # Category filter
    category: Optional[list] = Field(None, description="Job categories", example=["web, mobile & software dev"])
    
    # Rate filters
    hourly_min: Optional[int] = Field(None, description="Minimum hourly rate", example=25)
    hourly_max: Optional[int] = Field(None, description="Maximum hourly rate", example=100)
    
    # Client filters
    hires_min: Optional[int] = Field(None, description="Minimum client hires", example=1)
    hires_max: Optional[int] = Field(None, description="Maximum client hires", example=50)
    payment_verified: Optional[bool] = Field(None, description="Payment verified clients only")
    
    # Job type filters
    hourly: Optional[bool] = Field(True, description="Include hourly jobs")
    fixed: Optional[bool] = Field(True, description="Include fixed-price jobs")
    
    # Sort options
    sort: Optional[str] = Field("relevance", description="Sort order", 
                               regex="^(relevance|newest|client_total_charge|client_rating)$")
    
    # Login credentials
    username: Optional[str] = Field(None, description="Upwork username/email for login (optional)")
    password: Optional[str] = Field(None, description="Upwork password for login (optional)")


class JsonInputRequest(BaseModel):
    input: Dict[str, Any] = Field(..., description="Full input JSON matching the CLI jsonInput structure")


@app.on_event("startup")
async def on_startup() -> None:
    # Initialize the logger inside the imported scraper module so its functions can use it
    if not hasattr(scraper_main, "logger") or scraper_main.logger is None:
        logger_obj = Logger(level="DEBUG")
        scraper_main.logger = logger_obj.get_logger()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/run/keyword")
async def run_with_keyword(payload: KeywordRequest) -> Dict[str, Any]:
    try:
        # Validate credentials if provided
        if payload.username and not payload.password:
            raise HTTPException(status_code=400, detail="Username provided but password is missing")
        elif payload.password and not payload.username:
            raise HTTPException(status_code=400, detail="Password provided but username is missing")
        
        input_data: Dict[str, Any] = {
            "credentials": {"username": payload.username, "password": payload.password},
            "search": {"query": payload.query, "limit": payload.limit},
            "general": {"save_csv": True},
        }
        results = await scraper_main.main(input_data)
        return {"count": len(results), "results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/run/advanced")
async def run_with_advanced_filters(payload: AdvancedSearchRequest) -> Dict[str, Any]:
    try:
        # Validate credentials if provided
        if payload.username and not payload.password:
            raise HTTPException(status_code=400, detail="Username provided but password is missing")
        elif payload.password and not payload.username:
            raise HTTPException(status_code=400, detail="Password provided but username is missing")
        
        # Build search configuration from advanced request
        search_config = {
            "query": payload.query,
            "limit": payload.limit
        }
        
        # Add optional filters
        if payload.category:
            search_config["category"] = payload.category
        if payload.hourly_min is not None:
            search_config["hourly_min"] = payload.hourly_min
        if payload.hourly_max is not None:
            search_config["hourly_max"] = payload.hourly_max
        if payload.hires_min is not None:
            search_config["hires_min"] = payload.hires_min
        if payload.hires_max is not None:
            search_config["hires_max"] = payload.hires_max
        if payload.payment_verified is not None:
            search_config["payment_verified"] = payload.payment_verified
        if payload.hourly is not None:
            search_config["hourly"] = payload.hourly
        if payload.fixed is not None:
            search_config["fixed"] = payload.fixed
        if payload.sort and payload.sort != "relevance":
            search_config["sort"] = payload.sort
        
        input_data: Dict[str, Any] = {
            "credentials": {"username": payload.username, "password": payload.password},
            "search": search_config,
            "general": {"save_csv": True},
        }
        results = await scraper_main.main(input_data)
        return {"count": len(results), "results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/run/json")
async def run_with_json(payload: JsonInputRequest) -> Dict[str, Any]:
    try:
        results = await scraper_main.main(payload.input)
        return {"count": len(results), "results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


