# What's Next

## Description of the Project

  #### **Why This Project?**
  - As Lambda School grows there will be more and more students that participate in labs projects. Coming up with project ideas will be a near impossible task for the Lambda Labs staff in the future. Even if some ideas are recycled, or improved upon, there will always be a need for novel ideas. Without labs, students will not have a showcase project to discuss with employers. Without new ideas, labs will become less and less valuable for students in the future. This project aims not only to alleviate the idea formation process for the labs staff, but to save Labs for future Lambda students.
    
  #### **Initial Ideas**
  - At first, our team was looking to examine tweets from the general public on twitter. We could use the twitter API to pull data and examine as many tweets as we can. We aimed to detect sentiment to see if we could extract pain points, which could then be turned into ideas or problems for the Lambda Team.

      After some playing around and consultation with DS professors, our team decided to switch gears. While extracting pain points from tweets may have been possible, there was more direct manner to attack the problem. Instead we decided to create a large dataset of company descriptions from the internet. We sifted through Angel List, Pitchbook, LinkedIn and Crunchbase for the data. Ultimately crunchbase ended up being the easiest to extract data from.
      
  #### **Results**
  - After training a model with the crunchbase data, the team has come up with outputs that very closely resemble company descriptions. The text output is legible, and each describe an issue that is computer generated. Not every single output is sensible. Most are not ready to hand off to labs teams. What the team has been able to come up with is a trained model that generates text output in the format of a business problem. The future of this project will be to keep improving the output to the point that the Lambda Staff can cherry pick the best outputs from the model and put them straight into the hands of a Labs team.
  
## Challenges
 - One of the initial challenges for this project was that the original vision was perhaps just a bit wide.  Original plan was to use the twitter api to source tweets of people complaining, run them through a sentiment analysis filter, and run all this through BERT/ELMO.  The issue with this was a lack of consistency not only in what the tweets were complaining about (structural, emotional, value-based, etc.) but also a disconnect between things like subject verb agreement, and trying to find out if a tweet was a two+ part message, because all of that would require concatenation to train on.  
 - We also ran into issues with the amount of data we could lift per day from twitter.  Our original plan was to source at least 400k for BERT and then later LeakGAN, but you were only allowed a couple thousand a day, so even if we all pooled our api access we wouldnt even begin to approach that number, especially after refinement and filtering.
 - We then tried to source data from soomething more semantically similar, so the machine could parse the text and learn from it easier.  We settled on startup descriptions(all similarly structured, each contains a problem someone is trying to make money off of, each explains possible solution), but this too was not smooth.  The repositories for company descriptions were locked behind paywalls, except for one -angelist.  However, angelist had no api and anti-bot measures, making it hard to bulk collect.  Nonetheless, we ended up creating a scraper that could partially bypass catchas and scrape descriptions off the website, however due to the slow speed and inconsistent descriptions added to angelist, we ended up having to pay for the crunchbase API access, and ended up with about 180k descriptions (~65k post filtering).
 - After we got a more useful form of data by using the descriptions of startups, we ran into issues with our models.  Without a much larger data source, BERT was not going to do too well for our purposes.  We then switched to leakGAN, only to find out that some of the code base was in python 2.7, some in 3.x, and some only worked on linux and not windows.  So instead of trying to fix their entire codebase so that we could even begin the project proper, we hopped again, this time examining Language Models, and settled on the mid-sized GPT-2.
 - After this, we found generation to be easy, but there were still issues.  Many of the generated ideas were based in compliance, manufacturing, and other solutions that were unusable by the Lambda Labs staff.  We therefore began the task of stripping out companies that were likely useless, to ensure our primer text was clean and taught the machine to create more useful ideas.  At the other end, we needed to create some gates that would ensure the output could pass as mostly reasonable speech so it could be passed to our labeling portion.  This went through several iterations, with a few surprising discoveries along the way.
 - Once the output was refined, we faced one more issue: the consumer needed a way to quickly run through the hypothetically limitless amount of descriptions quickly to find the most usable ones.  Here we decided to implement a voting system, which essentially allowed us to have the students who would eventually use these products, do the labelling for us.  This helped ensure a wider range of viewpoints and ultimately stronger project, and 'should' make sure the top descriptions are things people want to make.  
 - Once the data science part was rolling along, the next hurdle was learning enough javascript, react, node, and knex to make a functioning website and backend complete with a voter mechanism, with none of us but our TL having any experience in it.  Thanks to the excellent teaching, guidance, and more than a little work by our TL Matt Feldman, a fine web developer, we were able to deploy in only 2 weeks, with each of us responsible for various parts.
 
