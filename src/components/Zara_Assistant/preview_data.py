from dash import Dash, html
import dash_mantine_components as dmc
from dash.dependencies import Input, Output
from dash_iconify import DashIconify
import dash_ag_grid as dag

from dash.exceptions import PreventUpdate

from ...data.source import DataSource
# from ..production_performance.multiselect_helper import to_multiselect_options
from .. import ids, cns
import random


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.PREVIEW_DATA_TABLE, "rowData", allow_duplicate=True),
        Input(ids.MEMORY_OUTPUT, "data"),
    )
    def create_table(dataset):
        if dataset is None:
            raise PreventUpdate
        
        # Select the first 7 rows instead of a random sample
        # first_rows = dataset
        
        # print(f"first rows: {first_rows}")
        
        # print(f"dataset avaliable (5 first rows): {dataset[:5]}")
        
        return dataset
        
    return html.Div(className='table-div',
                    children=[
                        dag.AgGrid(
                            id=ids.PREVIEW_DATA_TABLE,
                            className=cns.OVW_PREVIEW_DATA_TABLE,
                            defaultColDef={
                                "resizeable": True,
                                "sortable": True,
                                "filter": True,
                            },
                            dashGridOptions={"pagination": True, "paginationPageSize":7, "paginationPageSizeSelector": False, "animateRows": False},
                            style={'height':'400px'}
                            
                        )
                    ]
                    )