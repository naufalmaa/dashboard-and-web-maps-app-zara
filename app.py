from dash import Dash, html, Input, Output
import dash.exceptions
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from src.components.web_layout import create_layout
from src.data.loader import (
    load_well_production_data,
    load_all_blocks,
    load_all_wells,
    load_log_data,
    load_sbk_points,
    load_sbk_block
)
from src.components.header import (
    headerbar
)
from src.data.source import DataSource

from src.components import ids, cns


PRODUCTION_DATA_PATH = "./data/csv/aceh_production_data_daily_rev.csv"
BLOCK_DATA_PATH = "./data/geojson/all_blocks_rev.geojson"
WELL_DATA_PATH = "./data/geojson/all_wells_rev.geojson"
LOG_DATA_PATH = "./data/csv/aceh_log_data_rev.csv"
SBK_POINT_PATH = "./data/geojson/sbk_skkmigas_point.geojson"
SBK_BLOCK_PATH = "./data/geojson/sbk_skkmigas_blok.geojson"


data_well = load_well_production_data(PRODUCTION_DATA_PATH)
geodata_block = load_all_blocks(BLOCK_DATA_PATH)

# 150823
geodata_well = load_all_wells(WELL_DATA_PATH)

# 040823
data_log = load_log_data(LOG_DATA_PATH)

geodata_sbk_point = load_sbk_points(SBK_POINT_PATH)
geodata_sbk_block = load_sbk_block(SBK_BLOCK_PATH)


data = DataSource(
    _data=data_well,
    _geodata_blocks=geodata_block,
    _geodata_wells=geodata_well,
    _data_log=data_log,
    _geodata_sbk_point=geodata_sbk_point,
    _geodata_sbk_block=geodata_sbk_block
)

app = Dash(
    __name__,
    use_pages=True,
    # pages_folder="pages",
    prevent_initial_callbacks="initial_duplicate",
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.title = "W-Know"

def create_header_layout() -> html.Div:
    return html.Div(
        children=[
            dmc.Header(  # separator provided
                height=40,
                # fixed=True,
                children=[
                    
                    dmc.Group([
                        
                        dmc.Anchor("Home", href="/", underline=False),
                        dmc.Text("     |     ", color="#e9ecef"),
                        dmc.Anchor("Projects", href="/", underline=False),
                        dmc.Text("     |     ", color="#e9ecef"),
                        dmc.Anchor("Dashboards", href="/", underline=False),
                        dmc.Text("     |     ", color="#e9ecef"),
                        dmc.Anchor("About", href="/", underline=False),
                        dmc.Text("     |     ", color="#e9ecef"),
                        dmc.TextInput(
                            style={"width": 250},
                            placeholder="Search...",
                            rightSection=DashIconify(icon="ic:round-search"),
                        ),
                        dmc.Text("     |     ", color="#e9ecef"),
                        DashIconify(
                            className=cns.OVW_SC_ICON,
                            # id=ids.ICON_TITLE_SUMMARY_TOGETHER,
                            icon="ic:baseline-account-box",
                            # color="#012226",
                            height=25,
                            width=25,
                            # style={
                                # "marginTop": 5,
                                # "marginRight": 10,
                                # "float": "left",
                            # },
                        ),
                        dmc.Anchor("Sign in", href="/", underline=False),
                        dmc.Text("     |     ", color="#e9ecef"),
                        dmc.Image(
                        src="/assets/waviv_logo.jpg",
                        # alt="superman",
                        # caption="Funny Meme",
                        width=100,
                        style={
                                "marginTop": 5,
                                # "marginRight": 10,
                                "float": "left",
                            },
                        ),
                    ], 
                    className='header-center',
                    sx={'justifyContent': 'center'}
                    ),
                    # dmc.Space(h=10),
                ],
            )
        ], className=cns.NAVBAR,
    )

app.layout = html.Div(
    [
        create_header_layout(),
        create_layout(app, data),
        # dash.page_container
     ])


if __name__ == "__main__":
    app.run_server(debug=False, port=7500)