## Current Solution

•	Technical explanation of the project
Our Data Science team trained Open-AI’s GPT-2 language model using a Python wrapper developed by Data Scientist Max Woolf. GPT-2 is an unsupervised learning language model whose sole objective is to predict with the highest degree of accuracy what the best next word is given a set of inputs. In other words, conditionally, given an input A, the model predicts an output B. GPT-2 was trained from a library of 8 million websites (40gb) from Reddit outbound links that received over 3 karma; the idea here was for Open-AI to feed GPT-2 a diverse knowledge base in order to give GPT-2 a solid grasp of the English language (grammar, semantic structure) and allow GPT-2 to work in a variety of unsupervised learning tasks.

•	What technical avenues we used to solve the issues
We implemented GPT-2’s smaller model using Max Woolf’s wrapper and fine-tuned it by feeding it over 170,000 company descriptions from Crunchbase. As outlined in the earlier sections of this file, we wanted our model output to closely replicate our input of company descriptions. In the preprocessing stages of our project we implemented common data wrangling, cleaning & handling libraries in Python, such as Pandas, Sklearn and Numpy. Aside from the GPT-2 wrapper we used, imported as a PyPI package, we also used Tensorflow to begin our GPT-2 model session, fine-tuning, and start generating an output. In the post-processing stages of our project we filtered out through stop words by using one of Spacy’s language models ‘en_core_web_sm’.

•	Any lingering issues that couldn't be solved, or were added with the solution
Open AI definitely made a stride with GPT-2 as an unsupervised language model that performs well in a variety of tasks; however, there was a major bottleneck we found in our implementation of it: 

As we used a GPT-2 wrapper, we were not able to fine-tune all the models’ hyper-parameters necessary to increase the likelihood of generating output that was indistinguishable from human-generated text. We faced the trade-off between going with a simpler application of the model (the wrapper we used) in which we still had a certain degree of flexibility, and implementing Open-AI’s full GPT-2 model which would have required out of scope levels of complexity in our end. Nevertheless, we still managed to create value by making the selection process for Lambda Labs easier. The hyper-parameters that were at our disposal such as the number of steps (epochs), or at what temperature to generate text were sufficient for the scope of this project, however, to reproduce company descriptions that are AI-generated and mostly useful and innovative, an attempt at deconstructing Open-AI’s 1.5 billion parameter (still not publically released) model would have had to be made.

  
## Possible avenues for improvement
There are a couple clear avenues for continued refinement and improvement of the project:
  1. Website Admin Functionality
    - Batch selection of the DB: Exposing batches of 100 descriptions at a time so that descriptions get the vote quantity they need while allowing new descriptions to be cycled in without dumping and repopulating the database.
    - Topic Selection: Allow viewing of leaderboard filtered by topic
    - Export Options: Allow for exporting by current batch, by topic, by all, etc.
    - Remove Descriptions: Some of the descriptions will be a clear no, allow the admin to drop those descriptions easily
  2. Website User Functionality
    - Allow users to also vote on what discipline the description best fits (iOS, DS, Web, etc.)
    - Allow users to comment on descriptions with the project they might make from it
  3. Voting
    - Manual filtering of the descriptions requires votes. Requesting that all labs and build week start with five minutes of voting would result in a large amount of filtering/labeling of the data in a short period of time.
    - Use the voting results to train a regression model to predict outcomes of other fake descriptions thus reducing (pre-assign votes based on the prediction) or eliminating the need for voting (Use only the model predictions instead)
  4. Pre/Post Processing
    - Source a data set that closer fits the problem/solution format or describes projects instead of companies
    - Manually curate the input data for the GPT-2 model. The more refined the input is, the more refined the output is
    - Categorize the output via LDA or LSA and the categories provided by Crunchbase
    - Label the output with a predicted discipline
<br/>
Besides incremental improvement it may be possible to outperform GPT-2 through other models:
  - Generative Adversarial Network: White papers on LeakGAN and other GANs show potential for useful description generation but may need modification that is laborious or complex.
  - Language Models: GPT-2 is one of a growing number of available and high perfoming LM's such as Bert and Megatron-LM. It's possible that one of the existing models may outperform GPT-2 for our use case or that a new model will be released with greater performance.
