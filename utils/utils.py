import re


def extract_phone_from_vcf(vcf: str) -> str | None:
    m = re.search(r"^TEL(?:;[^:]*)?:(.+)$", vcf, flags=re.MULTILINE | re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).strip()  # например: 79878217816 или tel:+7...
    return re.sub(r"[^\d+]", "", raw)