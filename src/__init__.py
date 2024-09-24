from fastapi import FastAPI
from src.api.routes import sheet_data
from src.db.main import DatabaseLoad
import pickle


version = 'v1'
app = FastAPI()
main_df = DatabaseLoad().load_data()


output_path = r'C:\Users\vipul\OneDrive\Desktop\army\src\sharex_state\share_data.pkl'
with open(output_path, 'wb') as f:
    pickle.dump(main_df, f)

app.include_router(sheet_data, prefix="/data")
