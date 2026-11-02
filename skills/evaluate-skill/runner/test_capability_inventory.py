import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import capability_inventory as ci


class CapabilityInventoryTests(unittest.TestCase):
    def inventory_path(self):
        return Path(__file__).with_name("provider_capabilities_v0_2.json")

    def test_inventory_loads_pinned_local_baseline(self):
        inventory = ci.load_inventory(self.inventory_path())

        self.assertEqual(
            inventory.required_versions,
            {
                "promptfoo": "0.125.1",
                "codex": "0.163.0",
                "claude": "2.1.302",
            },
        )
        self.assertEqual(set(inventory.providers), {"codex", "claude"})
        for provider in inventory.providers:
            for backend in ("native", "docker"):
                for profile in (
                    "no-tool",
                    "read-only",
                    "disposable-write",
                    "mock-external",
                ):
                    self.assertTrue(
                        inventory.claims_for(provider, backend, profile),
                        (provider, backend, profile),
                    )

    def test_every_capability_has_verified_unverified_or_unsupported_status(self):
        inventory = ci.load_inventory(self.inventory_path())

        self.assertTrue(inventory.claims)
        for key, claim in inventory.claims.items():
            with self.subTest(claim=key):
                self.assertIn(claim.status, {"verified", "unverified", "unsupported"})
                if claim.status == "unverified":
                    self.assertTrue(claim.required_probes)

    def test_unverified_control_never_counts_as_enforced(self):
        inventory = ci.load_inventory(self.inventory_path())
        claim = inventory.claim("codex", "native", "read-only", "filesystem_read")

        self.assertEqual(claim.status, "unverified")
        self.assertFalse(
            inventory.is_enforced(
                "codex",
                "native",
                "read-only",
                "filesystem_read",
                passed_probes=claim.required_probes,
            )
        )

    def test_missing_cli_is_reported_as_version_mismatch(self):
        inventory = ci.load_inventory(self.inventory_path())
        observed = {"promptfoo": "0.125.1", "codex": None, "claude": "2.1.302"}

        mismatches = ci.validate_installed_versions(inventory, observed)

        self.assertEqual(mismatches, ["codex: missing (required 0.163.0)"])

    def test_provider_or_adapter_version_drift_is_reported(self):
        inventory = ci.load_inventory(self.inventory_path())
        completed = {
            "promptfoo": SimpleNamespace(returncode=0, stdout="promptfoo 0.125.2\n", stderr=""),
            "codex": SimpleNamespace(returncode=0, stdout="codex-cli 0.164.0\n", stderr=""),
            "claude": SimpleNamespace(returncode=0, stdout="2.1.302 (Claude Code)\n", stderr=""),
        }

        def fake_which(name):
            return f"/approved/bin/{name}"

        def fake_run(command, **kwargs):
            self.assertEqual(command[1:], ["--version"])
            self.assertFalse(kwargs.get("shell", False))
            return completed[Path(command[0]).name]

        with patch("capability_inventory.shutil.which", side_effect=fake_which), patch(
            "capability_inventory.subprocess.run", side_effect=fake_run
        ):
            observed = ci.inspect_installed_versions()

        self.assertEqual(
            ci.validate_installed_versions(inventory, observed),
            [
                "codex: observed 0.164.0, required 0.163.0",
                "promptfoo: observed 0.125.2, required 0.125.1",
            ],
        )

    def test_unknown_capability_name_is_rejected(self):
        source = json.loads(self.inventory_path().read_text(encoding="utf-8"))
        changed = copy.deepcopy(source)
        changed["claim_sets"]["native-unverified"]["telepathy"] = {
            "status": "verified",
            "required_probes": [],
        }

        with TemporaryDirectory() as temp:
            path = Path(temp) / "inventory.json"
            path.write_text(json.dumps(changed), encoding="utf-8")
            with self.assertRaises(ci.InventoryError):
                ci.load_inventory(path)


if __name__ == "__main__":
    unittest.main()
