import pickle
from src.db.main import DatabaseLoad


def options_data():
    df = DatabaseLoad().load_data()


    fmn_rows = df['Fmn'].unique().tolist()
    branch = df['Branch'].unique().tolist()
    sub_branch = df['Sub Branch'].unique().tolist()
    detailment = df['Detl'].unique().tolist()
    columns_names = df.columns.tolist()
    remove_column = ['Fmn', 'Branch', 'Sub Branch', 'Detl']
    for column in remove_column:
        if column in columns_names:
            columns_names.remove(column)
    return {
        "columns_names": columns_names,
        "fmn_rows": fmn_rows,
        "branch": branch,
        "sub_branch": sub_branch,
        "detl": detailment
    }


def filter_data(fmn=None, branch=None, sub_branch=None, detl=None):
    df = DatabaseLoad().load_data()

    # Apply filters based on provided parameters
    if fmn and fmn != 'All':
        df = df[df['Fmn'] == fmn]
    if branch and branch != 'All':
        df = df[df['Branch'] == branch]
    if sub_branch and sub_branch != 'All':
        df = df[df['Sub Branch'] == sub_branch]
    if detl and detl != 'All':
        df = df[df['Detl'] == detl]

    df_json = df.to_json(orient='records')  # Convert DataFrame to JSON format
    return df_json
