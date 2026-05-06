"""Tests for public/shared link API endpoints."""
import pytest
from httpx import AsyncClient


class TestPublic:
    """Public endpoint tests."""

    async def test_get_shared_spec(self, client: AsyncClient, auth_headers, test_spec):
        """Test getting a spec via shared link."""
        # First create a shared link
        share_resp = await client.post(
            f"/specifications/{test_spec.id}/share",
            headers=auth_headers
        )
        token = share_resp.json()["token"]

        # Now access via shared link
        response = await client.get(f"/shared/{token}")
        assert response.status_code == 200
        assert response.json()["title"] == test_spec.title

    async def test_get_shared_spec_invalid_token(self, client: AsyncClient):
        """Test getting spec with invalid token."""
        response = await client.get("/shared/invalid-token-12345")
        assert response.status_code == 404
        assert "недействительна" in response.json()["detail"]

    async def test_get_shared_spec_no_auth_required(self, client: AsyncClient, auth_headers, test_spec):
        """Test shared link works without authentication."""
        share_resp = await client.post(
            f"/specifications/{test_spec.id}/share",
            headers=auth_headers
        )
        token = share_resp.json()["token"]

        # Access without auth headers
        response = await client.get(f"/shared/{token}")
        assert response.status_code == 200

    async def test_shared_link_deleted_spec(self, client: AsyncClient, auth_headers, test_spec):
        """Test accessing shared link after spec deletion."""
        share_resp = await client.post(
            f"/specifications/{test_spec.id}/share",
            headers=auth_headers
        )
        token = share_resp.json()["token"]

        # Delete the spec
        await client.delete(f"/specifications/{test_spec.id}", headers=auth_headers)

        # Try to access shared link
        response = await client.get(f"/shared/{token}")
        assert response.status_code == 404

    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Generator TZ API"

    async def test_health_endpoint(self, client: AsyncClient):
        """Test health endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"