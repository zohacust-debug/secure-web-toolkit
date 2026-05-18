import threading
import uuid
from services.zap_scanner import scan_website

# Dictionary to store scan results and progress
scan_results = {}

def start_scan(scan_id, url):
    """
    Starts a scan in a separate thread and saves result in scan_results
    """
    # Set initial status
    scan_results[scan_id] = {
        "status": "running",
        "spiderProgress": 0,
        "ascanProgress": 0,
        "alerts": []
    }

    # Run scan in a thread
    def run_scan():
        try:
            result = scan_website(url)

            # Save final result
            scan_results[scan_id] = result
        except Exception as e:
            scan_results[scan_id] = {
                "status": "failed",
                "error": str(e),
                "spiderProgress": 0,
                "ascanProgress": 0,
                "alerts": []
            }

    thread = threading.Thread(target=run_scan)
    thread.start()


def create_scan(url):
    """
    Create a new scan and return its unique ID
    """
    scan_id = str(uuid.uuid4())
    start_scan(scan_id, url)
    return scan_id


def get_scan_status(scan_id):
    """
    Retrieve the current status or result of a scan
    """
    return scan_results.get(scan_id, {"status": "running"})
