import warnings
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uvicorn import run as app_run

from src.pipeline.prediction_pipeline import PredictionPipeline
from src.pipeline.train_pipeline import TrainPipeline
from src.constant.application import APP_HOST, APP_PORT

CLUSTER_PROFILES = {
    0: {
        "title": "Cluster 1",
        "summary": "Typically a lower-engagement or value-sensitive customer segment.",
        "reason_1": "This segment usually has more controlled spending and fewer premium purchases.",
        "reason_2": "It often represents customers who buy less frequently or in a more selective way.",
    },
    1: {
        "title": "Cluster 2",
        "summary": "Typically a regular, middle-value customer segment.",
        "reason_1": "This segment usually shows balanced income, spending, and purchase activity.",
        "reason_2": "It often reflects a steady customer with moderate use of different channels.",
    },
    2: {
        "title": "Cluster 3",
        "summary": "Typically a high-value, highly engaged customer segment.",
        "reason_1": "This segment usually has higher total spending and stronger category purchases.",
        "reason_2": "It often represents loyal customers who use web, store, and catalog channels more actively.",
    },
}

# Suppress system runtime warnings for a clean and readable terminal output stream
warnings.filterwarnings('ignore')

app = FastAPI(title="Customer Categorizer Service")

# Setup template engine directory tracking
templates = Jinja2Templates(directory='templates')

# Bind your static assets folder directory structure to the /static URL route path
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable global Cross-Origin Resource Sharing (CORS) security context exceptions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/train")
async def trainRouteClient():
    """
    Triggers the end-to-end data engineering pipeline sequence:
    Pulls collections from MongoDB, processes anomalies, refits weights,
    and updates the final model configuration directly to AWS S3.
    """
    try:
        TrainPipeline().run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/")
@app.get("/predict")
async def predictGetRouteClient(request: Request):
    """
    Renders the modern Bootstrap dashboard UI structure on the base path.
    Passes request explicitly as the first parameter to satisfy modern FastAPI versions.
    """
    try:
        return templates.TemplateResponse(
            request=request,
            name="customer.html",
            context={"result": None}
        )
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/")
@app.post("/predict")
async def predictRouteClient(
    request: Request,
    Age: str = Form(...), Education: str = Form(...), Marital_Status: str = Form(...), Parental_Status: str = Form(...),
    Children: str = Form(...), Income: str = Form(...), Total_Spending: str = Form(...), Days_as_Customer: str = Form(...),
    Recency: str = Form(...), Wines: str = Form(...), Fruits: str = Form(...), Meat: str = Form(...), Fish: str = Form(...),
    Sweets: str = Form(...), Gold: str = Form(...), Web: str = Form(...), Catalog: str = Form(...), Store: str = Form(...),
    Discount_Purchases: str = Form(...), Total_Promo: str = Form(...), NumWebVisitsMonth: str = Form(...)
):
    """
    Collects form metrics from the request context payload, transforms features,
    authenticates with S3 components, and returns the target cluster index.
    """
    try:
        input_data = [
            Age, Education, Marital_Status, Parental_Status, Children, Income,
            Total_Spending, Days_as_Customer, Recency, Wines, Fruits, Meat,
            Fish, Sweets, Gold, Web, Catalog, Store, Discount_Purchases,
            Total_Promo, NumWebVisitsMonth
        ]
        
        # Calculate cluster classification utilizing models pulled from S3
        predicted_cluster = PredictionPipeline().run_pipeline(input_data=input_data)
        raw_cluster_output = int(predicted_cluster[0])
        display_cluster_output = raw_cluster_output + 1
        cluster_profile = CLUSTER_PROFILES.get(
            raw_cluster_output,
            {
                "title": f"Cluster {display_cluster_output}",
                "summary": "The model returned a valid cluster label.",
            },
        )
        
        return templates.TemplateResponse(
            request=request,
            name="customer.html",
            context={
                "result": display_cluster_output,
                "raw_result": raw_cluster_output,
                "cluster_title": cluster_profile["title"],
                "cluster_summary": cluster_profile["summary"],
                "cluster_reason_1": cluster_profile["reason_1"],
                "cluster_reason_2": cluster_profile["reason_2"],
            }
        )
    except Exception as e:
        return {"status": False, "error": f"{e}"}

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)