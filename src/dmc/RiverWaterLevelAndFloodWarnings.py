from dataclasses import dataclass

from utils import Log

from dmc.AbstractDMCPDFDoc import AbstractDMCPDFDoc

log = Log("RiverWaterLevelAndFloodWarnings")


@dataclass
class RiverWaterLevelAndFloodWarnings(AbstractDMCPDFDoc):

    @classmethod
    def get_doc_class_label(cls) -> str:
        return "lk_dmc_river_water_level_and_flood_warnings"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return "River Water Level and Flood Warnings for various places in Sri Lanka."  # noqa: E501

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "💧"

    @classmethod
    def get_base_params(cls):
        return dict(
            option="com_dmcreports",
            view="reports",
            Itemid=277,
            report_type_id=6,
            lang="en",
        )
