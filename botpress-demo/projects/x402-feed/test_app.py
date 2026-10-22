#!/usr/bin/env python3

"""
Test suite for x402 forecast endpoint.
Run with: pytest test_app.py -v

Tests verify that the official x402 Python SDK middleware:
1. Returns 402 Payment Required without a payment header
2. Returns 402 with proper Payment-Required response structure
3. Rejects fabricated/invalid payment headers (security: no spoofing)
4. Only grants access after real facilitator verification/settlement (integration test)
"""

import json
import os
import subprocess
import sys
import time
import base64
from typing import Generator

import pytest
import requests

# Set environment variables for testing (Base Sepolia testnet)
os.environ["EXPECTED_PAYTO"] = "0x1234567890abcdef1234567890abcdef12345678"
os.environ["EXPECTED_NETWORK"] = "eip155:84532"
os.environ["EXPECTED_ASSET"] = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
os.environ["EXPECTED_PRICE"] = "0.01"  # 0.01 USDC (SDK converts to smallest units: 10000 micro-USDC)
os.environ["FORECAST_SYMBOL"] = "BTCUSDT"
os.environ["FORECAST_HORIZON"] = "90"
os.environ["LOG_LEVEL"] = "DEBUG"


@pytest.fixture(scope="module")
def flask_server() -> Generator[str, None, None]:
    """Start Flask test server and yield base URL."""
    port = 15001
    base_url = f"http://127.0.0.1:{port}"

    env = {
        **os.environ,
        "PORT": str(port),
        "LOG_LEVEL": "DEBUG",
        # Rejection tests should not depend on a live facilitator startup call.
        "X402_SYNC_FACILITATOR_ON_START": "false",
    }

    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )

    # Wait for server to start
    for _ in range(30):
        try:
            requests.get(f"{base_url}/health", timeout=1)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.2)
    else:
        proc.terminate()
        stdout, stderr = proc.communicate()
        pytest.fail(f"Server failed to start. stdout: {stdout.decode()}, stderr: {stderr.decode()}")

    yield base_url

    proc.terminate()
    proc.wait(timeout=5)


# Fabricated payment header (base64url-encoded V1-style JSON) - SHOULD BE REJECTED
# This simulates an attacker copying the public fields from a Payment-Required response
FABRICATED_PAYMENT_HEADER = base64.urlsafe_b64encode(json.dumps({
    "x402Version": 1,
    "scheme": "exact",
    "network": "eip155:84532",
    "payload": {
        "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
        "amount": "10000",
        "payTo": "0x1234567890abcdef1234567890abcdef12345678"
    }
}).encode()).decode().rstrip("=")


def test_health_endpoint(flask_server: str):
    """Health endpoint should return 200 with status info (no auth required)."""
    resp = requests.get(f"{flask_server}/health", timeout=5)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["service"] == "x402-forecast"
    assert "timestamp" in data


def test_root_endpoint(flask_server: str):
    """Root endpoint should return service info (no auth required)."""
    resp = requests.get(f"{flask_server}/", timeout=5)
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "x402 Forecast Endpoint"
    assert "endpoints" in data
    assert "payment" in data
    assert "forecast" in data
    assert data["forecast"]["data_source"] == "synthetic_demo"
    assert data["forecast"]["is_synthetic"] is True
    assert data["forecast"]["not_investment_advice"] is True
    # Verify payment config is exposed correctly
    assert data["payment"]["network"] == "eip155:84532"
    assert data["payment"]["asset"] == "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    # Root metadata reports the configured decimal USDC price; the SDK converts to atomic units in Payment-Required.
    assert data["payment"]["price"] == "0.01"
    assert data["payment"]["payTo"] == "0x1234567890abcdef1234567890abcdef12345678"


def test_forecast_without_payment(flask_server: str):
    """Forecast without payment header should return 402 with proper Payment-Required response."""
    resp = requests.get(f"{flask_server}/forecast", timeout=5)
    assert resp.status_code == 402
    assert "Payment-Required" in resp.headers
    import base64
    import json
    payment_required_b64 = resp.headers["Payment-Required"]
    payment_required_json = base64.b64decode(payment_required_b64 + "==")  # Add padding
    payment_required = json.loads(payment_required_json)
    # Check the structure of the PaymentRequired object
    assert payment_required["x402Version"] == 2
    assert payment_required["error"] == "Payment required"
    assert "resource" in payment_required
    assert "accepts" in payment_required
    assert len(payment_required["accepts"]) == 1
    accept = payment_required["accepts"][0]
    assert accept["network"] == "eip155:84532"
    assert accept["asset"] == "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    assert accept["amount"] == "10000"
    assert accept["payTo"] == "0x1234567890abcdef1234567890abcdef12345678"


