# karachi-airwatch
"An end-to-end Machine Learning-powered daily AQI forecasting and public health advisory system for Karachi, featuring an interactive bilingual (English/Roman Urdu) Streamlit dashboard and a robust XGBoost model trained on historical atmospheric data."
# 🌍 Karachi AirWatch — ML-Based Air Quality Forecasting

### Predict. Explain. Protect.

**Karachi AirWatch** is a machine learning project focused on forecasting the next day's air quality in Karachi, Pakistan. It uses historical air quality data, time-series feature engineering, and machine learning models to predict the next day's average Air Quality Index (AQI).

The goal is to make air quality forecasting more understandable and useful through data-driven predictions and accessible health guidance.

---

## 📌 Project Overview

Air pollution is an important environmental concern in Karachi. Understanding changes in air quality can help people make more informed decisions about outdoor activities and potential health risks.

Karachi AirWatch explores whether historical air quality patterns can help predict the following day's AQI.

The project compares multiple machine learning models against a simple persistence baseline to evaluate whether machine learning provides a meaningful improvement.

### 🎯 Objectives

* Analyze historical air quality data for Karachi.
* Develop a next-day AQI forecasting model.
* Compare machine learning models with a baseline.
* Evaluate performance using MAE and RMSE.
* Explore ways to communicate air quality forecasts through understandable health guidance.
* Develop an interactive dashboard for presenting predictions and trends.

---

## 📊 Dataset

The project uses hourly air quality data obtained through the Open-Meteo Air Quality API.

**Dataset summary:**

| Property                                       | Details                            |
| ---------------------------------------------- | ---------------------------------- |
| Location                                       | Karachi, Pakistan                  |
| Data period                                    | January 1, 2024 – October 20, 2026 |
| Original data frequency                        | Hourly                             |
| Hourly records                                 | 24,576                             |
| Daily aggregated records                       | 1,016                              |
| Missing values in the collected hourly dataset | 0                                  |
| Prediction target                              | Next-day average AQI               |

The hourly observations were aggregated into daily records for forecasting.

**Data source:** [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)

---

## ⚙️ Project Workflow

The project follows a time-series machine learning workflow:

1. **Data Collection** — Retrieve historical air quality data.
2. **Data Preparation** — Organize hourly observations and aggregate them into daily records.
3. **Feature Engineering** — Create lag features and rolling averages using historical information.
4. **Chronological Train-Test Split** — Separate training and testing data according to time.
5. **Model Training** — Train and compare multiple regression models.
6. **Evaluation** — Measure performance using MAE and RMSE.
7. **Model Comparison** — Compare machine learning predictions against a persistence baseline.
8. **Dashboard Development** — Planned interactive interface for forecasts, trends, and health guidance.

---

## 🧠 Feature Engineering

Time-series features help the models learn from previous air quality observations.

| Feature  | Description                                  |
| -------- | -------------------------------------------- |
| `aqi`    | Current day's AQI                            |
| `lag_1`  | Previous day's AQI                           |
| `lag_2`  | AQI from two days earlier                    |
| `lag_7`  | AQI from seven days earlier                  |
| `roll_3` | Rolling average over the previous three days |
| `roll_7` | Rolling average over the previous seven days |
| `month`  | Month of the year                            |

**Preventing data leakage:** Rolling averages are shifted before calculation so that future observations are not included in historical features.

The target variable is the next day's average AQI.

---

## 🤖 Machine Learning Models

The following models were evaluated:

* **Persistence Baseline** — Predicts tomorrow's AQI using today's AQI.
* **Linear Regression** — Establishes a linear relationship between historical features and the target.
* **Random Forest Regressor** — Captures nonlinear patterns using an ensemble of decision trees.
* **XGBoost Regressor** — Uses gradient boosting to learn patterns in the engineered features.

The models are compared using the same chronological test period.

---

## 📈 Model Evaluation

The dataset was split chronologically, preserving the order of observations.

| Dataset  | Period                            | Records |
| -------- | --------------------------------- | ------: |
| Training | January 8, 2024 – March 29, 2026  |     812 |
| Testing  | March 30, 2026 – October 19, 2026 |     204 |

### Evaluation Results

| Model                |      MAE |     RMSE |
| -------------------- | -------: | -------: |
| Persistence Baseline |     6.31 |     8.49 |
| Linear Regression    |     6.12 |     8.20 |
| Random Forest        |     6.06 |     8.37 |
| **XGBoost**          | **5.86** | **8.14** |

**Best-performing model in this evaluation: XGBoost**

### What Do These Results Mean?

* XGBoost achieved the lowest MAE and RMSE among the evaluated models.
* Its MAE improved by approximately **7% compared with the persistence baseline**.
* Linear Regression and Random Forest also performed slightly better than the baseline on MAE.
* The results suggest that machine learning can improve next-day AQI predictions on this test period, although the improvement is modest.

