import json
import statistics

def handler(request):
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    # Parse request
    body = request.get_json()
    regions = body.get('regions', [])
    threshold_ms = body.get('threshold_ms', 180)
    
    # Load telemetry data from the JSON file
    with open('q-vercel-latency.json', 'r') as f:
        telemetry_data = json.load(f)
    
    # Calculate metrics per region
    results = {}
    for region in regions:
        region_records = [r for r in telemetry_data if r['region'] == region]
        
        if region_records:
            latencies = [r['latency_ms'] for r in region_records]
            uptimes = [r['uptime'] for r in region_records]
            
            results[region] = {
                'avg_latency': statistics.mean(latencies),
                'p95_latency': statistics.quantiles(latencies, n=20)[18],
                'avg_uptime': statistics.mean(uptimes),
                'breaches': sum(1 for l in latencies if l > threshold_ms)
            }
    
    return (json.dumps(results), 200, headers)
```

Click "Commit changes"

### **Step 3: Create Requirements File**

1. Click "Add file" → "Create new file"
2. Name it: `requirements.txt`
3. Paste:
```
fastapi==0.104.1
uvicorn==0.24.0
