from serpapi import GoogleSearch
from os import getenv

params = {
    "engine": "google_scholar_author",
    "author_id": "8mIJ8mcAAAAJ",
    "api_key": getenv("SERP_API_KEY"),
    "num": 100
}

search = GoogleSearch(params)
data = search.get_dict()
results = data["articles"]
cited_by = data["cited_by"]

title = """---
hide:
  - toc
---

# Highly Cited Researches\n
"""

markdown_list = [title]

columns = set()
for item in cited_by["table"]:
    for metric, values in item.items():
        columns.update(values.keys())

columns = sorted(list(columns))

header_columns = [col.replace('_', ' ').title() for col in columns]
header = "| Metric | " + " | ".join(header_columns) + " |"
markdown_list.append(header)

header_separator = "| ------ |" + " | ".join([" -------- " for _ in columns]) + "|"
markdown_list.append(header_separator)

for item in cited_by["table"]:
    for metric, values in item.items():
        row = [f"{values[col]}" if col in values else "N/A" for col in columns]
        markdown_list.append(f"| {metric.replace('_', ' ').title()} | " + " | ".join(row) + " |")

markdown_list.append("\n")

for item in results:
    try:
        title = item["title"]
        link = item["link"]
        authors = item["authors"]
        publication = item['publication']
        cited_by = item["cited_by"]["value"]
        year = item["year"]
    except KeyError:
        continue

    markdown_list.append(
        f"**[{title}]({link})**, \n"
        f"{authors}, \n"
        f"{publication}. \n"
        f"***Cited by**: {cited_by} times*\n"
    )

markdown_output = "\n".join(markdown_list)
print(markdown_output)

with open("docs/achievements/highly_cited.md", "w") as f:
    f.write(markdown_output)
