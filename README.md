# Coding challenge: DataAPI
The aim of the challenge was to implement a customer data management API (DataAPI), so that data - pushed from a background job - after customer consents, is saved in a database. DataAPI will also be used by data scientists to retrieve data to further improve the chatbot. 

To solve the challenge, I decided to use Python as programming language and Fast API as web framework. (The choice was mainly dictated by the fact that I have been working with these technologies for the past few months).

I decided to structure the project in the following way: data arriving during the customer's interaction with the chatbot is first saved in memory and, at the end of the conversation, is stored in the database (only if the user agrees to save it).

For in-memory storage, I simply used a python dictionary. When messages are pushed from the background job they are saved in the dictionary and after a consents from the user the batch of messages of the specific dialog are saved in the database.

In case of millions of data points in the system, the best choice would be to avoid in-memory storage using a simple dictionary and instead use a lightning-fast in-memory key-value store, such as Redis.

I used MongoDB for data storage. The choice fell on a NoSQL database for the simple reasons of adapting future changes in the data structure - that can occur in contexts similar to the one described - but also for the simplicity of implementation given the purpose.

## Data Model

First of all, I defined the model for which data will be based on, which will represent how data are stored in the in-memory storage (before the consent) and in the MongoDB database at the end.

Data model:
- `CustomerInput` - dataclass modeling the message received from the user (text, language and timestamp)
- `CustomerDialog` - dataclass modeling the list of messages received associated with the customerId
- `CustomerDialogStorage` - dictionary to store (in-memory) the messages for each dialog

## APIs implementation

I have implemented the three endpointed required:

- `POST /data/${customerId}/${dialogId}` with payload `{text: "", language: ""}`
  - This API will return a 201 status code when successful because items are created in memory when the requested is handled

- `POST /consents/${dialogId}` with payload `{value: true|false}` (I added a Pydantic model for the consents payload in order to have a smooth implementation and error handling with fastAPI. With this type declaration fastAPI will read the body of the request as a JSON, will validate the data.)
  - This API will return a 200 status code when successful (in case of negative consents no datapoint are stored in the database, datapoint are simply removed from the in-memory storage)
- `GET /data/(?language=${language}|customer_id=${customer_id}|page_number=${page_number}&n_per_page={$n_per_page_)`
Note that I changed the syntax for the query param customerId in snake case 

## Interaction with the MongoDB database
I installed PyMongo the official MongoDB driver, to interact with the database. 

You will find a `DATABASE_URL` environement variable in the config file to be able to connect to the specific database. Inside the Database class a connection is estabilished with that url, a database and a collection are created. I left those names hard-coded during the initialization (it can be improved adding them as config variables).

## Tests

I usually prefer a test-driven approach, in this context I spent a little more time on other aspects,implementing only a few examples of unit tests for the APIs. 

## Run and deploy the application
Whit the `docker-compose` file is possible to create docker containers to run the application.

I started with a slim Docker image for `Python 3.10.4`. 
I then set up a working directory along with two environment variables:

PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)

Then, I copied over the `requirements.txt` file, installed the dependencies, and copied over the project.

The docker-compose will also create a data-api-mongodb container allowing the connection with the data-api container through the env variable `DATABASE_URL`.

In order to build the image, run: 
`docker-compose build`

Once the image is built, run the container:
`docker-compose up -d`

Navigate to `http://localhost:8008/` 
(I left the hello world api in the main.py in order to rapidly check that the web service is up and running)
