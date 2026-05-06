"""Test fixtures."""
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db.database import Base, get_db
from app.models.models import User, Template, Specification, SharedLink

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/generator_tz_test"


@pytest_asyncio.fixture(scope="function")
async def engine():
    """Per-test engine to avoid asyncpg/SQLAlchemy loop mismatch."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine):
    """Per-test session with rollback."""
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.connect() as conn:
        await conn.begin()
        async with async_session(bind=conn) as session:
            yield session
        await conn.rollback()


@pytest_asyncio.fixture
async def client(engine, db_session):
    """Test client with DB override (use same db_session as fixtures)."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # FastAPI/Starlette lifespan will call app.main.lifespan -> init_db()
    # In unit tests we don't want it.
    # httpx ASGITransport in your environment doesn't support lifespan="off",
    # so we disable lifespan via app router context.
    app.router.lifespan_context = lambda _app: None

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):
    from app.services.auth_service import get_password_hash

    # Ensure deterministic state even if previous tests left data behind
    # (email column is unique).
    await db_session.execute(
        User.__table__.delete().where(User.email == "test@example.com")
    )

    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=get_password_hash("password123"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_template(db_session):
    template = Template(type="Web", complexity=1, structure={
        "goal": "Test goal", "description": "Test description",
        "functional_requirements": ["Req1", "Req2"],
        "db_requirements": ["DB1"], "tech_stack": ["Python"],
        "features": ["Feature1"]
    })
    db_session.add(template)
    await db_session.commit()
    await db_session.refresh(template)
    return template


@pytest_asyncio.fixture
async def auth_headers(test_user):
    from app.services.auth_service import create_access_token
    token = create_access_token({"sub": str(test_user.id), "email": test_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def test_spec(db_session, test_user, test_template):
    spec = Specification(user_id=test_user.id, template_id=test_template.id,
                         title="Test Spec", content=test_template.structure,
                         type="Web", complexity=1)
    db_session.add(spec)
    await db_session.commit()
    await db_session.refresh(spec)
    return spec