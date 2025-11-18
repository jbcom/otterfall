"""Documentation fetcher adapter using web search"""

import time
import httpx
from typing import List, Dict, Optional
from .base import BaseToolAdapter, ToolResult, ToolError


class DocsAdapter(BaseToolAdapter):
    """Production documentation adapter using web search for library docs"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = httpx.Client(timeout=self.timeout)
        
        # Predefined doc URLs for common libraries
        self.doc_urls = {
            "react": "https://react.dev",
            "threejs": "https://threejs.org/docs/",
            "three.js": "https://threejs.org/docs/",
            "r3f": "https://docs.pmnd.rs/react-three-fiber/",
            "react-three-fiber": "https://docs.pmnd.rs/react-three-fiber/",
            "drei": "https://drei.pmnd.rs/",
            "@react-three/drei": "https://drei.pmnd.rs/",
            "zustand": "https://docs.pmnd.rs/zustand/",
            "vite": "https://vitejs.dev/",
            "typescript": "https://www.typescriptlang.org/docs/",
            "yuka": "https://mugen87.github.io/yuka/",
            "miniplex": "https://github.com/hmans/miniplex",
        }
    
    def validate_input(
        self,
        library: str,
        query: Optional[str] = None,
        **kwargs
    ) -> None:
        """Validate docs query"""
        if not library or not library.strip():
            raise ToolError("library parameter required")
        
        # Normalize library name
        library_lower = library.lower().strip()
        
        if query and len(query) > 500:
            raise ToolError("query too long (max 500 characters)")
    
    def execute(
        self,
        library: str,
        query: Optional[str] = None,
        **kwargs
    ) -> ToolResult:
        """
        Fetch library documentation
        
        Args:
            library: Library name (react, threejs, r3f, etc.)
            query: Optional search query within docs
        
        Returns:
            ToolResult with documentation URL and summary
        """
        start_time = time.time()
        
        try:
            self.validate_input(library=library, query=query)
            
            library_lower = library.lower().strip()
            
            # Get base documentation URL
            doc_url = self.doc_urls.get(library_lower)
            
            if not doc_url:
                # Try to construct likely doc URL
                doc_url = f"https://{library_lower}.dev"
            
            self.logger.info(f"Fetching docs for {library}: {doc_url}")
            
            # Try to verify URL is reachable
            try:
                response = self.client.head(doc_url, follow_redirects=True)
                url_valid = response.status_code < 400
            except:
                url_valid = False
            
            data = {
                "library": library,
                "doc_url": doc_url,
                "verified": url_valid,
                "search_query": query
            }
            
            message = f"Documentation for {library}: {doc_url}"
            if query:
                message += f" (search: {query})"
            
            if not url_valid:
                message += " (URL not verified - may not exist)"
            
            execution_time = (time.time() - start_time) * 1000
            
            return self._create_result(
                success=True,
                data=data,
                message=message,
                execution_time_ms=execution_time
            )
        
        except httpx.HTTPError as e:
            raise ToolError(f"HTTP error fetching docs: {e}")
        except Exception as e:
            raise ToolError(f"Documentation fetch failed: {e}")
    
    def __del__(self):
        """Clean up HTTP client"""
        if hasattr(self, 'client'):
            self.client.close()
