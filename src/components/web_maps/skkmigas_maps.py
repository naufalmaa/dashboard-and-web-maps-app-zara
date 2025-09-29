from dash import Dash, html
import dash_leaflet as dl
import dash_mantine_components as dmc
from dash.dependencies import Input, Output
from dash_iconify import DashIconify
from dash_extensions.javascript import arrow_function, assign

from ...data.source import DataSource
from .. import ids, cns

import json
import geopandas as gpd
from statistics import mean
import os


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output("webmaps_skk", "children"),
        [
            Input("webmaps_color", "value"),
        ],
        prevent_initial_call=False,
    )
    def plot_skkmigas_map(
        map_color_chosen: str,
    ) -> html.Div:
        # # Load SKKMigas data
        # skkmigas_blocks_path = "./data/geojson/sbk_skkmigas_blok.geojson"
        # skkmigas_points_path = "./data/geojson/sbk_skkmigas_point.geojson"
        
        # # Check if files exist
        # if os.path.exists(skkmigas_blocks_path):
        #     skkmigas_blocks = gpd.read_file(skkmigas_blocks_path)
        # else:
        #     skkmigas_blocks = gpd.GeoDataFrame()
            
        # if os.path.exists(skkmigas_points_path):
        #     skkmigas_points = gpd.read_file(skkmigas_points_path)
        # else:
        #     skkmigas_points = gpd.GeoDataFrame()
            
        # print(f"skkmigas_blocks: {skkmigas_blocks}")
        # print(f"skkmigas_points: {skkmigas_points}")
        
        skkmigas_blocks = source.gdf_sbk_blocks
        skkmigas_points = source.gdf_sbk_points

        # print(f"SKK Migas Blocks Loaded: {'Empty' if skkmigas_blocks.empty else f'{(skkmigas_blocks.columns)} features'}")
        # print(f"SKK Migas Points Loaded: {'Empty' if skkmigas_points.empty else f'{(skkmigas_points.columns)} features'}")

        map_children = []
        center = [-3.5, 117.5]  # Default center for Indonesia
        zoom = 5 # Default zoom

        # Create and add GeoJSON layer for points if data exists
        if not skkmigas_points.empty:
            layer_points = dl.GeoJSON(
                id="skkmigas_points",
                data=json.loads(skkmigas_points.to_json()),
                # options={
                #     "pointToLayer": assign(
                #         """function(feature, latlng) {
                #             return L.circleMarker(latlng, {
                #                 radius: 6,
                #                 fillColor: "#ff0000",
                #                 color: "#000",
                #                 weight: 1,
                #                 opacity: 1,
                #                 fillOpacity: 0.8
                #             });
                #         }"""
                #     )
                # }
            )
            # map_children.append(layer_points)
            # If there are no blocks, center on the points
            if skkmigas_blocks.empty:
                bounds = skkmigas_points.total_bounds
                x = mean([bounds[0], bounds[2]])
                y = mean([bounds[1], bounds[3]])
                center = [y, x]
                zoom = 10

        # Create and add GeoJSON layer for blocks if data exists
        if not skkmigas_blocks.empty:
            layer_blocks = dl.GeoJSON(
                data=json.loads(skkmigas_blocks.to_json()),
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
                },
            )
            # map_children.append(layer_blocks)
            # Calculate center and zoom based on block boundaries
            bounds = skkmigas_blocks.total_bounds
            x = mean([bounds[0], bounds[2]])
            y = mean([bounds[1], bounds[3]])
            center = [y, x]
            zoom = 10
            
        # Add base map layers
        # map_children.extend([
        #     dl.TileLayer(
        #         url=map_color_chosen,
        #         attribution='&copy; <a href="http://www.waviv.com/">Waviv Technologies</a> ',
        #     ),
        #     dl.GestureHandling(),
        #     dl.FullScreenControl(),
        #     dl.MeasureControl(
        #         position="topleft",
        #         primaryLengthUnit="kilometers",
        #         primaryAreaUnit="hectares",
        #         activeColor="#C29200",
        #         completedColor="#972158",
        #     ),
        # ])

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
                    layer_points
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
            center=center,
            zoom=zoom,
            style={
                "width": "100%",
                "height": "800px",
            },
        )
    return html.Div(id="webmaps_skk")