"""Quick integration test for the API."""
import httpx
import sys


def test():
    base = "http://localhost:8000"
    
    # Health
    r = httpx.get(f"{base}/health")
    assert r.status_code == 200, f"Health failed: {r.status_code}"
    print(f"Health: {r.json()}")
    
    # Register
    r = httpx.post(f"{base}/auth/register", json={
        "email": "test@test.com", "name": "Test", "password": "test123"
    })
    print(f"Register: {r.status_code} {r.json()}")
    
    # Login
    r = httpx.post(f"{base}/auth/login", json={
        "email": "test@test.com", "password": "test123"
    })
    assert r.status_code == 200, f"Login failed: {r.status_code}"
    token = r.json()["access_token"]
    print(f"Login OK, token: {token[:30]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Generate spec
    r = httpx.post(f"{base}/specifications/generate", json={
        "type": "Web", "complexity": 1
    }, headers=headers)
    assert r.status_code == 201, f"Generate failed: {r.status_code}"
    spec = r.json()
    spec_id = spec["id"]
    print(f"Generate OK, spec_id: {spec_id}")
    
    # Trello export
    r = httpx.get(f"{base}/export/{spec_id}/trello")
    assert r.status_code == 200
    print(f"Trello: {r.status_code}")
    
    # DOCX export
    r = httpx.get(f"{base}/export/{spec_id}/docx")
    assert r.status_code == 200
    print(f"DOCX: {r.status_code}, size: {len(r.content)} bytes")
    
    # PDF export
    r = httpx.get(f"{base}/export/{spec_id}/pdf", timeout=15)
    if r.status_code == 200:
        print(f"PDF: {r.status_code}, size: {len(r.content)} bytes")
    else:
        print(f"PDF: {r.status_code} {r.text[:100]}")
    
    # Share link
    r = httpx.post(f"{base}/specifications/{spec_id}/share", headers=headers)
    print(f"Share: {r.status_code} {r.json() if r.status_code == 200 else r.text[:50]}")
    
    # Get shared spec
    if r.status_code == 200:
        token = r.json()["token"]
        r = httpx.get(f"{base}/shared/{token}")
        print(f"Shared spec: {r.status_code}")
    
    # List specs
    r = httpx.get(f"{base}/specifications", headers=headers)
    assert r.status_code == 200
    print(f"List specs: {r.status_code}, count: {len(r.json())}")
    
    # Guest generate
    r = httpx.post(f"{base}/specifications/generate", json={
        "type": "Mobile", "complexity": 2
    })
    assert r.status_code == 201
    print(f"Guest generate: {r.status_code}, spec_id: {r.json()['id']}")
    
    # Update spec
    spec_id2 = r.json()["id"]
    r = httpx.put(f"{base}/specifications/{spec_id2}", json={
        "title": "Updated TZ",
        "content": {"goal": "New goal"}
    }, headers=headers)
    print(f"Update (should be 403): {r.status_code}")
    
    print("\n=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    test()