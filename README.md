# uSquam - procrastinate productively, anywhere and anytime

uSquam (Latin: "anywhere") is a crowdsourcing platform foccussing on full flexibility and 
easy access such that you can use any spare minute to do some good and earn a buck or two 
while your at it. 

That is why we focus on easy interface through chatbots. Currently the following systems
are implemented: 

* Telegram - uSquam-bot

Just download the app and start a chat, it's super simple!

## Installation (for developers)
The backend requires the [flask](http://flask.pocoo.org) framework to be installed which is
a python library. 

```shell
$ pip install flask flask-restful
```

For testing you can either use ```nose``` which outputs just plain text or 
[```green```](https://github.com/CleanCut/green) which 
outputs beautifully colored code. You have to install either of those as well 

```shell
$ pip install nose
$ pip install green
```

## API keys

In order to keep our development bots separate you should generate your own 
API keys for your test bots. For **Slack** go to 
[this](https://in4325.slack.com/apps/new/A0F7YS25R-bots) link and add your 
bot. Afterwards update the key value in our secrets file `utils/secrets.py`.


## Testing (for developers)
All methods that we write should be tested. There is a ```test``` folder. Its contents are 
structured in the same way as the rest of the root of the package. Each file should have a
corresponding test_MODULENAME.py file. You can run tests either like this:

```shell
$ python setup.py test # runs tests with nose
$ green -vvv -r
```

## Architecture

Just a quick overview of how we thought to structure the project. 

### Folder structure
In general every file should include 

* **src** inlcudes our API classes like the `InteractionManager` and it's dependent classes
* **resources** includes all database documents and it's REST API endpoint definitions, each 
of those are in a separate subfolder
    - *task* would be one of the resources connected to the task
        * `blueprint.py` defines which HTTP methods perform which actions, the actions are 
        defined in `service.py` (Controller)
        * `service.py` defines the operations on the model (Controller)
        * `RESOURCENAME_model.py` defines the data model of the resource (Model)
    - `register.py` assign a URL for each resource blueprint
* **utils** includes all the tools we use and write but are not specific to this project, so 
they should not depend on anyhting connected to usquam.
* **test** includes our unit-tests and at some points also integration and end-to-end tests. 
It mirrors the root-folders structure with file names like `test_MODULENAME.py`

### Important components

One of the major components is the `InteractionRedirector`. This class is our framework independent
chatbot that handles input from the user based on the task they are performing. All interaction 
is handled through one function `onInput(user_id, message)` which receives the user_id and the 
message. For every user that interacts with the `InteractionRedirector`, a session is created. Thus,
based on the user_id we can check if the user is engaged in a session already or not. In the two
situations, the received message is processed differently:

* **idle**: No session exists yet, so the messages is interpreted to fit any of the following 
actions (handled by the `IdleInteractionHandler`)
    - *request task*: the user would like a task to work on
    - *check balance*: the user would like to know how many credits he or she has earned
    - *list tasks*: the user would like to see all available tasks
    - *...*: we could think of some chitchat like 'how are you?' or show statistics of how 
    many tasks have been performed so far or an option to give feedback 
* **engaged**: The user is engaged in a Session. In that case the Session object should be 
loaded from the database and based on the current step of the task and the input, the next
query should be send. This is done by the `SessionInteractionHandler` which is simply a 
state-machine which gets the current state from the Session object and runs a specific 
routine to determine the next state based on the message of the user.

### Requester API
The addition and management of tasks can be performed using our REST API. 
First, a `requester` account needs to be created:
```json
POST to /requesters
body: {
    "name": "string",
    "password": "string",
    "email": "string"
}
```
This request will yield a response containing your `requester_id`. 
Now, before a task can be created, a `data_collection` is needed. When a worker is assigned to a task,
  a random `task_data` item is chosen from the data collection that is specified in the task.
  We allow multiple `question_data` items to be created in a `task_data` item, 
  so that your task can contain questions about multiple pieces of data.
  
Such a data collection can be created as follows:
```json
POST to /requesters/<requester_id>/data
body: {
    "name": "string",
    "task_data": [
        {
            "question_data": [
                {
                    "type": "TEXT/IMAGE/URL",
                    "content":"string"
                }
            ]
        }
    ]
}
```

This request will yield a response containing a `data_collection_id`, which needs to be added to the request
for creating the `task` itself. Each question can contain a `question_data_idx`, 
which refers to the index of the `question_data` item from your `data_collection`. If no index is specified,
no data will be send along with that question. This can be useful for asking questions about the same
piece of data.
```json
POST to /tasks
body: {
	"name": "string",
	"requester_id": "<requester_id>",
	"data_collection_id": "<data_collection_id>",
	"questions": [
		{
			"message": "string",
			"expected_type": "TEXT/NUMBER/DATE/...",
			"suggestions": ["<string>"],
			"question_data_idx": <number, optional>
		}
	],
	"time_indication": <number>,
	"reward": <number>,
	"active": <boolean>
}
```
