from fastapi import APIRouter, Depends, HTTPException
import jwt
from typing import List

from api.controllers import reddits_controller
from api.exceptions import reddits_exceptions
from api.schemas import reddit_schema, subreddit_schema
from api.utils import auth_bearer
from api.models import jwt_bearer_model

router = APIRouter()
jwt_bearer = jwt_bearer_model.JWTBearer()


@router.get("/postsbysubreddit")
def get_posts(subreddit: str, category: str):
    try:
        return reddits_controller.get_posts_from_reddit(subreddit, category)
    
    except reddits_exceptions.RedditResultsNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except reddits_exceptions.RedditRequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except reddits_exceptions.RedditResponseError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error occurred")
    

@router.post("/redditsearches")
def create_reddit_search(reddit_search: reddit_schema.RedditSearchCreate):
    try:
        return reddits_controller.create_reddit_search(reddit_search.reddit, reddit_search.category, reddit_search.user_id)
    
    except reddits_exceptions.RedditDatabaseAccessError:
        raise HTTPException(status_code=500, detail="Error accessing the database")
    except reddits_exceptions.RedditValidationError:
        raise HTTPException(status_code=400, detail="Invalid parameters provided")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error occurred")
    

@router.post("/subredditsearches")
def create_subreddit_search(subreddit_search: List[subreddit_schema.SubredditSearchCreate]):
    try:
        return reddits_controller.create_subreddits_search(subreddit_search)
    
    except reddits_exceptions.RedditDatabaseAccessError as e:
        raise HTTPException(status_code=500, detail="Error accessing the database") from e
    except reddits_exceptions.RedditValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid parameters provided") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred") from e


@router.get("/history")
def get_recent_searches(jwt_token: str = Depends(jwt_bearer)):
    try:
        payload = auth_bearer.decodeJWT(jwt_token)
        user_id = payload['sub']
        return reddits_controller.get_history_searches_for_user(user_id)
    
    except reddits_exceptions.RedditDatabaseAccessError as e:
        raise HTTPException(status_code=500, detail="Error accessing the database") from e
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred") from e


@router.get("/history/{reddit_id}")
def get_recent_searches_for_user(reddit_id: int):
    try:
        return reddits_controller.get_history_posts_by_reddit_id(reddit_id)
    
    except reddits_exceptions.RedditDatabaseAccessError as e:
        raise HTTPException(status_code=500, detail="Error accessing the database") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred") from e
