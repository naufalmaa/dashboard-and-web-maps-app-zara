from dash import Dash, html
import dash_mantine_components as dmc
from dash.dependencies import Input, Output
from dash_iconify import DashIconify
import pandas as pd

from ...data.source import DataSource
from .. import ids, cns
from ..production_performance.multiselect_helper import to_multiselect_options
from ...data.loader import allWELLS


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.WELL_NAME_MULTISELECT, "value", allow_duplicate=True),
        [
            Input(ids.FROM_DATE_WELL, "value"),
            Input(ids.TO_DATE_WELL, "value"),
            Input(ids.ORIENTATION_WELL_CHECKBOX, "value"),
            Input(ids.STATUS_WELL_CHECKBOX, "value"),
            Input(ids.PURPOSE_WELL_CHECKBOX, "value"),
            Input(ids.TYPE_WELL_CHECKBOX, "value"),
        ],
    )
    def filter_well_func(
        chosen_from_date, chosen_to_date, chosen_orientation, chosen_status, chosen_purpose, chosen_type
    ):
        # df_filtered_oil_prod = source.filter(
        #     from_date=chosen_from_date, to_date=chosen_to_date
        # ).to_dataframe
        
        df_filtered_well_input = source.filter_well(
            orientation_well=chosen_orientation,
            status_well=chosen_status,
            purpose_well=chosen_purpose,
            type_well=chosen_type,
        ).to_dataframe_geopandas_temp
        return df_filtered_well_input[allWELLS.WELLBORE]

    return html.Div(
        children=[
            html.H5("Well Name", style={"marginTop": 10}),
            dmc.MultiSelect(
                placeholder="Select Borehole Name",
                id=ids.WELL_NAME_MULTISELECT,
                data=to_multiselect_options(source.all_name_well),
                value=source.all_name_well,
                style={"marginTop": 10},
                clearable=True,
                searchable=True,
                nothingFound="No Options Found",
            ),
            # html.H5('TVDSS in Meters', style={'marginTop':20}),
            # dmc.RangeSlider(
            #     id='range-slider-TVDSS',
            #     value=[500,2000],
            #     max=5000,
            #     min=0,
            #     marks=[
            #         {'value':2000, 'label':'2000m'},
            #         {'value':4000, 'label':'4000m'},
            #         ],
            #     style={'marginTop':10},
            #     color='dark'),
            # dmc.Text(id='output-porosity'), #output for slider porosity
            html.H5("Wellbore Orientation", style={"marginTop": 30}),
            dmc.CheckboxGroup(
                id=ids.ORIENTATION_WELL_CHECKBOX,
                orientation="vertical",
                children=[
                    dmc.Checkbox(
                        label="Vertical",
                        value="Vertical",
                        color="dark",
                        style={"marginTop": 0},
                    ),
                    dmc.Checkbox(
                        label="Horizontal",
                        value="Horizontal",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                    dmc.Checkbox(
                        label="Directional",
                        value="Directional",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                ],
                value=source.all_orientation_well
            ),
            html.H5("Status", style={"marginTop": 20}),
            dmc.CheckboxGroup(
                id=ids.STATUS_WELL_CHECKBOX,
                orientation="vertical",
                children=[
                    dmc.Checkbox(
                        label="Active",
                        value="Active",
                        color="dark",
                        style={"marginTop": 0},
                    ),
                    # dmc.Checkbox(
                    #     label="Inactive",
                    #     value="Inactive",
                    #     color="dark",
                    #     style={"marginTop": -15},
                    # ),
                    dmc.Checkbox(
                        label="Shut-in",
                        value="Shut-in",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                    dmc.Checkbox(
                        label="Suspended",
                        value="Suspended",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                    dmc.Checkbox(
                        label="Abandonment",
                        value="Abandonment",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                ],
                value=source.all_status_well
            ),
            html.H5("Purpose", style={"marginTop": 20}),
            dmc.CheckboxGroup(
                id=ids.PURPOSE_WELL_CHECKBOX,
                orientation="vertical",
                children=[
                    dmc.Checkbox(
                        label="Exploration",
                        value="Exploration",
                        color="dark",
                        style={"marginTop": 0},
                    ),
                    dmc.Checkbox(
                        label="Production",
                        value="Production",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                    # dmc.Checkbox(
                    #     label="Appraisal",
                    #     value="Appraisal",
                    #     color="dark",
                    #     style={"marginTop": -15},
                    # ),
                    dmc.Checkbox(
                        label="Injection",
                        value="Injection",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                    dmc.Checkbox(
                        label="Monitoring",
                        value="Monitoring",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                    # dmc.Checkbox(
                    #     label="Abandonment",
                    #     value="Abandonment",
                    #     color="dark",
                    #     style={"marginTop": -15},
                    # ),
                ],
                value=source.all_purpose_well
            ),
            html.H5("Type", style={"marginTop": 20}),
            dmc.CheckboxGroup(
                id=ids.TYPE_WELL_CHECKBOX,
                orientation="vertical",
                children=[
                    dmc.Checkbox(
                        label="Oil", value="Oil", color="dark", style={"marginTop": 0}
                    ),
                    dmc.Checkbox(
                        label="Gas", value="Gas", color="dark", style={"marginTop": -15}
                    ),
                    dmc.Checkbox(
                        label="Water",
                        value="Water",
                        color="dark",
                        style={"marginTop": -15},
                    ),
                    # dmc.Checkbox(
                    #     label="Observation",
                    #     value="Observation",
                    #     color="dark",
                    #     style={"marginTop": -15},
                    # ),
                ],
                value=source.all_type_well
            ),
        ]
    )
