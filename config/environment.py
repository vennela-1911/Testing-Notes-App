import yaml


class Config:

    def __init__(self):

        with open(
            "config/config.yaml",
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(file)

        self.application = type(
            "Application",
            (),
            data["application"]
        )

        self.credentials = type(
            "Credentials",
            (),
            data["credentials"]
        )

        self.browser = type(
            "Browser",
            (),
            data["browser"]
        )

        self.timeouts = type(
            "Timeouts",
            (),
            data["timeouts"]
        )


config = Config()