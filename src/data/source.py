from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date
import json

import pandas as pd
import geopandas as gpd
import numpy as np

from .loader import (
    allBLOCKS, 
    allWELLS, 
    ProductionDataSchema,
    LogDataSchema
)


@dataclass
class DataSource:
    _data: Optional[pd.DataFrame] = None
    _geodata_blocks: Optional[gpd.GeoDataFrame] = None
    _geodata_wells: Optional[gpd.GeoDataFrame] = None
    _data_log: Optional[pd.DataFrame] = None

    # main filter map
    # for blocks
    def filter_block(
        self,
        name_block: Optional[list[str]] = None,
        status_block: Optional[list[str]] = None,
        operator_block: Optional[list[str]] = None,
        total_wellMin: Optional[int] = None,
        total_wellMax: Optional[int] = None,
        sq_kmMin: Optional[float] = None,
        sq_kmMax: Optional[float] = None,
        reserveMin: Optional[float] = None,
        reserveMax: Optional[float] = None,
    ) -> DataSource:
        if name_block is None:
            name_block = self.all_name_blocks
        if status_block is None:
            status_block = self.all_status_block
        if operator_block is None:
            operator_block = self.all_operator_block
        if total_wellMin is None:
            total_wellMin = self.minimum_total_well
        if total_wellMax is None:
            total_wellMax = self.maximum_total_well
        if sq_kmMin is None:
            sq_kmMin = self.minimum_area_km
        if sq_kmMax is None:
            sq_kmMax = self.maximum_area_km
        if reserveMin is None:
            reserveMin = self.minimum_reserve
        if reserveMax is None:
            reserveMax = self.maximum_reserve

        filtered_block_data = self._geodata_blocks[
            (self._geodata_blocks[allBLOCKS.BLOCK_NAME].isin(name_block))
            & (self._geodata_blocks[allBLOCKS.STATUS_BLOCK].isin(status_block))
            & (self._geodata_blocks[allBLOCKS.OPERATOR_BLOCK].isin(operator_block))
            & (
                self._geodata_blocks[allBLOCKS.TOTAL_WELL].between(
                    total_wellMin, total_wellMax
                )
            )
            & (self._geodata_blocks[allBLOCKS.AREA_BLOCK].between(sq_kmMin, sq_kmMax))
            & (
                self._geodata_blocks[allBLOCKS.RESERVE_BLOCK].between(
                    reserveMin, reserveMax
                )
            )
        ]
        return DataSource(filtered_block_data)

    # 150823
    # for wells
    def filter_well(
        self,
        name_well: Optional[list[str]] = None,
        orientation_well: Optional[list[str]] = None,
        status_well: Optional[list[str]] = None,
        purpose_well: Optional[list[str]] = None,
        type_well: Optional[list[str]] = None,
    ) -> DataSource:
        if name_well is None:
            name_well = self.all_name_well
        if orientation_well is None:
            orientation_well = self.all_orientation_well
        if status_well is None:
            status_well = self.all_status_well
        if purpose_well is None:
            purpose_well = self.all_purpose_well
        if type_well is None:
            type_well = self.all_type_well

        filtered_well_data = self._geodata_wells[
            (self._geodata_wells[allWELLS.WELLBORE].isin(name_well))
            & (self._geodata_wells[allWELLS.ORIENTATION_WELL].isin(orientation_well))
            & (self._geodata_wells[allWELLS.STATUS_WELL].isin(status_well))
            & (self._geodata_wells[allWELLS.PURPOSE_WELL].isin(purpose_well))
            & (self._geodata_wells[allWELLS.TYPE_WELL].isin(type_well))
        ]
        return DataSource(filtered_well_data)
    
    # # 250823
    # for filter overview
    def filter_overview(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        blocks: Optional[list[str]] = None,
    ) -> DataSource:
        if from_date is None:
            from_date = self.unique_from_date
        if to_date is None:
            to_date = self.unique_to_date
        if blocks is None:
            blocks = self.unique_blocks

        filtered_data = self._data[
            (self._data[ProductionDataSchema.DATE] >= from_date)
            & (self._data[ProductionDataSchema.DATE] <= to_date)
            & (self._data[ProductionDataSchema.BLOCK].isin(blocks))
        ]

        return DataSource(filtered_data)
    
    # for generating amount of operators, numwells, oil prod mnth, gas prod mnth, depth
    def generator_amount(
        self,
        all_unique_blocks: Optional[list[str]] = None,
        type: Optional[str] = None,
    ) -> float:
        if all_unique_blocks is not None and type is not None:
            
            filter_gdf_blocks = self.gdf_blocks[self.gdf_blocks[allBLOCKS.BLOCK_NAME].isin(all_unique_blocks)]
            filter_gdf_wells = self.gdf_wells[self.gdf_wells[allWELLS.BLOCK_WELL].isin(all_unique_blocks)]
            filter_df_prod = self.df_production[self.df_production[ProductionDataSchema.BLOCK].isin(all_unique_blocks)]
            filter_df_log = self.df_log[self.df_log[LogDataSchema.BLOCK].isin(all_unique_blocks)]
            
            if type == "amount_operator":
                list_operator = filter_gdf_blocks[allBLOCKS.OPERATOR_BLOCK].tolist()
                unique_operator = sorted(set(list_operator))
                return len(unique_operator)
            
            elif type == "num_wells":
                num_total_well = filter_gdf_blocks[allBLOCKS.TOTAL_WELL].sum()
                num_monitor_well = len(sorted(set(filter_gdf_wells[allWELLS.WELLBORE].tolist())))
                return f"{num_total_well} / {num_monitor_well}"
            
            elif type == "avg_oil_prod_block":
                total_oil_prod = filter_df_prod[ProductionDataSchema.BORE_OIL_VOL].mean()
                return total_oil_prod
            
            elif type == "avg_gas_prod_block":
                total_gas_prod = filter_df_prod[ProductionDataSchema.BORE_GAS_VOL].mean()
                return total_gas_prod
            
            elif type == "avg_depth":
                total_depth = filter_df_log[LogDataSchema.Z].mean()
                
                if total_depth == 0:
                    return total_depth
                else:
                    return -(total_depth)
        
        else:
            return 0
        
    # create table for average_production_month_graph.py
    def create_table_prod_mth(
        self,
        df: pd.DataFrame = None,
        type: Optional[str] = None    
    ) -> pd.DataFrame:
        
        if type == "avg":
        
            df[ProductionDataSchema.DATE] = pd.to_datetime(df[ProductionDataSchema.DATE])
            
            # Extract year and month from the 'Date' column
            df['Year'] = df[ProductionDataSchema.DATE].dt.year
            df['Month'] = df[ProductionDataSchema.DATE].dt.month
            
            df['Year_Month'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)

            # Group the data by year and month, then calculate the average oil production for each month
            average_oil_gas_per_month = df.groupby(['Year_Month'])[[ProductionDataSchema.BORE_OIL_VOL, ProductionDataSchema.BORE_GAS_VOL]].mean()

            # Convert cubic meters to barrels (1 m^3 = 6.28981 barrels)
            average_oil_gas_per_month["BORE_OIL_VOL_barrels"] = average_oil_gas_per_month[ProductionDataSchema.BORE_OIL_VOL] * 6.28981

            # Convert cubic meters to MCF (1 m^3 = 35.3147 cubic feet, 1 MCF = 35.3147 * 1000 cubic feet)
            average_oil_gas_per_month["BORE_GAS_VOL_MCF"] = average_oil_gas_per_month[ProductionDataSchema.BORE_GAS_VOL] * (35.3147 * 1000)
            # Reset the index for the new DataFrame
            average_oil_gas_per_month = average_oil_gas_per_month.reset_index()
            
            return average_oil_gas_per_month
        
        elif type == "avg_well":
            
            df[ProductionDataSchema.DATE] = pd.to_datetime(df[ProductionDataSchema.DATE])
            
            # Extract year and month from the 'Date' column
            df['Year'] = df[ProductionDataSchema.DATE].dt.year
            df['Month'] = df[ProductionDataSchema.DATE].dt.month
            
            df['Year_Month'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)

            # Group the data by year and month, then calculate the average oil production for each month
            sum_oil_gas_per_month = df.groupby(['Year_Month','WELL_BORE_CODE'])[[ProductionDataSchema.BORE_OIL_VOL, ProductionDataSchema.BORE_GAS_VOL]].sum()
            # sum_oil_gas_per_month = df.groupby(['Year_Month', 'WELL_BORE_CODE'])[['BORE_OIL_VOL', 'BORE_GAS_VOL']].sum()

            # Convert cubic meters to barrels (1 m^3 = 6.28981 barrels)
            sum_oil_gas_per_month["BORE_OIL_VOL_barrels"] = sum_oil_gas_per_month[ProductionDataSchema.BORE_OIL_VOL] * 6.28981

            # Convert cubic meters to MCF (1 m^3 = 35.3147 cubic feet, 1 MCF = 35.3147 * 1000 cubic feet)
            sum_oil_gas_per_month["BORE_GAS_VOL_MCF"] = sum_oil_gas_per_month[ProductionDataSchema.BORE_GAS_VOL] * (35.3147 * 1000)
            # Reset the index for the new DataFrame
            sum_oil_gas_per_month = sum_oil_gas_per_month.reset_index()
            
            unique_wells = sum_oil_gas_per_month['WELL_BORE_CODE'].unique().tolist()

            # Filter the DataFrame to include only rows with well bore codes in the list
            filtered_df = sum_oil_gas_per_month[sum_oil_gas_per_month['WELL_BORE_CODE'].isin(unique_wells)]

            # Group the filtered DataFrame by 'WELL_BORE_CODE' and calculate the sum of 'BORE_OIL_VOL_barrels' and 'BORE_GAS_VOL_MCF'
            result_df = filtered_df.groupby(['WELL_BORE_CODE'])[['BORE_OIL_VOL_barrels', 'BORE_GAS_VOL_MCF']].mean().reset_index()

            result_df = result_df.sort_values(by=['BORE_OIL_VOL_barrels', 'BORE_GAS_VOL_MCF'], ascending=True)
            
            return result_df
        
        else:
            pass
        
    # for preview data
    
            

    # 040823
    # main filter well-log
    def filter_log(
        self,
        wells: Optional[str] = None,
        params: Optional[list[str]] = None,
    ) -> DataSource:
        if wells is None:
            wells = self.unique_wells_log
        if params is None:
            params = self.unique_params_log

        filtered_log_data = self._data_log[
            (self._data_log[LogDataSchema.WELLBORE] == wells)
        ][self.columns_name_xyz_log + params + self.columns_lith_log]

        return DataSource(filtered_log_data)

    # main filter productions
    def filter(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        wells: Optional[list[str]] = None,
    ) -> DataSource:
        if from_date is None:
            from_date = self.unique_from_date
        if to_date is None:
            to_date = self.unique_to_date
        if wells is None:
            wells = self.unique_wells

        filtered_data = self._data[
            (self._data[ProductionDataSchema.DATE] >= from_date)
            & (self._data[ProductionDataSchema.DATE] <= to_date)
            & (self._data[ProductionDataSchema.WELLBORE].isin(wells))
        ]

        return DataSource(filtered_data)

    # pivot table-ing
    # Date, Well - for Moving Average Chart
    def create_pivot_table_date_well_ma(self, column_name: str) -> pd.DataFrame:
        pt = self._data.pivot_table(
            values=[column_name],
            index=[ProductionDataSchema.DATE, ProductionDataSchema.WELLBORE],
            # aggfunc="sum",
            # fill_value=0,
            # dropna=False,
        )
        return pt.sort_values(ProductionDataSchema.DATE, ascending=True).reset_index()

    # Cumulative Amount based on Well - for Pie Chart
    def create_pivot_table_well(
        self, column_name: str, column_name2: Optional[str] = None
    ) -> pd.DataFrame:
        if column_name2 is not None:
            pt = self._data.pivot_table(
                values=[column_name, column_name2],
                index=[ProductionDataSchema.WELLBORE],
                aggfunc="sum",
            )

        else:
            pt = self._data.pivot_table(
                values=[column_name],
                index=[ProductionDataSchema.WELLBORE],
                aggfunc="sum",
            )

        return pt.sort_values(
            ProductionDataSchema.WELLBORE, ascending=True
        ).reset_index()

    # Cumulative Amount based on Dates - for Line Chart
    def create_pivot_table_date(
        self, column_name: str, column_name2: Optional[str] = None
    ) -> pd.DataFrame:
        if column_name2 is not None:
            pt = self._data.pivot_table(
                values=[column_name, column_name2],
                index=[ProductionDataSchema.DATE],
                aggfunc="sum",
            )

        else:
            pt = self._data.pivot_table(
                values=[column_name], index=[ProductionDataSchema.DATE], aggfunc="sum"
            )
        return pt.sort_values(ProductionDataSchema.DATE, ascending=True).reset_index()

    # Cumulative amount based on Dates, fill value with 0, for Water Cut and Gas Oil Ratio
    def create_pivot_table_date_avg(
        self, column_name: str, column_name2: Optional[str] = None
    ) -> pd.DataFrame:
        if column_name2 is not None:
            pt = self._data.pivot_table(
                values=[column_name, column_name2],
                index=[ProductionDataSchema.DATE, ProductionDataSchema.WELLBORE],
                aggfunc="mean",
                dropna=False,
            )

        else:
            pt = self._data.pivot_table(
                values=[column_name],
                index=[ProductionDataSchema.DATE, ProductionDataSchema.WELLBORE],
                aggfunc="mean",
                dropna=False,
            )
        return (
            pt.sort_values(by=[ProductionDataSchema.DATE, ProductionDataSchema.WELLBORE], ascending=True)
            # .interpolate(method="linear")
            .bfill()
            .ffill()
            .reset_index()
        )

    # for summary card
    def abbreviate_value(self, value: float) -> str:
        units = [
            "",
            "K",
            "M",
            # 'B', 'T'
        ]
        unit_index = 0
        while value >= 1000 and unit_index < len(units) - 1:
            value /= 1000
            unit_index += 1
        formatted_value = f"{value:,.2f}".rstrip("0").rstrip(".")
        return f"{formatted_value}{units[unit_index]}"

    # property for filtering data
    # property it's about something that we really need to do with all the properties of the dataframe:)
    # basic = create dataframe of pandas to be called
    
    # get production data
    @property
    def df_production(self):
        df = pd.DataFrame(self._data)
        return df
    
    # get log data
    @property
    def df_log(self):
        df = pd.DataFrame(self._data_log)
        return df
    
    # get block gpd data
    @property
    def gdf_blocks(self):
        gdf = gpd.GeoDataFrame(self._geodata_blocks)
        return gdf
    
    # get wells gpd data
    @property
    def gdf_wells(self):
        gdf = gpd.GeoDataFrame(self._geodata_wells)
        return gdf
    
    
    @property
    def to_dataframe(self):
        dataframe = pd.DataFrame(self._data)
        return dataframe

    @property
    def to_dataframe_geopandas(self):
        dataframe_geo = gpd.GeoDataFrame(self._geodata_blocks)
        return dataframe_geo

    @property  # karena kegeser kalo cuma dimasukkin 1 dataframe
    def to_dataframe_geopandas_temp(self):
        dataframe_geo = gpd.GeoDataFrame(self._data)
        return dataframe_geo

    @property
    def to_json_(self):
        json_geo = self._geodata_blocks[allBLOCKS].to_json()
        return json_geo

    # Map Utilization
    # for blocks
    @property
    def all_name_blocks(self) -> list[str]:
        return self._geodata_blocks[allBLOCKS.BLOCK_NAME].tolist()

    @property
    def all_status_block(self) -> list[str]:
        return self._geodata_blocks[allBLOCKS.STATUS_BLOCK].tolist()

    @property
    def unique_status(self) -> list[str]:
        return sorted(set(self.all_status_block))

    @property
    def all_operator_block(self) -> list[str]:
        return self._geodata_blocks[allBLOCKS.OPERATOR_BLOCK].tolist()

    @property
    def unique_operator(self) -> list[str]:
        return sorted(set(self.all_operator_block))

    @property
    def minimum_total_well(self) -> int:
        return self._geodata_blocks[allBLOCKS.TOTAL_WELL].min()

    @property
    def maximum_total_well(self) -> int:
        return self._geodata_blocks[allBLOCKS.TOTAL_WELL].max()

    @property
    def all_total_well(self) -> int:
        return self._geodata_blocks[allBLOCKS.TOTAL_WELL]

    @property
    def minimum_area_km(self) -> float:
        return self._geodata_blocks[allBLOCKS.AREA_BLOCK].min()

    @property
    def maximum_area_km(self) -> float:
        return self._geodata_blocks[allBLOCKS.AREA_BLOCK].max()

    @property
    def minimum_reserve(self) -> float:
        return self._geodata_blocks[allBLOCKS.RESERVE_BLOCK].min()

    @property
    def maximum_reserve(self) -> float:
        return self._geodata_blocks[allBLOCKS.RESERVE_BLOCK].max()
    
    # 150823
    # for wells 
    @property
    def all_name_well(self) -> list[str]:
        return self._geodata_wells[allWELLS.WELLBORE].tolist()
    
    @property
    def all_orientation_well(self) -> list[str]:
        return self._geodata_wells[allWELLS.ORIENTATION_WELL].tolist()
    
    @property
    def all_status_well(self) -> list[str]:
        return self._geodata_wells[allWELLS.STATUS_WELL].tolist()
    
    @property
    def all_purpose_well(self) -> list[str]:
        return self._geodata_wells[allWELLS.PURPOSE_WELL].tolist()
    
    @property
    def all_type_well(self) -> list[str]:
        return self._geodata_wells[allWELLS.TYPE_WELL].tolist()
    
    # geometry purposes

    @property
    def geometry_(self) -> str:
        return self._geodata_blocks[allBLOCKS.GEOMETRY_BLOCK].tolist()
    
    ## for overview analysis
    # summary card
    @property
    def all_blocks(self)-> list[str]:
        return self._data[ProductionDataSchema.BLOCK].tolist()
    
    @property    
    def unique_blocks(self) -> list[str]:
        return sorted(set(self.all_blocks))
    
    @property    
    def amount_blocks(self) -> float:
        return len(self.unique_blocks)
    
    # @property
    # def amount_operators(self) -> float:
    #     filter_operator = self.gdf_blocks[self.gdf_blocks[allBLOCKS.BLOCK_NAME].isin(self.unique_blocks)]
    #     list_operator = filter_operator[allBLOCKS.OPERATOR_BLOCK].tolist()
    #     unique_operator = sorted(set(list_operator))
    #     return len(unique_operator)
    
    
    # for production performance
    # production filter

    @property
    def all_dates(self):
        return self._data[ProductionDataSchema.DATE]

    @property
    def earliest_date(self) -> str:
        return self._data[ProductionDataSchema.DATE].min()

    @property
    def latest_date(self) -> str:
        return self._data[ProductionDataSchema.DATE].max()

    @property
    def unique_from_date(self) -> str:
        return self._data[ProductionDataSchema.DATE]

    @property
    def unique_to_date(self) -> str:
        return self._data[ProductionDataSchema.DATE]

    @property
    def all_wells(self) -> list[str]:
        return self._data[ProductionDataSchema.WELLBORE].tolist()

    @property
    def unique_wells(self) -> list[str]:
        return sorted(set(self.all_wells))
    

    # property for summary card
    @property
    def sum_oil(self) -> float:
        return self._data[ProductionDataSchema.BORE_OIL_VOL].sum()

    @property
    def sum_gas(self) -> float:
        return self._data[ProductionDataSchema.BORE_GAS_VOL].sum()

    @property
    def sum_wi(self) -> float:
        return self._data[ProductionDataSchema.BORE_WI_VOL].sum()

    @property
    def sum_on_hours(self) -> float:
        return self._data[ProductionDataSchema.ON_STREAM_HRS].sum()

    # property for oil rate line chart
    @property
    def moving_average(self):
        return self._data[ProductionDataSchema.MOVING_AVERAGE]

    # 150823
    # for gng analysis
    # property for well-log graph
    @property
    def all_wells_log(self) -> list[str]:
        return self._data_log[LogDataSchema.WELLBORE].tolist()

    @property
    def unique_wells_log(self) -> str:
        return ", ".join(sorted(set(self.all_wells_log)))

    @property
    def columns_name_xyz_log(self) -> list[str]:
        return self._data_log.iloc[:, :6].columns.tolist()

    @property
    def unique_params_log(self) -> list[str]:
        return self._data_log.iloc[:, 6:13].columns.tolist()

    @property
    def columns_lith_log(self) -> list[str]:
        return self._data_log.iloc[:, 13:].columns.tolist()
