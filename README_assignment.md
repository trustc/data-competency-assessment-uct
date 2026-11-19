# Provincial Health Data Centre - Data Engineer Challenge

## Purpose

The purpose of this challenge is to evaluate the skills of prospective data engineers for the Western Cape Government Provincial Health Data Centre. 

## Intended audience

We will only evaluate responses to this challenge from people who we have requested to complete it.

## Way of working and expected structure of submission
Principles of reproducible analysis and code versioning are very important to our workflow. Structuring your work to aid in reproducibility and readability is important. 

So, follow common conventions with respect to directory structure and names to make your work as easy to follow as possible.

## What we're looking for
### Expectation of Effort
We expect you to spend up to 2 hours working on this assessment per position. If you are finding that you are spending significantly more time than this, then please contact whomever sent you the link to this assessment to let them know.

### Things to focus on
As a data engineer, we would like you to focus on writing for easy comprehension, modularity, clean code, and testing if applicable.

### Candidates where programming is required (Data Scientist; Engineers, Visualisation Engineer and Front End Developers)
Requirements and notes:
* Our primary programming languages are `python`, and `SQL`. We will accept code that is packaged in `.py` files.
* Bash or similar scripting language files are fine for glue. You may develop in any development environment you choose.
* We expect to be able to clone your repo, immediately identify what script to execute from your README file, and execute it to completion with no human interaction.
  In order to ensure that our environment has the right libraries or packages, please follow standard python (PEP8) for structure in your code, i.e place `import` commands at the top of your scripts.
* If your repo does not clone and run, we will not attempt to fix it.
* If your analysis makes use of any external data, the data must either be included in the repo, or be downloaded automatically during script execution.

### Follow-on Questions
If we invite you to an interview, after completing and submitting this technical assessment, we will be asking follow-up 
questions about the work submitted. These questions might be at a very detailed level, or broadly conceptual, relating to 
the choices made in completing this assessment.

We do not expect perfect recall of what you may have submitted, but we do expect a deep knowledge of the content, and 
how it works.

### Use of Generative AI and/or Coding Agents
There is no restriction on the tools that you may use to complete this assessment. However we have tried to make the nature of this assessment within the scope of someone completing it without using AI assistance, as well as someone using them effectively.

If you do make use of Generative AI/Coding Agents, ensure that you have a deep understanding of the content generated as you will be asked questions on your submission.
## How to submit
1. Clone this repository and load it into your development environment. 
2. Work the challenge, committing regularly to document your progress. Try have structured, meaningful commits, where each one adds significant functionality in a coherent manner.
3. Host your repository somewhere that is publicly accessible. If you're using GitHub, please use a fork of our original repository.
4. Inform us via email that your challenge is complete, including a link to your repo. Be sure to make sure it is set to public.

## Challenge
Follow the below steps, completing those indicated as relevant to the positions for which you are interviewing. If there are any steps that you can not complete after a reasonable amount of effort, rather move on to later steps, attempting everything relevant at least once.

Your code should be well formatted according to generally accepted style guides and include whatever is necessary for a team-mate unfamiliar with it to maintain it.

### 0. Setup
#### Data
The data for this challenge is the City of Cape Town's service request (C3) dataset, published on the City's Open Data Portal (ArcGIS Hub):

https://odp-cctegis.opendata.arcgis.com/datasets/cctegis::service-requests-2023-until-06-october-2026-deprecated/explore

The dataset lists service requests and notifications captured in the City's SAP C3 Notifications system. Note that it is marked as deprecated and is no longer updated, so results should be stable between runs.

You must **not** download the data manually or commit a copy of the full dataset to the repo. The data must be retrieved programmatically by your code (see step 1).

Set up your repository so that it can be run end-to-end with a single documented command, with dependencies declared in a `requirements.txt` (or equivalent).

### 1. Data Extraction
Write a script that retrieves the data by making requests to the dataset's API.

* Work out the API endpoint behind the dataset page above. ArcGIS Hub datasets are backed by a feature service that exposes a REST query interface. Document in your README how you found it.
* Inspect the dataset's schema (field names and types) and record what you find.
* Filter on the server side (not after downloading everything) so that only records where `C3_Complaint_Type` is `'No Power'` are returned.
* Handle the API's limits correctly. Feature services cap the number of records returned per request, so your code must page through the results and retrieve **all** matching records.
* Include sensible error handling for network failures, timeouts and unexpected responses (e.g. retries with back-off), and use logging rather than `print` statements.
* Save the raw extracted records to a file in your repo's data directory (e.g. a `data/raw/` folder that is git-ignored) so that later steps do not have to call the API again.

### 2. Initial Data Transformation
Using the extracted data, produce a count of the 'No Power' reports by suburb.

* Aggregate the number of reports for each suburb and write the result to a CSV file (one row per suburb, with the suburb name and the report count), sorted by count in descending order.
* Examine the suburb field for data quality problems (for example missing or blank values, inconsistent capitalisation, stray whitespace, or spelling variants of the same suburb) and decide how to handle them. Document the decisions you made and why.
* Validate your result. At a minimum, check that the sum of the suburb counts reconciles to the total number of records extracted (accounting for any records with no suburb), and compare your total against the record count the API reports for the same filter.