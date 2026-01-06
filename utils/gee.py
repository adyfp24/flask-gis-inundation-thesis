import ee
import os

def init_gee():
    try:
        ee.Initialize(project=os.getenv("GEE_PROJECT_ID", "newokejek-58ec0"))
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=os.getenv("GEE_PROJECT_ID", "newokejek-58ec0"))
