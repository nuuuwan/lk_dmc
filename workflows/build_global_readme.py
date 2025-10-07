from scraper import GlobalReadMe


def main():
    GlobalReadMe(
        {
            "lk_dmc": [
                "lk_dmc_situation_reports",
                "lk_dmc_weather_forecasts",
            ]
        }
    ).build()


if __name__ == "__main__":
    main()
