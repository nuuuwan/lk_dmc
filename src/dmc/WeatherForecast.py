from dataclasses import dataclass

from utils import Log

from dmc.AbstractDMCPDFDoc import AbstractDMCPDFDoc

log = Log("WeatherForecast")


@dataclass
class WeatherForecast(AbstractDMCPDFDoc):

    @classmethod
    def get_doc_class_label(cls) -> str:
        return "lk_dmc_weather_forecasts"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return (
            "Weather Forecasts for various places in Sri Lanka."  # noqa: E501
        )

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "☔️"

    @classmethod
    def get_base_params(cls):
        # E.g. https://www.dmc.gov.lk/index.php?option=com_dmcreports&view=reports&Itemid=274&report_type_id=2&lang=en # noqa: E501
        return dict(
            option="com_dmcreports",
            view="reports",
            Itemid=274,
            report_type_id=2,
            lang="si-ta-en",
        )
