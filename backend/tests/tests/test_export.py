"""Tests for export API endpoints and services."""
import pytest
from httpx import AsyncClient
from app.services.export_service import generate_docx, generate_pdf, generate_trello_json
from io import BytesIO


SAMPLE_SPEC = {
    "goal": "Test goal",
    "description": "Test description",
    "functional_requirements": ["Req1", "Req2"],
    "db_requirements": ["DB1", "DB2"],
    "tech_stack": ["Python", "FastAPI"],
    "features": ["Feature1", "Feature2", "Feature3"]
}


class TestExportService:
    """Unit tests for export service functions."""

    def test_generate_docx_success(self):
        """Test DOCX generation returns bytes."""
        result = generate_docx(SAMPLE_SPEC, "Test Title")
        assert isinstance(result, bytes)
        assert len(result) > 0
        # DOCX files start with PK (zip magic bytes)
        assert result[:2] == b'PK'

    def test_generate_docx_with_minimal_data(self):
        """Test DOCX generation with minimal data."""
        minimal = {"goal": "Test"}
        result = generate_docx(minimal, "Minimal")
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_generate_docx_with_empty_spec(self):
        """Test DOCX generation with empty spec."""
        result = generate_docx({}, "Empty")
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_generate_trello_json_success(self):
        """Test Trello JSON generation."""
        result = generate_trello_json(SAMPLE_SPEC, "Test Title")
        assert result["board_name"] == "TZ: Test Title"
        assert len(result["lists"]) == 3
        assert result["lists"][0]["name"] == "To Do"
        assert len(result["lists"][0]["cards"]) == 3

    def test_generate_trello_json_without_features(self):
        """Test Trello JSON when features list is empty."""
        spec = {"functional_requirements": ["FR1", "FR2", "FR3", "FR4", "FR5"]}
        result = generate_trello_json(spec, "No Features")
        # Should fall back to functional_requirements
        assert len(result["lists"][0]["cards"]) == 3

    def test_generate_trello_json_limited_features(self):
        """Test Trello JSON with fewer than 3 features."""
        spec = {"features": ["F1"]}
        result = generate_trello_json(spec, "Few")
        assert len(result["lists"][0]["cards"]) == 1

    def test_generate_trello_json_empty_everything(self):
        """Test Trello JSON with completely empty data."""
        result = generate_trello_json({}, "Empty")
        assert result["lists"][0]["cards"] == []
        assert result["lists"][1]["cards"] == []
        assert result["lists"][2]["cards"] == []


class TestExportAPI:
    """Integration tests for export API endpoints."""

    async def test_export_docx(self, client: AsyncClient, test_spec):
        """Test exporting spec as DOCX."""
        response = await client.get(f"/export/{test_spec.id}/docx")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        assert len(response.content) > 0

    async def test_export_pdf(self, client: AsyncClient, test_spec):
        """Test exporting spec as PDF."""
        response = await client.get(f"/export/{test_spec.id}/pdf")
        # PDF may fail in test env without weasyprint deps, but should return 200
        assert response.status_code == 200
        assert len(response.content) > 0

    async def test_export_trello(self, client: AsyncClient, test_spec):
        """Test exporting spec as Trello JSON."""
        response = await client.get(f"/export/{test_spec.id}/trello")
        assert response.status_code == 200
        data = response.json()
        assert "board_name" in data
        assert "lists" in data
        assert len(data["lists"]) == 3

    async def test_export_docx_not_found(self, client: AsyncClient):
        """Test exporting non-existent spec."""
        response = await client.get(
            "/export/00000000-0000-0000-0000-000000000000/docx"
        )
        assert response.status_code == 404

    async def test_export_pdf_not_found(self, client: AsyncClient):
        """Test PDF export non-existent spec."""
        response = await client.get(
            "/export/00000000-0000-0000-0000-000000000000/pdf"
        )
        assert response.status_code == 404

    async def test_export_trello_not_found(self, client: AsyncClient):
        """Test Trello export non-existent spec."""
        response = await client.get(
            "/export/00000000-0000-0000-0000-000000000000/trello"
        )
        assert response.status_code == 404