# from functools import partial, reduce
from typing import Callable, Optional

import pandas as pd
import geopandas as gpd

# Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


class allBLOCKS:
    BLOCK_NAME = 'name'
    STATUS_BLOCK = 'status'
    OPERATOR_BLOCK = 'operator'
    TOTAL_WELL = 'num_well'
    AREA_BLOCK = 'sq_km'
    RESERVE_BLOCK = 'reserve'
    GEOMETRY_BLOCK = 'geometry'
    TOOLTIP = 'tooltip'
    POPUP = 'popup'

def create_tooltip_block_column(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf[allBLOCKS.TOOLTIP] = gdf[allBLOCKS.BLOCK_NAME]
    return gdf[allBLOCKS.TOOLTIP]

def create_popup_block_column(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf[allBLOCKS.POPUP] =  '''


    <strong><H4 style="margin-top:10px; margin-bottom:20px; font-family:Ubuntu, sans-serif; font-size: 25px; color:#3F72AF;">
    ''' + gdf['name'] + '</H4></strong>' + """


    <table style="height: 50px; width: 250px;">
        <tbody>
        <tr>
        <th class="data-cell-left"><strong>Status</strong></th>
        <td class="data-cell-right"> """ + gdf['status'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Operator</strong></th>
        <td class="data-cell-right"> """ + gdf['operator'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Number of Wells</strong></th>
        <td class="data-cell-right"> """ + gdf['num_well'].map(str) + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Area</strong></th>
        <td class="data-cell-right"> """ + gdf['sq_km'].map(str) + """ km<sup>2</sup></td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Reserve Estimation</strong></th>
        <td class="data-cell-right"> """ + gdf['reserve'].map(str) + """ MMbbl</td>
        </tr>
        """
    
    return gdf[allBLOCKS.POPUP]
    
def load_all_blocks(path: str) -> gpd.GeoDataFrame:
    
    all_blocks = gpd.read_file(
        path,
        dtype={
            allBLOCKS.BLOCK_NAME: str,
            allBLOCKS.STATUS_BLOCK: str,
            allBLOCKS.OPERATOR_BLOCK: str,
            allBLOCKS.TOTAL_WELL: int,
            allBLOCKS.AREA_BLOCK: float,
            allBLOCKS.RESERVE_BLOCK: float,
            allBLOCKS.GEOMETRY_BLOCK: str,
        }
    )
    all_blocks[allBLOCKS.TOOLTIP] = create_tooltip_block_column(all_blocks)
    all_blocks[allBLOCKS.POPUP] = create_popup_block_column(all_blocks)
    
    return all_blocks

################################################################

class allWELLS:
    WELLBORE = 'name'
    BLOCK_WELL = 'block'
    ORIENTATION_WELL = 'orient'
    STATUS_WELL = 'status'
    PURPOSE_WELL = 'purpose'
    TYPE_WELL = 'type'
    GEOMETRY_WELL = 'geometry'
    TOOLTIP = 'tooltip'
    POPUP = 'popup'

def create_tooltip_wells_column(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf[allWELLS.TOOLTIP] = gdf[allWELLS.WELLBORE]
    return gdf[allWELLS.TOOLTIP]

def create_popup_wells_column(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf[allWELLS.POPUP] = '''

    <strong><H4 style="margin-top:10px; margin-bottom:20px; font-family:Ubuntu, sans-serif; font-size: 25px; color:#3F72AF;">
    ''' + gdf['name'] + '</H4></strong>' + """


    <table style="height: 50px; width: 250px;">
        <tbody>
        <tr>
        <th class="data-cell-left"><strong>Orientation</strong></th>
        <td class="data-cell-right"> """ + gdf['orient'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Status</strong></th>
        <td class="data-cell-right"> """ + gdf['status'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Purpose</strong></th>
        <td class="data-cell-right"> """ + gdf['purpose'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Area</strong></th>
        <td class="data-cell-right"> """ + gdf['type'] + """</td>
        </tr>
        """
        
    return gdf[allBLOCKS.POPUP]

def load_all_wells(path: str) -> gpd.GeoDataFrame:
    
    all_wells = gpd.read_file(
        path,
        dtype={
            allWELLS.WELLBORE: str,
            allWELLS.BLOCK_WELL:str,
            allWELLS.ORIENTATION_WELL: str,
            allWELLS.STATUS_WELL: str,
            allWELLS.PURPOSE_WELL: str,
            allWELLS.TYPE_WELL: str,
            allWELLS.GEOMETRY_WELL: str,
        }
    )
    all_wells[allWELLS.TOOLTIP] = create_tooltip_wells_column(all_wells)
    all_wells[allWELLS.POPUP] = create_popup_wells_column(all_wells)
    
    return all_wells

##################################################################

# sbk viewer

def create_tooltip_sbk_points_column(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf["tooltip"] = gdf["WELL_NAME"]
    return gdf["tooltip"]

def create_popup_sbk_points_column(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf["popup"] = '''

    <strong><H4 style="margin-top:10px; margin-bottom:20px; font-family:Ubuntu, sans-serif; font-size: 25px; color:#3F72AF;">
    ''' + gdf['WELL_NAME'] + '</H4></strong>' + """


    <table style="height: 50px; width: 250px;">
        <tbody>
        <tr>
        <th class="data-cell-left"><strong>Basin Name</strong></th>
        <td class="data-cell-right"> """ + gdf['BASIN_NAME'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Operator</strong></th>
        <td class="data-cell-right"> """ + gdf['OPERATOR_N'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Contract</strong></th>
        <td class="data-cell-right"> """ + gdf['CONTRACT_N'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Block Name</strong></th>
        <td class="data-cell-right"> """ + gdf['BLOCK_NAME'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Class</strong></th>
        <td class="data-cell-right"> """ + gdf['WELL_CLASS'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Technical</strong></th>
        <td class="data-cell-right"> """ + gdf['TECHNICAL_'] + """</td>
        </tr>
        <tr>
        <th class="data-cell-left"><strong>Content</strong></th>
        <td class="data-cell-right"> """ + gdf['CONTENT'] + """</td>
        </tr>
        """
        
    return gdf["popup"]

def load_sbk_points(path: str) -> gpd.GeoDataFrame:
    
    all_wells = gpd.read_file(
        path
    )
    all_wells["tooltip"] = create_tooltip_sbk_points_column(all_wells)
    all_wells["popup"] = create_popup_sbk_points_column(all_wells)
    
    return all_wells

def load_sbk_block(path: str) -> gpd.GeoDataFrame:
    
    all_block = gpd.read_file(
        path
    )
    
    return all_block


##################################################################

class LogDataSchema:
    WELLBORE = "WELL_BORE_CODE"
    BLOCK = "BLOCK"
    DEPTH = "DEPTH_MD"
    X     = "X_LOC"
    Y     = "Y_LOC"
    Z     = "Z_LOC"
    CALI  = "CALI"
    RDEP  = "RDEP"
    GR    = "GR"
    RHOB  = "RHOB"
    NPHI  = "NPHI"
    SP    = "SP"
    DTC   = "DTC"
    LITH  = "LITH"
    # WELL_BORE_CODE,DEPTH_MD,X_LOC,Y_LOC,Z_LOC,CALI,RDEP,GR,RHOB,NPHI,SP,DTC,LITH

def load_log_data(path: str) -> pd.DataFrame:
    
    log_data = pd.read_csv(
        path,
        dtype={
            LogDataSchema.WELLBORE: str,
            LogDataSchema.BLOCK: str,
            LogDataSchema.DEPTH: float,
            LogDataSchema.X: float,
            LogDataSchema.Y: float,
            LogDataSchema.Z: float,
            LogDataSchema.CALI: float,
            LogDataSchema.RDEP: float,
            LogDataSchema.GR  : float,
            LogDataSchema.RHOB: float,
            LogDataSchema.NPHI: float,
            LogDataSchema.SP  : float,
            LogDataSchema.DTC : float,
            LogDataSchema.LITH: str,
        }
    )
    
    return log_data

################################################################
class ProductionDataSchema:
    DATE                  = "DATEPRD"
    MONTH                 = "MONTHPRD"
    YEAR                  = "YEARPRD"
    BLOCK                 = "BLOCK"
    WELLBORE              = "WELL_BORE_CODE"
    ON_STREAM_HRS         = "ON_STREAM_HRS"
    AVG_DOWNHOLE_PRESSURE = "AVG_DOWNHOLE_PRESSURE"
    AVG_DP_TUBING         = "AVG_DP_TUBING"
    AVG_WHP_P             = "AVG_WHP_P"
    AVG_WHT_P             = "AVG_WHT_P"
    DP_CHOKE_SIZE         = "DP_CHOKE_SIZE"
    BORE_OIL_VOL          = "BORE_OIL_VOL"
    BORE_GAS_VOL          = "BORE_GAS_VOL"
    BORE_WAT_VOL          = "BORE_WAT_VOL"
    BORE_WI_VOL           = "BORE_WI_VOL"
    FLOW_KIND             = "FLOW_KIND"
    MOVING_AVERAGE        = "MOVING_AVERAGE"
    MOVING_AVERAGE_OIL    = "MOVING_AVERAGE_OIL"
    MOVING_AVERAGE_WI     = "MOVING_AVERAGE_WI"
    WATER_CUT_DAILY       = "WATER_CUT_DAILY"
    GAS_OIL_RATIO         = "GAS_OIL_RATIO"
    # DATEPRD,WELL_BORE_CODE,ON_STREAM_HRS,AVG_DOWNHOLE_PRESSURE,AVG_DP_TUBING,AVG_WHP_P,AVG_WHT_P,DP_CHOKE_SIZE,BORE_OIL_VOL,BORE_GAS_VOL,BORE_WAT_VOL,BORE_WI_VOL,FLOW_KIND
    
# create new column moving average on production data csv
def create_moving_avg_column(df: pd.DataFrame, column_name: str, days: Optional[int] = None, ) -> pd.DataFrame:
    if days is None:
        days = 14
    
    df[ProductionDataSchema.MOVING_AVERAGE] = df[column_name].rolling(days).mean()
    return df[ProductionDataSchema.MOVING_AVERAGE]

# create new column water cut daily
def create_water_cut_column(df: pd.DataFrame) -> pd.DataFrame:
    df[ProductionDataSchema.WATER_CUT_DAILY] = (df[ProductionDataSchema.BORE_WAT_VOL] / (df[ProductionDataSchema.BORE_OIL_VOL] + df[ProductionDataSchema.BORE_GAS_VOL] + df[ProductionDataSchema.BORE_WAT_VOL])) * 100
    return df[ProductionDataSchema.WATER_CUT_DAILY]

# create new column gas oil ratio
def create_gor_column(df: pd.DataFrame) -> pd.DataFrame:
    df[ProductionDataSchema.GAS_OIL_RATIO] = df[ProductionDataSchema.BORE_GAS_VOL] / df[ProductionDataSchema.BORE_OIL_VOL]
    return df[ProductionDataSchema.GAS_OIL_RATIO]

def load_well_production_data(path: str) -> pd.DataFrame:
    
    production_data = pd.read_csv(
        path,
        dtype={
            ProductionDataSchema.WELLBORE             : str,
            ProductionDataSchema.BLOCK                : str,
            ProductionDataSchema.ON_STREAM_HRS        : float,
            ProductionDataSchema.AVG_DOWNHOLE_PRESSURE: float,
            ProductionDataSchema.AVG_DP_TUBING        : float,
            ProductionDataSchema.AVG_WHP_P            : float,
            ProductionDataSchema.AVG_WHT_P            : float,
            ProductionDataSchema.DP_CHOKE_SIZE        : float,
            ProductionDataSchema.BORE_OIL_VOL         : float,
            ProductionDataSchema.BORE_GAS_VOL         : float,
            ProductionDataSchema.BORE_WAT_VOL         : float,
            ProductionDataSchema.BORE_WI_VOL          : float,
            ProductionDataSchema.FLOW_KIND            : str,
        },
        parse_dates=[ProductionDataSchema.DATE],
    )
    production_data[ProductionDataSchema.MOVING_AVERAGE_OIL] = create_moving_avg_column(production_data, ProductionDataSchema.BORE_OIL_VOL)
    production_data[ProductionDataSchema.MOVING_AVERAGE_WI] = create_moving_avg_column(production_data, ProductionDataSchema.BORE_WI_VOL)
    production_data[ProductionDataSchema.WATER_CUT_DAILY] = create_water_cut_column(production_data)
    production_data[ProductionDataSchema.GAS_OIL_RATIO] = create_gor_column(production_data)
    # production_data[ProductionDataSchema]
    
    return production_data

################################################################

class ProductionDataMonthlySchema:
    DATE                  = "DATEPRD"
    MONTH                 = "MONTHPRD"
    YEAR                  = "YEARPRD"
    WELLBORE              = "WELL_BORE_CODE"
    ON_STREAM_HRS         = "ON_STREAM_HRS"
    OIL_SM3               = "OIL_SM3"
    GAS_SM3               = "GAS_SM3"
    WATER_SM3             = "WATER_SM3"
    GI_SM3                = "GI_SM3"
    WI_SM3                = "WI_SM3"
    # ,WELL_BORE_CODE,YEAR,MONTH,ON_STEAM_HRS,OIL_SM3,GAS_SM3,WATER_SM3,GI_SM3,WI_SM3


def load_well_production_data_monthly(path: str) -> pd.DataFrame:
    
    production_data_monthly = pd.read_csv(
        path,
        dtype={
            
            ProductionDataMonthlySchema.MONTH         : str,
            ProductionDataMonthlySchema.YEAR          : str,
            ProductionDataMonthlySchema.WELLBORE      : str,
            ProductionDataMonthlySchema.ON_STREAM_HRS : float,
            ProductionDataMonthlySchema.OIL_SM3       : float,
            ProductionDataMonthlySchema.GAS_SM3       : float,
            ProductionDataMonthlySchema.WATER_SM3     : float,
            ProductionDataMonthlySchema.GI_SM3        : float,
            ProductionDataMonthlySchema.WI_SM3        : float,
            
        },
        parse_dates=[ProductionDataMonthlySchema.DATE]
    )
    
    return production_data_monthly

