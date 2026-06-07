import os
from dotenv import load_dotenv
load_dotenv()
print("GOOGLE_CLIENT_ID:", os.getenv("GOOGLE_CLIENT_ID"))

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import create_tables, verify_database_connection, get_db, engine
from routes.analyze import router as analyze_router
from routes.auth import router as auth_router
from services.auth_service import GOOGLE_CLIENT_ID, log_google_client_id_on_startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Verify Supabase PostgreSQL connection on startup."""
    log_google_client_id_on_startup()

    frontend_client_id = os.getenv("VITE_GOOGLE_CLIENT_ID", "").strip()
    if frontend_client_id and GOOGLE_CLIENT_ID and frontend_client_id != GOOGLE_CLIENT_ID:
        print(
            "[auth] WARNING: Client ID mismatch — "
            f"VITE_GOOGLE_CLIENT_ID={frontend_client_id!r} "
            f"!= GOOGLE_CLIENT_ID={GOOGLE_CLIENT_ID!r}"
        )
    elif frontend_client_id and GOOGLE_CLIENT_ID:
        print("[auth] Frontend and backend Google client IDs match")

    try:
        verify_database_connection()
        create_tables()
        print("Database Connected Successfully")
        
        # Add startup log here
        with engine.connect() as connection:
            db_name = connection.execute(text("SELECT current_database()")).scalar()
            schema = connection.execute(text("SELECT current_schema()")).scalar()
            user = connection.execute(text("SELECT current_user")).scalar()
            host = engine.url.host
            print(f"--- DB STARTUP LOG ---")
            print(f"Host: {host}")
            print(f"Database: {db_name}")
            print(f"Schema: {schema}")
            print(f"User: {user}")
            print(f"----------------------")

    except ValueError as exc:
        print(f"Database configuration error: {exc}")
    except ConnectionError as exc:
        print(f"Database connection error: {exc}")
    except Exception as exc:
        print(f"Unexpected database error: {type(exc).__name__}: {exc}")

    yield


app = FastAPI(lifespan=lifespan)

# Enable CORS so our React frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the external routes
app.include_router(analyze_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Backend Running"}

@app.get("/debug/database")
def debug_database(db: Session = Depends(get_db)):
    try:
        current_db = db.execute(text("SELECT current_database()")).scalar()
        current_schema = db.execute(text("SELECT current_schema()")).scalar()
        current_user = db.execute(text("SELECT current_user")).scalar()
        users_count = db.execute(text("SELECT count(*) FROM users")).scalar()
        history_count = db.execute(text("SELECT count(*) FROM analysis_history")).scalar()
        
        return {
            "current_database": current_db,
            "current_schema": current_schema,
            "current_user": current_user,
            "users_count": users_count,
            "analysis_history_count": history_count
        }
    except Exception as e:
        return {"error": str(e)}
