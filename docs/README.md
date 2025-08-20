# SSL Certificate Monitor

A web application to monitor SSL certificates expiration status for multiple websites, with WeChat enterprise alerts.

## Features

- Monitor SSL certificates for multiple websites
- Daily automatic checks
- WeChat enterprise alerts when certificates are about to expire
- Web interface to view certificate status
- Add/remove websites to monitor

## Technology Stack

- **Backend**: Python 3, Flask
- **Frontend**: React, Bootstrap, Chart.js
- **SSL Check**: Python OpenSSL
- **Scheduling**: Python schedule

## Installation

1. Clone this repository
2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Configuration

1. Copy `.env.example` to `.env`
2. Update the WeChat enterprise configuration in `.env`:
   ```
   CORP_ID=your_corp_id
   APP_SECRET=your_app_secret
   AGENT_ID=your_agent_id
   ```
3. Add websites to monitor in `sites.json`

## Usage

1. Start the backend server:
   ```bash
   python app.py
   ```
2. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```
3. Open `http://localhost:3000` in your browser

## Project Structure

```
.
├── app.py                # Flask backend
├── config.py             # Configuration loader
├── ssl_monitor.py        # SSL certificate monitoring
├── wechat_alert.py       # WeChat alert service
├── sites.json            # List of monitored websites
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── frontend/             # React frontend
│   ├── src/              # React source files
│   ├── package.json      # Frontend dependencies
│   └── ...
└── README.md             # This file
```

## Notes

- The backend runs on port 5000 by default
- The frontend runs on port 3000 by default
- Certificate checks run daily at midnight
- Alerts are sent when certificates expire in 30 days or less