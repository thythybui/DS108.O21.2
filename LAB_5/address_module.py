import re

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_whitespace(text):
    if isinstance(text, str):
        return re.sub(r"\s+", " ", text.strip())
    return text

def extract_address(text, address_dict):
    """
    Trích xuất street, ward, district, province từ chuỗi địa chỉ đầu vào
    sử dụng từ điển địa chỉ theo format chuẩn.
    """
    text_norm = normalize_text(text)
    found_province = ""
    found_district = ""
    found_ward = ""

    for province_data in address_dict.values():
        prov_norm = normalize_text(province_data["name"])
        if prov_norm in text_norm:
            found_province = province_data["name"]

            for district in province_data["district"]:
                dist_full = normalize_text(f"{district['pre']} {district['name']}")
                if dist_full in text_norm:
                    found_district = f"{district['pre']} {district['name']}"

                    for ward in district.get("ward", []):
                        ward_full = normalize_text(f"{ward['pre']} {ward['name']}")
                        if ward_full in text_norm:
                            found_ward = f"{ward['pre']} {ward['name']}"
                            break
                    break
            break

    clean_text = text_norm
    for part in [normalize_text(found_province), normalize_text(found_district), normalize_text(found_ward)]:
        if part:
            clean_text = clean_text.replace(part, "")
    street = clean_text.strip(",. ")

    return {
        "street": street,
        "ward": found_ward,
        "district": found_district,
        "province": found_province
    }