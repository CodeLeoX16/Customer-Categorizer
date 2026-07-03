# 🛍️ Customer Categorizer - End-to-End Machine Learning Project

An end-to-end **Machine Learning** application that segments customers based on their demographic and purchasing behavior using **K-Means Clustering** and predicts the customer's segment using a **Logistic Regression** classifier.

The project implements a complete ML pipeline including data ingestion, validation, transformation, clustering, model training, evaluation, model versioning with AWS S3, MongoDB Atlas integration, Docker containerization, and deployment on Render.

---

## 🚀 Live Demo

🔗 **Application:**  
https://customer-categorizer-h3e6.onrender.com/

> **Note:** The application is hosted on Render's Free Tier. If inactive, the first request may take **45–60 seconds** while the server starts.

---

## 📌 Project Overview

Businesses collect a large amount of customer data but often struggle to identify meaningful customer groups.

This project automatically segments customers into different categories using **unsupervised learning (K-Means Clustering)**. After generating cluster labels, a **Logistic Regression classifier** is trained to predict the customer category for new users without re-running the clustering algorithm.

The system enables businesses to:

- Identify similar customers
- Build targeted marketing campaigns
- Improve customer engagement
- Personalize recommendations
- Increase customer retention

---

# ✨ Features

- End-to-End Machine Learning Pipeline
- Customer Segmentation using K-Means
- Customer Category Prediction
- Automated Data Validation
- Feature Engineering Pipeline
- Model Evaluation
- AWS S3 Model Storage
- MongoDB Atlas Integration
- Dockerized Application
- Responsive Flask Web Application
- Easy Deployment on Render

---

# 🛠️ Tech Stack

## Machine Learning

- Scikit-learn
- Pandas
- NumPy

## Backend

- Python
- Flask

## Database

- MongoDB Atlas

## Cloud

- AWS S3

## Deployment

- Docker
- Render

## Version Control

- Git
- GitHub

---

# 📂 Project Structure

```text
Customer-Categorizer/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── setup.py
├── config/
├── notebooks/
├── src/
│   ├── components/
│   ├── configuration/
│   ├── cloud_storage/
│   ├── pipeline/
│   ├── utils/
│   ├── logger/
│   ├── entity/
│   ├── constant/
│   └── exception/
│
├── templates/
├── static/
└── README.md
```

---

# 📊 Machine Learning Workflow

```
Raw Dataset
      │
      ▼
Data Ingestion
      │
      ▼
Data Validation
      │
      ▼
Feature Engineering
      │
      ▼
K-Means Clustering
      │
      ▼
Generate Cluster Labels
      │
      ▼
Train Logistic Regression
      │
      ▼
Model Evaluation
      │
      ▼
AWS S3 Model Storage
      │
      ▼
Prediction Pipeline
      │
      ▼
Flask Web Application
```

---

# 📈 Machine Learning Models

### Clustering Model

- K-Means Clustering

Purpose:

- Discover hidden customer groups
- Generate customer segment labels

---

### Classification Model

- Logistic Regression

Purpose:

- Predict customer segment for new customers
- Fast inference without re-running clustering

---

# 📁 Dataset

**Marketing Campaign Dataset**

Dataset Link:

https://github.com/entbappy/Branching-tutorial/blob/master/marketing_campaign.zip

The dataset contains customer information such as:

- Age
- Income
- Education
- Marital Status
- Purchase History
- Campaign Responses
- Spending Behavior

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/CodeLeoX16/Customer-Categorizer.git
```

---

## Move into Project

```bash
cd Customer-Categorizer
```

---

## Create Conda Environment

```bash
conda create -n customer python=3.11 -y
```

---

## Activate Environment

```bash
conda activate customer
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file and configure the following variables:

```env
AWS_ACCESS_KEY_ID=YOUR_KEY

AWS_SECRET_ACCESS_KEY=YOUR_SECRET

AWS_DEFAULT_REGION=YOUR_REGION

MONGODB_URL=YOUR_MONGODB_CONNECTION_STRING
```

---

# ▶️ Run Application

```bash
python app.py
```

Open:

```
http://localhost:5000/
```

---

# 🏋️ Train the Model

```
http://localhost:5000/train
```

The training pipeline performs:

- Data Ingestion
- Data Validation
- Data Transformation
- Feature Engineering
- Clustering
- Classification
- Evaluation
- Model Upload to AWS S3

---

# 🔍 Predict Customer Category

```
http://localhost:5000/predict
```

Enter customer details through the web interface and receive the predicted customer segment.

---

# 🐳 Docker Support

## Build Docker Image

```bash
docker build \
--build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
--build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
--build-arg AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> \
--build-arg MONGODB_URL=<MONGODB_URL> \
-t customer-categorizer .
```

---

## Run Docker Container

```bash
docker run -p 5000:5000 customer-categorizer
```

---

# ☁️ Cloud Services Used

## MongoDB Atlas

- Stores customer dataset

## AWS S3

- Stores trained models
- Stores preprocessing objects
- Enables model versioning

---

# 📷 Application Screenshots

Add screenshots here after deployment.

Example:

```
screenshots/
│
├── Home.png
├── Prediction.png
├── Training.png
└── Result.png
```

Then display them:

```markdown
![Home](screenshots/Home.png)

![Prediction](screenshots/Prediction.png)

![Result](screenshots/Result.png)
```

---

# 🚀 Future Improvements

- XGBoost Classifier
- Random Forest Classifier
- Model Monitoring
- MLflow Integration
- User Authentication
- REST API Documentation
- Kubernetes Deployment
- CI/CD Pipeline
- Explainable AI using SHAP

---

# 👨‍💻 Author

## Somnath Bhunia

Computer Science Engineering Student

GitHub:

https://github.com/CodeLeoX16

LinkedIn:

https://www.linkedin.com/in/YOUR-LINKEDIN/

---

# ⭐ If you found this project useful

Please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates further improvements.
