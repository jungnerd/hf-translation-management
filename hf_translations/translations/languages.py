from enum import Enum, unique


@unique
class HFLanguages(Enum):
    """Languages supported by Hugging Face documentation translations.
    
    This enum contains common languages that HF repos typically support.
    The actual supported languages may vary by repository.
    """
    
    ar = "ar"  # Arabic
    bn = "bn"  # Bengali  
    de = "de"  # German
    es = "es"  # Spanish
    fa = "fa"  # Persian
    fr = "fr"  # French
    hi = "hi"  # Hindi
    it = "it"  # Italian
    ja = "ja"  # Japanese
    ko = "ko"  # Korean
    nl = "nl"  # Dutch
    pl = "pl"  # Polish
    pt = "pt"  # Portuguese
    ru = "ru"  # Russian
    te = "te"  # Telugu
    th = "th"  # Thai
    tr = "tr"  # Turkish
    vi = "vi"  # Vietnamese
    zh = "zh"  # Chinese Simplified
    zh_hant = "zh-hant"  # Chinese Traditional