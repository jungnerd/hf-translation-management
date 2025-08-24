from datetime import datetime

from pydantic import BaseModel, computed_field


class Document(BaseModel):
    """Represents a documentation file and its translation status."""
    
    official_lang: str = "en"
    translation_lang: str
    original_file: str
    original_commit: datetime | None
    translation_file: str | None = None
    translation_exists: bool
    translation_commit: datetime | None

    @computed_field  # type: ignore
    @property
    def translation_is_outdated(self) -> bool:
        """Check if translation is outdated compared to original."""
        if not self.original_commit or not self.translation_commit:
            return False

        return self.original_commit > self.translation_commit

    @computed_field  # type: ignore
    @property
    def needs_translation(self) -> bool:
        """Check if document needs translation."""
        return not self.translation_exists

    @computed_field  # type: ignore
    @property
    def status(self) -> str:
        """Get human-readable status of translation."""
        if not self.translation_exists:
            return "Missing"
        elif self.translation_is_outdated:
            return "Outdated" 
        else:
            return "Up-to-date"