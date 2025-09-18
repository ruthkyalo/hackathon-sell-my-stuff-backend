import json
import pytest
import boto3
from unittest.mock import patch, Mock
from fastapi import HTTPException
from sell_my_stuff.api.endpoints.listings import analyze_image
from sell_my_stuff.api.models.models import AnalyzeImageRequest


class TestAnalyzeImage:
    """Test analyze_image endpoint."""
    
    @pytest.mark.anyio
    async def test_analyze_image_success(self, sample_image_base64):
        """Test successful image analysis."""
        request = AnalyzeImageRequest(
            image=f"data:image/jpeg;base64,{sample_image_base64}"
        )
        
        # Mock Bedrock response
        mock_response = {
            'body': Mock(),
            'contentType': 'application/json'
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [
                {
                    'text': json.dumps({
                        'description': 'A vintage leather jacket in excellent condition, perfect for a stylish look.',
                        'suggested_price': '$50 - $75'
                    })
                }
            ]
        }).encode('utf-8')
        
        with patch('boto3.client') as mock_client:
            mock_bedrock = mock_client.return_value
            mock_bedrock.invoke_model.return_value = mock_response
            
            response = await analyze_image(request)
            
            assert response.success is True
            assert response.message == "Image analyzed successfully"
            assert response.description == "A vintage leather jacket in excellent condition, perfect for a stylish look."
            assert response.suggested_price == "$50 - $75"
    
    @pytest.mark.anyio
    async def test_analyze_image_invalid_base64(self):
        """Test image analysis with invalid base64 data."""
        request = AnalyzeImageRequest(
            image="invalid-base64-data"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await analyze_image(request)
        
        assert exc_info.value.status_code == 400
        assert "Invalid image data" in str(exc_info.value.detail)
    
    @pytest.mark.anyio
    async def test_analyze_image_bedrock_failure(self, sample_image_base64):
        """Test image analysis when Bedrock fails."""
        request = AnalyzeImageRequest(
            image=f"data:image/jpeg;base64,{sample_image_base64}"
        )
        
        with patch('boto3.client') as mock_client:
            mock_bedrock = mock_client.return_value
            mock_bedrock.invoke_model.side_effect = Exception("Bedrock service error")
            
            with pytest.raises(HTTPException) as exc_info:
                await analyze_image(request)
            
            assert exc_info.value.status_code == 500
            assert "Failed to analyze image with Bedrock" in str(exc_info.value.detail)
    
    @pytest.mark.anyio
    async def test_analyze_image_invalid_json_response(self, sample_image_base64):
        """Test image analysis when Bedrock returns invalid JSON."""
        request = AnalyzeImageRequest(
            image=f"data:image/jpeg;base64,{sample_image_base64}"
        )
        
        # Mock Bedrock response with invalid JSON
        mock_response = {
            'body': Mock(),
            'contentType': 'application/json'
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [
                {
                    'text': 'This is not valid JSON'
                }
            ]
        }).encode('utf-8')
        
        with patch('boto3.client') as mock_client:
            mock_bedrock = mock_client.return_value
            mock_bedrock.invoke_model.return_value = mock_response
            
            with pytest.raises(HTTPException) as exc_info:
                await analyze_image(request)
            
            assert exc_info.value.status_code == 500
            assert "Failed to parse AI response as JSON" in str(exc_info.value.detail)
