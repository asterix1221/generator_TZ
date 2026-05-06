"""Tests for auth API endpoints."""
import pytest
from httpx import AsyncClient
from app.services.auth_service import create_access_token, get_password_hash


class TestAuth:
    """Authentication endpoint tests."""

    async def test_register_success(self, client: AsyncClient, db_session):
        """Test successful user registration."""
        response = await client.post("/auth/register", json={
            "email": "new@example.com",
            "name": "New User",
            "password": "password123"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["name"] == "New User"
        assert "id" in data
        assert "password_hash" not in data

    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        """Test registration with existing email."""
        response = await client.post("/auth/register", json={
            "email": test_user.email,
            "name": "Another",
            "password": "password123"
        })
        assert response.status_code == 400
        assert "уже существует" in response.json()["detail"]

    async def test_register_short_password(self, client: AsyncClient):
        """Test registration with short password."""
        response = await client.post("/auth/register", json={
            "email": "short@example.com",
            "name": "Short",
            "password": "ab"
        })
        assert response.status_code == 422

    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email."""
        response = await client.post("/auth/register", json={
            "email": "not-an-email",
            "name": "Test",
            "password": "password123"
        })
        assert response.status_code == 422

    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login."""
        response = await client.post("/auth/login", json={
            "email": test_user.email,
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Test login with wrong password."""
        response = await client.post("/auth/login", json={
            "email": test_user.email,
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert "Неверный" in response.json()["detail"]

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user."""
        response = await client.post("/auth/login", json={
            "email": "nobody@example.com",
            "password": "password123"
        })
        assert response.status_code == 401

    async def test_login_missing_fields(self, client: AsyncClient):
        """Test login with missing fields."""
        response = await client.post("/auth/login", json={})
        assert response.status_code == 422

    async def test_token_decode_valid(self, test_user):
        """Test JWT token decoding."""
        token = create_access_token({"sub": str(test_user.id), "email": test_user.email})
        from app.services.auth_service import decode_token
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == str(test_user.id)

    async def test_token_decode_invalid(self):
        """Test JWT token decoding with invalid token."""
        from app.services.auth_service import decode_token
        payload = decode_token("invalid.token.here")
        assert payload is None

    async def test_password_hashing(self):
        """Test password hashing and verification."""
        from app.services.auth_service import verify_password
        hashed = get_password_hash("test_password")
        assert hashed != "test_password"
        assert verify_password("test_password", hashed) is True
        assert verify_password("wrong", hashed) is False