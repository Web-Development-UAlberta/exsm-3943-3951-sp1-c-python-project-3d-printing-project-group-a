# app/services/stock_service.py

LOW_STOCK_THRESHOLD = 0.30   # 30%
DEFAULT_MAX_STOCK_G = 1000   # assume 1kg max per filament

def is_low_stock(quantity_in_stock, max_stock=DEFAULT_MAX_STOCK_G):
    if max_stock <= 0:
        return False
    return (quantity_in_stock / max_stock) < LOW_STOCK_THRESHOLD

def get_low_stock_filaments(db, Filament):
    all_filaments = db.query(Filament).all()
    return [
        {
            "filament_id":       f.filament_id,
            "material_name":     f.material_name,
            "color_hex":         f.color_hex,
            "quantity_in_stock": f.quantity_in_stock,
            "status":            "LOW STOCK"
        }
        for f in all_filaments
        if is_low_stock(f.quantity_in_stock)
    ]