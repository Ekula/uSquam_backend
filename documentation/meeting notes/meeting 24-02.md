# Meeting notes, February 24

## Requirements of platform

[Pavel's architecture](https://docs.google.com/drawings/d/1fbf5gVKvewwAHR3CKzhkDPumq-MS6L65V2qJOWIKA_c/edit)

* The bot should be passive, so the worker should initiate the conversation. The worker could ask ‘show me the tasks’ and then the bot could show a list of the tasks (or ask the worker how much time he has to do the task and then recommend him suitable tasks)
* Most chatbots use linear communication, but you are free to decide if you want to use more tree-based conversation (Worker: ‘show me tasks’ Chatbot: ‘how much time do you have?’ Worker: “10 minutes” Chatbot: “Where are you right now?” Worker: “Supermarket” 
instead of: Worker: “Show me tasks” Chatbot: *shows list*)
* Some kind of quality control, e.g. agreement scheme (present the same question to multiple people and check similarity) and gold standard questions (include some questions for which you have already defined the answers, check if the answers of the worker match with your answers. If not, you could decide to block the worker or to give him feedback ‘we didn’t expect that answer’)
* Offer three types of tasks: generated based on a global data source (twitter is recommended), local data source (csv with public links to photos on your dropbox e.g.) and situational tasks (e.g. ask worker to take a picture of EWI’s lunch room at 12:15. This could lead to tree-based conversations: after the picture is made, ask the worker to count the number of heads in the picture, ask if it is crowded, show two pictures and ask which one is more crowded.). Result of the situational task should always be a type of media (photo, video, audio). The situational task could be checked with a ‘review task’: ask another worker if two pictures are made in the same place e.g..
* The requesters’ API should at least enable you to show list of tasks and add a task (look up the crowdflower API for inspiration). Post data source using JSON. 
* Python is recommended for the requesters’ side and NodeJS for the workers’ side

## Additional notes
* No UI expected for the requesters’ side
* API endpoint is to collect results (think of ways the results could be utilized in a future project - e.g. the lunchroom pictures could be used to determine when the peak hours are in the canteen)
* Nice extension: tasks could be based on the GPS location of the worker, e.g. if the worker is nearby the supermarket the chatbot could ask him to make a picture of the Colgate toothpaste. Since the chatbot would not be able to access the GPS location of the worker all the time, he could also explicitly ask the worker before giving him a task.  

## IR side of the project:
* Apply IR techniques for quality control
* Natural language processing technique (use third party library!)
* Gather twitter data and sort it using an ElasticSearch instance

## Summary
We discussed the architecture of the platform: the workers side and requesters side. The requesters’ API should at least enable you to show list of tasks and add a task. The endpoint is to collect results (think of ways the results could be utilized in a future project). Three types of tasks need to be implemented: generated based on a global data source, generated based on local data source and situation based. The chatbot should be passive, preferably using tree-based conversation. Some kind of quality control (agree schement, gold standard questions) should be implemented to verify the workers’ answers. 

Nice extension: tasks could be generated based on the GPS location of the worker.