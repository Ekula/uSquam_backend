# Meeting notes, March 9

## Requirements discussion
* Flow diagram: UI not required, but would be nice
* Maybe finite state automata for conversation flow? Simple steps without complex tree is fine (might take to long, or cause problems. Don't aim too high)
Use existing framework for conversation (what to do with loops etc.)
Tree: "Are there many bikes in this picture? " -> few/many -> other answer
Input control: True / false: "How many bikes?" "Hundred" "I don't understand that, please enter a number"
* Stick to one messaging platform: Telegram
* Elastic search: Use for processing big data (e.g. twitter pipeline), not for 5 tasks/ 25 users. Also for complex search/processing. Input: 1000 tweets with #TUDelft, use elastic search to find tweets with requirements (e.g. geo), output: 50 tweets
* Use normal DB (MySQL, MongoDB) for the actual system
* For data import: Seperate conversion for services -> convert json of flickr/twitter to something our service can use. Our service doesn't know about other api's
Web form with download + progress

## Project idea document/ final report discussion
* Could discuss optimization of caching/db querying in presentation or final report
* Understand and appreciate complexity, approach in a simpler way
* Separate challenge type (technical, marketing, ) or prototype vs product challenges
* Requirements: Split for each part
* Do not add constraints (do not mention dropbox, twitter, etc.) -> generic
* Add use-cases with specific services

