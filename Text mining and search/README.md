# Text Mining: Italian Job Advertisements Analysis

This project analyses Italian online job advertisements through two complementary tasks: predicting
the professional title from the job description and discovering recurrent topics without supervision.

After exact deduplication, the dataset contains 28,130 descriptions and 615 job classes. The pi-
peline compares sparse TF–IDF features with 768-dimensional contextual embeddings from multi-
sentence-BERTino. Logistic regression, Random Forest and SGD classifiers are evaluated for both

representations, with explicit removal of job-title strings to reduce label leakage.
For topic modeling, the project compares LSA, LDA, HDP and BERTopic using topic coherence,

diversity and log-perplexity when applicable. TF–IDF with Random Forest obtains the best leakage-
controlled classification accuracy, while LDA offers the most balanced combination of topic coherence

and diversity.



## Execution Instructions

1. Ensure all required packages are installed:
```
   pip install -r requirements.txt
```

2. Place the dataset `sample_skill_extraction.csv` and tmes_functions.py in the project root directory.

3. Execute the notebook `text_mining_ita_jobs_ads.ipynb` from start to finish.

4. To visualize the outputs and plots it is possible to open the already created folder. 
There are html files regarding BERTopic and LDA, with their respective interactive interfaces, to open them you have to download.

**Note:** The notebook uses a caching system. To force regeneration of any component, set the corresponding flag to `True` in the configuration cell:
- `FORCE_REGENERATE_DATA`
- `FORCE_REGENERATE_EMBEDDINGS`
- `FORCE_REGENERATE_CLASSIFIERS`
- `FORCE_REGENERATE_TOPICS`

