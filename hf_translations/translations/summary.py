import fnmatch
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pydantic import BaseModel, computed_field
from rich.progress import Progress, TaskID

from ..git import HFGitDocs
from .document import Document

base_docs_path = Path("docs/source")
"""The base path for HF documentation."""

en_docs_path = Path("docs/source/en") 
"""The base path for HF English documentation."""

restricted_list = [
    "*.png",
    "*.jpg", 
    "*.jpeg",
    "*.gif",
    "*.svg",
    "*/_toctree.yml",
    "*/README.md",
]
"""list[str]: Restricted files and patterns.

Files that should not be considered for translation.
"""


class Summary(BaseModel):
    """Summary of translation status for a specific language."""
    
    lang: str
    repo_url: str = "https://github.com/huggingface/transformers.git"
    files_analyzed: int = 0
    files_translated: int = 0
    files_outdated: int = 0
    files_missing_translation: int = 0
    files: list[Document] = []

    @computed_field  # type: ignore
    @property
    def percentage_translated(self) -> float:
        """Percentage of files that have been translated."""
        try:
            return (
                100 * float(self.files_translated) / float(self.files_analyzed)
            )
        except Exception:
            return 0.0

    @computed_field  # type: ignore
    @property
    def percentage_missing_translation(self) -> float:
        """Percentage of files missing translation."""
        try:
            return (
                100
                * float(self.files_missing_translation)
                / float(self.files_analyzed)
            )
        except Exception:
            return 0.0

    @computed_field  # type: ignore
    @property
    def percentage_outdated_translation(self) -> float:
        """Percentage of files with outdated translations."""
        try:
            return 100 * float(self.files_outdated) / float(self.files_analyzed)
        except Exception:
            return 0.0

    def generate(self) -> None:
        """Generate translation summary by analyzing documentation files."""
        git = HFGitDocs(self.repo_url)
        repo_path = git.clone_or_update()
        
        docs_path = repo_path / "docs" / "source" / "en"
        if not docs_path.exists():
            return
            
        with Progress() as progress:
            futures = []

            for root, _, files in os.walk(docs_path):
                if self._skip_directory(root):
                    continue

                task = progress.add_task(
                    f"🚶 Walking through 📂 {root} looking for 🔠 translations",
                    start=False,
                )
                with ThreadPoolExecutor(max_workers=50) as pool:
                    future = pool.submit(
                        self.process_file, git, repo_path, root, files, progress, task
                    )
                    futures.append(future)

            for future in futures:
                future.result()

        git.cleanup()

    def _skip_directory(self, directory: str) -> bool:
        """Check if directory should be skipped."""
        skip_patterns = ["*/img", "*/images", "*/_static", "*/js", "*/css"]
        for pattern in skip_patterns:
            if fnmatch.fnmatch(directory, pattern):
                return True
        return False

    def process_file(
        self,
        git: HFGitDocs,
        repo_path: Path,
        root_dir: str,
        files: list[str],
        progress: Progress,
        task: TaskID,
    ) -> None:
        """Process files in a directory for translation analysis."""
        progress.update(task, total=len(files))
        progress.start_task(task)

        for file in files:
            if file.endswith((".md", ".mdx", ".rst")):
                file_path = Path(root_dir) / file
                relative_path = file_path.relative_to(repo_path / "docs" / "source" / "en")
                
                if self.file_in_restricted_list(str(relative_path)):
                    progress.update(task, advance=1)
                    continue

                translated_path = repo_path / "docs" / "source" / self.lang / relative_path
                translation_exists = translated_path.exists()

                original_doc_date = git.get_commit_date_for(str(file_path))
                translated_date = git.get_commit_date_for(str(translated_path)) if translation_exists else None

                document = Document(
                    translation_lang=self.lang,
                    original_file=str(file_path),
                    original_commit=original_doc_date,
                    translation_file=str(translated_path),
                    translation_exists=translation_exists,
                    translation_commit=translated_date,
                )
                self.append_document(document)

            progress.update(task, advance=1)

    def file_in_restricted_list(self, file: str) -> bool:
        """Check if file should be excluded from translation."""
        for restricted in restricted_list:
            if fnmatch.fnmatch(file, restricted):
                return True
        return False

    def append_document(self, doc: Document) -> None:
        """Add document to summary and update counters."""
        self.files.append(doc)
        self.files_analyzed += 1

        if doc.translation_exists:
            self.files_translated += 1

        if not doc.translation_exists:
            self.files_missing_translation += 1

        if doc.translation_is_outdated:
            self.files_outdated += 1

    def first_outdated_files(self, length: int = 10) -> list[Document]:
        """Get first N outdated files."""
        return [d for d in self.files if d.translation_is_outdated][:length]

    def first_missing_translation_files(self, length: int = 10) -> list[Document]:
        """Get first N files missing translation."""
        return [d for d in self.files if not d.translation_exists][:length]