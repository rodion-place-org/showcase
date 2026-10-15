# x402 Forecast and Payer Feed

## Overview
A prototype endpoint serving Bitcoin price forecasts via the x402 payment protocol. The endpoint requires a valid x402 payment header to return forecast data; otherwise, it responds with `402 Payment Required` and payment details.

## Status
- **Prototype**: Functional locally and tested with `curl`.
- **Endpoint**: `/forecast` (GET)
- **Payment Required**: 0.01 USDC on Base network to payee `0x1234567890abcdef1234567890abcdef12345678`
- **Forecast Data**: Algorithmically generated BTCUSDT 90-minute horizon forecast, updated per request.

## How It Works
1. **Without valid payment**: Returns `402 Payment Required` with a `Payment-Required` header specifying the expected payment.
2. **With valid payment header**: Returns a JSON forecast containing symbol, horizon, timestamp, and predicted price paths.

## Local Testing
```bash
# Start the server (runs on port 5001 by default)
python app.py

# Test without payment (should return 402)
curl -i http://localhost:5001/forecast

# Test with invalid payment header
curl -i http://localhost:5001/forecast -H "Payment: invalid json"

# Test with valid payment header (replace with actual signed header in production)
curl -i http://localhost:5001/forecast -H "Payment: {\"network\":\"base\",\"asset\":\"usdc\",\"price\":\"0.01\",\"payTo\":\"0x1234567890abcdef1234567890abcdef12345678\"}"
```

## Implementation Details
- Built with Flask and Python 3.12.
- Payment verification currently checks for valid JSON matching expected values (network, asset, price, payTo).
- In a production setting, payment verification would include cryptographic signature verification.
- Forecast data is generated algorithmically based on the current time to demonstrate freshness.

## Source Code
Available in the showcase repository under `projects/x402-feed/`.

## Next Steps
- Deploy to a public server with a domain (e.g., `forecast.rodion.place`).
- Integrate with a payment processor or wallet to validate real x402 payments.
- Add logging and metrics for payment attempts and successful forecasts.
- Expand to multiple symbols and horizons.

## Verification
The prototype has been verified to return:
- `402 PAYMENT REQUIRED` when the `Payment` header is missing or invalid.
- `200 OK` with forecast data when a valid payment header is provided.

---
*Last updated: 2026-10-14*