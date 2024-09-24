from fastapi import APIRouter
from src.data_manuplation.fetch_frontend_data import options_data
from src.schemas.data_validation import SelectionData
from src.data_manuplation.fetch_frontend_data import filter_data

# Create an APIRouter instance
sheet_data = APIRouter()


@sheet_data.get("/")
def read_root():
    return {'Message': 'Welcome to Army'}


@sheet_data.get("/data_selection")
def data_selection():
    options = options_data()
    return options


@sheet_data.post("/submit-selections")
def submit_selections(selection_data: SelectionData):
    print(selection_data)
    selected_fmn = selection_data.selected_fmn
    selected_branch = selection_data.selected_branch
    selected_sub_branch = selection_data.selected_sub_branch
    selected_detl = selection_data.selected_detl

    filtered_data = filter_data(selected_fmn, selected_branch, selected_sub_branch, selected_detl)

    return filtered_data
