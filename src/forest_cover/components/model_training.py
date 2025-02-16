import sys
from src.forest_cover.constants import *
from src.forest_cover.exeception import CustomException
from src.forest_cover.logger import logging
from src.forest_cover.entity.config_entity import *
from src.forest_cover.entity.artifact_entity import *
from neuro_mf  import ModelFactory
from src.forest_cover.entity.estimator import ForestModel
from src.forest_cover.utils.main_utils import *
from typing import List, Tuple
from sklearn.metrics import f1_score, precision_score, recall_score

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
        """
        Method Name :   get_model_object_and_report
        Description :   This function uses neuro_mf to get the best model object and report of the best model
        
        Output      :   Returns metric artifact object and best model object
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            
            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]

            best_model_detail = model_factory.get_best_model(
                X=x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_accuracy
            )
            model_obj = best_model_detail.best_model

            y_pred = model_obj.predict(x_test)
            
            f1 = f1_score(y_test, y_pred, average='micro')  
            precision = precision_score(y_test, y_pred, average='micro')  
            recall = recall_score(y_test, y_pred, average='micro')
            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
            
            return best_model_detail, metric_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            
            best_model_detail ,metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            
            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")

            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            forest_model = ForestModel(preprocessing_object=preprocessing_obj,trained_model_object=best_model_detail.best_model)
            
            logging.info("Created Forest model object with preprocessor and model")
            logging.info("Created best model file path.")
            save_object(self.model_trainer_config.trained_model_file_path, forest_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
            
        except Exception as e:
            raise CustomException(e, sys) from e






# import sys
# import mlflow
# from src.forest_cover.constants import *
# from src.forest_cover.exeception import CustomException
# from src.forest_cover.logger import logging
# from src.forest_cover.entity.config_entity import *
# from src.forest_cover.entity.artifact_entity import *
# from neuro_mf import ModelFactory
# from src.forest_cover.entity.estimator import ForestModel
# from src.forest_cover.utils.main_utils import *
# from typing import List, Tuple
# from sklearn.metrics import f1_score, precision_score, recall_score

# class ModelTrainer:
#     def __init__(self, data_transformation_artifact: DataTransformationArtifact,
#                  model_trainer_config: ModelTrainerConfig):
#         self.data_transformation_artifact = data_transformation_artifact
#         self.model_trainer_config = model_trainer_config

#     def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
#         """
#         Method Name :   get_model_object_and_report
#         Description :   This function uses neuro_mf to get the best model object and report of the best model
        
#         Output      :   Returns metric artifact object and best model object
#         On Failure  :   Write an exception log and then raise an exception
#         """
#         try:
#             logging.info("Using neuro_mf to get best model object and report")
#             model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            
#             x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]

#             best_model_detail = model_factory.get_best_model(
#                 X=x_train, y=y_train, base_accuracy=self.model_trainer_config.expected_accuracy
#             )
#             model_obj = best_model_detail.best_model

#             y_pred = model_obj.predict(x_test)
            
#             f1 = f1_score(y_test, y_pred, average='micro')  
#             precision = precision_score(y_test, y_pred, average='micro')  
#             recall = recall_score(y_test, y_pred, average='micro')
#             metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
            
#             # Log metrics to MLflow
#             mlflow.log_metric("f1_score", f1)
#             mlflow.log_metric("precision_score", precision)
#             mlflow.log_metric("recall_score", recall)
            
#             return best_model_detail, metric_artifact
        
#         except Exception as e:
#             raise CustomException(e, sys) from e
    
#     def initiate_model_trainer(self) -> ModelTrainerArtifact:
#         logging.info("Entered initiate_model_trainer method of ModelTrainer class")
#         try:
#             # set the tracking url
#             # mlflow.set_tracking_uri("http://127.0.0.1:8080")
#             # mlflow.set_tracking_uri("http://127.0.0.1:5000")
#             # Start an MLflow experiment
#             mlflow.set_experiment(self.model_trainer_config.experiment_name)
#             with mlflow.start_run() as run:
#                 train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
#                 test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
                
#                 best_model_detail, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
                
#                 if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
#                     logging.info("No best model found with score more than base score")
#                     raise Exception("No best model found with score more than base score")

#                 preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

#                 forest_model = ForestModel(preprocessing_object=preprocessing_obj, trained_model_object=best_model_detail.best_model)
                
#                 logging.info("Created Forest model object with preprocessor and model")
                
#                 # Save model with MLflow
#                 mlflow.sklearn.log_model(forest_model, "trained_model")
                
#                 # Save best model details
#                 save_object(self.model_trainer_config.trained_model_file_path, forest_model)

#                 model_trainer_artifact = ModelTrainerArtifact(
#                     trained_model_file_path=self.model_trainer_config.trained_model_file_path,
#                     metric_artifact=metric_artifact,
#                 )
                
#                 # Log model and artifact path to MLflow
#                 mlflow.log_artifact(self.model_trainer_config.trained_model_file_path)
#                 mlflow.log_params({
#                     "model_config_file": self.model_trainer_config.model_config_file_path,
#                     "expected_accuracy": self.model_trainer_config.expected_accuracy
#                 })
                
#                 logging.info(f"Model trainer artifact: {model_trainer_artifact}")
                
#                 # Log a message indicating the completion of training
#                 mlflow.log_param("status", "Training completed successfully")
                
#                 return model_trainer_artifact
            
#         except Exception as e:
#             raise CustomException(e, sys) from e