These results are based on the available dataset and test period. Further validation is needed to assess performance across different seasons and pollution conditions.

---

## 🔍 Key Findings

### 1. Historical AQI Is an Important Predictor

The current AQI feature had an importance of approximately 0.57 in the current feature-importance analysis.

The lag-1 autocorrelation was approximately 0.80, suggesting that consecutive daily AQI observations tend to be related.

### 2. XGBoost Performed Best Among the Tested Models

XGBoost achieved an MAE of 5.86, compared with 6.31 for the persistence baseline.

### 3. A Baseline Is Essential

Comparing machine learning models against a simple baseline helps establish whether the additional model complexity provides a meaningful improvement.

### 4. Evaluation Needs to Cover Different Seasons

The test period does not include the winter months from November through February. Performance during those months remains to be evaluated.

---

## 🚀 Planned Dashboard Features

The following features are planned for the interactive dashboard:

* **Next-Day AQI Forecast** — Display the predicted AQI.
* **AQI Category** — Communicate the forecast using an appropriate air quality category.
* **Roman Urdu Health Guidance** — Present accessible, general advice based on the relevant AQI category.
* **7-Day and 30-Day Trends** — Visualize recent air quality patterns.
* **Actual vs. Predicted Chart** — Compare model predictions with observed AQI values.
* **Model Performance** — Display evaluation metrics.
* **Limitations Panel** — Explain data limitations and forecasting uncertainty.

The dashboard is planned; these features should be marked as completed only after they have been implemented and tested.

---

## 🛠️ Technology Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| Python           | Core programming language       |
| Pandas           | Data manipulation and analysis  |
| NumPy            | Numerical operations            |
| Matplotlib       | Data visualization              |
| Scikit-learn     | Machine learning and evaluation |
| XGBoost          | Gradient boosting model         |
| Jupyter Notebook | Experimentation and analysis    |
| Open-Meteo API   | Air quality data source         |
| Streamlit        | Planned interactive dashboard   |

---

## 📂 Suggested Project Structure

```text
Karachi-AirWatch/
│
├── data/
│   └── README.md
│
├── notebooks/
│   └── air_quality_analysis.ipynb
│
├── app/
│   └── streamlit_app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

*This is a suggested structure. Update the filenames to match the actual files in your repository.*

---

## 💻 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your actual GitHub username and repository name.

### 2. Navigate to the Project Folder

```bash
cd YOUR-REPOSITORY
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

If your repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

A starting list of dependencies for this project is:

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

Update this list to reflect the libraries actually used in the project.

### 5. Run the Notebook

```bash
jupyter notebook
```

### 6. Run the Dashboard

Once the Streamlit dashboard has been implemented:

```bash
streamlit run app/streamlit_app.py
```

---

## ⚠️ Limitations

Transparency is an important part of this project.

* **Data source:** The data comes from Open-Meteo's air quality service. It should not be presented as direct measurements from Karachi's ground-based monitoring stations unless independently verified.
* **Geographic scope:** The project focuses on Karachi and does not establish neighborhood-level air quality differences.
* **Seasonal evaluation:** The current test period excludes November through February, so winter performance has not yet been evaluated.
* **Prediction uncertainty:** Forecasts are estimates, not guarantees of future air quality.
* **Limited improvement:** The approximately 7% reduction in MAE over the persistence baseline is promising but modest.
* **Fresh forecasts:** A genuine next-day forecast requires the appropriate latest observations and a correctly configured prediction pipeline. A prediction for a date whose AQI is already known is not a future forecast.

The model should be evaluated on additional time periods before its predictions are used for practical decision-making.

---

## 🔮 Future Improvements

* Develop and test an interactive Streamlit dashboard.
* Add a genuine next-day forecasting pipeline using the latest available observations.
* Evaluate performance across different seasons, including winter.
* Test weather features such as temperature, humidity, and wind speed to determine whether they improve forecasting accuracy.
* Evaluate forecast reliability under different AQI conditions.
* Explore multi-day forecasting if it can be validated appropriately.
* Improve visualization and make health guidance accessible to a wider audience.

---

## 👨‍💻 Author

**Kamran Ali Jarwar**

IT Student | Machine Learning Enthusiast

Interested in machine learning, data analysis, and building practical AI-driven solutions to real-world problems.

---

## 📚 Data Source

* [Open-Meteo Air Quality API Documentation](https://open-meteo.com/en/docs/air-quality-api)
* [Open-Meteo](https://open-meteo.com/)


https://karachi-airwatch-hjbrisa9pat3ewuhwmkstb.streamlit.app
---

## 📄 License

A license has not yet been specified. Add an appropriate open-source license if you intend to allow others to reuse, modify, or distribute this project.
