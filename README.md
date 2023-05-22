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