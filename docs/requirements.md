# Project Requirements & Scope

## 1. Objective

Build a simple application that ingests Apple (AAPL) stock data from a public API, stores the data in a database, and presents it in a UI along with basic statistics

## 2. Stakeholder / Intended End User

For this project I will assume that the relevant stakeholder and consumer would be an **investment analyst**. This assumption has guided research about what the user would need in the application, and therefore guides the technical requirements for the project.

An investment analyst would want to see the daily historical OHLCV data, as well as what price the stock last settled at, i.e. the 'Latest Close' price from the previous trading day. Most applications of the same nature also include the Daily Change value, representing the change in price for a stock from the previous day to current day. 

I have chosen therefore to include the **Latest Close** and **Daily Change** values in the dashboard.

## 3. Functional Requirements

- **FR1 - Ingestion:** Retrieve daily historical data for AAPL stock from a public API
- **FR2 - Validation:** Validate the incoming data before it is persisted
- **FR3 - Transformation:** Transform the source data into a defined schema
- **FR4 - Storage:** Persist the processed data in a separate database, avoiding data discrepancies
- **FR5 - Liveliness:** Keep database up to date with available AAPL stock data in accordance with an established data ingestion policy 
- **FR6 - Retrieval:** Retrieve stored data independently of source data API
- **FR7 - Dashboard:** Provide a simple UI displaying the stored AAPL daily historical data
- **FR8 - Statistics:** In addition to the historical data, display basic statistics: latest close and daily change. Due to this project not requiring live data, the daily change will be based on the Latest Close price

## 4. Non-functional Requirements

- **NFR1 - Reproducibility:** Application can run on a separate machine with low effort setup, following the instructions in the repository
- **NFR2 - Legibility:** Display layer is simple and understandable to the User
- **NFR3 - Reliability:** Ingestion handles simple API failures in a reasonable way, without corrupting stored data
- **NFR4 - Security:** API credentials and sensitive info shall not be committed in repository
- **NFR5 - Data Quality:** Invalid or incomplete source data etc will be marked before storing, and data shall be idempotent

## 5. MVP Scope

- Stock data API > ingestion > validation > transformation > database storage > dashboard

## 6. Out of Scope

- Real time stock price
- Multiple stocks
- Authentication
- Complex monitoring
- Analytics functionality

## 7. Assumptions

- "Stock data" means daily historical data
- API is treated as the source of truth
- A limited historical period is sufficient for MVP
- Local database is sufficient

## 8. Acceptance Criteria

- Application pulls latest stock data from stock API 
- Stock data is persisted in database and application attempts to keep it up to date
- Display shows daily historical AAPL data, Latest Close, and Daily Change
- Stored data is not lost between sessions

## 9. Initial Technical Questions

- Which API?
- What data does it provide?
- What data is relevant for the assumed stakeholder?
- What is the behaviour of the API? e.g. is there occasional historical changes to the API data?
- What ingestion strategy should be used?
- Which data processing framework should be used? Distributed or in-memory computing?
- How will the application be deployed?
- What should be used to build the UI?
- Which database technology should be used?

## 10. Optional Enhancements

- CI implementation
- Graph visual of historical stock price data