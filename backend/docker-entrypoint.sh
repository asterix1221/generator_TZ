#!/bin/bash
set -e

echo "=== Generator TZ Backend Entrypoint ==="

# Wait for PostgreSQL to be ready using Python
echo "Waiting for PostgreSQL..."
python3 -c "
import asyncio
import asyncpg
import os

async def wait():
    dsn = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/generator_tz')
    for i in range(30):
        try:
            conn = await asyncpg.connect(dsn)
            await conn.close()
            print('PostgreSQL is ready!')
            return
        except Exception:
            if i % 5 == 0:
                print(f'Waiting for PostgreSQL... ({i+1}/30)')
            await asyncio.sleep(1)
    raise Exception('PostgreSQL not available after 30 seconds')

asyncio.run(wait())
"

# Wait for Redis to be ready using Python
echo "Waiting for Redis..."
python3 -c "
import asyncio
import redis.asyncio as aioredis
import os

async def wait():
    url = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
    for i in range(30):
        try:
            r = await aioredis.from_url(url)
            await r.ping()
            await r.close()
            print('Redis is ready!')
            return
        except Exception:
            if i % 5 == 0:
                print(f'Waiting for Redis... ({i+1}/30)')
            await asyncio.sleep(1)
    raise Exception('Redis not available after 30 seconds')

asyncio.run(wait())
"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head
echo "Migrations complete!"

# Start the application
echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000