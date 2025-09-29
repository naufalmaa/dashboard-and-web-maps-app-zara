from dash import Dash, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from src.components import ids, cns

from ...data.source import DataSource

from ..web_maps import (
    skkmigas_maps,
)

from ..web_maps.data_color_map import colormap


def create_layout_skkmigas_map(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className=cns.MAP_WRAPPER,
        children=[
            
            # div left-side map (content(2)) map filter
            html.Div(
                className=cns.LEFT_SIDE_MAP,
                children=[
                    html.Div(
                        className=cns.TITLE_SUMMARY_LAYOUT,
                        children=[
                            html.H1("W-Know: SKKMigas", className=cns.TITLE_BLOCK),
                            html.H4("Summary"),
                            dmc.Spoiler(
                                className=cns.SUMMARY_BLOCK,
                                showLabel="Show More",
                                hideLabel="Hide",
                                maxHeight=50,
                                style={"marginBottom": 35},
                                children=[
                                    dmc.Text(
                                        """
                                        SKKMigas (Satuan Kerja Khusus Pelaksana Kegiatan Hulu Minyak dan Gas Bumi) is the Indonesian government agency responsible for managing and supervising upstream oil and gas activities. This map shows the concession blocks and well locations under SKKMigas jurisdiction.
                                        """
                                    )
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className=cns.MAP_ALL_FILTER,
                        children=[
                            # MAP COLOR FILTER
                            dmc.Accordion(
                                # value="color map filter",
                                radius=10,
                                variant="contained",
                                style={"marginBottom": 10},
                                children=[
                                    dmc.AccordionItem(
                                        [
                                            dmc.AccordionControl(
                                                "Map Settings",
                                                icon=DashIconify(
                                                    icon="ic:twotone-map", width=25
                                                ),
                                            ),
                                            dmc.AccordionPanel(
                                                html.Div(
                                                    children=[
                                                        # MAP COLOR FILTER
                                                        html.H5("Layout Map"),
                                                        dmc.RadioGroup(
                                                            [
                                                                dmc.Radio(
                                                                    i, value=k, color=c
                                                                )
                                                                for i, k, c in colormap()
                                                            ],
                                                            id="webmaps_color",
                                                            value="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                                                            orientation="vertical",
                                                            spacing="xs",
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ],
                                        value="color map filter",
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # div map-map (content(3))
            html.Div(
                className=cns.MAP_LEAFLET, children=[skkmigas_maps.render(app, source)]
            ),

        ],
    )