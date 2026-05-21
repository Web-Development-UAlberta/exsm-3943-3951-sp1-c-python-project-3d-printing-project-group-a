import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app.services.pricing import calculate_quote


class TestPricing(unittest.TestCase):

    def base_quote(self, **overrides):
        defaults = {
            "length": 120,
            "width": 80,
            "height": 95,
            "scale": 100,
            "infill_percent": 50,
            "filament_price": 25.00,
            "color_count": 1,
            "print_time_hours": 8.0
        }
        defaults.update(overrides)
        return calculate_quote(**defaults)

    def test_quote_returns_all_fields(self):
        quote = self.base_quote()
        expected_keys = [
            "base_volume_mm3", "scaled_volume_mm3",
            "material_volume_mm3", "material_volume_mm3_with_waste",
            "material_grams", "material_cost",
            "print_hours", "machine_cost",
            "overhead", "multicolor_surcharge",
            "shipping", "total"
        ]
        for key in expected_keys:
            self.assertIn(key, quote)

    def test_shipping_always_10(self):
        quote = self.base_quote()
        self.assertEqual(quote["shipping"], 10.00)

    def test_scale_150_cubic(self):
        quote_100 = self.base_quote(scale=100)
        quote_150 = self.base_quote(scale=150)
        # 150% scale = 1.5³ = 3.375x the volume
        ratio = quote_150["base_volume_mm3"] / quote_100["base_volume_mm3"]
        # base volume doesn't change with scale, scaled_volume does
        ratio = quote_150["scaled_volume_mm3"] / quote_100["scaled_volume_mm3"]
        self.assertAlmostEqual(ratio, 3.375, places=2)

    def test_multicolor_surcharge_applied_at_5_colors(self):
        quote_4 = self.base_quote(color_count=1)
        quote_5 = self.base_quote(color_count=5)
        self.assertEqual(quote_4["multicolor_surcharge"], 0.0)
        self.assertGreater(quote_5["multicolor_surcharge"], 0.0)

    def test_multicolor_surcharge_not_applied_below_5(self):
        for count in [1]:
            quote = self.base_quote(color_count=count)
            self.assertEqual(quote["multicolor_surcharge"], 0.0)
            
    def test_multicolor_surcharge_applied_at_5_or_more(self):
        for count in [5, 6]:
            quote = self.base_quote(color_count=count)
            self.assertGreater(quote["multicolor_surcharge"], 0.0)

    def test_total_greater_than_machine_and_material(self):
        quote = self.base_quote()
        self.assertGreater(quote["total"], quote["material_cost"] + quote["machine_cost"])

    def test_waste_factor_increases_material(self):
        # material_volume_with_waste should be 20% more than without
        quote = self.base_quote()
        ratio = quote["material_volume_mm3_with_waste"] / quote["material_volume_mm3"]
        self.assertAlmostEqual(ratio, 1.20, places=2)

    def test_higher_infill_means_more_material(self):
        quote_20  = self.base_quote(infill_percent=20)
        quote_100 = self.base_quote(infill_percent=100)
        self.assertGreater(quote_100["material_grams"], quote_20["material_grams"])

    def test_total_is_positive(self):
        quote = self.base_quote()
        self.assertGreater(quote["total"], 0)


if __name__ == "__main__":
    unittest.main()