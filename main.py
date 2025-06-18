from app.utils.constants import GET_DETECTED_PIIS
from typing import Dict, List
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

# Create an MCP server
mcp = FastMCP()

@mcp.tool(GET_DETECTED_PIIS)
# @mcp.tool()
def get_detected_piis(text: str) -> List[Dict]:
    """
    Analyzes text for Personally Identifiable Information (PII) using regex patterns.

    This function scans the input text for common PII patterns including:
    - Email addresses
    - Phone numbers (US format: XXX-XXX-XXXX)
    - Social Security Numbers (XXX-XX-XXXX)
    - Credit card numbers (XXXX-XXXX-XXXX-XXXX)
    - IP addresses (IPv4)

    Args:
        text (str): The text content to be analyzed for PII entities.

    Returns:
        List[Dict]: A list of detected PII entities, sorted by their position in the text.
        Each dictionary contains:
            - type (str): Type of PII detected (EMAIL, PHONE, SSN, etc.)
            - value (str): The actual PII string found
            - start (int): Starting character position in the text
            - end (int): Ending character position in the text

    Example:
        >>> text = "Contact john.doe@email.com or 123-456-7890"
        >>> get_detected_piis(text)
        [
            {
                "type": "EMAIL",
                "value": "john.doe@email.com",
                "start": 8,
                "end": 25
            },
            {
                "type": "PHONE",
                "value": "123-456-7890",
                "start": 29,
                "end": 41
            }
        ]
    """
    import re

    pii_patterns = {
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'PHONE': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'SSN': r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
        'CREDIT_CARD': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        'IP_ADDRESS': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    }

    results = []
    for pii_type, pattern in pii_patterns.items():
        matches = re.finditer(pattern, text)
        for match in matches:
            results.append({
                'type': pii_type,
                'value': match.group(),
                'start': match.start(),
                'end': match.end()
            })
    
    return sorted(results, key=lambda x: x['start'])

@mcp.custom_route("/", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(
        transport='streamable-http',
        path="/zerotrusted-ai/pii-detection",
        port=80,
        )