from server.util.EnvironmentReader import EnvironmentReader


class TwitterAuth:
    apiKey = EnvironmentReader.get("API_KEY")
    apiKeySecret = EnvironmentReader.get("API_KEY_SECRET")
    bearerToken = EnvironmentReader.get("BEARER_TOKEN")
    accessToken = EnvironmentReader.get("ACCESS_TOKEN")
    accessTokenSecret = EnvironmentReader.get("ACCESS_TOKEN_SECRET")

