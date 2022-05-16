## KMS Tech Challenge 1 - Text to SQL

The challenge is to clean, add or remove data, continue fine-tuning the ML model to the best of your ability, and build a front-end UI that allows end-users to input the question in the native language then the system generates an SQL query for the final answer.

## Setup

To run on Google Drive, refer to [this file](./tech_step_drive.ipynb) or [click this link](https://drive.google.com/file/d/1dfrPY8gv2lM5_31ioT7IEZm9el1f8p7N/view?usp=sharing)

To run locally, git clone then refer to [package file](package.json)

The Google drive of project is [here](https://drive.google.com/drive/folders/1FjsHmYlKLp99j4wYI7ZtY62OnJXL95fR?usp=sharing)

The trained models are place [here](https://drive.google.com/drive/u/0/folders/1HRvlP4nsM8z4Jyn2yJ96hfNOjH4KA-Nc) for web, and you can change the path in [this file](./techchallenge1-sample/WebApp/API/server/text2sql/text2sql.py). Our current used one is train_model2.

Port:

> API: 8010

> UI: 8051

## Items:

1. Dataset resource: [WikiSQL](https://github.com/salesforce/WikiSQL) and [TextSQL Academic](https://github.com/jkkummerfeld/text2sql-data/tree/master/data)

2. Pre-processing

- Format academic text-to-sql dataset to trainable dataset
- Common NLP techniques: stemming, remove_punctuation, remove_whitespace, remove_stopwords, lemmatizing, numeric text to number

3. Training:

- Cloud resources utilization: Google Colab
- Get model result

4. Post-processing: handle invalid SQL syntax (for example, aggregation operation), handle short questions

5. Task achievements

- Get result with not high accuracy (have to improve and learn more)
- Still cannot answer more complex question

6. UI/UX: take sample UI from [here](https://github.com/kms-technology/techchallenge1-sample)

After taking this interesting challenge for 4 weeks, we have researched and learned quite a deal of things about the data, new technology, and we can actually start to step in the world of machine learning with some basic knowledge and fun stuff.
