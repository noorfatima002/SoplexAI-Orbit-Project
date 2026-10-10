import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_defaults_point_to_postgres():
    settings = Settings(_env_file=None)
    assert settings.database_url.startswith("postgresql")
    assert settings.is_production is False


def test_production_requires_real_secrets():
    with pytest.raises(ValidationError):
        Settings(app_env="production", api_key="", secret_key="", _env_file=None)
    with pytest.raises(ValidationError):
        Settings(app_env="production", api_key="change_me_dev_api_key", secret_key="x", _env_file=None)


def test_production_accepts_real_secrets():
    settings = Settings(app_env="production", api_key="a-real-key", secret_key="a-real-secret", _env_file=None)
    assert settings.is_production is True


def test_cors_origins_are_split():
    settings = Settings(cors_origins="http://a.com, http://b.com", _env_file=None)
    assert settings.cors_origin_list == ["http://a.com", "http://b.com"]
