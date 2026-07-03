# 🛍️ Customer Categorizer - End-to-End Machine Learning Project

An end-to-end **Machine Learning** application that segments customers based on demographic and purchasing behavior using **K-Means Clustering** and predicts the customer's segment using a **Logistic Regression** classifier.

The project implements a complete ML pipeline including **Data Ingestion**, **Data Validation**, **Feature Engineering**, **Customer Segmentation**, **Model Training**, **Model Evaluation**, **AWS S3 Model Storage**, **MongoDB Atlas Integration**, **Docker Containerization**, and **Render Deployment**.

---

## 🚀 Live Demo

🔗 **Live Application:**  
https://customer-categorizer-h3e6.onrender.com/

> **Note:** This application is hosted on Render's Free Tier. If inactive, the first request may take **45–60 seconds** while the server starts.

---

# 📌 Problem Statement

Businesses collect large amounts of customer data but often struggle to identify meaningful customer groups for personalized marketing.

The objective of this project is to build an intelligent Machine Learning system that automatically segments customers based on their demographic and purchasing behavior. Once the customer groups are generated using clustering, a classification model predicts the appropriate customer segment for new customers.

This enables businesses to:

- Customer Segmentation
- Targeted Marketing
- Personalized Recommendations
- Customer Retention
- Better Business Decisions

---

# ✨ Features

- End-to-End Machine Learning Pipeline
- Customer Segmentation using K-Means
- Customer Category Prediction
- Automated Data Validation
- Feature Engineering
- Model Evaluation
- AWS S3 Model Storage
- MongoDB Atlas Integration
- Dockerized Application
- Responsive Flask Web Interface
- One-click Model Training
- Real-time Customer Prediction

---

# 🛠️ Tech Stack

### Programming Language

- Python

### Machine Learning

- Scikit-learn
- Pandas
- NumPy

### Backend

- Flask

### Database

- MongoDB Atlas

### Cloud

- AWS S3

### Deployment

- Docker
- Render

### Version Control

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
├── README.md
├── setup.py
│
├── config/
│
├── notebooks/
│
├── src/
│   ├── cloud_storage/
│   ├── components/
│   ├── configuration/
│   ├── constant/
│   ├── data_access/
│   ├── entity/
│   ├── exception/
│   ├── logger/
│   ├── ml/
│   ├── pipeline/
│   └── utils/
│
├── static/
├── templates/
└── flowchart/
```

---

# 🏗️ Project Architecture



 ![WhatsApp Image 2022-09-22 at 15 29 19](https://user-images.githubusercontent.com/71321529/192722336-54016f79-89ef-4c8c-9d71-a6e91ebab03f.jpeg)


---

# 📥 Data Collection Architecture


  ![WhatsApp Image 2022-09-22 at 15 29 10](https://user-images.githubusercontent.com/71321529/192721926-de265f9b-f301-4943-ac7d-948bff7be9a0.jpeg)


---

# ☁️ Deployment Architecture


![deployment](https://user-images.githubusercontent.com/104005791/199660875-c8e63457-432a-44cb-8a95-800870f3da15.png)


---

# 📊 Machine Learning Models

## Customer Segmentation

### K-Means Clustering

Used to group customers with similar purchasing behavior into different clusters.

---

## Customer Prediction

### Logistic Regression

Used to predict the customer segment for new customer records without re-running the clustering algorithm.

---

## Hyperparameter Optimization

- GridSearchCV

---

# 📁 Dataset

### Marketing Campaign Dataset

Dataset Link:

https://github.com/entbappy/Branching-tutorial/blob/master/marketing_campaign.zip

### Dataset Features

- Age
- Education
- Income
- Marital Status
- Number of Purchases
- Campaign Responses
- Spending Behaviour
- Customer Information

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/CodeLeoX16/Customer-Categorizer.git
```

---

## Move to Project Directory

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

Create a `.env` file and configure the following variables.

```env
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY

AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY

AWS_DEFAULT_REGION=YOUR_REGION

MONGODB_URL=YOUR_MONGODB_CONNECTION_STRING
```

---

# ▶️ Run the Application

```bash
python app.py
```

Open your browser:

```
http://localhost:5000/
```

---

# 🚀 Train the Model

Visit

```
http://localhost:5000/train
```

The training pipeline performs:

- Data Ingestion
- Data Validation
- Data Transformation
- Feature Engineering
- Customer Clustering
- Model Training
- Model Evaluation
- Model Upload to AWS S3

---

# 🔍 Predict Customer Category

Visit

```
http://localhost:5000/predict
```

Fill in the customer details and the trained model predicts the customer's category.

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

# ☁️ Cloud Services

## MongoDB Atlas

- Stores customer dataset

## AWS S3

- Stores trained models
- Stores preprocessing objects
- Model Versioning

---

# 📸 Application Screenshots

Create a folder named `screenshots/` and add images such as:

```text
screenshots/
│
├── home.png
├── prediction.png
├── result.png
└── training.png
```

Then display them:

```markdown
## Home Page

![Home](screenshots/home.png)

## Prediction Page

![Prediction](screenshots/prediction.png)

## Prediction Result

![Result](screenshots/result.png)
```

---

# 🚀 Future Improvements

- XGBoost Classifier
- Random Forest
- MLflow Integration
- Explainable AI (SHAP)
- CI/CD with GitHub Actions
- Kubernetes Deployment
- REST API Documentation
- User Authentication

---

# 👨‍💻 Author

## Somnath Bhunia

Computer Science Engineering Student

**GitHub**

https://github.com/CodeLeoX16

**LinkedIn**

[https://www.linkedin.com/in/YOUR-LINKEDIN/](https://www.linkedin.com/in/somnath-bhunia-3b300b328/)

---

# ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.
