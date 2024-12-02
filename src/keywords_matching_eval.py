from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import llm_chat_system

def filter_similar_keywords(true_keywords, selected_keywords, threshold=0.7, model_name='all-MiniLM-L6-v2'):
    """
    Filters selected keywords based on semantic similarity with true keywords.
    
    Args:
        true_keywords (list): List of correct keywords.
        selected_keywords (list): List of LLM-selected keywords.
        threshold (float): Similarity threshold for filtering.
        model_name (str): Pre-trained embedding model to use (default is all-MiniLM-L6-v2).
    
    Returns:
        list: Keywords from `true_keywords` similar to those in `selected_keywords`.
    """
    print('filter_similar_keywords is running...')
    # Load a pre-trained embedding model
    model = SentenceTransformer(model_name)

    # Generate embeddings for both sets of keywords
    true_keywords = [keyword.strip() for keyword in true_keywords]
    selected_keywords = [keyword.strip() for keyword in selected_keywords]
    true_embeddings = model.encode(true_keywords)
    selected_embeddings = model.encode(selected_keywords)

    # Find similar keywords
    similar_keywords = []
    for i, selected in enumerate(selected_keywords):
        for j, true in enumerate(true_keywords):
            similarity = cosine_similarity([selected_embeddings[i]], [true_embeddings[j]])[0][0]
            if similarity >= threshold:
                similar_keywords.append(true)
                # break  # Add only one matching keyword from true_keywords

    return similar_keywords
def evaluate_keywords(true_keywords, selected_keywords):
    print('evaluate_keywords is running...')
    # Convert lists to sets for easier comparison
    true_keywords = [keyword.strip() for keyword in true_keywords]
    selected_keywords = [keyword.strip() for keyword in selected_keywords]
    true_set = set(true_keywords)
    print('True set:',true_set)
    selected_set = set(selected_keywords)
    print('Selected set:',selected_set)

    # Calculate True Positives (TP), False Positives (FP), and False Negatives (FN)
    tp = len(true_set & selected_set)  # Intersection
    print('TP:',true_set & selected_set)
    fp = len(selected_set - true_set) # Selected but not true
    print('FP:',selected_set - true_set)
    fn = len(true_set - selected_set) # True but not selected
    print('FN:',true_set - selected_set)
    tn = len(set(true_keywords + selected_keywords) - true_set - selected_set) # True or selected but not both
    print('TN:',set(true_keywords + selected_keywords) - true_set - selected_set)
    
    # Calculate Precision, Recall, F1 Score, and Accuracy
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0

    # Return results as a dictionary
    return {
        "True Positives": tp,
        "False Positives": fp,
        "False Negatives": fn,
        "True Negatives": tn,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1_score,
        "Accuracy": accuracy
    }

def evaluate_with_vectors(true_keywords, selected_keywords, model_name='all-MiniLM-L6-v2'):
    print('evaluate_with_vectors is running...')
    # Load a pre-trained embedding model
    model = SentenceTransformer(model_name)

    # Compute embeddings for true and selected keywords
    true_embeddings = model.encode(true_keywords)
    selected_embeddings = model.encode(selected_keywords)

    # Compute cosine similarity between all pairs of true and selected keywords
    similarity_matrix = cosine_similarity(true_embeddings, selected_embeddings)

    # Measure maximum similarity for each true keyword
    max_similarities = similarity_matrix.max(axis=1)  # Max similarity for each true keyword
    avg_similarity = np.mean(max_similarities)  # Average similarity across all true keywords

    # Optional: Count how many selected keywords are above a similarity threshold
    threshold = 0.7
    correct_matches = sum(sim > threshold for sim in max_similarities)

    # Return metrics
    return {
        "Average Similarity": avg_similarity,
        "Correct Matches": correct_matches,
        "Total True Keywords": len(true_keywords),
        "Threshold": threshold
    }

def load_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

schedule=load_config('./data/context/schedule.json')
unique_titles = set()  # Using a set for uniqueness
for day, slots in schedule.items():
    for timeslot, details in slots.items():
        unique_titles.add(details["title"])  # Add title to the set
# print('Title list:',unique_titles)
# Selected test keyword
test_keyword='healthcare'

# LLM generated keywords
desires=llm_chat_system.getDesire(user_input=test_keyword)
desire_data=desires.replace('\n','').split(',')

# LLM generated keywords
selected_keywords = desire_data
# Relevant keywords from schedule that similar with generated keyword

similar_topics = filter_similar_keywords(list(unique_titles), [test_keyword], threshold=0.2)
true_keywords = list(similar_topics)



# Precision and recall
results_keywords = evaluate_keywords(true_keywords, selected_keywords)

# Similarity
results_vector = evaluate_with_vectors(true_keywords, selected_keywords)

print(f'\nTrue topics based on {test_keyword} as a keyword: {true_keywords}')
print(f'Generated topics based on {test_keyword} as a keyword: {selected_keywords}')
print("\nEvaluation based on keywords accuracy:")
for metric, value in results_keywords.items():
    print(f"{metric}: {value}")
print("\nEvaluation based on vector representation (semantic):")
for metric, value in results_vector.items():
    print(f"{metric}: {value}")