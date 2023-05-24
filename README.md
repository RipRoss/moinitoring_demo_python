# Monitoring Demonstration in Python

This project is designed to demonstrate monitoring a Python application using Prometheus and logging via Loki. The solution will be dockerised and designed to run within a docker swarm, hosting a DB, an API service, Promtail, Prometheus and Grafana.

# Technologies

* Python (Main programming language)
* Prometheus (Metric collection and storage)
* Loki (Log aggregation)
* Promtail (Log collection and forwarder (forwards to Loki))
* Mongo (Our database storage solution)


# The purpose of the app itself

We want this application to serve some sort of purpose and be somewhat functional. So what we are going to do, to demonstrate the capabilities of the monitoring stack we have selected is build a service that retrieves data from *insert external API here* on a schedule, using Celery and thus the API can access and serve.

* The API will be a very simple data access API with full CRUD capability on the data in the database.
* Celery will be used as our task scheduling engine to asynchronously update our database (Mongo) for quicker retrieval of data
* Mongo will be used for the API to retrieve, insert and update data, as well as a way for us to store the data retrieved by the API.

## What problems does this solve?

In the real world, you may have rate limits and other such things to worry about when communicating with an external service. If you make a request to this external API on a per request basis to retrieve the most up to date information, you may risk the chance of hitting the rate limit as your service grows. What we can do instead, is ensure that we use Celery to retrieve the data from the API on an interval that keeps us under the rate limit defined by the API and then store it in our own database. This removes any risk of hitting the rate limit as well as always have a certain amount of data to give back. This is only useful, if the external API goes down - and of course, there's a risk of stale data. This is what the monitoring will come in.

# Metrics

* Total Request Count - This will measure the total amount of requests our service receives. The metric will include a label for the `status_code` so that we can differentiate successes and failures when monitoring
* Total Request Duration - This will measure the total request duration. The metric will include a label for the `path` and the `method` so that we can determine why an endpoint may be taking longer than another. (POST vs GET for example). This will be a histogram which will automatically segregate the variables into buckets representing how long the requests took
* Total Request Size in Bytes - This will measure the total amount of bytes a request size is. This will be a histogram and so will be sorted into buckets for us to monitor
* Total Response Size in Bytes - This will measure the total amount of bytes a response size is. This will be a histogram and so will be sorted into buckets for us to monitor

# Logging

Logging works hand in hand with metrics and will allow us to look through logs at any particular time our metrics go haywire to look a little deeper into what the root cause of that issue might be but from a centralised location. Loki and our logging infrastructure will enable us to view and display our logs and metrics together, so that we can correlate the two and easily pin point application logs for a specific time period.

## Format

When formatting our logs, we want to include as much of the most useful information we can in there without over populating the log output. This is important so that they are quick and easy to read. The format we have so far is below, and is always encouraged to put forward any improvements if you have them.

`tsp=%(asctime)s lvl=[%(levelname)s] proc=[%(process)d:%(thread)d] file=%(filename)s line=%(lineno)d msg=%(message)s`

The reason i have followed each section with a descriptive key, is so that they make sense to anyone reading the log message, familiar or not. 

## Custom key/value fields

When creating our logs, the default format should only be the mandatory required fields. However, there should also be functionality that allows us to add our own custom key/value fields. For example, a HTTP request would include all of what's in the default log format but you may want to include the following also: `remote_addr`, `url`, `method`, `status_code` and any other key/value pairs that are relevant to the particular action you're performing in code.

# Alerts setup (TODO atm)

