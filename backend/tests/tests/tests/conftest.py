"""Test fixtures and configuration."""
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from unittest.mock import AsyncMock, patch

from app.main import app
from app.db.database import Base, get_db, engine
from app.models.models import User, Template, Specification, SharedLink
from app.core.config import get_settings


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for tests."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session():
    """Create a fresh in-memory SQLite database for each test."""
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    """Create test client with mocked DB session."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):
    """Create a test user."""
    from app.services.auth_service import get_password_hash
    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=get_password_hash("password123")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_template(db_session):
    """Create a test template."""
    template = Template(
        type="Web",
        complexity=1,
        structure={
            "goal": "Test goal",
            "description": "Test description",
            "functional_requirements": ["Req1", "Req2"],
            "db_requirements": ["DB1"],
            "tech_stack": ["Python", "FastAPI"],
            "features": ["Feature1"]
        }
    )
    db_session.add(template)
    await db_session.commit()
    await db_session.refresh(template)
    return template


@pytest_asyncio.fixture
async def auth_headers(client, test_user):
    """Get auth headers for test user."""
    from app.services.auth_service import create_access_token
    token = create_access_token({"sub": str(test_user.id), "email": test_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def test_spec(db_session, test_user, test_template):
    """Create a test specification."""
    spec = Specification(
        user_id=test_user.id,
        template_id=test_template.id,
        title="Test Spec",
        content=test_template.structure,
        type="Web",
        complexity=1
    )
    db_session.add(spec)
    await db_session.commit()
    await db_session.refresh(spec)
    return spec