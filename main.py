from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import os
import datetime
import logging
import time
from typing import Dict

# DB path can be overridden for tests using SYNOVA_DB env var
DB = os.environ.get('SYNOVA_DB', 'synova.db')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title='Synova AI',
    description='AI chat system with multiple tiers',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc'
)

# Allow all origins for the demo (file:// frontends and local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_conn():
    # Check if we're running on Railway (PostgreSQL) or locally (SQLite)
    if os.environ.get('RAILWAY_ENVIRONMENT') or 'DATABASE_URL' in os.environ:
        import psycopg2
        from urllib.parse import urlparse

        # Get database URL from Railway's environment variable
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        # Retry mechanism for Railway database startup
        max_retries = 10
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                # Parse the database URL
                result = urlparse(db_url)

                # Extract connection parameters
                dbname = result.path[1:]  # Remove leading '/'
                user = result.username
                password = result.password
                host = result.hostname
                port = result.port or 5432  # Default PostgreSQL port

                # Connect to PostgreSQL
                conn = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    connect_timeout=10
                )
                logger.info(
                    "Successfully connected to PostgreSQL on attempt %d",
                    attempt + 1,
                )
                return conn

            except Exception as e:
                logger.warning(
                    "Database connection attempt %d failed: %s",
                    attempt + 1,
                    str(e),
                )
                if attempt < max_retries - 1:
                    logger.info("Retrying in %d seconds...", retry_delay)
                    time.sleep(retry_delay)
                else:
                    logger.error("Max retries reached. Database connection failed.")
                    raise e
    else:
        # Local SQLite connection
        return sqlite3.connect(DB)


def init_db():
    conn = get_conn()
    c = conn.cursor()

    # Check if we're using PostgreSQL
    is_postgres = 'psycopg2' in str(type(conn))

    if is_postgres:
        # PostgreSQL table creation
        c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            tier TEXT,
            query TEXT,
            response TEXT,
            timestamp TEXT
        )
        ''')
    else:
        # SQLite table creation
        c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tier TEXT,
            query TEXT,
            response TEXT,
            timestamp TEXT
        )
        ''')

    conn.commit()
    conn.close()


init_db()


class ChatRequest(BaseModel):
    query: str
    tier: str = 'terrestrial'


@app.get('/')
async def root():
    return FileResponse('static/index.html')

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/api/health')
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        conn = get_conn()
        conn.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "database": "disconnected",
            "error": str(e)
        }


@app.get('/api/stats')
async def get_stats():
    """Get application statistics"""
    try:
        conn = get_conn()
        c = conn.cursor()
        
        # Count messages by tier
        c.execute("SELECT tier, COUNT(*) FROM messages GROUP BY tier")
        tier_counts = dict(c.fetchall())
        
        # Get total messages
        c.execute("SELECT COUNT(*) FROM messages")
        total_messages = c.fetchone()[0]
        
        conn.close()
        
        return {
            "users_by_tier": tier_counts,
            "total_messages": total_messages,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Stats endpoint failed: {e}")
        return {
            "users_by_tier": {},
            "total_messages": 0,
            "error": str(e)
        }


@app.post('/api/chat')
async def chat(req: ChatRequest) -> Dict[str, str]:
    q = (req.query or '').strip()
    tier = (req.tier or 'terrestrial').lower()

    logger.info(
        "Received chat request - Tier: %s, Query: %s...",
        tier,
        q[:50],
    )

    if not q:
        logger.warning("Empty query received")
        raise HTTPException(status_code=400, detail='Empty query')

    tier_responses = {
        'terrestrial': {
            'greeting': (
                "Hello! I'm Synova Terrestrial, your free AI assistant. "
                "How can I help you today?"
            ),
            'default': "I'm a lightweight demo AI. Ask me about features, jokes, or facts!"
        },
        'aerial': {
            'greeting': "Hi — Aerial here. I give more detailed answers.",
            'default': "Aerial (pro) answer: I can go deeper on many topics."
        },
        'celestial': {
            'greeting': "Welcome, Celestial user. Premium responses engaged.",
            'default': (
                "Celestial (premium) answer: I'll provide the most detailed response I can."
            )
        }
    }

    ql = q.lower()
    if any(w in ql for w in ('hello', 'hi', 'hey')):
        response = tier_responses.get(tier, tier_responses['terrestrial'])['greeting']
    elif 'joke' in ql:
        response = "Why don't scientists trust atoms? Because they make up everything!"
    elif 'fact' in ql or 'interesting' in ql:
        response = "Fun fact: Octopuses have three hearts!"
    elif 'weather' in ql:
        response = (
            "I can't fetch live weather in this demo, but you can integrate a weather API for that feature."
        )
    else:
        response = tier_responses.get(tier, tier_responses['terrestrial'])['default']

    try:
        conn = get_conn()
        c = conn.cursor()

        # Check if we're using PostgreSQL for proper placeholder syntax
        is_postgres = 'psycopg2' in str(type(conn))

        if is_postgres:
            c.execute(
                'INSERT INTO messages (tier, query, response, timestamp) '
                'VALUES (%s,%s,%s,%s)',
                (tier, q, response, datetime.datetime.utcnow().isoformat()),
            )
        else:
            c.execute(
                'INSERT INTO messages (tier, query, response, timestamp) '
                'VALUES (?,?,?,?)',
                (tier, q, response, datetime.datetime.utcnow().isoformat()),
            )

        conn.commit()
        logger.info("Successfully saved message to database")

    except Exception as e:
        logger.error("Database error: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="Database operation failed",
        ) from e
    finally:
        if 'conn' in locals():
            conn.close()

    return {'response': response}


# Test helper endpoints
@app.post('/__test/clear')
def _test_clear():
    conn = get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return {'status': 'ok'}


@app.get('/__test/count')
def _test_count():
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM messages')
    n = c.fetchone()[0]
    conn.close()
    return {'count': n}
