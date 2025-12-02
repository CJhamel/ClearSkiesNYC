import unittest
from .urbanflow import CityRecord, CityDataSet

class TestCityRecord(unittest.TestCase):
    def test_high_traffic_detection(self):
        record = CityRecord("Test St", 1200, 10.0)
        self.assertTrue(record.is_high_traffic())

        record_low = CityRecord("Low St", 500, 10.0)
        self.assertFalse(record_low.is_high_traffic())

    def test_poor_air_detection(self):
        record = CityRecord("Polluted St", 500, 15.0)
        self.assertTrue(record.is_poor_air())

        record_clean = CityRecord("Clean St", 500, 5.0)
        self.assertFalse(record_clean.is_poor_air())

    def test_pollution_to_traffic_ratio(self):
        record = CityRecord("Ratio St", 200, 10.0)
        self.assertAlmostEqual(record.compute_pollution_to_traffic_ratio(), 0.05)

        # Zero traffic should return 0
        record_zero_traffic = CityRecord("Zero Traffic", 0, 10.0)
        self.assertEqual(record_zero_traffic.compute_pollution_to_traffic_ratio(), 0.0)

        # Zero PM2.5 should still compute ratio
        record_zero_pm = CityRecord("Zero PM", 100, 0.0)
        self.assertEqual(record_zero_pm.compute_pollution_to_traffic_ratio(), 0.0)

    def test_to_dict(self):
        record = CityRecord("Dict St", 100, 5.0, "2025-12-01")
        d = record.to_dict()
        self.assertEqual(d['location'], "Dict St")
        self.assertEqual(d['traffic_volume'], 100)
        self.assertEqual(d['pm25'], 5.0)
        self.assertEqual(d['date'], "2025-12-01")
        self.assertFalse(d['is_high_traffic'])
        self.assertFalse(d['is_poor_air'])
        self.assertAlmostEqual(d['pollution_to_traffic_ratio'], 0.05)


class TestCityDataSet(unittest.TestCase):
    def setUp(self):
        # Create sample CityRecords
        self.record1 = CityRecord("A St", 100, 5.0, "2025-01-01")
        self.record2 = CityRecord("B St", 200, 1.0, "2025-01-02")
        self.record3 = CityRecord("C St", 0, 0.0, "2025-01-03")  # edge case
        self.dataset = CityDataSet("Test City")
        self.dataset.records.extend([self.record1, self.record2, self.record3])

    def test_average_traffic(self):
        # Only records with traffic > 0 count
        avg = self.dataset.average_traffic()
        expected_avg = (100 + 200 + 0) / 3
        self.assertEqual(avg, expected_avg)

    def test_average_air_quality(self):
        avg_air = self.dataset.average_air_quality()
        expected_avg = (5.0 + 1.0 + 0.0) / 3
        self.assertEqual(avg_air['pm25'], expected_avg)

    def test_find_hotspots(self):
        hotspots = self.dataset.find_hotspots(0.01)
        # Record1 ratio = 5/100 = 0.05 > 0.01
        # Record2 ratio = 1/200 = 0.005 < 0.01
        self.assertIn(self.record1, hotspots)
        self.assertNotIn(self.record2, hotspots)
        # Record3 has 0 traffic/PM2.5, should be skipped
        self.assertNotIn(self.record3, hotspots)

    def test_export_summary_creates_file(self):
        import os
        output_file = "test_summary.txt"
        # Ensure file does not exist first
        if os.path.exists(output_file):
            os.remove(output_file)
        self.dataset.export_summary(output_file)
        self.assertTrue(os.path.exists(output_file))
        # Optionally check that file is not empty
        with open(output_file, 'r') as f:
            content = f.read()
        self.assertIn("Test City", content)
        # Clean up
        os.remove(output_file)


if __name__ == "__main__":
    unittest.main()
