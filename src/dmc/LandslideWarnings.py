from dataclasses import dataclass

from utils import Log

from dmc.AbstractDMCPDFDoc import AbstractDMCPDFDoc

log = Log("LandslideWarnings")


@dataclass
class LandslideWarnings(AbstractDMCPDFDoc):

    @classmethod
    def get_doc_class_label(cls) -> str:
        return "lk_dmc_landslide_warnings"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return " ".join(
            [
                "Landslide Warnings including early warnings,",
                "locations of potential risk,",
                "areas and places which need special attention,",
                "and automated landslide early warning map.",
            ]
        )

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "🗻"

    @classmethod
    def get_base_params(cls):
        # https://www.dmc.gov.lk/index.php?option=com_dmcreports&view=reports&Itemid=276&report_type_id=5&lang=en # noqa: E501
        return dict(
            option="com_dmcreports",
            view="reports",
            Itemid=276,
            report_type_id=5,
            lang="en",
        )
