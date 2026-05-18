from zapv2 import ZAPv2
import time
import re

ZAP_ADDRESS = "127.0.0.1"
ZAP_PORT = 8080

zap = ZAPv2(
    apikey=None,
    proxies={
        "http": f"http://{ZAP_ADDRESS}:{ZAP_PORT}",
        "https": f"http://{ZAP_ADDRESS}:{ZAP_PORT}"
    }
)

def scan_website(url, mode="fast", progress_cb=None):
    """
    OWASP ZAP Scanner (FAST & FULL)
    progress_cb: function to update progress in scan_manager
    """

    if not url or not re.match(r"^https?://", url):
        return {"status": "failed", "error": "Invalid URL", "alerts": []}

    try:
        # -------- ACCESS TARGET --------
        zap.core.access_url(url, followredirects=True)
        time.sleep(1)

        # -------- SPIDER --------
        spider_id = zap.spider.scan(url)
        spider_timeout = 60
        start = time.time()

        while int(zap.spider.status(spider_id)) < 100:
            progress = int(zap.spider.status(spider_id))
            if progress_cb:
                progress_cb(spider=progress, ascan=0)
            if time.time() - start > spider_timeout:
                break
            time.sleep(1)

        # -------- PASSIVE --------
        while int(zap.pscan.records_to_scan) > 0:
            if progress_cb:
                progress_cb(spider=100, ascan=0)
            time.sleep(1)

        # -------- ACTIVE (OPTIONAL) --------
        if mode == "full":
            ascan_id = zap.ascan.scan(url, recurse=False)
            ascan_timeout = 90
            start = time.time()

            while int(zap.ascan.status(ascan_id)) < 100:
                progress = int(zap.ascan.status(ascan_id))
                if progress_cb:
                    progress_cb(spider=100, ascan=progress)
                if time.time() - start > ascan_timeout:
                    break
                time.sleep(2)

        # -------- COLLECT ALERTS --------
        zap_alerts = list(zap.core.alerts(baseurl=url))  # FIXED
        alerts = []

        for a in zap_alerts:
            alerts.append({
                "name": a.get("alert"),
                "risk": a.get("risk"),
                "confidence": a.get("confidence"),
                "description": a.get("description"),
                "solution": a.get("solution"),
                "reference": a.get("reference")
            })

        return {
            "status": "completed",
            "url": url,
            "scan_type": "FAST" if mode == "fast" else "FULL",
            "total_alerts": len(alerts),
            "alerts": alerts,
            "spiderProgress": 100,
            "ascanProgress": 100
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "alerts": [],
            "spiderProgress": 0,
            "ascanProgress": 0
        }
