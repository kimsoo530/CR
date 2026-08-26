import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_statistical_country_profile.py"
SPEC = importlib.util.spec_from_file_location("build_statistical_country_profile", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class StatisticalCountryProfileTests(unittest.TestCase):
    def test_dotted_indicator_extension_is_appended(self):
        self.assertEqual(
            MODULE.append_extension(Path("GOV_WGI_GE.EST"), ".png").name,
            "GOV_WGI_GE.EST.png",
        )

    def test_build_writes_html_manifest_and_complete_images(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            run_dir = root / "run"
            output_dir = root / "output"
            run_dir.mkdir()
            rows = []
            for country, values in {"NGA": [1, 2], "GHA": [2, 3], "KEN": [3, 4]}.items():
                for year, value in zip([2020, 2021], values):
                    rows.append(
                        {
                            "source": "world_bank",
                            "country_code": country,
                            "country_name": country,
                            "year": year,
                            "indicator_code": "TEST.CODE",
                            "indicator_name": "Test indicator",
                            "value": value,
                            "lower_bound": "",
                            "upper_bound": "",
                            "unit": "index",
                            "frequency": "annual",
                            "value_type": "estimate",
                        }
                    )
            pd.DataFrame(rows).to_csv(run_dir / "observations.csv", index=False)
            pd.DataFrame(
                [
                    {
                        "institution": "World Bank",
                        "dataset": "Test data",
                        "indicator_code": "TEST.CODE",
                        "limitations": "Test limitation",
                    }
                ]
            ).to_csv(run_dir / "statistical_metadata.csv", index=False)
            (run_dir / "manifest.json").write_text(
                json.dumps({"validation_status": "pass"}), encoding="utf-8"
            )
            config = {
                "country_code": "NGA",
                "title": "Test profile",
                "required_coverage": [
                    {
                        "domain": "Core test domain",
                        "indicator_codes": ["TEST.CODE", "MISSING.CODE"],
                        "minimum_available": 1,
                        "rationale": "At least one test signal is required.",
                    }
                ],
                "categories": [
                    {
                        "id": "test",
                        "title": "Test",
                        "indicators": [
                            {
                                "indicator_code": "TEST.CODE",
                                "title": "Test indicator",
                                "chart_type": "trend",
                            }
                        ],
                    }
                ],
            }
            config_path = root / "config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            output = MODULE.build(config_path, run_dir, output_dir)
            validation = json.loads((output_dir / "validation.json").read_text())
            chart = pd.read_csv(output_dir / "chart_manifest.csv").iloc[0]
            self.assertTrue(output.exists())
            self.assertEqual(validation["missing_images"], [])
            self.assertEqual(validation["core_coverage_status"], "pass")
            self.assertEqual(validation["core_coverage_failed_domains"], [])
            self.assertIn("MISSING.CODE", validation["core_coverage_requirements"][0]["missing_indicators"])
            self.assertEqual(chart["actual_chart_type"], "latest_bar")
            self.assertTrue((output_dir / "figures" / "TEST.CODE.svg").exists())

    def test_required_coverage_flags_undercovered_domain(self):
        rows, status = MODULE.audit_required_coverage(
            {
                "required_coverage": [
                    {
                        "domain": "Fiscal capacity",
                        "indicator_codes": ["REVENUE", "DEBT"],
                        "minimum_available": 2,
                    }
                ]
            },
            {"REVENUE"},
        )
        self.assertEqual(status, "review")
        self.assertEqual(rows[0]["missing_indicators"], ["DEBT"])


if __name__ == "__main__":
    unittest.main()
