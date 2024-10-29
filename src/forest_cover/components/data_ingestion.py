import os,sys
import pandas as pd
from src.forest_cover.logger import logging
from src.forest_cover.exeception import CustomException
from src.forest_cover.entity.config_entity import *
from src.forest_cover.entity.artifact_entity import *
from src.forest_cover.constants import *
from src.forest_cover.utils.main_utils import *
from sklearn.model_selection import train_test_split
# import os
# import sys

# from pandas import DataFrame
# from sklearn.model_selection import train_test_split

# from us_visa.entity.config_entity import DataIngestionConfig
# from us_visa.entity.artifact_entity import DataIngestionArtifact
# from us_visa.exception import USvisaException
# from us_visa.logger import logging

class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    # def load_data_from_local_file(self,file_path: str)->pd.DataFrame:
    #     try:
    #         feature_store_file_path = self.data_ingestion_config.feature_store_file_path
    #         dir_path = os.path.dirname(feature_store_file_path)
    #         os.makedirs(dir_path,exist_ok=True)
    #         if os.path.exists(feature_store_file_path):
    #             dataframe = pd.read_csv(feature_store_file_path)

    #         else:
    #             logging.info(f"Exporting data from local folder")
    #             forest_data = Forest_data()
    #             dataframe = forest_data.export_collection_as_dataframe(collection_name=COLLECTION_NAME)
    #             logging.info(f"Shape of dataframe: {dataframe.shape}")
                
    #             logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
    #             dataframe.to_csv(feature_store_file_path, index=False, header=True)
            
    #         return dataframe

    #     except Exception as e:
    #         raise CustomException(e, sys)




    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load a CSV file from a local path into a DataFrame, saving it to a feature store file path.
        
        Args:
            file_path (str): The path to the CSV file.
        
        Returns:
            pd.DataFrame: The loaded DataFrame.
        """
        try:
            # Define feature store file path and ensure the directory exists
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Load the file if it already exists in the feature store path
            if os.path.exists(feature_store_file_path):
                self.dataframe = pd.read_csv(feature_store_file_path)
                logging.info(f"Data loaded from feature store at {feature_store_file_path}")

            # Otherwise, load from the specified file path and save to feature store
            else:
                logging.info(f"Exporting data from local folder: {file_path}")
                self.dataframe = pd.read_csv(file_path)
                logging.info(f"Shape of dataframe: {self.dataframe.shape}")
                
                # Save to the feature store path
                self.dataframe.to_csv(feature_store_file_path, index=False, header=True)
                logging.info(f"Data saved to feature store at {feature_store_file_path}")
                
            return self.dataframe
        
        except Exception as e:
            raise CustomException(e, sys)
        
        # except FileNotFoundError:
        #     logging.error(f"Error: The file at {file_path} was not found.")
        #     return None
        

    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            train_set, test_set = train_test_split(dataframe, test_size = self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            dir_name = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_name, exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path, index= False, header= True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index= False, header= True)
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            dataframe = self.load_csv("notebook/covtype.csv")
            _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            dataframe = dataframe.drop(_schema_config['drop_columns'], axis=1)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path= self.data_ingestion_config.testing_file_path
            )
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e, sys)