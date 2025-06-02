import sys
import time
import logging
import requests
from typing import Optional, Dict, Any, Tuple, Annotated
from datetime import datetime

def check_youtube_intermediate(url: str = "https://www.youtube.com", 
                              timeout: int = 5) -> Dict[str, Any]:
    """
    Intermediate version: Better error handling, logging and returns detailed information
    
    Args:
        url: The URL to check (default: https://www.youtube.com)
        timeout: Connection timeout in seconds
        
    Returns:
        Dictionary with status information
    """
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger("youtube_checker")
    
    start_time = time.time()
    result = {
        "url": url,
        "is_up": False,
        "status_code": None,
        "response_time_ms": None,
        "error": None,
        "checked_at": datetime.now().isoformat()
    }
    
    try:
        logger.info(f"Checking status of {url}")
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        
        result["status_code"] = response.status_code
        result["response_time_ms"] = int((time.time() - start_time) * 1000)
        result["is_up"] = 200 <= response.status_code < 400
        
        if result["is_up"]:
            logger.info(f"YouTube is UP! Status code: {response.status_code}, " 
                      f"Response time: {result['response_time_ms']}ms")
        else:
            logger.warning(f"YouTube returned status code {response.status_code}, "
                         f"Response time: {result['response_time_ms']}ms")
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while connecting to {url}")
        result["error"] = "Connection timeout"
        
    except requests.exceptions.ConnectionError:
        logger.error(f"Could not connect to {url}")
        result["error"] = "Connection error"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        result["error"] = str(e)
        
    return result

if __name__ == "__main__":
    result = check_youtube_intermediate()
    print(result)

    with open("result.txt", "w") as f:
        for key, value in result.items():
            f.write(f"{key}: {value}\n")

    print(result)
