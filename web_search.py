import httpx
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class WebSearcher:
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev/search"
        
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search the web using Serper.dev API"""
        print(f"🔍 Starting web search for: '{query}'")
        
        if not self.api_key:
            print("❌ API key: MISSING - Web search disabled")
            return []
        else:
            print("✅ API key: PRESENT")
            
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "num": num_results
        }
        
        try:
            print(f"📡 Making API call to Serper.dev...")
            response = httpx.post(self.base_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if "organic" in data:
                for result in data["organic"]:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "link": result.get("link", ""),
                        "source": "web"
                    })
            
            print(f"✅ Web search returned {len(results)} results")
            
            if results:
                print("\n📄 Actual Search Results from Serper.dev:")
                for i, result in enumerate(results, 1):
                    print(f"{i}. Title: {result['title']}")
                    print(f"   Snippet: {result['snippet'][:100]}{'...' if len(result['snippet']) > 100 else ''}")
                    print(f"   URL: {result['link']}")
                    print()
            else:
                print("⚠️ No web information available for this query")
                
            return results
            
        except Exception as e:
            print(f"❌ Web search error: {e}")
            return []
    
    def format_search_results(self, results: List[Dict]) -> str:
        """Format web search results for context"""
        if not results:
            return ""
            
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"{i}. {result['title']}\n{result['snippet']}\nSource: {result['link']}")
        
        return "\n\n".join(formatted)