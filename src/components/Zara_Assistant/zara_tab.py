from dash import Dash, html, Input, Output, callback, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from ...data.source import DataSource
from ...data.loader import ProductionDataSchema
from ...components import ids, cns


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.MEMORY_OUTPUT, 'data', allow_duplicate=True),
        Output(ids.PREVIEW_DATA_TABLE, 'columnDefs', allow_duplicate=True),
        Input(ids.ZARA_SEGMENTED_PREV, 'value'),
        # prevent_initial_call=True,
    )
    
    def create_table(data: str):

        df_production = source.df_production
        # df_gor = source.create_pivot_table_date_avg(ProductionDataSchema.WATER_CUT_DAILY, ProductionDataSchema.GAS_OIL_RATIO)
        df_log = source.df_log
        gdf_blocks = source.gdf_blocks
        gdf_wells = source.gdf_wells
        
        production_columns = df_production.columns.to_list()
        # gor_columns = df_gor.columns.to_list()
        log_columns = df_log.columns.to_list()
        blocks_columns = gdf_blocks.drop(columns=["tooltip","popup","geometry"]).columns.to_list()
        wells_columns = gdf_wells.drop(columns=["tooltip","popup","geometry"]).columns.to_list()
        
        if data == "data_production":
            return df_production.to_dict("records"), [{"field": i} for i in production_columns]
        
        # if data == 'data_gor':
        #     return df_gor.to_dict('records'), [{'field':i} for i in gor_columns]
        
        elif data == "data_log":
            return df_log.to_dict("records"), [{"field": i} for i in log_columns]
        
        elif data == "geodata_blocks":
            return gdf_blocks.drop(columns=["tooltip","popup","geometry"]).to_dict("records"),[{"field": i} for i in blocks_columns]
        
        elif data == "geodata_wells":
            return gdf_wells.drop(columns=["tooltip","popup","geometry"]).to_dict("records"),[{"field": i} for i in wells_columns]
        
        else:
            pass
        

    return html.Div(
        children=[
            dcc.Store(id=ids.MEMORY_OUTPUT),
            html.Div(
                className=cns.ZARA_TAB_SECTION,
                children=[
                    dmc.SegmentedControl(
                        id=ids.ZARA_SEGMENTED_PREV,
                        radius="md",
                        size="sm",
                        value="data_production",
                        data=[
                        {"value": "data_production", "label": "Production Data"},
                        # {'value': 'data_gor', 'label': 'Water Cut Daily Gas Ratio'},
                        {"value": "data_log", "label": "Log Data"},
                        {"value": "geodata_blocks", "label": "Blocks Data"},
                        {"value": "geodata_wells", "label": "Wells Data"},
                        ],
                    )
                ],
            )
        ],
    )
