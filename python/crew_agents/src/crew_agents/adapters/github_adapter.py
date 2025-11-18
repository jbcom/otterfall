"""GitHub adapter for API operations"""

import os
import time
import httpx
from typing import Optional, List
from .base import BaseToolAdapter, ToolResult, ToolError


class GitHubAdapter(BaseToolAdapter):
    """Production GitHub adapter using REST API"""
    
    def __init__(self, token: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.token = token or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        if not self.token:
            raise ToolError("GitHub token required (GITHUB_PERSONAL_ACCESS_TOKEN)")
        
        self.client = httpx.Client(
            base_url="https://api.github.com",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Rivermarsh-CrewAI"
            },
            timeout=self.timeout
        )
    
    def validate_input(
        self,
        action: str,
        repo: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> None:
        """Validate GitHub action and parameters"""
        allowed_actions = ["create_issue", "list_issues", "get_repo", "list_prs"]
        
        if action not in allowed_actions:
            raise ToolError(f"Action '{action}' not allowed. Allowed: {allowed_actions}")
        
        if action == "create_issue":
            if not repo:
                raise ToolError("repo parameter required for create_issue")
            if not title or len(title) < 1:
                raise ToolError("title must be non-empty")
            if len(title) > 256:
                raise ToolError("title too long (max 256 characters)")
            
            # Validate repo format (owner/repo)
            if "/" not in repo:
                raise ToolError("repo must be in format 'owner/repo'")
    
    def execute(
        self,
        action: str,
        repo: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        labels: Optional[List[str]] = None,
        **kwargs
    ) -> ToolResult:
        """
        Execute GitHub API action
        
        Args:
            action: API action to perform
            repo: Repository in format 'owner/repo'
            title: Issue title
            body: Issue body
            labels: Issue labels
        
        Returns:
            ToolResult with API response
        """
        start_time = time.time()
        
        try:
            self.validate_input(action=action, repo=repo, title=title)
            
            if action == "create_issue":
                payload = {"title": title}
                if body:
                    payload["body"] = body
                if labels:
                    payload["labels"] = labels
                
                self.logger.info(f"Creating GitHub issue in {repo}: {title}")
                
                response = self.client.post(
                    f"/repos/{repo}/issues",
                    json=payload
                )
                
                execution_time = (time.time() - start_time) * 1000
                
                if response.status_code == 201:
                    data = response.json()
                    return self._create_result(
                        success=True,
                        data={
                            "number": data["number"],
                            "url": data["html_url"],
                            "state": data["state"]
                        },
                        message=f"Issue #{data['number']} created successfully",
                        execution_time_ms=execution_time
                    )
                else:
                    return self._create_result(
                        success=False,
                        data=response.text,
                        message=f"GitHub API error: {response.status_code}",
                        execution_time_ms=execution_time
                    )
            
            elif action == "list_issues":
                response = self.client.get(f"/repos/{repo}/issues")
                execution_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    issues = response.json()
                    return self._create_result(
                        success=True,
                        data=[{
                            "number": i["number"],
                            "title": i["title"],
                            "state": i["state"]
                        } for i in issues[:10]],  # Limit to 10
                        message=f"Found {len(issues)} issues",
                        execution_time_ms=execution_time
                    )
                else:
                    return self._create_result(
                        success=False,
                        data=response.text,
                        message=f"Failed to list issues: {response.status_code}",
                        execution_time_ms=execution_time
                    )
            
            else:
                raise ToolError(f"Action '{action}' not implemented yet")
        
        except httpx.TimeoutException:
            raise ToolError(f"GitHub API request timed out after {self.timeout}s")
        except httpx.HTTPError as e:
            raise ToolError(f"GitHub API error: {e}")
        except Exception as e:
            raise ToolError(f"GitHub operation failed: {e}")
    
    def __del__(self):
        """Clean up HTTP client"""
        if hasattr(self, 'client'):
            self.client.close()
