from scraper import GlobalReadMe


def main():
    GlobalReadMe(
        {
            "lk_dmc": [
                "lk_dmc_situation_reports",
            ]
        }
    ).build()


if __name__ == "__main__":
    main()
