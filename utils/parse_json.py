import json
import re
from typing import Any, Dict

def extract_and_inject_json(completion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts the valid JSON portion from the 'content' field in the first choice's message
    of the completion object and injects the parsed JSON back into that message.
    
    This function handles cases where the content may include extraneous text such as 
    markdown code fences (e.g., "```json"), additional text before/after the JSON, or
    other noise. If the JSON is present and valid, it will be extracted; if it is malformed,
    an error will be raised.
    
    Parameters:
        completion (dict): The completion object containing a "choices" list with a message.
    
    Returns:
        dict: The updated completion object with the "content" field replaced by the parsed JSON.
    
    Raises:
        ValueError: If no valid JSON can be extracted or parsed.
    """
    try:
        # Retrieve the raw content from the first choice's message.
        raw_content: str = completion["choices"][0]["message"]["content"]
        raw_content = raw_content.strip()
        
        # Remove markdown code fences if present.
        if raw_content.startswith("```"):
            lines = raw_content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_content = "\n".join(lines).strip()
        
        # Try extracting JSON using the first and last brace positions.
        start = raw_content.find("{")
        end = raw_content.rfind("}")
        json_candidate = None
        if start != -1 and end != -1 and start < end:
            json_candidate = raw_content[start:end+1].strip()
        
        # If substring extraction failed or candidate is unparseable, try regex fallback.
        if json_candidate:
            try:
                parsed_json = json.loads(json_candidate)
            except json.JSONDecodeError:
                match = re.search(r"({.*})", raw_content, re.DOTALL)
                if match:
                    json_candidate = match.group(1).strip()
                    parsed_json = json.loads(json_candidate)
                else:
                    raise ValueError("No valid JSON object found via regex.")
        else:
            match = re.search(r"({.*})", raw_content, re.DOTALL)
            if match:
                json_candidate = match.group(1).strip()
                parsed_json = json.loads(json_candidate)
            else:
                raise ValueError("No JSON object found in content.")
        
        # Inject the parsed JSON back into the completion object.
        completion["choices"][0]["message"]["content"] = parsed_json
        return completion
    except Exception as e:
        raise ValueError(f"Error extracting valid JSON from content: {e}")
