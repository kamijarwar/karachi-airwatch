# karachi-airwatch
"An end-to-end Machine Learning-powered daily AQI forecasting and public health advisory system for Karachi, featuring an interactive bilingual (English/Roman Urdu) Streamlit dashboard and a robust XGBoost model trained on historical atmospheric data."
# 🌍 Karachi AirWatch

### Machine Learning-Based Air Quality Forecasting for Karachi, Pakistan

**Predict. Explain. Protect.**

Karachi AirWatch is a machine learning project designed to forecast Karachi's next-day average US Air Quality Index (AQI) using historical air-quality data. The project combines time-series feature engineering, machine learning model comparison, and an evaluation-focused workflow to explore how historical pollution patterns can support air-quality awareness.

The project uses historical air-quality data from the Open-Meteo Air Quality API and compares multiple regression models to identify the best-performing approach.

> **Project Status:** Model training and offline evaluation are complete. An interactive Streamlit dashboard with live forecasting and Roman Urdu health guidance is planned.

---

## 📌 Table of Contents

* [Project Overview](#-project-overview)
* [The Problem](#-the-problem)
* [Project Objectives](#-project-objectives)
* [Dataset](#-dataset)
* [Machine Learning Workflow](#-machine-learning-workflow)
* [Feature Engineering](#-feature-engineering)
* [Models Used](#-models-used)
* [Model Evaluation](#-model-evaluation)
* [Key Findings](#-key-findings)
* [Planned Features](#-planned-features)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Installation and Setup](#-installation-and-setup)
* [How It Works](#-how-it-works)
* [Limitations](#-limitations)
* [Future Improvements](#-future-improvements)
* [Team](#-team)
* [Data Source](#-data-source)

---

## 🔎 Project Overview

Air pollution is an important environmental concern in large cities such as Karachi. Air-quality conditions can change over time, making it valuable to investigate whether historical observations can help estimate future AQI levels.

Karachi AirWatch applies machine learning to historical air-quality data to predict the next day's average US AQI.

The project follows an end-to-end machine learning workflow:

**Data Collection → Data Cleaning → Exploratory Data Analysis → Feature Engineering → Model Training → Evaluation → Forecasting Dashboard**

Rather than relying solely on a complex model, the project evaluates multiple algorithms against a simple persistence baseline to measure whether machine learning provides a meaningful improvement.

### Project Highlights

* Historical air-quality data covering January 2024 to October 2026.
* 24,576 hourly observations collected.
* Daily aggregation for time-series forecasting.
* Lag-based and rolling-average features.
* Comparison of four forecasting approaches.
* Chronological train/test split.
* Evaluation using MAE and RMSE.
* Transparent reporting of model performance and limitations.

---

## 🚨 The Problem

Karachi faces environmental challenges associated with air pollution. Understanding recent air-quality patterns can help people explore how pollution levels change over time.

However, a forecasting model must be evaluated carefully before its predictions can be treated as reliable.

Karachi AirWatch investigates three questions:

1. Can historical AQI observations help predict the following day's average AQI?
2. Does a machine learning model outperform a simple baseline?
3. How can predictions and their limitations be communicated clearly to users?

The project is an experimental forecasting system, not an official air-quality monitoring or public-warning service.

---

## 🎯 Project Objectives

The main objectives are:

1. Collect historical hourly air-quality data for Karachi.
2. Perform data quality checks and exploratory data analysis.
3. Convert hourly observations into daily average values.
4. Engineer time-dependent features from historical AQI.
5. Train and compare different regression models.
6. Evaluate model performance on chronologically later observations.
7. Compare machine learning results against a persistence baseline.
8. Develop an interactive dashboard for presenting forecasts and historical trends.
9. Investigate whether adding weather features improves forecasting performance.

---

## 📊 Dataset

### Data Source

The dataset was collected using the **Open-Meteo Air Quality API**.

**Location:** Karachi, Pakistan
**Date Range:** January 1, 2024 – October 20, 2026
**Data Frequency:** Hourly

### Dataset Summary

| Property                    | Details                       |
| --------------------------- | ----------------------------- |
| Raw observations            | 24,576 hourly rows            |
| Daily modeling table        | 1,016 rows                    |
| Missing values              | 0 reported                    |
| Main variables              | PM2.5, PM10, US AQI           |
| Forecast target             | Next-day daily average US AQI |
| Data frequency for modeling | Daily                         |

Hourly observations were aggregated into daily averages before feature engineering and model training.

Rows without sufficient historical information for the lag and rolling features were excluded from the modeling table.

### Important Data Consideration

The air-quality data used in this project is model-derived data from Open-Meteo, rather than direct measurements from a network of Karachi ground-level monitoring stations.

Therefore, the results should not be interpreted as verified street-level measurements or as proof of pollution conditions in individual Karachi neighbourhoods.

---

## ⚙️ Machine Learning Workflow

The project follows these stages:

### 1. Data Collection

Retrieve historical hourly air-quality observations from the Open-Meteo API.

### 2. Data Preparation

Inspect the dataset, check missing values, and aggregate hourly observations into daily averages.

### 3. Exploratory Data Analysis

Examine AQI distributions, temporal trends, and relationships between recent observations.

### 4. Feature Engineering

Create lagged AQI features, rolling averages, and calendar features.

### 5. Model Training

Train multiple regression models using the chronological training dataset.

### 6. Model Evaluation

Evaluate each approach on the later test period using Mean Absolute Error and Root Mean Squared Error.

### 7. Model Comparison

Compare machine learning performance against a persistence baseline.

### 8. Dashboard Development

The planned next stage is an interactive dashboard for displaying next-day forecasts, historical trends, evaluation results, and limitations.

---

## 🧠 Feature Engineering

Feature engineering is an important part of this project because air quality can exhibit temporal patterns.

The following features were used:

| Feature  | Description                      |
| -------- | -------------------------------- |
| `aqi`    | Current day's AQI                |
| `lag_1`  | AQI from one day earlier         |
| `lag_2`  | AQI from two days earlier        |
| `lag_7`  | AQI from seven days earlier      |
| `roll_3` | Recent three-day rolling average |
| `roll_7` | Recent seven-day rolling average |
| `month`  | Calendar month                   |

### Preventing Data Leakage

Rolling features were shifted before calculating their averages so that the target day's AQI was not included in the corresponding historical feature window.

The target is the next day's daily average AQI.

This approach is intended to ensure that the model uses historical information available before the prediction target.

Exploratory analysis indicated a correlation of approximately **0.80** between consecutive daily AQI observations in the collected series.

This suggests that recent AQI values contain useful information about short-term changes.

---

## 🤖 Models Used

Four approaches were evaluated.

### 1. Persistence Baseline

The baseline predicts that tomorrow's AQI will be the same as today's AQI.

This provides a simple reference point for determining whether more complex models add predictive value.

### 2. Linear Regression

A regression model used to evaluate linear relationships between the engineered features and the next day's AQI.

### 3. Random Forest Regressor

An ensemble learning approach that can model nonlinear relationships between features and the target.

### 4. XGBoost Regressor

A gradient-boosting model that builds an ensemble of decision trees to learn patterns in the training data.

XGBoost achieved the best results among the four evaluated approaches on the current chronological test set.

---

## 📈 Model Evaluation

The dataset was divided chronologically into training and testing periods.

| Dataset  | Date Range                        | Rows |
| -------- | --------------------------------- | ---: |
| Training | January 8, 2024 – March 29, 2026  |  812 |
| Testing  | March 30, 2026 – October 19, 2026 |  204 |

A chronological split was used instead of a random split to better reflect the task of predicting future observations from historical data.

### Evaluation Metrics

**Mean Absolute Error (MAE)** measures the average absolute difference between predicted and observed values.

**Root Mean Squared Error (RMSE)** penalizes larger errors more strongly.

For both metrics, lower values indicate better performance.

### Results

| Model                |    MAE ↓ |   RMSE ↓ |
| -------------------- | -------: | -------: |
| Persistence Baseline |     6.31 |     8.49 |
| Linear Regression    |     6.12 |     8.20 |
| Random Forest        |     6.06 |     8.37 |
| **XGBoost**          | **5.86** | **8.14** |

### Best Performing Model: XGBoost

XGBoost achieved the lowest MAE and RMSE among the evaluated approaches.

Compared with the persistence baseline, its MAE improved by approximately **7.1%**.

This is a modest improvement, and the project does not claim that the model provides highly accurate predictions under all conditions.

Performance on future observations may differ from the reported test results.

---

## 🔍 Key Findings

### 1. Recent AQI Is Informative

The reported correlation between consecutive daily AQI observations is approximately 0.80, indicating substantial short-term persistence in the collected data.

### 2. XGBoost Performed Best

XGBoost achieved an MAE of 5.86 and RMSE of 8.14 on the current chronological test set.

### 3. Improvement Over the Baseline Is Modest

The MAE improvement over the persistence baseline was approximately 7.1%.

This highlights why simple baselines are important when evaluating forecasting models.

### 4. Feature Importance Reflects Historical Dependence

The current day's AQI had the highest reported feature importance, approximately 0.57.

This is consistent with the observed temporal correlation, but feature importance does not establish causation.

### 5. Seasonal Evaluation Remains Important

The current test period does not include the November–February winter season. The model's performance during those months therefore remains insufficiently established by the reported evaluation.

---

## 🖥️ Planned Features

The next development stage is a Streamlit dashboard.

Planned functionality includes:

### 📅 Next-Day AQI Forecast

Display the predicted daily average AQI for the following day using freshly retrieved data and correctly constructed prediction features.

### 🎨 US AQI Category

Display the predicted AQI category with a corresponding colour.

### 📊 Historical Trends

Visualize recent seven-day and thirty-day AQI trends.

### 📉 Actual vs. Predicted Comparison

Show historical test observations alongside model predictions.

### 🧠 Model Performance

Display MAE, RMSE, and the comparison with the persistence baseline.

### 🌐 Roman Urdu Health Guidance

Provide simple informational guidance based on recognized AQI categories.

### ⚠️ Transparency Panel

Explain the data source, last update time, forecasting limitations, and historical model performance.

**Note:** These features are planned and should not be considered implemented until they have been developed and tested.

---

## 🧰 Technology Stack

| Technology       | Purpose                           |
| ---------------- | --------------------------------- |
| Python           | Core programming language         |
| Pandas           | Data manipulation and aggregation |
| NumPy            | Numerical operations              |
| Matplotlib       | Data visualization                |
| Scikit-learn     | Machine learning and evaluation   |
| XGBoost          | Gradient-boosting regression      |
| Jupyter Notebook | Data analysis and experimentation |
| Open-Meteo API   | Air-quality data source           |
| Streamlit        | Planned interactive dashboard     |

---

## 📁 Project Structure

A suggested repository structure is shown below. Update it to match the files actually included in your repository.

```text
karachi-airwatch/
│
├── README.md
├── data/
│   └── README.md
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_eda_and_feature_engineering.ipynb
│   └── 03_model_training_and_evaluation.ipynb
│
├── app/
│   └── streamlit_app.py
│
├── requirements.txt
└── .gitignore
```

The notebook and application filenames above are examples. Replace them with your actual filenames, and do not list files that are not present.

---

## 🚀 Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the placeholders with your GitHub username and repository name.

### Step 2: Create a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

Create a `requirements.txt` file containing the packages required by your actual notebooks and application.

A starting point may include:

```text
pandas
numpy
matplotlib
scikit-learn
xgboost
requests
jupyter
streamlit
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Notebooks

Start Jupyter Notebook:

```bash
jupyter notebook
```

Run the notebooks in the appropriate order, beginning with data collection and preprocessing.

The model-evaluation workflow should reproduce the chronological split and compare the baseline, Linear Regression, Random Forest, and XGBoost models.

Exact results may vary depending on the retrieved data, package versions, model parameters, and execution environment.

### Step 5: Run the Dashboard

After the Streamlit application has been implemented, run:

```bash
streamlit run app/streamlit_app.py
```

Adjust the command if your application uses a different filename or location.

---

## ⚠️ Limitations

Karachi AirWatch is an educational and experimental machine learning project.

Its current limitations include:

* **Model-derived data:** The selected air-quality series is not a direct network of verified ground-level measurements.
* **No street-level verification:** The current dataset does not support verified neighbourhood-level or street-level pollution claims.
* **Modest improvement:** XGBoost improves test MAE by approximately 7.1% over the persistence baseline.
* **Incomplete seasonal validation:** The current test period excludes November–February.
* **Changing environmental conditions:** Air quality can be influenced by weather, emissions, atmospheric processes, and other factors not fully represented by the current features.
* **Forecast uncertainty:** Historical evaluation metrics do not guarantee the accuracy of an individual future prediction.
* **Live forecast validation:** Fresh API retrieval and correct next-day prediction logic must be implemented and tested before the dashboard can be described as a live forecasting service.

Health guidance is informational and should not replace official local advisories or professional medical advice.

---

## 🚀 Future Improvements

* [ ] Complete the Streamlit dashboard.
* [ ] Implement and test fresh API retrieval for next-day forecasting.
* [ ] Display data update timestamps and handle API failures.
* [ ] Add rolling-origin time-series validation.
* [ ] Evaluate model performance across different seasons.
* [ ] Add weather features such as wind speed, humidity, and temperature.
* [ ] Compare the expanded model against the same baseline and test protocol.
* [ ] Investigate and validate prediction uncertainty estimates.
* [ ] Add Roman Urdu health guidance based on recognized AQI categories.
* [ ] Document model parameters and package versions.
* [ ] Improve reproducibility and application testing.

New features will be considered successful only when their benefits are supported by evaluation or appropriate testing.

---

## 👥 Team

**Karachi AirWatch Team**

* **Kamran** — Machine learning workflow and model evaluation
* **Hasnain** — Dashboard and application development
* **Rameen** — User experience, AQI guidance, and presentation

Update these roles to reflect each member's actual contributions.

---

## 📚 Data Source

**Open-Meteo Air Quality API**

* API: https://air-quality-api.open-meteo.com/
* Documentation: https://open-meteo.com/en/docs/air-quality-api

Please review the provider's current documentation, attribution requirements, and terms before publishing or redistributing the dataset.

---

## 📜 License

No license has been specified yet.

If you want others to reuse, modify, or distribute this project, select an appropriate open-source license and add a `LICENSE` file to the repository.

---

### 🌍 Karachi AirWatch

**Making air-quality forecasting more understandable through machine learning, transparent evaluation, and responsible communication.**
