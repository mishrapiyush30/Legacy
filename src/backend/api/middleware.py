import time
from fastapi import Request

# Global metrics (keeping for backward compatibility)
metrics = {
    "requests": 0,
    "search_requests": 0,
    "coach_requests": 0,
    "crisis_detected": 0,
    "gate_passed": 0,
    "gate_failed": 0,
    "latencies": [],
    "search_latencies": [],
    "coach_latencies": [],
}

async def add_metrics(request: Request, call_next):
    """Middleware to collect metrics."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Update metrics
    if request.url.path in ["/api/search_cases", "/api/coach"]:
        metrics["requests"] += 1
        metrics["latencies"].append(process_time * 1000)  # Convert to ms
        
        if request.url.path == "/api/search_cases":
            metrics["search_requests"] += 1
            metrics["search_latencies"].append(process_time * 1000)
        elif request.url.path == "/api/coach":
            metrics["coach_requests"] += 1
            metrics["coach_latencies"].append(process_time * 1000)
    
    return response 