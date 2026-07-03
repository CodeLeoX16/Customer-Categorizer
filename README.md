Markdown
# Customer Personality Segmentation

## Problem statement

In this data science project, you will build a machine learning system which will be able predict the personality of the customer using machine learning algorithms. This project will be very usefull for malls, various stores and companies which are product based. Based on customer's personal details and purchase details, we can cluster them and we can predict the customer's cluster number using classification techniques.

## Solution Proposed

Now the question is how to dynamically predict the cluster of the customer ?. One of the approaches which we can use of machine learning approach, where we can cluster the customer based on the details we have and predict the cluster type based on the domain knowledge and leverage previous customer data to predict the cluster. In this update, the user interface has been overhauled into a dark-mode glassmorphism dashboard that delivers a dynamic Executive Marketing Action Playbook tailored to each cluster.

### 🌐 Live Deployment Link
👉 **Production API Dashboard:** [https://customer-segmenter-service.onrender.com](https://customer-segmenter-service.onrender.com)
*(Note: App builds on Render Free Tier. If inactive, allow 45-60 seconds for the cloud container instance to spin back up).*

Dataset used
<html>
<a href="https://github.com/entbappy/Branching-tutorial/blob/master/marketing_campaign.zip"> Dataset Link</a>
</html>

## Tech Stack Used

1. Python (3.9+)
2. FastAPI
3. Machine learning algorithms (Scikit-Learn)
4. Docker
5. MongoDB Atlas

## Infrastructure required

1. AWS S3 (Region: eu-north-1)
2. Render / Azure
3. Github Actions

## How to run

Before you run this project make sure you have MongoDB Atlas account and you have the customer campaign dataset into it.

Step 1. Cloning the repository.

git clone https://github.com/Machine-Learning-01/Customer_segmentation.git


Step 2. Create a conda environment.

conda create --prefix venv python=3.9 -y


conda activate venv/


Step 3. Install the requirements

pip install -r requirements.txt


Step 4. Export the environment variable

```bash
# For Linux/macOS Bash Terminal:
export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=eu-north-1
export MONGO_DB_URL="mongodb+srv://somnath:Somnath2003@customercategorization.vbknzhm.mongodb.net/ineuron?appName=customercategorization"

# For Windows Command Prompt (cmd) use:
# set AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
# set AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
# set AWS_DEFAULT_REGION=eu-north-1
# set MONGO_DB_URL=mongodb+srv://somnath:Somnath2003@customercategorization.vbknzhm.mongodb.net/ineuron?appName=customercategorization
Step 5. Run the application server

python app.py
Step 6. Train application

Bash
http://localhost:5000/train
Step 7. Prediction application

Bash
http://localhost:5000/
Run locally
Check if the Dockerfile is available in the project directory

Build the Docker image

docker build --build-arg AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID> --build-arg AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY> --build-arg AWS_DEFAULT_REGION=eu-north-1 --build-arg MONGO_DB_URL="mongodb+srv://somnath:Somnath2003@customercategorization.vbknzhm.mongodb.net/ineuron?appName=customercategorization" -t customer-segmentation-app . 
Run the Docker image

docker run -d -p 5000:5000 customer-segmentation-app
Project Architecture -
Data Collection Architecture -
Deployment Architecture -
Models Used
K-Means

LogisticRegression

From these above models after hyperparameter optimization we selected these two models which were K-Means for clustering and Logistic Regression for classification and used the following in Pipeline.

GridSearchCV is used for Hyperparameter Optimization in the pipeline to optimize clustering silhouette boundaries and classification accuracy weights.

src is the main package folder which contains
Components : Contains all components of Machine Learning Project

Data Ingestion: Imports pipeline raw data from MongoDB Atlas database and creates train/test records.

Data Validation: Validates parameters schema definitions against data drift risks.

Data Transformation: Normalizes extreme variations, processes outliers via PowerTransform, and applies encoding mappings.

Data Clustering: Executes K-Means algorithms to label behavioral market clusters.

Model Trainer: Fits Logistic Regression models with nested hyperparameter checks.

Model Evaluation: Assesses trained scores against active model artifacts stored in cloud buckets.

Model Pusher: Synchronizes production-ready weights seamlessly with remote storage configurations.

Custom Logger and Exceptions are used in the Project for better debugging purposes.

Conclusion
This Project can be used in real-life by Users to translate mathematical cluster targets (Cluster 0-3) directly into automated business action strategies, helping retail structures retain churn-risk accounts and optimize loyalty conversions.
