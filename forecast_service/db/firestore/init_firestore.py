import importlib.util
import numpy
import pandas
import os
import sys
from google.cloud import firestore

mode_options = ["dev", "devcloud", "stage", "prod"]

print("""
App mode:
- options: {}
""".format(mode_options))
mode = input("Please make a selection: ")
if mode in mode_options:
    os.environ["APP_MODE"] = mode
else:
    sys.exit("Invalid mode")

# load models module
models_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
    "..", "..", "forecast_service", "forecast", "models.py"))
spec = importlib.util.spec_from_file_location("models", models_dir)
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)

# load parse_instance module
instance_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
    "..", "..", "forecast_service", "parse_instance.py"))
spec = importlib.util.spec_from_file_location("parse_instance", instance_dir)
parse_instance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parse_instance)


def get_db():
    # keyfile = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
    # "..", "..", "forecast_service", "instance", "google_service_account_default.json"))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = parse_instance.google_creds
    db = firestore.Client()
    return db

def insert_data(db):
    df = models.build_empty_df()
    df.loc[0] = ["01-01-2018", "VIX", "01-02-2018", 0.1, 1.0]
    df.loc[1] = ["01-01-2018", "VIX", "01-03-2018", 0.1, 1.0]
    models.insert_forecast_df(db, df)

if __name__ == "__main__":
    db = get_db()
    insert_data(db)