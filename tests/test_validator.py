import unittest

from fit_exporter.validator import validate_activity_schema


class ValidatorTest(unittest.TestCase):
    def test_missing_metadata(self):
        activity = {"summary": {}, "records": []}
        issues = validate_activity_schema(activity)
        self.assertTrue(any("metadata" in issue.lower() for issue in issues))

    def test_missing_summary_fields(self):
        activity = {"metadata": {"schema_version": "1.0", "activity_date": "2026-07-03T00:00:00Z", "sport": "running"}, "summary": {}, "records": [{"timestamp": "2026-07-03T00:00:00Z"}]}
        issues = validate_activity_schema(activity)
        self.assertTrue(any("summary" in issue.lower() for issue in issues))

    def test_missing_record_fields(self):
        activity = {
            "metadata": {"schema_version": "1.0", "activity_date": "2026-07-03T00:00:00Z", "sport": "running"},
            "summary": {"distance_m": 1000, "moving_time_s": 300, "elapsed_time_s": 300, "avg_speed_mps": 3.3, "max_speed_mps": 4.0, "avg_pace_min_per_km": 5.0, "calories": 100, "avg_hr": 150, "max_hr": 160, "avg_cadence_spm": 160, "max_cadence_spm": 165, "avg_power": 180, "max_power": 220, "total_ascent": 10, "total_descent": 8},
            "records": [{"timestamp": "2026-07-03T00:00:00Z", "distance_m": 0}]
        }
        issues = validate_activity_schema(activity)
        self.assertTrue(any("record missing field" in issue.lower() for issue in issues))


if __name__ == "__main__":
    unittest.main()
