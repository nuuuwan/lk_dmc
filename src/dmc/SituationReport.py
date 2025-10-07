import sys
from dataclasses import dataclass
from urllib.parse import urlencode

from scraper import AbstractPDFDoc, GlobalReadMe
from utils import WWW, Log

log = Log("SituationReport")


@dataclass
class SituationReport(AbstractPDFDoc):
    time_str: str

    URL_BASE = "https://www.dmc.gov.lk"

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
    def gen_docs_from_page(cls, url_page):
        www = WWW(url_page)
        soup = www.soup
        table = soup.find("table", class_="mtable")
        for tr in table.find_all("tr"):
            if "mhead" in tr.get("class"):
                continue
            tds = tr.find_all("td")
            assert len(tds) == 4, f"Expected 3 tds, got {len(tds)}"
            description, date_str, time_str = (
                tds[0].text,
                tds[1].text,
                tds[2].text,
            )
            assert (
                "Situation Report" in description
            ), f"Expected Situation Report, got {description}"
            assert len(date_str) == 10, f"Expected date, got {date_str}"
            assert len(time_str) == 5, f"Expected time, got {time_str}"

            a = tds[3].find("a")
            if not a:
                continue
            href = a.get("href")
            assert href.endswith(".pdf"), f"Expected pdf, got {href}"

            url_pdf = f"{cls.URL_BASE}{href}"
            num = time_str.replace(":", "-")
            lang = "en"
            yield cls(
                num=num,
                date_str=date_str,
                description=description,
                url_metadata=url_page,
                lang=lang,
                url_pdf=url_pdf,
                time_str=time_str,
            )

    @classmethod
    def gen_docs(cls):
        base_url = "https://www.dmc.gov.lk/index.php"
        base_params = dict(
            option="com_dmcreports",
            view="reports",
            Itemid=273,
            report_type_id=1,
            lang="en",
        )
        limitstart = 0
        while True:
            params = base_params | dict(limitstart=limitstart)
            url_page = f"{base_url}?{urlencode(params)}"
            n_docs_for_page = 0
            for doc in cls.gen_docs_from_page(url_page):
                yield doc
                n_docs_for_page += 1

            log.debug(f"{url_page=} -> {n_docs_for_page} docs")
            if n_docs_for_page == 0:
                break

            limitstart += 10

    @classmethod
    def run_pipeline(cls, max_dt=None):
        max_dt = (
            max_dt
            or (float(sys.argv[2]) if len(sys.argv) > 2 else None)
            or cls.MAX_DT
        )
        log.debug(f"{max_dt=}s")

        cls.cleanup_all()
        cls.scrape_all_metadata(max_dt)
        cls.write_all()
        cls.scrape_all_extended_data(max_dt)
        cls.build_summary()
        cls.build_doc_class_readme()
        cls.build_and_upload_to_hugging_face()

        if not cls.is_multi_doc():
            GlobalReadMe(
                {cls.get_repo_name(): [cls.get_doc_class_label()]}
            ).build()
