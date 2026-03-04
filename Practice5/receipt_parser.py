import re
import json


def clean_money(value: str) -> float:
    """
    Converts money string like '1 234,56' to float 1234.56
    """
    return float(value.replace(" ", "").replace(",", "."))


def parse_receipt(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1 Extract all prices
    price_pattern = r'[\d\s]+,\d+'
    all_prices = [clean_money(p) for p in re.findall(price_pattern, text)]

    # 2️ Extract products (name, quantity, unit price)
    product_pattern = r'\d+\.\s*\n(.+?)\n(\d+,\d+)\s*x\s*([\d\s]+,\d+)'
    matches = re.findall(product_pattern, text, re.DOTALL)

    products = []
    calculated_total = 0.0

    for name, quantity, price in matches:
        name = name.strip().replace("\n", " ")
        qty = float(quantity.replace(",", "."))
        price_per_unit = clean_money(price)
        total_price = round(qty * price_per_unit, 2)

        calculated_total += total_price

        products.append({
            "name": name,
            "quantity": qty,
            "price_per_unit": price_per_unit,
            "total_price": total_price
        })

    calculated_total = round(calculated_total, 2)

    # 3️ Extract receipt total
    total_match = re.search(r'ИТОГО:\s*\n?([\d\s]+,\d+)', text)
    receipt_total = clean_money(total_match.group(1)) if total_match else None

    # 4️ Extract date and time
    datetime_match = re.search(r'\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2}', text)
    datetime_value = datetime_match.group() if datetime_match else None

    # 5️ Extract payment method
    payment_match = re.search(r'(Банковская карта|Наличные)', text)
    payment_method = payment_match.group() if payment_match else None

    # 6️ Structured output
    return {
        "products": products,
        "all_prices": all_prices,
        "calculated_total": calculated_total,
        "receipt_total": receipt_total,
        "datetime": datetime_value,
        "payment_method": payment_method
    }


if __name__ == "__main__":
    result = parse_receipt("raw.txt")
    print(json.dumps(result, indent=4, ensure_ascii=False))