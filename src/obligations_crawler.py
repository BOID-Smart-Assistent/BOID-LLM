import arxiv
from datasets import load_dataset
import pandas as pd
from collections import defaultdict
import json

def search_by_author_name(author_name, max_results=2, category_dict={}):
    """
    Search for papers by author name and return the paper titles, years and categories.

    Args:
        author_name (str): The name of the author to search for.
        max_results (int): The maximum number of results to return. Defaults to 2.
        category_dict (dict): A dictionary mapping category IDs to category names.

    Returns:
        list: A list of dictionaries, each containing the title, year and categories of a paper.
    """
    # Initialize the arxiv client
    client = arxiv.Client()
    
    search = arxiv.Search(
    # search = client.results(
        query=f"au:{author_name}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    # for result in search.results():
    for result in client.results(search):
        categories = [category_dict.get(cat_id, cat_id) for cat_id in result.categories]
        paper = {
            "title": result.title,
            "year": result.published.year,
            "keywords": categories
        }
        papers.append(paper)
    return papers

def analyze_keywords(papers):
    """
    Analyze the keywords in a list of papers and return the top 3 keywords per year and across all years.

    Args:
        papers (list of dict): A list of dictionaries, each containing the title, year and categories of a paper.

    Returns:
        dict: A dictionary containing the top 3 keywords per year and across all years.
    """
    # Initialize dictionaries
    keywords_by_year = defaultdict(lambda: defaultdict(int))
    total_keyword_counts = defaultdict(int)

    # Process each paper
    for paper in papers:
        year = paper['year']
        for keyword in paper['keywords']:
            # Count occurrences per year
            keywords_by_year[year][keyword] += 1
            # Count total occurrences across all years
            total_keyword_counts[keyword] += 1

    # Get top 3 keywords per year
    top_keywords_by_year = {
        year: sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:3]
        for year, keywords in keywords_by_year.items()
    }

    # Get top 3 keywords across all years
    top_keywords_across_years = sorted(total_keyword_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    # Return the result
    result = {
        "top_keywords_by_year": {year: dict(keywords) for year, keywords in top_keywords_by_year.items()},
        "top_keywords_across_years": dict(top_keywords_across_years)
    }

    return result
def get_obligations(authors,max_results=100):
    # Get dataset
    ds_categories = load_dataset("christopher/arxiv-taxonomy")
    ds_dataset = ds_categories['train']

    # Convert to a dictionary
    category_dict = {row['category_id']: row['category_name'].replace("(", "").replace(")", "") for row in ds_dataset}

    # Search for papers
    papers = search_by_author_name(authors, max_results,category_dict)
    number_of_papers = len(papers)
    
    # Anayze keywords
    result = analyze_keywords(papers)
    
    return result,number_of_papers

# Print result
author_name="Jan Broersen"
result,number_of_papers = get_obligations(author_name,500)
print(f"Number of extracted papers from {author_name}:", number_of_papers)
print("Top Keywords by Year:", json.dumps(result['top_keywords_by_year'], indent=4))
print("Top Keywords Across Years:", json.dumps(result['top_keywords_across_years'], indent=4))
