from urllib.parse import urlparse


def normalize_domain(value: str) -> str:
    """'https://www.Acme.com/about' -> 'acme.com'. Used as the company de-duplication key."""
    v = value.strip().lower()
    if "://" not in v:
        v = "//" + v
    host = urlparse(v).hostname or ""
    if host.startswith("www."):
        host = host[4:]
    return host
