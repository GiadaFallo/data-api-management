# Coding challenge: DataAPI

We have a chatbot where we process data from our customers in real time.
We also have a background job that pushes the data from the customers via HTTP to a customer data management API (that we'll call DataAPI)
so that it gets saved in a database. DataAPI is also used by data scientists to retrieve data to further improve the chatbot.
Finally customers also need to provide us with an explicit consent so that we're allowed to store their data and DataAPI is also used to manage that.


##Requirements for DataAPI:

Create an application with an API layer with the following endpoints:

* POST /data/${customerId}/${dialogId}
    * With the payload
    `{
        "text": "the text from the customer",
        "language": "EN"
        }
      `

   * This is the endpoint used by the background job to push each customer input during his/her dialogue with our chatbot


* POST /consents/${dialogId}
    * With the payload
		`true|false`
    * This endpoint is called AT THE END of the dialogue when the customer is asked if he/she gives consent for us to store and use their data for further improving the chatbot.
    * If false it should delete the customer's data

* GET /data/(?language=${language}|customerId=${customerId})
    * This endpoint is used by data scientists to retrieve data to improve the chatbot, it should return all the datapoints:

        * that match the query params (if any)
        * for which we have consent for
        * and sorted by most recent data first
        * implement pagination for the returned data

## Things to take into consideration

You are free to use any data storage technology you want (in-memory or database), but please explain your decision

Save this on your own GitHub and send us the link or send us a zip file containing a GIT repo. Make sure to commit like you would at work

Add a reasonable amount of automated tests to the application

Include documentation on how to run/deploy the application

Include a document explaining the decisions you took during the implementation

Think about and explain in the documentation how to improve the system when there are millions of datapoints in the system

If you use a database or any external service make sure to include a docker-compose file, so we can run the full stack on our own
