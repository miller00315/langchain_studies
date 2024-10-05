from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()


def get_profile_url_tavily(name: str) -> str:
    """Searches for Linkedin Profile page."""
    search = TavilySearchResults()

    res = search.run(f"{name}")

    return res[0]["url"]
