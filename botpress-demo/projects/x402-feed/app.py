#!/usr/bin/env python3

"""
x402 Forecast Endpoint - Production Version

A Flask endpoint serving Bitcoin price forecasts via the x402 payment protocol.
Returns 402 Payment Required without valid payment header, serves forecast data with valid x402 header.

Environment variables:
- PORT: Server port (default: 5001)
- EXPECTED_NETWORK: Payment network (default: eip155:84532 for Base Sepolia)
- EXPECTED_ASSET: Payment asset (default: usdc)
- EXPECTED_PRICE: Payment price as string (default: 0.01)
- EXPECTED_PAYTO: Payment recipient address (required, no default)
- LOG_LEVEL: Logging level (default: INFO)
- FORECAST_SYMBOL: Trading symbol (default: BTCUSDT)
- FORECAST_HORIZON: Forecast horizon in minutes (default: 90)
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Any, Dict

from flask import Flask, jsonify, g, request
from pythonjsonlogger import jsonlogger

# Import x402 server components
from x402.http import FacilitatorConfig, HTTPFacilitatorClientSync
from x402.server import (
    PaymentPayloadV1,
    PaymentRequirementsV1,
    x402ResourceServerSync,
)
from x402.http.middleware.flask import PaymentMiddleware
from x402.http import PaywallConfig, RoutesConfig, RouteConfig, PaymentOption
from x402.mechanisms.evm.exact import ExactEvmServerScheme

# Configure JSON logging
log_handler = logging.StreamHandler()
log_handler.setFormatter(jsonlogger.JsonFormatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"))
logger = logging.getLogger(__name__)
logger.addHandler(log_handler)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())

@dataclass(frozen=True)
class PaymentConfig:
    """Expected payment configuration."""
    network: str
    asset: str
    price: str
    pay_to: str

@dataclass(frozen=True)
class ForecastConfig:
    """Forecast generation configuration."""
    symbol: str
    horizon: int

def load_config() -> tuple[PaymentConfig, ForecastConfig]:
    """Load configuration from environment variables."""
    network = os.environ.get("EXPECTED_NETWORK", "eip155:84532")
    if not network:
        raise ValueError("EXPECTED_NETWORK must be set")
    
    pay_to = os.environ.get("EXPECTED_PAYTO")
    if not pay_to:
        raise ValueError("EXPECTED_PAYTO must be set to a controlled recipient address")
    
    payment = PaymentConfig(
        network=network,
        asset=os.environ.get("EXPECTED_ASSET", "usdc"),
        price=os.environ.get("EXPECTED_PRICE", "0.01"),
        pay_to=pay_to,
    )
    forecast = ForecastConfig(
        symbol=os.environ.get("FORECAST_SYMBOL", "BTCUSDT"),
        horizon=int(os.environ.get("FORECAST_HORIZON", "90")),
    )
    return payment, forecast

PAYMENT_CONFIG, FORECAST_CONFIG = load_config()

# Set up facilitator client
facilitator_config = FacilitatorConfig(url="https://x402.primer.systems")
facilitator_client = HTTPFacilitatorClientSync(config=facilitator_config)

# Set up the x402 resource server with our expected requirements and facilitator
REQUIREMENTS = PaymentRequirementsV1(
    scheme="exact",  # Use 'exact' scheme as returned by facilitator
    network=PAYMENT_CONFIG.network,
    max_amount_required=PAYMENT_CONFIG.price,
    resource="/forecast",
    description="Bitcoin forecast endpoint",
    mime_type="application/json",
    asset=PAYMENT_CONFIG.asset,
    pay_to=PAYMENT_CONFIG.pay_to,
    max_timeout_seconds=30,
)

RESOURCE_SERVER = x402ResourceServerSync(facilitator_clients=[facilitator_client])
# Register the EVM exact scheme for our network
RESOURCE_SERVER.register(PAYMENT_CONFIG.network, ExactEvmServerScheme())

# Initialize the server (fetch supported payment kinds from facilitator)
try:
    RESOURCE_SERVER.initialize()
    logger.info("x402 resource server initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize x402 resource server: {e}")
    # Fail closed - don't start server if initialization fails
    raise

app = Flask(__name__)

def generate_forecast_data(base_time: int) -> dict[str, Any]:
    """Generate forecast data based on current time."""
    # Deterministic but time-varying for demo freshness
    price_base = 65000.0 + (base_time % 1000) - 500
    price_low = 63000.0 + (base_time % 1000) - 500
    price_high = 67000.0 + (base_time % 1000) - 500
    price_tight_low = 64000.0 + (base_time % 1000) - 500
    price_tight_high = 66000.0 + (base_time % 1000) - 500

    forecast_time = base_time + 86400  # 24h ahead

    return {
        "symbol": FORECAST_CONFIG.symbol,
        "horizon": FORECAST_CONFIG.horizon,
        "status": "demo",
        "data_source": "synthetic_demo",
        "is_synthetic": True,
        "not_investment_advice": True,
        "build_at_utc": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(base_time)),
        "forecasts": {
            "1d": {
                "mean_path": {
                    forecast_time: {"price": round(price_base, 2)}
                },
                "sample_paths": [
                    {forecast_time: {"price": round(price_base, 2)}}
                ],
                "prediction_interval_95": [
                    {forecast_time: {
                        "low": round(price_low, 2),
                        "high": round(price_high, 2)
                    }}
                ],
                "uncertainty_bounds": [
                    {forecast_time: {
                        "low": round(price_tight_low, 2),
                        "high": round(price_tight_high, 2)
                    }}
                ],
            }
        }
    }

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for load balancers and orchestration."""
    return jsonify({
        "status": "healthy",
        "service": "x402-forecast",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
        "version": "1.0.0"
    })

