import pytest
from sell_my_stuff.api.models.models import AnalyzeImageRequest, AnalyzeImageResponse


class TestAnalyzeImageRequest:
    """Test AnalyzeImageRequest model."""
    
    def test_valid_request(self):
        """Test valid request with image data."""
        request = AnalyzeImageRequest(image="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD")
        assert request.image == "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD"
    
    def test_missing_image(self):
        """Test request with missing image field."""
        with pytest.raises(ValueError):
            AnalyzeImageRequest()


class TestAnalyzeImageResponse:
    """Test AnalyzeImageResponse model."""
    
    def test_successful_response(self):
        """Test successful response with all fields."""
        response = AnalyzeImageResponse(
            success=True,
            message="Image analyzed successfully",
            description="A beautiful vintage item in excellent condition",
            suggested_price="$25 - $35"
        )
        assert response.success is True
        assert response.message == "Image analyzed successfully"
        assert response.description == "A beautiful vintage item in excellent condition"
        assert response.suggested_price == "$25 - $35"
    
    def test_response_with_optional_fields_none(self):
        """Test response with optional fields as None."""
        response = AnalyzeImageResponse(
            success=False,
            message="Analysis failed"
        )
        assert response.success is False
        assert response.message == "Analysis failed"
        assert response.description is None
        assert response.suggested_price is None
