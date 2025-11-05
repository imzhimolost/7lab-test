# tests/test_bmc_api.py
import requests
import pytest

BASE_URL = "http://localhost:4430"
AUTH = ("root", "0penBmc")

# Отключаем предупреждения (опционально)
requests.packages.urllib3.disable_warnings()

def test_redfish_root():
    r = requests.get(f"{BASE_URL}/redfish/v1", auth=AUTH)
    assert r.status_code == 200
    data = r.json()
    assert "RedfishVersion" in data
    assert data["RedfishVersion"] == "1.0.0"

def test_bmc_version():
    r = requests.get(f"{BASE_URL}/redfish/v1/Managers/bmc", auth=AUTH)
    assert r.status_code == 200
    data = r.json()
    assert "FirmwareVersion" in data
    print(f"Версия прошивки: {data['FirmwareVersion']}")

def test_power_status():
    r = requests.get(f"{BASE_URL}/redfish/v1/Systems/system", auth=AUTH)
    assert r.status_code == 200
    data = r.json()
    assert "PowerState" in data
    assert data["PowerState"] in ["On", "Off", "PoweringOn", "PoweringOff"]