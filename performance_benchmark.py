#!/usr/bin/env python3
"""
Performance Benchmark Script for Smart Product Finder
Generates comprehensive performance metrics for PPT presentation
"""

import time
import requests
import json
import statistics
from datetime import datetime
from typing import List, Dict

# Configuration
BASE_URL = "https://productfinderai.org"
# BASE_URL = "http://localhost:5000"  # For local testing

class PerformanceBenchmark:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": base_url,
            "tests": []
        }
    
    def test_page_load(self, url: str, test_name: str, iterations: int = 10) -> Dict:
        """Test page load time"""
        print(f"\n🔍 Testing: {test_name}")
        times = []
        
        for i in range(iterations):
            try:
                start = time.time()
                response = requests.get(url, timeout=30)
                end = time.time()
                
                if response.status_code == 200:
                    times.append((end - start) * 1000)  # Convert to ms
                    print(f"  Iteration {i+1}: {times[-1]:.2f}ms")
                else:
                    print(f"  Iteration {i+1}: Failed (Status {response.status_code})")
            except Exception as e:
                print(f"  Iteration {i+1}: Error - {e}")
        
        if times:
            result = {
                "test_name": test_name,
                "url": url,
                "iterations": len(times),
                "avg_time_ms": round(statistics.mean(times), 2),
                "min_time_ms": round(min(times), 2),
                "max_time_ms": round(max(times), 2),
                "median_time_ms": round(statistics.median(times), 2),
                "std_dev_ms": round(statistics.stdev(times), 2) if len(times) > 1 else 0
            }
            print(f"  ✅ Average: {result['avg_time_ms']}ms")
            return result
        return None
    
    def test_api_endpoint(self, endpoint: str, method: str, data: Dict, test_name: str, iterations: int = 5) -> Dict:
        """Test API endpoint performance"""
        print(f"\n🔍 Testing API: {test_name}")
        times = []
        
        for i in range(iterations):
            try:
                start = time.time()
                if method == "POST":
                    response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=60)
                else:
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=30)
                end = time.time()
                
                if response.status_code == 200:
                    times.append((end - start) * 1000)
                    print(f"  Iteration {i+1}: {times[-1]:.2f}ms")
                else:
                    print(f"  Iteration {i+1}: Failed (Status {response.status_code})")
            except Exception as e:
                print(f"  Iteration {i+1}: Error - {e}")
        
        if times:
            result = {
                "test_name": test_name,
                "endpoint": endpoint,
                "method": method,
                "iterations": len(times),
                "avg_time_ms": round(statistics.mean(times), 2),
                "min_time_ms": round(min(times), 2),
                "max_time_ms": round(max(times), 2),
                "median_time_ms": round(statistics.median(times), 2)
            }
            print(f"  ✅ Average: {result['avg_time_ms']}ms")
            return result
        return None
