import datetime
import tempfile
from pathlib import Path

import requests
from git import Repo


class HFGitDocs:
    """Manage Hugging Face documentation repositories."""
    
    def __init__(self, repo_url: str = "https://github.com/huggingface/transformers.git") -> None:
        self.repo_url = repo_url
        self._repo: Repo | None = None
        self._repo_path: Path | None = None

    def clone_or_update(self) -> Path:
        """Clone or update the HF docs repository."""
        if self._repo_path is None:
            temp_dir = tempfile.mkdtemp(prefix="hf_docs_")
            self._repo_path = Path(temp_dir)
            self._repo = Repo.clone_from(self.repo_url, self._repo_path)
        else:
            if self._repo:
                self._repo.remotes.origin.pull()
        
        return self._repo_path

    def get_commit_date_for(self, file_path: str) -> datetime.datetime | None:
        """Get the last commit date for a specific file."""
        if not self._repo:
            return None
            
        try:
            commits = list(self._repo.iter_commits(paths=file_path, max_count=1))
            if commits:
                return commits[0].committed_datetime
        except Exception:
            pass
            
        return None

    def get_supported_languages(self) -> list[str]:
        """Get list of supported languages by checking docs directory."""
        if not self._repo_path:
            return []
            
        docs_path = self._repo_path / "docs" / "source"
        if not docs_path.exists():
            return []
            
        languages = []
        for item in docs_path.iterdir():
            if item.is_dir() and item.name != "en":
                languages.append(item.name)
                
        return sorted(languages)

    def cleanup(self) -> None:
        """Clean up temporary repository."""
        if self._repo_path and self._repo_path.exists():
            import shutil
            shutil.rmtree(self._repo_path, ignore_errors=True)
            self._repo_path = None
            self._repo = None