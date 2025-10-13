#!/usr/bin/env python3
"""
Cache Performance Test Script
============================

Simple script to demonstrate and test Redis caching performance
in the Bio Supply Digital Twin system.

Usage:
    python cache_test.py

Features:
    - Tests API response times with and without caching
    - Shows cache hit/miss ratios
    - Demonstrates cache performance improvements
"""

import requests
import time

BASE_URL = "http://localhost:8001"

def test_basic_caching():
    """Test basic cache hit/miss behavior."""
    print("🎓 Learning Redis Cache Basics")
    print("=" * 40)
    
    # Step 1: Clear cache to start fresh
    print("\n1️⃣ Clearing cache...")
    requests.delete(f"{BASE_URL}/cache/clear")
    
    # Step 2: First request (should be CACHE MISS)
    print("\n2️⃣ First request (Cache MISS - slow):")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/stats")
    duration = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ⏱️  Response time: {duration*1000:.0f}ms")
        print(f"   📊 Data from: {'Cache' if data.get('from_cache') else 'Database'}")
        print(f"   📦 Boxes: {data['num_boxes']}, Samples: {data['num_samples']}")
    
    # Step 3: Second request (should be CACHE HIT)
    print("\n3️⃣ Second request (Cache HIT - fast):")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/stats")
    duration = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ⏱️  Response time: {duration*1000:.0f}ms")
        print(f"   � Data from: {'Cache' if data.get('from_cache') else 'Database'}")
        print(f"   ⚡ Much faster!")
    
    # Step 4: Wait for cache to expire (30 seconds)
    print(f"\n4️⃣ Cache expires in 30 seconds...")
    print("   (In real usage, you'd just wait, but let's clear it manually)")
    requests.delete(f"{BASE_URL}/cache/clear")
    
    # Step 5: Request after expiration (CACHE MISS again)
    print("\n5️⃣ After cache expired (Cache MISS again):")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/stats")
    duration = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ⏱️  Response time: {duration*1000:.0f}ms")
        print(f"   📊 Data from: {'Cache' if data.get('from_cache') else 'Database'}")

def show_cache_info():
    """Show cache statistics."""
    print("\n� Cache Information:")
    print("-" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/cache/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Status: {stats.get('status')}")
            print(f"   Memory Used: {stats.get('memory_used', 'N/A')}")
            print(f"   Total Keys: {stats.get('total_keys', 0)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("🚀 Redis Cache Learning Demo")
    print("Start services first: docker-compose up")
    print()
    
    # Wait for services
    print("⏳ Waiting for API...")
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✅ API is ready!")
                break
        except:
            time.sleep(1)
            if i == 9:
                print("❌ API not ready. Start with: docker-compose up")
                return
    
    # Run the demo
    test_basic_caching()
    show_cache_info()
    
    print("\n🎉 Demo complete!")
    print("\n💡 Key Redis concepts you just learned:")
    print("   • Cache MISS = slow (database query)")
    print("   • Cache HIT = fast (Redis memory lookup)")  
    print("   • TTL = cache expires after set time")
    print("   • Redis stores data in memory for speed")

if __name__ == "__main__":
    main()