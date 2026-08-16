# Oakland Stock Data Pipeline

Hi there! Thank you for taking the time to look through my project. I look forward to going through it with you on Monday :)

## Overview

Take home project for Oakland Data Engineering Interview.

Application to ingest AAPL stock data and display on a Web UI

## Architecture

The application is split into a few simple layers:

```text
Twelve Data API
      ↓
  Ingestion
      ↓
  Validation
      ↓
Transformation
      ↓
   SQLite
      ↓
  Streamlit UI
```

### Layers

* **Ingestion** — Fetches Apple stock data from Twelve Data.
* **Validation** — Checks the incoming data is valid and contains the required fields.
* **Transformation** — Converts the data into the required schema and formats.
* **Storage** — Stores the data in SQLite and handles updates and retention.
* **Orchestration** — Coordinates the pipeline using `run.py`.
* **Streamlit UI** — Displays the latest price, daily change and historical data.

The application is packaged in **Docker**. The SQLite database is created inside the container and is intentionally not persisted using a Docker volume, to demonstrate it's features. API credentials are supplied through environment variables.


## Setup

### Prerequisites
- Git
- Docker Desktop
- A Twelve Data API Key (complete steps 1 and 2 at [Twelve Data API Quickstart Docs](https://twelvedata.com/docs/introduction/overview))

### Usage

### 1. Clone the repository
```
git clone https://github.com/shakib108/oakland-aapl-data-pipeline.git
cd oakland-aapl-data-pipeline
```

### 2. Create the environment file

#### 2.1 -  Copy `.env.example` to `.env`:

#### PowerShell:

```
Copy-Item .env.example .env
```

#### macOS/Linux:

```
cp .env.example .env
```

#### 2.2 - Open `.env` and add your Twelve Data API key:

```
TWELVE_DATA_API_KEY=your_api_key_here
DB_PATH=data/stocks.db
```

Do not commit .env to source control. It is included in .gitignore because it contains credentials.

### 3. Build the Docker image

From the project root:

```
docker build -t oakland-aapl-pipeline .
```

### 4. Run the application
```
docker run --rm -p 8501:8501 --env-file .env oakland-aapl-pipeline
```

The application will be available at:
```
http://localhost:8501
```

## Testing

Tests are written using **pytest** and cover the main pipeline functionality, including:

* Data ingestion
* Data validation
* Data transformation
* Database storage
* Calculations and statistics

Run the tests with:

```bash
python -m pytest
```

The tests can also be run inside the Docker container with:
```
docker run --rm --env-file .env oakland-aapl-pipeline python -m pytest
```


## What Works

* Fetches Apple stock data from Twelve Data according to ingestion policy
* Validates and transforms incoming data
* Stores data in SQLite
* Handles API failures and retries
* Calculates latest close price and daily change
* Displays data through a Streamlit dashboard
* Runs in Docker


## Known Limitations

* SQLite data is not persisted between Docker containers.
* The application currently supports Apple (AAPL) stock data only.
* Twelve Data API limits can affect data refreshes.
* The Streamlit UI is intentionally simple and designed for this project scope.
* Tests do not accurately test the source code, due to some issues along the way


## Future Improvements

* Use PostgreSQL or another persistent database.
* Support multiple stocks.
* Add automated scheduled ingestion.
* Improve the dashboard and data visualisations.
* Add CI/CD for automated testing and deployment.
* Add monitoring and alerting for pipeline failures.
