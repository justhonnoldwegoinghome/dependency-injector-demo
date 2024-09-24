from dependency_injector import containers, providers


class Database:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __str__(self):
        return f"Database(host={self.host}, port={self.port}, username={self.username})"


class ApiClient:
    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key
        self.timeout = timeout

    def __str__(self):
        return f"ApiClient(api_key={self.api_key}, timeout={self.timeout})"


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])

    database = providers.Singleton(
        Database,
        host=config.db.host,
        port=config.db.port,
        username=config.db.username,
        password=config.db.password,
    )

    api_client = providers.Factory(
        ApiClient,
        api_key=config.api.key,
        timeout=config.api.timeout.as_int(),
    )


if __name__ == "__main__":

    container = Container()

    # Load some config values programmatically
    container.config.from_dict({"misc": {"password": "super_secret"}})

    print(container.config())
    print(container.database())
