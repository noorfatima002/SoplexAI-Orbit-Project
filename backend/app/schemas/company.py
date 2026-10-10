from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.services.domain import normalize_domain


class CompanyCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=255)
    domain: str | None = Field(default=None, max_length=255)
    website: str | None = Field(default=None, max_length=500)
    industry: str | None = Field(default=None, max_length=100)
    size_range: str | None = Field(default=None, max_length=50)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    description: str | None = None
    source: str | None = Field(default=None, max_length=100)
    source_url: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def _derive_domain(self) -> "CompanyCreate":
        raw = self.domain or self.website
        if not raw:
            raise ValueError("Provide either 'domain' or 'website'")
        domain = normalize_domain(raw)
        if "." not in domain:
            raise ValueError("Could not derive a valid domain")
        self.domain = domain
        return self


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    domain: str
    website: str | None
    industry: str | None
    country: str | None
    source: str | None
    created_at: datetime
