from dash import Dash, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from src.components import ids, cns

from ..data.source import DataSource

from .header import headerbar

from .footer import footerbar

from .web_maps import (
    wmaps_layout,
    skkmigas_layout,
    # filter_maps,
    # restart_button,
    # leaflet_maps,
    # filter_well_maps,
    # restart_well_button,
)

from .overview import (
    overview_layout,
    # filter_maps,
    # restart_button,
    # leaflet_maps,
    # filter_well_maps,
    # restart_well_button,
)

from .production_performance import (
    production_performance_layout,
    # summary_card,
    # oil_rate_line_chart,
    # # forecasting_oil_rate_line_chart,
    # well_stats_subplots,
    # water_injection_subplots,
    # water_cut_gor_line_subplots,
    # oil_vs_water_subplots,
    # # dp_choke_size_vs_avg_dp_subplots,
    # well_main_multiselect,
    # from_date_datepicker,
    # to_date_datepicker
)

from .gng_analysis import (
    gng_layout,
    # well_log_filter,
    # well_log_graph,
)

from .Zara_Assistant import zara_layout

from .web_maps.data_color_map import colormap


def create_layout(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className=cns.WEB_CONTAINER,
        children=[
            # # div navbar (header(1))
            # html.Div(
            #     className=cns.NAVBAR,
            #     children=[
            #         # html.H1("Navigation Bar")
            #         headerbar.create_layout()
            #     ]
            # ),
            # # div for webmaps
            # html.Div(
            #     className=cns.MAP_CONTAINER,
            #     children=[
            #         wmaps_layout.create_layout_map(app, source)
            #     ]
            # ),
            # div for tab and tab list after map
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Overview", value="1"),
                            dmc.Tab("Operation Analysis", value="2"),
                            dmc.Tab("Production Performance Analysis", value="3"),
                            dmc.Tab("Geology & Geophysics Analysis", value="4"),
                            dmc.Tab(
                                html.A(
                                    "SEGY & LAS Viewer",
                                    href="http://127.0.0.1:8050/",
                                    target="_blank",
                                    style={
                                        "textDecoration": "none",
                                        "color": "inherit",
                                    },
                                ),
                                value="5",
                            ),
                        ],
                        className=cns.MAIN_TABLIST,
                        position="center",
                        grow=True,
                    ),
                    # # # Overview Wmaps
                    dmc.TabsPanel(
                        children=[
                            dmc.Tabs(
                                children=[
                                    dmc.TabsList(
                                        [
                                            dmc.Tab("Project Aceh", value="8"),
                                            dmc.Tab("SKK Demo", value="9"),
                                        ],
                                        # className=cns.MAIN_TABLIST,
                                        position="center",
                                        grow=True,
                                    ),
                                    # div for webmaps
                                    dmc.TabsPanel(
                                        children=[
                                            html.Div(
                                                className=cns.MAP_CONTAINER,
                                                children=[
                                                    wmaps_layout.create_layout_map(
                                                        app, source
                                                    )
                                                ],
                                            )
                                        ],
                                        value="8",
                                        className=cns.OVW_CONTAINER,
                                    ),
                                    dmc.TabsPanel(
                                        children=[
                                            html.Div(
                                                className=cns.MAP_CONTAINER,
                                                children=[
                                                    skkmigas_layout.create_layout_skkmigas_map(
                                                        app, source
                                                    )
                                                ],
                                            )
                                        ],
                                        value="9",
                                        className=cns.OVW_CONTAINER,
                                    ),
                                ],
                                value="8",
                                className=cns.MAIN_TABS,
                            )
                        ],
                        value="1",
                        className=cns.OVW_CONTAINER,
                    ),
                    # Operation Analysis (chatbot, preview data, about data)
                    dmc.TabsPanel(
                        overview_layout.create_layout(app, source),
                        value="2",
                        className=cns.OVW_CONTAINER,
                    ),
                    # tabs for production performance analysis
                    dmc.TabsPanel(
                        production_performance_layout.create_layout(app, source),
                        value="3",
                        className=cns.PPD_CONTAINER,
                    ),
                    # tabs for gng analysis
                    dmc.TabsPanel(
                        gng_layout.create_layout(app, source),
                        value="4",
                        className=cns.GNG_CONTAINER,
                    ),
                    # tabs for segy viewer
                    dmc.TabsPanel(
                        "You will be redirected to SEGY & LAS Viewer",
                        value="5",
                        className=cns.CAD_CONTAINER,
                    ),
                ],
                value="1",
                # value="2",
                # variant="default",
                className=cns.MAIN_TABS,
            ),
            #     ]
            # )
            html.Div(
                className=cns.ZARA_FLOAT_BUTTON,
                children=[zara_layout.create_layout(app, source)],
            ),
            # Div Footer (Footer(6))
            html.Div(
                className=cns.FOOTER_WEB,
                children=[
                    # html.H1("Footer"),
                    footerbar.create_layout(app, source)
                ],
            ),
        ],
    )
    #     ]
    # )
