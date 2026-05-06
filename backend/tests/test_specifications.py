"""Tests for specification API endpoints."""
import pytest
from httpx import AsyncClient


class TestSpecifications:
    """Specification endpoint tests."""

    async def test_generate_authorized(self, client: AsyncClient, auth_headers):
        """Test generating a spec as authorized user."""
        response = await client.post(
            "/specifications/generate",
            json={"type": "Web", "complexity": 1},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "Web"
        assert data["complexity"] == 1
        assert "id" in data
        assert data["user_id"] is not None

    async def test_generate_guest(self, client: AsyncClient):
        """Test generating a spec as guest (no auth)."""
        response = await client.post(
            "/specifications/generate",
            json={"type": "Mobile", "complexity": 2}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "Mobile"
        assert data["complexity"] == 2
        assert data["user_id"] is None

    async def test_generate_invalid_type(self, client: AsyncClient):
        """Test generating with invalid project type."""
        response = await client.post(
            "/specifications/generate",
            json={"type": "InvalidType", "complexity": 1}
        )
        assert response.status_code == 422

    async def test_generate_invalid_complexity(self, client: AsyncClient):
        """Test generating with invalid complexity level."""
        response = await client.post(
            "/specifications/generate",
            json={"type": "Web", "complexity": 5}
        )
        assert response.status_code == 422

    async def test_generate_negative_complexity(self, client: AsyncClient):
        """Test generating with negative complexity."""
        response = await client.post(
            "/specifications/generate",
            json={"type": "Web", "complexity": -1}
        )
        assert response.status_code == 422

    async def test_list_specs_authorized(self, client: AsyncClient, auth_headers, test_spec):
        """Test listing specs for authorized user."""
        response = await client.get("/specifications", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == test_spec.title

    async def test_list_specs_unauthorized(self, client: AsyncClient):
        """Test listing specs without auth."""
        response = await client.get("/specifications")
        assert response.status_code == 401

    async def test_get_spec_authorized(self, client: AsyncClient, auth_headers, test_spec):
        """Test getting a specific spec."""
        response = await client.get(f"/specifications/{test_spec.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == str(test_spec.id)

    async def test_get_spec_not_found(self, client: AsyncClient, auth_headers):
        """Test getting non-existent spec."""
        response = await client.get(
            "/specifications/00000000-0000-0000-0000-000000000000",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_get_spec_forbidden(self, client: AsyncClient, test_spec):
        """Test getting another user's spec."""
        from app.services.auth_service import create_access_token
        other_token = create_access_token({"sub": "other-user-id"})
        response = await client.get(
            f"/specifications/{test_spec.id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )
        assert response.status_code == 403

    async def test_update_spec_authorized(self, client: AsyncClient, auth_headers, test_spec):
        """Test updating spec title."""
        response = await client.put(
            f"/specifications/{test_spec.id}",
            json={"title": "Updated Title"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    async def test_update_spec_content(self, client: AsyncClient, auth_headers, test_spec):
        """Test updating spec content."""
        response = await client.put(
            f"/specifications/{test_spec.id}",
            json={"content": {"goal": "New goal"}},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["content"]["goal"] == "New goal"
        # Original content should be preserved and merged
        assert "description" in data["content"]

    async def test_update_spec_unauthorized(self, client: AsyncClient, test_spec):
        """Test updating spec without auth."""
        response = await client.put(
            f"/specifications/{test_spec.id}",
            json={"title": "Hacked"}
        )
        assert response.status_code == 401

    async def test_update_spec_forbidden(self, client: AsyncClient, test_spec):
        """Test updating another user's spec."""
        from app.services.auth_service import create_access_token
        other_token = create_access_token({"sub": "other-user-id"})
        response = await client.put(
            f"/specifications/{test_spec.id}",
            json={"title": "Hacked"},
            headers={"Authorization": f"Bearer {other_token}"}
        )
        assert response.status_code == 403

    async def test_delete_spec_authorized(self, client: AsyncClient, auth_headers, test_spec):
        """Test deleting spec."""
        response = await client.delete(f"/specifications/{test_spec.id}", headers=auth_headers)
        assert response.status_code == 204

    async def test_delete_spec_unauthorized(self, client: AsyncClient, test_spec):
        """Test deleting spec without auth."""
        response = await client.delete(f"/specifications/{test_spec.id}")
        assert response.status_code == 401

    async def test_delete_spec_not_found(self, client: AsyncClient, auth_headers):
        """Test deleting non-existent spec."""
        response = await client.delete(
            "/specifications/00000000-0000-0000-0000-000000000000",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_share_spec(self, client: AsyncClient, auth_headers, test_spec):
        """Test creating a share link."""
        response = await client.post(
            f"/specifications/{test_spec.id}/share",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "url" in data

    async def test_share_spec_unauthorized(self, client: AsyncClient, test_spec):
        """Test sharing spec without auth."""
        response = await client.post(f"/specifications/{test_spec.id}/share")
        assert response.status_code == 401

    async def test_share_spec_duplicate(self, client: AsyncClient, auth_headers, test_spec):
        """Test sharing already shared spec returns same link."""
        response1 = await client.post(f"/specifications/{test_spec.id}/share", headers=auth_headers)
        response2 = await client.post(f"/specifications/{test_spec.id}/share", headers=auth_headers)
        assert response1.json()["token"] == response2.json()["token"]

    async def test_generate_all_types(self, client: AsyncClient, auth_headers):
        """Test generating specs for all project types."""
        for ptype in ["Web", "Mobile", "Game", "Corp IS", "Other"]:
            response = await client.post(
                "/specifications/generate",
                json={"type": ptype, "complexity": 1},
                headers=auth_headers
            )
            assert response.status_code == 201, f"Failed for type: {ptype}"
            assert response.json()["type"] == ptype

    async def test_generate_all_complexities(self, client: AsyncClient, auth_headers):
        """Test generating specs for all complexity levels."""
        for level in [1, 2, 3, 4]:
            response = await client.post(
                "/specifications/generate",
                json={"type": "Web", "complexity": level},
                headers=auth_headers
            )
            assert response.status_code == 201, f"Failed for level: {level}"
            assert response.json()["complexity"] == level