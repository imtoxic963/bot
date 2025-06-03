# Capital Doubler Bot

This is a Telegram investment bot that requires users to join a channel, invest 20 USDT (TRC20), and earn referral commissions.

## Features
- User must join the Telegram channel @globalinvestmentt
- Investment is processed via NOWPayments (TRC20 USDT)
- Earn $10 per verified referral who invests
- Earn $1 commission for referrals who join but don't invest
- Withdraw allowed only after 3 verified referrals
- Automatic payment verification via NOWPayments IPN

## Deployment on Render (Free Tier)

1. Create a Render account at https://render.com
2. Create a new Web Service, connect your GitHub repo, and configure:
   - Runtime: Python
   - Start Command: python capital_doubler_bot.py
3. Set the `ipn_callback_url` in the Python file to your Render service URL `/ipn` endpoint (e.g., https://your-service.onrender.com/ipn)
4. Deploy and run!

## Dependencies

- python-telegram-bot==20.3
- flask
- requests

## Running Locally

```bash
pip install -r requirements.txt
python capital_doubler_bot.py
```

## Notes

Make sure your Telegram bot token, NOWPayments API key, IPN secret, and wallet address are configured properly in the Python file.
