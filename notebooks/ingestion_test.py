from RAG.ingestion.web_loader import GithubDocLoader

loader = GithubDocLoader()

doc= loader.load("https://docs.github.com/en/rest/issues/issues")

print(doc["title"])
print(doc["content"][:1000])