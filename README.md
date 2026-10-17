# YouTube Data Visualization

A Python project that pulls video data from any YouTube channel using the YouTube Data API v3, cleans it with pandas, saves it to Excel, and builds an interactive Plotly dashboard.

## Features

- Fetches video data (title, publish date, duration, views, likes, comments) for any channel
- Cleans and enriches the data with pandas (date conversion, duration in minutes, engagement rate)
- Saves the results to an Excel file
- Generates 5 interactive Plotly charts on a single dashboard page:
  - Top 10 videos by views
  - Views over time
  - Likes vs views
  - Views distribution
  - Average views by upload day

## Tech Stack

Python, pandas, Plotly Express, requests, openpyxl, python-dotenv

## Project Structure

```
Youtube data/
├── main.py             # Runs the whole pipeline with one command
├── fetch_data.py       # Fetches data from the API and saves it to Excel
├── visualize.py        # Reads the Excel file and builds the dashboard
├── requirements.txt    # Python dependencies
├── .env                # Your API key (not uploaded to GitHub)
├── data/               # Generated Excel file
└── charts/             # Generated dashboard HTML
```

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/MuhammadxRehan/youtube-data-viz.git
   cd youtube-data-viz
   ```

2. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Get a YouTube Data API key**

   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Create a project and enable **YouTube Data API v3**
   - Create an API key under **APIs & Services > Credentials**

4. **Create a `.env` file** in the project folder:

   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

   Never share this key or commit it to GitHub.

## Usage

1. Open `fetch_data.py` and set the channel you want to analyze:

   ```python
   HANDLE = "@MrBeast"
   ```

2. Run the full pipeline:

   ```bash
   python main.py
   ```

   This fetches the data, saves it to `data/youtube_data.xlsx`, and opens the dashboard (`charts/dashboard.html`) in your browser.

You can also run each step separately:

```bash
python fetch_data.py   # fetch data and save to Excel
python visualize.py    # build the dashboard from the Excel file
```

## API Quota

The YouTube Data API gives 10,000 free units per day. This project uses cheap endpoints (`channels`, `playlistItems`, `videos`), so fetching 200 videos costs only a handful of units.

## Future Improvements

- Streamlit dashboard with a channel search box
- Compare multiple channels side by side
- More charts (duration vs views, engagement trends)