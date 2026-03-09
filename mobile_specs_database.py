"""
Mobile Phone Specifications Database
Fallback database for popular phone models when API descriptions are insufficient
"""

MOBILE_SPECS_DB = {
    # OnePlus Models
    "oneplus nord 5": {
        "processor": "Snapdragon 8s Gen 3",
        "battery": "5200mAh",
        "display": "6.83 inch AMOLED 144Hz",
        "camera": "50MP Dual Camera",
        "connectivity": "5G"
    },
    "oneplus nord ce5": {
        "processor": "Snapdragon 7s Gen 2",
        "battery": "5110mAh",
        "display": "6.67 inch AMOLED 120Hz",
        "camera": "50MP Dual Camera",
        "connectivity": "5G"
    },
    "oneplus nord 4": {
        "processor": "Snapdragon 8s Gen 3",
        "battery": "5500mAh",
        "display": "6.74 inch AMOLED 120Hz",
        "camera": "50MP Dual Camera",
        "connectivity": "5G"
    },
    "oneplus 12": {
        "processor": "Snapdragon 8 Gen 3",
        "battery": "5400mAh",
        "display": "6.82 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    "oneplus 11": {
        "processor": "Snapdragon 8 Gen 2",
        "battery": "5000mAh",
        "display": "6.7 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    
    # Samsung Galaxy S Series
    "samsung galaxy s24 ultra": {
        "processor": "Snapdragon 8 Gen 3",
        "battery": "5000mAh",
        "display": "6.8 inch AMOLED 120Hz",
        "camera": "200MP Quad Camera",
        "connectivity": "5G"
    },
    "samsung galaxy s24": {
        "processor": "Exynos 2400",
        "battery": "4000mAh",
        "display": "6.2 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    "samsung galaxy s23": {
        "processor": "Snapdragon 8 Gen 2",
        "battery": "3900mAh",
        "display": "6.1 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    
    # Samsung Galaxy A Series
    "samsung galaxy a55": {
        "processor": "Exynos 1480",
        "battery": "5000mAh",
        "display": "6.6 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    "samsung galaxy a35": {
        "processor": "Exynos 1380",
        "battery": "5000mAh",
        "display": "6.6 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    
    # iPhone Models
    "iphone 15 pro max": {
        "processor": "A17 Pro Bionic",
        "battery": "4422mAh",
        "display": "6.7 inch Super Retina XDR",
        "camera": "48MP Triple Camera",
        "connectivity": "5G"
    },
    "iphone 15 pro": {
        "processor": "A17 Pro Bionic",
        "battery": "3274mAh",
        "display": "6.1 inch Super Retina XDR",
        "camera": "48MP Triple Camera",
        "connectivity": "5G"
    },
    "iphone 15": {
        "processor": "A16 Bionic",
        "battery": "3349mAh",
        "display": "6.1 inch Super Retina XDR",
        "camera": "48MP Dual Camera",
        "connectivity": "5G"
    },
    "iphone 14": {
        "processor": "A15 Bionic",
        "battery": "3279mAh",
        "display": "6.1 inch Super Retina XDR",
        "camera": "12MP Dual Camera",
        "connectivity": "5G"
    },
    
    # Xiaomi Redmi Note Series
    "redmi note 13 pro": {
        "processor": "Snapdragon 7s Gen 2",
        "battery": "5100mAh",
        "display": "6.67 inch AMOLED 120Hz",
        "camera": "200MP Triple Camera",
        "connectivity": "5G"
    },
    "redmi note 13": {
        "processor": "Snapdragon 685",
        "battery": "5000mAh",
        "display": "6.67 inch AMOLED 120Hz",
        "camera": "108MP Triple Camera",
        "connectivity": "4G"
    },
    "redmi note 12": {
        "processor": "Snapdragon 4 Gen 1",
        "battery": "5000mAh",
        "display": "6.67 inch AMOLED 120Hz",
        "camera": "48MP Triple Camera",
        "connectivity": "5G"
    },
    
    # Realme Models
    "realme 12 pro": {
        "processor": "Snapdragon 6 Gen 1",
        "battery": "5000mAh",
        "display": "6.7 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    "realme 11 pro": {
        "processor": "Dimensity 7050",
        "battery": "5000mAh",
        "display": "6.7 inch AMOLED 120Hz",
        "camera": "100MP Dual Camera",
        "connectivity": "5G"
    },
    
    # Vivo Models
    "vivo v30": {
        "processor": "Snapdragon 7 Gen 3",
        "battery": "5000mAh",
        "display": "6.78 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    "vivo v29": {
        "processor": "Snapdragon 778G",
        "battery": "4600mAh",
        "display": "6.78 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    
    # Oppo Models
    "oppo reno 11": {
        "processor": "Dimensity 7050",
        "battery": "5000mAh",
        "display": "6.7 inch AMOLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    "oppo f25": {
        "processor": "Dimensity 7050",
        "battery": "5000mAh",
        "display": "6.67 inch AMOLED 120Hz",
        "camera": "64MP Triple Camera",
        "connectivity": "5G"
    },
    
    # Google Pixel
    "google pixel 8 pro": {
        "processor": "Google Tensor G3",
        "battery": "5050mAh",
        "display": "6.7 inch OLED 120Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    "google pixel 8": {
        "processor": "Google Tensor G3",
        "battery": "4575mAh",
        "display": "6.2 inch OLED 120Hz",
        "camera": "50MP Dual Camera",
        "connectivity": "5G"
    },
    
    # Motorola
    "motorola edge 50": {
        "processor": "Snapdragon 7 Gen 1",
        "battery": "5000mAh",
        "display": "6.7 inch OLED 144Hz",
        "camera": "50MP Triple Camera",
        "connectivity": "5G"
    },
    "moto g84": {
        "processor": "Snapdragon 695",
        "battery": "5000mAh",
        "display": "6.5 inch OLED 120Hz",
        "camera": "50MP Dual Camera",
        "connectivity": "5G"
    },
    
    # Nothing Phone
    "nothing phone 2": {
        "processor": "Snapdragon 8+ Gen 1",
        "battery": "4700mAh",
        "display": "6.7 inch OLED 120Hz",
        "camera": "50MP Dual Camera",
        "connectivity": "5G"
    },
    "nothing phone 1": {
        "processor": "Snapdragon 778G+",
        "battery": "4500mAh",
        "display": "6.55 inch OLED 120Hz",
        "camera": "50MP Dual Camera",
        "connectivity": "5G"
    }
}


def extract_base_model_name(title):
    """Extract base model name from product title"""
    title_lower = title.lower()
    
    # Remove storage variants
    cleaned = title_lower
    import re
    cleaned = re.sub(r'\b\d+\s*(gb|tb|mb)\b', '', cleaned, flags=re.IGNORECASE)
    # Remove RAM variants
    cleaned = re.sub(r'\b\d+\s*gb\s*(ram|memory)\b', '', cleaned, flags=re.IGNORECASE)
    # Remove color variants in parentheses
    cleaned = re.sub(r'\([^)]*\)', '', cleaned)
    # Remove extra spaces
    cleaned = ' '.join(cleaned.split())
    
    return cleaned.strip()


def get_specs_from_database(title):
    """
    Try to find specs in database by matching phone model
    Returns specs dict or None if not found
    """
    base_model = extract_base_model_name(title)
    
    # Direct match
    if base_model in MOBILE_SPECS_DB:
        return MOBILE_SPECS_DB[base_model].copy()
    
    # Fuzzy match - check if any database key is in the title
    for model_key, specs in MOBILE_SPECS_DB.items():
        # Check if all words from database key are in the title
        key_words = model_key.split()
        if all(word in base_model for word in key_words):
            return specs.copy()
    
    return None
