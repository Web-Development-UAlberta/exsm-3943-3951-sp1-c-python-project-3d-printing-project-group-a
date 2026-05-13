from decimal import Decimal, ROUND_HALF_UP


def calculate_quote(length, width, height, scale, infill_percent, filament_price, color_count, print_time_hours):

    length = Decimal(str(length))
    width = Decimal(str(width))
    height = Decimal(str(height))
    scale_factor = Decimal(str(scale)) / Decimal("100")
    infill_factor = Decimal(str(infill_percent)) / Decimal("100")
    filament_price = Decimal(str(filament_price))
    print_time_hours = Decimal(str(print_time_hours))

    # base volume in mm³
    base_volume_mm3 = length * width * height

    # scale cubically
    scaled_volume_mm3 = base_volume_mm3 * (scale_factor ** 3)

    # apply infill
    material_volume_mm3 = scaled_volume_mm3 * infill_factor

    # apply 20% waste factor
    material_volume_mm3_with_waste = material_volume_mm3 * Decimal("1.20")

    # convert mm³ -> cm³ (using waste-adjusted volume)
    material_volume_cm3 = material_volume_mm3_with_waste / Decimal("1000")

    # PLA density almost 1.24 g/cm³
    material_grams = material_volume_cm3 * Decimal("1.24")

    # material cost (price per kg)
    material_cost = (material_grams / Decimal("1000")) * filament_price

    # machine cost ($5/hr)
    machine_cost = print_time_hours * Decimal("5")

    # overhead 15%
    subtotal = material_cost + machine_cost
    overhead = subtotal * Decimal("1.15")

    # multi-color surcharge 5% if 5 or more colors
    surcharge = overhead * Decimal("0.05") if color_count >= 5 else Decimal("0")

    # 25% profit margin
    pre_margin = overhead + surcharge
    total = pre_margin / (Decimal("1") - Decimal("0.25"))

    def r(val):
        return float(val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    return {
        "base_volume_mm3": r(base_volume_mm3),
        "scaled_volume_mm3": r(scaled_volume_mm3),
        "material_volume_mm3": r(material_volume_mm3),
        "material_volume_mm3_with_waste": r(material_volume_mm3_with_waste),
        "material_grams": r(material_grams),
        "material_cost": r(material_cost),
        "print_hours": r(print_time_hours),
        "machine_cost": r(machine_cost),
        "overhead": r(overhead),
        "multicolor_surcharge": r(surcharge),
        "shipping": 10.00,
        "total": r(total)
    }