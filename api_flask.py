import asyncio
from typing import Any, Dict

from flask import Flask, jsonify, request
from flasgger import Swagger

import main as scraper_main
from utils.logger import Logger


app = Flask(__name__)
swagger = Swagger(
    app,
    config={
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs",
    },
)


def ensure_logger() -> None:
    if not hasattr(scraper_main, "logger") or scraper_main.logger is None:
        logger_obj = Logger(level="DEBUG")
        scraper_main.logger = logger_obj.get_logger()


@app.route("/health", methods=["GET"]) 
def health() -> tuple[Dict[str, str], int]:
    return jsonify({"status": "ok"}), 200


@app.route("/run/keyword", methods=["POST"]) 
def run_with_keyword():
    """
    Run scraper with a simple keyword.
    ---
    tags:
      - run
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            query:
              type: string
              example: python developer
            limit:
              type: integer
              default: 50
              minimum: 1
              maximum: 200
            username:
              type: string
              description: Upwork username/email for login (optional)
              example: your_email@example.com
            password:
              type: string
              description: Upwork password for login (optional)
              example: your_password
    responses:
      200:
        description: Results returned
        schema:
          type: object
          properties:
            count:
              type: integer
            results:
              type: array
              items:
                type: object
      400:
        description: Bad request
      500:
        description: Internal error
    """
    try:
        payload = request.get_json(force=True, silent=False) or {}
        query = payload.get("query")
        if not query or not isinstance(query, str):
            return jsonify({"error": "Field 'query' (string) is required"}), 400
        limit = payload.get("limit", 50)
        try:
            limit = int(limit)
        except Exception:
            return jsonify({"error": "Field 'limit' must be an integer"}), 400
        # Extract optional credentials
        username = payload.get("username")
        password = payload.get("password")
        
        # Validate credentials if provided
        if username and not password:
            return jsonify({"error": "Username provided but password is missing"}), 400
        elif password and not username:
            return jsonify({"error": "Password provided but username is missing"}), 400
        
        ensure_logger()
        input_data: Dict[str, Any] = {
            "credentials": {"username": username, "password": password},
            "search": {"query": query, "limit": limit},
            "general": {"save_csv": True},
        }
        results = asyncio.run(scraper_main.main(input_data))
        return jsonify({"count": len(results), "results": results}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/run/advanced", methods=["POST"]) 
def run_with_advanced_filters():
    """
    Run scraper with advanced filters.
    ---
    tags:
      - run
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - query
          properties:
            query:
              type: string
              example: data engineering
            limit:
              type: integer
              default: 50
              minimum: 1
              maximum: 200
            category:
              type: array
              items:
                type: string
              example: ["data science & analytics"]
            hourly_min:
              type: integer
              example: 25
            hourly_max:
              type: integer
              example: 100
            hires_min:
              type: integer
              example: 1
            hires_max:
              type: integer
              example: 50
            payment_verified:
              type: boolean
              example: true
            hourly:
              type: boolean
              default: true
            fixed:
              type: boolean
              default: true
            sort:
              type: string
              enum: [relevance, newest, client_total_charge, client_rating]
              default: relevance
            username:
              type: string
              description: Upwork username/email for login (optional)
              example: your_email@example.com
            password:
              type: string
              description: Upwork password for login (optional)
              example: your_password
    responses:
      200:
        description: Results returned
        schema:
          type: object
          properties:
            count:
              type: integer
            results:
              type: array
              items:
                type: object
      400:
        description: Bad request
      500:
        description: Internal error
    """
    try:
        payload = request.get_json(force=True, silent=False) or {}
        query = payload.get("query")
        if not query or not isinstance(query, str):
            return jsonify({"error": "Field 'query' (string) is required"}), 400
        
        # Build search configuration
        search_config = {
            "query": query,
            "limit": payload.get("limit", 50)
        }
        
        # Add optional filters
        if "category" in payload and payload["category"]:
            search_config["category"] = payload["category"]
        if "hourly_min" in payload and payload["hourly_min"] is not None:
            search_config["hourly_min"] = int(payload["hourly_min"])
        if "hourly_max" in payload and payload["hourly_max"] is not None:
            search_config["hourly_max"] = int(payload["hourly_max"])
        if "hires_min" in payload and payload["hires_min"] is not None:
            search_config["hires_min"] = int(payload["hires_min"])
        if "hires_max" in payload and payload["hires_max"] is not None:
            search_config["hires_max"] = int(payload["hires_max"])
        if "payment_verified" in payload:
            search_config["payment_verified"] = bool(payload["payment_verified"])
        if "hourly" in payload:
            search_config["hourly"] = bool(payload["hourly"])
        if "fixed" in payload:
            search_config["fixed"] = bool(payload["fixed"])
        if "sort" in payload and payload["sort"]:
            search_config["sort"] = payload["sort"]
        
        # Extract optional credentials
        username = payload.get("username")
        password = payload.get("password")
        
        # Validate credentials if provided
        if username and not password:
            return jsonify({"error": "Username provided but password is missing"}), 400
        elif password and not username:
            return jsonify({"error": "Password provided but username is missing"}), 400
        
        ensure_logger()
        input_data: Dict[str, Any] = {
            "credentials": {"username": username, "password": password},
            "search": search_config,
            "general": {"save_csv": True},
        }
        results = asyncio.run(scraper_main.main(input_data))
        return jsonify({"count": len(results), "results": results}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/run/json", methods=["POST"]) 
def run_with_json():
    """
    Run scraper with full jsonInput structure.
    ---
    tags:
      - run
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            input:
              type: object
              example:
                credentials:
                  username: null
                  password: null
                search:
                  query: chatbot
                  limit: 10
                general:
                  save_csv: true
    responses:
      200:
        description: Results returned
        schema:
          type: object
          properties:
            count:
              type: integer
            results:
              type: array
              items:
                type: object
      400:
        description: Bad request
      500:
        description: Internal error
    """
    try:
        body = request.get_json(force=True, silent=False) or {}
        if not isinstance(body, dict):
            return jsonify({"error": "JSON body must be an object"}), 400
        if "input" not in body or not isinstance(body["input"], dict):
            return jsonify({"error": "Field 'input' (object) is required"}), 400
        ensure_logger()
        results = asyncio.run(scraper_main.main(body["input"]))
        return jsonify({"count": len(results), "results": results}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    # Run local dev server
    app.run(host="127.0.0.1", port=8000, debug=False)


