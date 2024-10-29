import os 
from pathlib import Path

package_name = 'forest_cover'

list_of_files = [
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/components/__init__.py",
    f"src/{package_name}/components/data_ingestion.py",
    f"src/{package_name}/components/data_validation.py",
    f"src/{package_name}/components/data_transformation.py",
    f"src/{package_name}/components/model_training.py",
    f"src/{package_name}/components/model_evaluation.py",
    f"src/{package_name}/components/mode_pusher.py",
    f"src/{package_name}/constants/__init__.py",
    f"src/{package_name}/configuration/__init__.py",
    f"src/{package_name}/entity/__init__.py",
    f"src/{package_name}/exeception/__init__.py",
    f"src/{package_name}/logger/__init__.py",
    f"src/{package_name}/utils/__init__.py",
    f"src/{package_name}/pipeline/__init__.py",
    f"src/{package_name}/pipeline/training_pipeline.py",
    f"src/{package_name}/pipeline/prediction_pipeline.py",
    "notebooks",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "config/model.yaml",
    "config/schema.yaml",
    
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")