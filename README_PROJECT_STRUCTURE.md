# Project File Structure

This file provides a clean overview of the current project layout for the Customer Categorizer project.

```text
Customer-Categorizer/
├── app.py
├── Dockerfile
├── README.md
├── README_PROJECT_STRUCTURE.md
├── requirements.txt
├── setup.py
├── assignment/
│   └── assignment.md
├── config/
│   ├── model.yaml
│   ├── prediction_schema.yaml
│   └── schema.yaml
├── customer_segmentation/
│   ├── artifact/
│   │   ├── 06_27_2026_02_03_24/
│   │   ├── 06_27_2026_02_09_40/
│   │   ├── 06_27_2026_02_11_09/
│   │   ├── 06_27_2026_02_12_25/
│   │   ├── 06_27_2026_02_17_56/
│   │   ├── 06_27_2026_02_19_37/
│   │   ├── 06_27_2026_02_21_06/
│   │   ├── 06_27_2026_02_27_00/
│   │   ├── 06_27_2026_02_35_28/
│   │   ├── 06_27_2026_02_37_12/
│   │   ├── 06_27_2026_02_46_00/
│   │   ├── 06_27_2026_02_52_33/
│   │   ├── 06_27_2026_03_05_59/
│   │   ├── 06_27_2026_03_12_20/
│   │   ├── 06_27_2026_03_45_13/
│   │   ├── 07_01_2026_14_31_35/
│   │   └── logs/
├── docs/
│   ├── automated_setup.md
│   └── manual_setup.md
├── flowchart/
├── notebooks/
│   ├── EDA.ipynb
│   ├── Feature_engineering_and_clustering.ipynb
│   ├── Feature_Selection_and_classification.ipynb
│   ├── marketing_campaign.csv
│   └── data/
│       └── clustered_data.csv
├── scripts/
│   ├── create_initial_setup.sh
│   └── delete_initial_setup.sh
├── src/
│   ├── cloud_storage/
│   │   ├── __init__.py
│   │   └── aws_storage.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_clustering.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── data_validation.py
│   │   ├── model_evaluation.py
│   │   ├── model_pusher.py
│   │   └── model_trainer.py
│   ├── configuration/
│   │   ├── __init__.py
│   │   ├── aws_connection.py
│   │   └── mongo_db_connection.py
│   ├── constant/
│   │   ├── __init__.py
│   │   ├── application.py
│   │   ├── database.py
│   │   ├── env_variable.py
│   │   └── s3_bucket.py
│   ├── data_access/
│   │   ├── __init__.py
│   │   └── customer_data.py
│   ├── entity/
│   │   ├── __init__.py
│   │   ├── artifact_entity.py
│   │   └── config_entity.py
│   ├── exception/
│   │   └── __init__.py
│   ├── logger/
│   │   └── __init__.py
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── metric/
│   │   └── model/
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── prediction_pipeline.py
│   │   └── train_pipeline.py
│   └── utils/
│       ├── __init__.py
│       └── main_utils.py
├── src.egg-info/
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── static/
│   └── css/
│       └── style.css
└── templates/
    └── customer.html
```

## Short Description

- `app.py`: application entry point
- `config/`: YAML configuration for model, schema, and prediction inputs
- `customer_segmentation/artifact/`: saved pipeline artifacts and logs from training runs
- `docs/`: setup and usage documentation
- `notebooks/`: exploration, feature engineering, and clustering notebooks
- `scripts/`: helper shell scripts for setup and cleanup
- `src/`: core application package with components, pipelines, utils, and entity definitions
- `static/` and `templates/`: frontend assets for the web interface

## Main Pipeline Areas

- Data ingestion and validation
- Data transformation and clustering
- Model training, evaluation, and push
- Prediction pipeline for inference

## Notes

- The artifact folders are timestamped run outputs and can grow over time.
- This file is meant as a quick navigation guide for the repository.
```