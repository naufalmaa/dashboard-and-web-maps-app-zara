from dash import Dash, html
import dash_leaflet as dl
import dash_mantine_components as dmc
from dash.dependencies import Input, Output
from dash_iconify import DashIconify
from dash_extensions.javascript import arrow_function, assign


from ...data.source import DataSource
from .. import ids, cns

import json
from statistics import mean


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.MAP_LAYOUT, "children"),
        [
            Input(ids.BLOCK_NAME_MULTISELECT, "value"),
            Input(ids.MAP_COLOR, "value"),
            Input(ids.WELL_NAME_MULTISELECT, "value"),
        ],
        prevent_initial_call=True,
    )
    def plot_map(
        block_name_multi_value: list[str],
        map_color_chosen: str,
        well_name_multi_value: list[str],
    ) -> html.Div:
        edited_blocks = source.filter_block(name_block=block_name_multi_value)
        edited_wells = source.filter_well(name_well=well_name_multi_value)

        series_geometry = edited_blocks.to_dataframe_geopandas_temp
        series_geometry_well = edited_wells.to_dataframe_geopandas_temp
        # edited

        layer_blocks = dl.GeoJSON(
            data=json.loads(series_geometry.to_json()),
            hoverStyle=arrow_function(
                dict(
                    weight=5,
                    fillColor="#45b6fe",
                    fillOpacity=0.5,
                    color="black",
                    dashArray="",
                )
            ),
            options={
                "style": {
                    "color": "black",
                    "weight": 3,
                    "dashArray": "30 10",
                    "dashOffset": "5",
                    "opacity": 1,
                    "fillColor": "#3a9bdc",
                },
                # 'onEachFeature': lambda feature, layer: layer.bindTooltip(feature['features']['properties']['name'])
            },
        )
        bounds = series_geometry.total_bounds
        x = mean([bounds[0], bounds[2]])
        y = mean([bounds[1], bounds[3]])
        location = (y, x)

        layer_wells = dl.GeoJSON(
            id="point_load",
            data=json.loads(series_geometry_well.to_json()),
        )
        bounds_point = series_geometry_well.total_bounds
        x_point = mean([bounds_point[0], bounds_point[2]])
        y_point = mean([bounds_point[1], bounds_point[3]])
        location_point = (y_point, x_point)

        if series_geometry.empty and series_geometry_well.empty:
            return dl.Map(
                children=[
                    dl.TileLayer(
                        url=map_color_chosen,
                        attribution='&copy; <a href="http://www.waviv.com/">Waviv Technologies</a> ',
                    ),
                    dl.GestureHandling(),
                    dl.FullScreenControl(),
                    dl.MeasureControl(
                        position="topleft",
                        primaryLengthUnit="kilometers",
                        primaryAreaUnit="hectares",
                        activeColor="#C29200",
                        completedColor="#972158",
                    ),
                ],
                center=[5.3, 96.3],
                zoom=11,
                style={
                    # 'z-index':'0',
                    "width": "100%",
                    "height": "800px",
                    # 'marginLeft':'0px',
                    # 'float':'right'
                },
            )

        elif series_geometry.empty:
            return dl.Map(
                children=[
                    dl.GeoJSON(layer_wells),
                    dl.TileLayer(
                        url=map_color_chosen,
                        attribution='&copy; <a href="http://www.waviv.com/">Waviv Technologies</a> ',
                    ),
                    dl.GestureHandling(),
                    dl.FullScreenControl(),
                    dl.MeasureControl(
                        position="topleft",
                        primaryLengthUnit="kilometers",
                        primaryAreaUnit="hectares",
                        activeColor="#C29200",
                        completedColor="#972158",
                    ),
                ],
                center=[5.3, 96.3],
                zoom=11,
                style={
                    # 'z-index':'0',
                    "width": "100%",
                    "height": "800px",
                    # 'marginLeft':'0px',
                    # 'float':'right'
                },
            )

        elif series_geometry_well.empty:
            return dl.Map(
                children=[
                    dl.GeoJSON(layer_blocks),
                    dl.TileLayer(
                        url=map_color_chosen,
                        attribution='&copy; <a href="http://www.waviv.com/">Waviv Technologies</a> ',
                    ),
                    dl.GestureHandling(),
                    dl.FullScreenControl(),
                    dl.MeasureControl(
                        position="topleft",
                        primaryLengthUnit="kilometers",
                        primaryAreaUnit="hectares",
                        activeColor="#C29200",
                        completedColor="#972158",
                    ),
                ],
                center=[x, y],
                zoom=11,
                style={
                    # 'z-index':'0',
                    "width": "100%",
                    "height": "800px",
                    # 'marginLeft':'0px',
                    # 'float':'right'
                },
            )

        return dl.Map(
            children=[
                dl.GeoJSON(
                    layer_blocks
                    # options={
                    #     "style": {"color": "blue", "weight": 1},
                    #     "onEachFeature": lambda feature, layer: layer.bindTooltip(
                    #         feature["properties"]["tooltip"]
                    #     ),
                    # },
                ),
                dl.GeoJSON(
                    layer_wells
                    # options={
                    #     'style': {'color': 'blue', 'weight': 1},
                    #     'onEachFeature': lambda feature, layer: layer.bindTooltip(
                    #         feature['properties']['tooltip']
                    #     ),
                    # }
                ),
                dl.TileLayer(
                    url=map_color_chosen,
                    attribution='&copy; <a href="http://www.waviv.com/">Waviv Technologies</a> ',
                ),
                dl.GestureHandling(),
                dl.FullScreenControl(),
                dl.MeasureControl(
                    position="topleft",
                    primaryLengthUnit="kilometers",
                    primaryAreaUnit="hectares",
                    activeColor="#C29200",
                    completedColor="#972158",
                ),
            ],
            center=[y, x],
            zoom=11,
            style={
                # 'z-index':'0',
                "width": "100%",
                "height": "800px",
                # 'marginLeft':'0px',
                # 'float':'right'
            },
        )

    return html.Div(id=ids.MAP_LAYOUT)
