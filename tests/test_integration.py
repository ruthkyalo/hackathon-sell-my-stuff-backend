import json
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sell_my_stuff.main import app


class TestAnalyzeImageAPI:
    """Integration tests for the analyze image API endpoint."""
    
    def test_analyze_image_endpoint_success(self, test_client, sample_image_base64):
        """Test the analyze image API endpoint with successful response."""
        # Mock Bedrock response
        mock_response = {
            'body': Mock(),
            'contentType': 'application/json'
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [
                {
                    'text': json.dumps({
                        'description': 'A beautiful vintage item in excellent condition.',
                        'suggested_price': '$25 - $35'
                    })
                }
            ]
        }).encode('utf-8')
        
        with patch('boto3.client') as mock_client:
            mock_bedrock = mock_client.return_value
            mock_bedrock.invoke_model.return_value = mock_response
            
            response = test_client.post(
                "/listings/analyze",
                json={
                    "image": f"data:image/jpeg;base64,{sample_image_base64}"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["message"] == "Image analyzed successfully"
            assert data["description"] == "A beautiful vintage item in excellent condition."
            assert data["suggested_price"] == "$25 - $35"
    
    def test_analyze_image_endpoint_invalid_image(self, test_client):
        """Test the analyze image API endpoint with invalid image data."""
        response = test_client.post(
            "/listings/analyze",
            json={
                "image": "invalid-base64-data"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Invalid image data" in data["detail"]
    
    def test_analyze_image_endpoint_missing_image(self, test_client):
        """Test the analyze image API endpoint with missing image field."""
        response = test_client.post(
            "/listings/analyze",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_root_endpoint(self, test_client):
        """Test the root endpoint."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Sell My Stuff API" in data["message"]