@app.route("/", methods=["GET"])
def index():
    """Root endpoint with service information."""
    return jsonify({
        "service": "x402 Forecast Endpoint",
        "version": "1.0.0",
        "endpoints": {
            "forecast": "/forecast (GET) - requires x402 Payment header",
            "health": "/health (GET) - no auth required"
        },
        "payment": {
            "network": PAYMENT_CONFIG.network,
            "asset": PAYMENT_CONFIG.asset,
            "price": PAYMENT_CONFIG.price,
            "payTo": PAYMENT_CONFIG.pay_to,
        },
        "forecast": {
            "symbol": FORECAST_CONFIG.symbol,
            "horizon_minutes": FORECAST_CONFIG.horizon,
            "data_source": "synthetic_demo",
            "is_synthetic": True,
            "not_investment_advice": True,
        }
    })

@app.route("/forecast", methods=["GET"])
def forecast():
    """Forecast endpoint - requires valid x402 payment header.
    Payment verification and settlement handled by x402 Flask middleware.
    """
    base_time = int(time.time())
    return jsonify(generate_forecast_data(base_time))

# Set up Flask middleware for x402 payment handling
# Define routes that require payment
routes: RoutesConfig = {
    "/forecast": RouteConfig(
        accepts=PaymentOption(
            scheme=REQUIREMENTS.scheme,
            pay_to=REQUIREMENTS.pay_to,
            price=REQUIREMENTS.max_amount_required,
            network=REQUIREMENTS.network,
            max_timeout_seconds=REQUIREMENTS.max_timeout_seconds,
            extra=None
        ),
        resource=REQUIREMENTS.resource,
        description=REQUIREMENTS.description,
        mime_type=REQUIREMENTS.mime_type
    )
}

# Create paywall config (optional, can be None)
paywall_config = PaywallConfig()

# Wrap the Flask app with x402 middleware
middleware = PaymentMiddleware(
    app=app,
    routes=routes,
    server=RESOURCE_SERVER,
    paywall_config=paywall_config,
    sync_facilitator_on_start=os.environ.get("X402_SYNC_FACILITATOR_ON_START", "true").lower() in {"1", "true", "yes", "on"},  # Disable for offline rejection tests; enabled by default
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    logger.info(f"Starting x402 forecast endpoint on port {port}")
    app.run(host="0.0.0.0", port=port)
