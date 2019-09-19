# 99 problems 

You can find the project at [99problems](ninenineproblems.com).

## Contributors


|                                       [Michael Bundick](https://github.com/)                                        |                                       [Daniel Harris](https://github.com/)                                        |                                       [Tomas Fox](https://github.com/)                                        |                                       [Nicolas Montoya](https://github.com/)                                        |                                       [Matthew Feldman](https://github.com/)                                        |
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="./img/michaelbundick.png" width = "200" />](https://github.com/bundickm)                       |                      [<img src="./img/daniel.png" width = "200" />](https://github.com/veritaem)                       |                      [<img src="./img/tomasfox.jpg" width = "200" />](https://github.com/tomfox1)                       |                      [<img src="./img/127A9539-1.jpg" width = "200" />](https://github.com/NicoMontoya)                       |                      [<img src="./img/Matt.jpeg" width = "200" />](https://github.com/matt0418)                       |
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/bundickm)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/veritaem)             |           [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/tomfox1)            |          [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/NicoMontoya)           |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/matt0418)             |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/michael-bundick/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/daniel-harris-45a417176/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/tomasfox1/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/nico-montoya/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/matthew-r-feldman/) |

## Project Overview


 [Trello Board](https://trello.com/b/he82E7wv/labs-15-pain-point)

 [Product Canvas](https://www.notion.so/Pain-Point-Radar-d6bb1298df424fe694c16df3885c23ff)

Coming up with ideas for new projects that can be used by Lambda School is a difficult and time consuming task which can end up creating sub-optimal or superfluous projects. 

Can we auto-generate project descriptions which can be used to help craft ideas for projects?

[Deployed Front End](https://www.ninenineproblems.com)

### Tech Stack

- Python,
- Jupyter,
- Anaconda,
- Colaboratory,
- Knex,
- Node.js,
- React,
- React-express,
- styled-components,

### Predictions

Model attempts to generate descriptions of problems that can be worked on by humans.  It does this by using issues identified by humans as potentially profitable as a primer, and then is allowed to create.  After some logical gates on quality of output, output is turned over to voters, who winnow down the full body of ideas into the most useable projects, which are then given to Lambda Labs staff as part of Labs team ideation.

### Explanatory 

- We acquired API keys for crunchbase, and used a scraper to extract a little info from angellist (ended up not using)
- We are utilizing a preprocess filter to ensure primer text gives greater chance of quality output
- Model was then finetuned to produce better output over successive iterations
- Text was generated with varying degrees of creativity allowed until a happy medium was decided
- We are utilizing a postprocess series of gates in order to make sure that the descriptions at least mostly conform to language requirements (less repeating yourself, less useless info like who founded it and when)

### Data Sources

-   [crunchbase] (https://www.crunchbase.com)
-   [Angelist] (https://angelist.co)

### Python Notebooks

[Initial Training](https://github.com/labs15-pain-point/Data-Science/blob/master/notebooks/training_the_mid_size_GPT_2_model.ipynb)

[Initial Post-process](https://github.com/labs15-pain-point/Data-Science/blob/master/notebooks/GPT_2_Simple_Post_Processing.ipynb)

[Combined/Iterated Notebook](https://github.com/labs15-pain-point/Data-Science/blob/master/notebooks/Pain_Point_Finder_MVP_1.ipynb)

[Reusable Script Form](https://github.com/labs15-pain-point/Data-Science/blob/master/script/script1.py)

### 3️⃣ How to connect to the web API

[backend link - can use postman etc to access more directly](https://github.com/labs15-pain-point/backend)

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./guidelines/code_of_conduct.md.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Documentation

See [Backend Documentation](https://github.com/labs15-pain-point/backend/blob/master/README.md) for details on the backend of our project.

See [Front End Documentation](https://github.com/labs15-pain-point/frontend/blob/master/README.md) for details on the front end of our project.
