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

## Deploying to GitHub

1. Create a new repository on GitHub
2. Connect your local repository to the GitHub repository:
   ```bash
   git remote add origin https://github.com/your-username/your-repo-name.git
   ```
3. Push the code to GitHub:
   ```bash
   git branch -M main
   git push -u origin main
   ```

## Notes

- The backend runs on port 5000 by default
- The frontend runs on port 3000 by default
- Certificate checks run daily at midnight
- Alerts are sent when certificates expire in 30 days or less