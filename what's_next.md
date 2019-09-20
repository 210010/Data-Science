# What's Next

## Description of the Project - Nico
  - Discuss why this project is important
  - initial thoughts regarding implementation (twitter api and assess)
  - Overall what the project looks like from here
  
## Challenges
 - One of the initial challenges for this project was that the original vision was perhaps just a bit wide.  Original plan was to use the twitter api to source tweets of people complaining, run them through a sentiment analysis filter, and run all this through BERT/ELMO.  The issue with this was a lack of consistency not only in what the tweets were complaining about (structural, emotional, value-based, etc.) but also a disconnect between things like subject verb agreement, and trying to find out if a tweet was a two+ part message, because all of that would require concatenation to train on.  
 - We also ran into issues with the amount of data we could lift per day from twitter.  Our original plan was to source at least 400k for BERT and then later LeakGAN, but you were only allowed a couple thousand a day, so even if we all pooled our api access we wouldnt even begin to approach that number, especially after refinement and filtering.
 - We then tried to source data from soomething more semantically similar, so the machine could parse the text and learn from it easier.  We settled on startup descriptions(all similarly structured, each contains a problem someone is trying to make money off of, each explains possible solution), but this too was not smooth.  The repositories for company descriptions were locked behind paywalls, except for one -angelist.  However, angelist had no api and anti-bot measures, making it hard to bulk collect.  Nonetheless, we ended up creating a scraper that could partially bypass catchas and scrape descriptions off the website, however due to the slow speed and inconsistent descriptions added to angelist, we ended up having to pay for the crunchbase API access, and ended up with about 180k descriptions (~65k post filtering).
 - After we got a more useful form of data by using the descriptions of startups, we ran into issues with our models.  Without a much larger data source, BERT was not going to do too well for our purposes.  We then switched to leakGAN, only to find out that some of the code base was in python 2.7, some in 3.x, and some only worked on linux and not windows.  So instead of trying to fix their entire codebase so that we could even begin the project proper, we hopped again, this time examining Language Models, and settled on the mid-sized GPT-2.
 - After this, we found generation to be easy, but there were still issues.  Many of the generated ideas were based in compliance, manufacturing, and other solutions that were unusable by the Lambda Labs staff.  We therefore began the task of stripping out companies that were likely useless, to ensure our primer text was clean and taught the machine to create more useful ideas.  At the other end, we needed to create some gates that would ensure the output could pass as mostly reasonable speech so it could be passed to our labeling portion.  This went through several iterations, with a few surprising discoveries along the way.
 - Once the output was refined, we faced one more issue: the consumer needed a way to quickly run through the hypothetically limitless amount of descriptions quickly to find the most usable ones.  Here we decided to implement a voting system, which essentially allowed us to have the students who would eventually use these products, do the labelling for us.  This helped ensure a wider range of viewpoints and ultimately stronger project, and 'should' make sure the top descriptions are things people want to make.  
 - Once the data science part was rolling along, the next hurdle was learning enough javascript, react, node, and knex to make a functioning website and backend complete with a voter mechanism, with none of us but our TL having any experience in it.  Thanks to the excellent teaching, guidance, and more than a little work by our TL Matt Feldman, a fine web developer, we were able to deploy in only 2 weeks, with each of us responsible for various parts.
 
## Current Solution - Tomas
  - Technical explanation of the project
  - What technical avenues we used to solve the issues
  - Any lingering issues that couldn't be solved, or were added with the solution
  
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