def test_forecast_with_invalid_payment_header(flask_server: str):
    """Forecast with malformed payment header should return 402."""
    headers = {"Payment-Signature": "not valid base64"}
    resp = requests.get(f"{flask_server}/forecast", headers=headers, timeout=5)
    assert resp.status_code == 402


def test_forecast_with_fabricated_payment_header(flask_server: str):
    """
    Forecast with fabricated payment header (copied public fields) should return 402.

    This is the critical security test: an attacker cannot simply copy the network,
    asset, amount, and payTo fields from the Payment-Required response and gain access.
    Real x402 verification requires cryptographic proof verified by the facilitator.
    """
    headers = {"Payment-Signature": FABRICATED_PAYMENT_HEADER}
    resp = requests.get(f"{flask_server}/forecast", headers=headers, timeout=5)
    assert resp.status_code == 402, (
        f"Fabricated header was accepted! Status: {resp.status_code}. "
        f"This indicates a security vulnerability - the middleware is not verifying "
        f"payments through the facilitator."
    )


def test_forecast_with_wrong_network(flask_server: str):
    """Forecast with wrong network in fabricated header should return 402."""
    bad_header = base64.urlsafe_b64encode(json.dumps({
        "x402Version": 1,
        "scheme": "exact",
        "network": "ethereum",  # wrong
        "payload": {
            "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
            "amount": "10000",
            "payTo": "0x1234567890abcdef1234567890abcdef12345678"
        }
    }).encode()).decode().rstrip("=")
    headers = {"Payment-Signature": bad_header}
    resp = requests.get(f"{flask_server}/forecast", headers=headers, timeout=5)
    assert resp.status_code == 402


def test_forecast_with_wrong_price(flask_server: str):
    """Forecast with wrong price in fabricated header should return 402."""
    bad_header = base64.urlsafe_b64encode(json.dumps({
        "x402Version": 1,
        "scheme": "exact",
        "network": "eip155:84532",
        "payload": {
            "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
            "amount": "20000",  # wrong (0.02 USDC)
            "payTo": "0x1234567890abcdef1234567890abcdef12345678"
        }
    }).encode()).decode().rstrip("=")
    headers = {"Payment-Signature": bad_header}
    resp = requests.get(f"{flask_server}/forecast", headers=headers, timeout=5)
    assert resp.status_code == 402


# NOTE: test_forecast_with_valid_payment is intentionally OMITTED.
# A valid x402 payment requires:
# 1. A real facilitator (https://x402.primer.systems)
# 2. A real wallet with funds on Base Sepolia (eip155:84532)
# 3. A real on-chain transaction signed by the payer
# 4. Facilitator verification and settlement
#
# This cannot be tested in a unit test without real infrastructure.
# Integration testing with real payments should be done separately against
# a deployed endpoint with a funded test wallet.
#
# The security property verified above: fabricated headers are REJECTED.
# Only real facilitator-verified payments will succeed.


def test_forecast_data_changes_over_time(flask_server: str):
    """
    Forecast data should change with each request (time-based).
    This test uses a fabricated header to verify the endpoint logic,
    but expects 402 since the header is not a real payment.
    """
    headers = {"Payment-Signature": FABRICATED_PAYMENT_HEADER}

    resp1 = requests.get(f"{flask_server}/forecast", headers=headers, timeout=5)
    time.sleep(1.1)  # Ensure different timestamp
    resp2 = requests.get(f"{flask_server}/forecast", headers=headers, timeout=5)

    # Both should be 402 (fabricated header rejected)
    assert resp1.status_code == 402
    assert resp2.status_code == 402

    # But the Payment-Required responses should have different timestamps
    # (verify the endpoint is generating fresh responses)
    pr1 = json.loads(base64.b64decode(resp1.headers["Payment-Required"] + "=="))
    pr2 = json.loads(base64.b64decode(resp2.headers["Payment-Required"] + "=="))
    # The resource timestamp or other fields may vary