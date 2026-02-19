import httpx

SAFE_DOMAINS = [
    "wikipedia.org",
    "archive.org",
    "github.com",
]

async def search_query(q, limit=10):
    # Minimal safe search via DuckDuckGo Instant Answer API as a placeholder
    url = "https://api.duckduckgo.com/"
    params = {"q": q, "format": "json", "no_html": 1, "skip_disambig": 1}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        data = r.json()
    results = []
    if 'RelatedTopics' in data:
        for item in data['RelatedTopics'][:limit]:
            if isinstance(item, dict):
                text = item.get('Text')
                href = item.get('FirstURL')
                if href and any(d in href for d in SAFE_DOMAINS):
                    results.append({"title": text, "url": href})
    return results
