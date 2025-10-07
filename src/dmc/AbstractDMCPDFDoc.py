import re
import sys
from dataclasses import dataclass
from urllib.parse import urlencode

from scraper import AbstractPDFDoc, GlobalReadMe
from utils import WWW, Log, TimeFormat

log = Log("AbstractDMCPDFDoc")


@dataclass
class AbstractDMCPDFDoc(AbstractPDFDoc):
    time_str: str
    ut: int

    URL_BASE = "https://www.dmc.gov.lk"

    @classmethod
    def parse_url_pdf(cls, td):
        a = td.find("a")
        if not a:
            return None
        href = a.get("href")
        if (
            href.endswith("jpg")
            or href.endswith("jpeg")
            or href.endswith("png")
        ):
            log.warning(f"Skipping image: {href}")
            return None
        assert href.endswith(".pdf"), f"Expected pdf, got {href}"
        url_pdf = f"{cls.URL_BASE}{href}"
        return url_pdf

    @classmethod
    def parse_tr(cls, url_page, tr):
        if "mhead" in tr.get("class"):
            return None
        tds = tr.find_all("td")
        assert len(tds) == 4, f"Expected 3 tds, got {len(tds)}"
        description, date_str, time_str = [td.text.strip() for td in tds[:3]]
        description = re.sub(r"\s+", " ", description)
        assert len(date_str) == 10, f"Expected date, got {date_str}"
        assert len(time_str) == 5, f"Expected time, got {time_str}"

        url_pdf = cls.parse_url_pdf(tds[3])
        if not url_pdf:
            return None

        description_cleaned = (
            re.sub(r"[^a-zA-Z0-9\s]", "", description)
            .strip()
            .replace(" ", "-")
            .lower()
        )
        num = time_str.replace(":", "-") + "-" + description_cleaned
        lang = "en"
        ut = TimeFormat("%Y-%m-%d %H:%M").parse(f"{date_str} {time_str}").ut
        return cls(
            num=num,
            date_str=date_str,
            description=description,
            url_metadata=url_page,
            lang=lang,
            url_pdf=url_pdf,
            time_str=time_str,
            ut=ut,
        )

    @classmethod
    def gen_docs_from_page(cls, url_page):
        www = WWW(url_page)
        soup = www.soup
        table = soup.find("table", class_="mtable")
        for tr in table.find_all("tr"):
            try:
                doc = cls.parse_tr(url_page, tr)
                if doc:
                    yield doc
            except Exception as e:
                log.error(f"[{url_page}] Error {e} parsin: {tr}")

    @classmethod
    def get_base_params(cls):
        raise NotImplementedError

    @classmethod
    def gen_docs(cls):
        base_url = "https://www.dmc.gov.lk/index.php"
        base_params = cls.get_base_params()
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
