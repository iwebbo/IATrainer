from duckduckgo_search import DDGS

query = "Tutoriel Python"
with DDGS() as ddgs:
    videos = list(ddgs.videos(query, max_results=3))

print(videos[0])  # Vérifier la structure réelle des résultats