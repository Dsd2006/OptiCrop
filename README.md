
# 🌱 OptiCrop – AI Powered Smart Agriculture

## About the Project

OptiCrop is an AI-powered crop recommendation system that
uses soil nutrients and environmental conditions to
recommend suitable crops using Machine Learning.

## Main Features

- AI-based crop recommendation
- Soil nutrient analysis
- Weather parameter analysis
- Random Forest classification model
- Prediction confidence display
- Interactive analytics dashboard
- Prediction history
- SQLite database integration
- Responsive premium web interface

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming |
| Flask | Web Framework |
| Pandas | Dataset Processing |
| Scikit-learn | Machine Learning |
| Random Forest | Crop Prediction |
| SQLite | Database |
| HTML & CSS | Frontend |
| JavaScript | Interactions |
| Chart.js | Analytics Charts |

## Project Structure

OptiCrop/
- dataset/
  - crop_data.csv
- model/
  - train_model.py
  - crop_model.pkl
  - predict.py
- templates/
  - base.html
  - index.html
  - dashboard.html
  - recommend.html
  - about.html
- static/
  - css/style.css
  - js/script.js
  - images/
- app.py
- database.py
- requirements.txt
- README.md
- opticrop.db

## Installation

1. Install Python.
2. Open the project folder in VS Code.
3. Install dependencies:

   pip install -r requirements.txt

4. Train the Machine Learning model:

   python model/train_model.py

5. Start the application:

   python app.py

6. Open your browser:

   http://127.0.0.1:5000

## Input Parameters

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

## Model

Algorithm: Random Forest Classifier

The model is trained using the supplied crop dataset.
Its performance is evaluated using a test dataset.

## Disclaimer

Crop recommendations are model predictions and are
not guaranteed agricultural outcomes. Consult local
agricultural experts before making farming decisions.

## Developed As

AI and Machine Learning Project – OptiCrop.
