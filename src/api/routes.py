from fastapi import APIRouter
from src.data_manuplation.fetch_frontend_data import options_data
from src.schemas.data_validation import SelectionData

# Create an APIRouter instance
sheet_data = APIRouter()


@sheet_data.get("/")
def read_root():
    return {'Message': 'Welcome to Army'}


@sheet_data.get("/data_selection")
def data_selection():
    # Assuming options_data returns the necessary selection options
    options = options_data()
    return options


@sheet_data.post("/submit-selections")
def submit_selections(selection_data: SelectionData):
    # Extracting selected values from the request
    selected_column = selection_data.selected_column
    selected_fmn = selection_data.selected_fmn
    selected_branch = selection_data.selected_branch
    selected_sub_branch = selection_data.selected_sub_branch

    # Example logic to process or store the selections
    # You could run queries or do any processing with these values here
    result = {
        "message": "Selections received successfully",
        "selected_column": selected_column,
        "selected_fmn": selected_fmn,
        "selected_branch": selected_branch,
        "selected_sub_branch": selected_sub_branch
    }

    # You can also fetch filtered data from your database or another source based on selections
    # For example:
    # filtered_data = fetch_filtered_data(selected_fmn, selected_branch, selected_sub_branch)

    return result
