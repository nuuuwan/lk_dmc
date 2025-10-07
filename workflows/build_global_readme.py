from scraper import GlobalReadMe


def main():
    GlobalReadMe(
        {
            "lk_dmc": [
                "lk_dmc_situation_reports",
                "lk_dmc_weather_forecasts",
                "lk_dmc_river_water_level_and_flood_warnings",
                "lk_dmc_landslide_warnings",
            ]
        }
    ).build()


if __name__ == "__main__":
    main()
