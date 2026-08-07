# In-Vehicle Coupon Acceptance Prediction

Bachelor's Degree Machine Learning Project  
University of Milano-Bicocca

## Overview

Machine learning project focused on predicting whether a user will accept an in-vehicle coupon based on demographic, behavioural and trip-related information.

The task was formulated as a **binary classification problem**, with **sensitivity** selected as the primary evaluation metric to prioritise the identification of users likely to accept a coupon.

The project covered the complete modelling pipeline: data preprocessing, missing-value imputation, feature analysis, model selection, cross-validation, comparison of multiple classifiers and decision-threshold optimisation.

## Approach

The dataset contains information about user characteristics, previous consumer behaviour, coupon type and expiration, travel conditions, destination, passengers, weather and distance from the coupon location.

Preprocessing included removal of zero-variance and redundant variables, analysis of missing-data patterns and **MICE imputation**.

Feature relevance was assessed using **Boruta**, while several statistical and machine learning classifiers were trained and compared under a common **10-fold cross-validation** framework.

Models considered included logistic regression, Ridge regression, Naive Bayes, Partial Least Squares, decision trees, C5.0, Bagged Trees, Random Forest, Gradient Boosting and a neural network.

Model assessment was based on sensitivity, specificity and ROC analysis. After selecting the best-performing model, the classification threshold was explicitly optimised to increase sensitivity.

## Results

**Bagged Trees** were selected as the final model.

- Test AUC: **0.792**
- Selected probability threshold: **0.23**
- Validation sensitivity: **96.1%**
- Final scoring sensitivity: **95.4%**
- Final scoring accuracy: **67.9%**

The threshold was intentionally lowered from the conventional 0.5 value to favour the identification of potential coupon acceptors.

## Technologies

`R` · `RStudio` · `caret` · `ggplot2` · `pROC` · `ROCR` · `mice` · `Boruta` · `rpart` · `glmnet`

## Methods

`Binary Classification` · `Data Preprocessing` · `Missing-Value Imputation` · `MICE` · `Feature Selection` · `Boruta` · `Logistic Regression` · `Ridge Regression` · `Naive Bayes` · `Partial Least Squares` · `Decision Trees` · `C5.0` · `Bagging` · `Random Forest` · `Gradient Boosting` · `Neural Networks` · `10-Fold Cross-Validation` · `Hyperparameter Tuning` · `ROC/AUC Analysis` · `Threshold Optimisation` · `Sensitivity/Specificity Analysis`


