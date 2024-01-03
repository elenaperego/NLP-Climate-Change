# Climate Analysis Project

## Introduction
The Climate Analysis Project explores the relationship between media portrayal and public perception of climate change. Employing advanced natural language processing (NLP) techniques, this project conducts sentiment analysis and forecast analysis (specifically Granger Causality analysis) on climate change-related articles and World Bank data. The goal is to assess how environmental events and media sentiment on climate change vary across different U.S. states.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Dependencies](#dependencies)
5. [Documentation](#documentation)
6. [Contributors](#contributors)

## Installation
To run the scripts and notebooks in this project, you will need Python installed on your machine. Additionally, several Python libraries are required, including Jupyter for running the notebooks.

```bash
pip install jupyter pandas numpy matplotlib seaborn requests beautifulsoup4 nltk vaderSentiment
```

## Usage
1. **`get_climate_data.py`**: Run this script to download and preprocess climate-related data. The output will be a structured dataset on a csv file ready for analysis.
   ```bash
   python get_climate_data.py
   ```

2. **`sentiment_analysis.py`**: This script performs sentiment analysis on textual data. It requires a preprocessed text file and outputs sentiment scores always in a csv file.
   ```bash
   python sentiment_analysis.py
   ```

3. **`climate_analysis.ipynb`**: Open this Jupyter notebook to perform detailed climate data analysis, including statistical tests and visualizations.

4. **`nyt_extraction.ipynb`**: Use this notebook to extract news articles from The New York Times, focusing on climate-related content. The output is also a csv file.

5. **`sentiment_analysis_results.ipynb`**: This notebook presents the results of the sentiment analysis, including charts and interpretation.

## Features
- Data extraction from the New York Times API and World Bank Climate Change Knowledge Portal.
- Sentiment analysis using VADER and DistilBERT on climate-related news articles.
- Forecast analysis with Granger Causality to assess predictive relationships between climate change patterns and media sentiment.
- Analysis of regional variations in media response to climate change across U.S. states.

## Dependencies
- Python: The core programming language used.
- Jupyter: For running and viewing the notebooks.
- Pandas & NumPy: For data manipulation and numerical calculations.
- Matplotlib & Seaborn: For data visualization.
- Requests & BeautifulSoup4: For web scraping (used in `nyt_extraction.ipynb`).
- NLTK & VaderSentiment: For natural language processing and sentiment analysis (used in `sentiment_analysis.py`).

## Documentation
The project involves several key methodologies:
- **Sentiment Analysis**: Using VADER and DistilBERT to analyze the tone of news articles.
- **Granger Causality Analysis**: To examine the predictive relationship between climate metrics and news sentiment.
- **Data Extraction**: Using New York Times API and World Bank data to gather relevant climate and media data.

## Contributors
- Junyan Zhu
- Lisa Carle
- Elena Perego
- Brennan Xavier McManus



