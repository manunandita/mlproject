import os
import sys
import pandas as pd
import numpy as np
import dill
from src.exception import CustomException


def save_object(file_path,file_obj):
    try:
        dir_path=os.makedirs(os.path.dirname(file_path),exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(file_obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)