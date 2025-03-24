import json
from typing import Any, Dict

def extract_valid_json(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts and returns only the valid JSON part from a response object.
    
    This function assumes that the response has a structure where the valid JSON
    is included in the 'content' field of the first choice's message, after the 
    closing "</think>" marker. Any markdown code fences (e.g. ```json) are stripped.

    Parameters:
        response (dict): The full API response object.

    Returns:
        dict: The parsed JSON object extracted from the content.
    
    Raises:
        ValueError: If no valid JSON can be parsed from the content.
    """
    # Navigate to the 'content' field; adjust if your structure differs.
    content = (
        response
        .get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    
    # Find the index of the closing </think> tag.
    marker = "</think>"
    idx = content.rfind(marker)
    
    if idx == -1:
        # If marker not found, try parsing the entire content.
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError("No </think> marker found and content is not valid JSON") from e
    
    # Extract the substring after the marker.
    json_str = content[idx + len(marker):].strip()
    
    # Remove markdown code fence markers if present.
    if json_str.startswith("```json"):
        json_str = json_str[len("```json"):].strip()
    if json_str.startswith("```"):
        json_str = json_str[3:].strip()
    if json_str.endswith("```"):
        json_str = json_str[:-3].strip()
    
    try:
        parsed_json = json.loads(json_str)
        return parsed_json
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse valid JSON from response content") from e
