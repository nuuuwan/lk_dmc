from dataclasses import dataclass

from utils import Log

from dmc.AbstractDMCPDFDoc import AbstractDMCPDFDoc

log = Log("SituationReport")


@dataclass
class SituationReport(AbstractDMCPDFDoc):

    @classmethod
    def get_doc_class_label(cls) -> str:
        return "lk_dmc_situation_reports"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return "Situation Report including information about Heavy Rain, Wind, Tree Falling, Lighting etc."  # noqa: E501

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "🌦️"

    @classmethod
    def get_base_params(cls):
        return dict(
            option="com_dmcreports",
            view="reports",
            Itemid=273,
            report_type_id=1,
            lang="en",
        )
