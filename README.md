# Oakland Stock Data Pipeline

## Overview

Take home project for Oakland Data Engineering Interview.

Application to ingest AAPL stock data and display on a frontend

## Architecture

_TBD_

## Setup

### Prerequisites
- Git
- Docker Desktop
- A Twelve Data API Key (complete steps 1 and 2 at [Twelve Data API Quickstart Docs](https://twelvedata.com/docs/introduction/overview))

## Usage

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

_TBD_

## What Works

_TBD_

## Known Limitations

_TBD_

## Future Improvements

_TBD_