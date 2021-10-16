# market_data_harvester

Simple container setup to collect market data (quotes) from [finhub.io](https://finnhub.io/)

It uses websocket connection to request and recieve financial data.
The data is handled by python script which puts quotes into PostgreSQL database.

## run

Apply the desired tickers into: `data_collector/symbols.yml` file (limited to 50 by finhub).

Then run it with:

```
docker-compose up -d --build
```

You should set up a `psql.env` and `collector.env` files locally, they should containd env variables:

```
#psql.env
POSTGRES_USER=<USERNAME>
POSTGRES_PASSWORD=<PASSWORD>

#collector.env
FINHUB_KEY=<YOUR TOKEN>
```
