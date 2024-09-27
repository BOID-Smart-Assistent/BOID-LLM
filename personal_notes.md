# Progress update: 26 August 2024
1. RAG has been develop in very basic feature which can perform information retrieval to enhance LLM context (challenge: sometimes the embedding results are not decodable like \u25a1)
2. Run LLM model locally and access via API
3. Integrate LLM with RAG to enrich context (Challenge: find a good prompt structure to maximize the result)
4. Prepare docker based setup for the code (challenge: still face an error, will be fixed soon)
5. Currently developing QnA based LLM and Experiment in prompt engineering

# Action Item 
1. Build the LLM prompt QnA Style
2. Experiment in Prompt engineering
3. Design how to assess model and code performance
4. Experiment with various LLM model both for chat and embedding
5. Fix the docker access


# Progress update: 2 September 2024
1. Develop auto QnA LLM (user assisted chatbot interaction)
2. Add context from RAG to the auto QnA LLM (need to develop more data extraction mode such as table based data)


# Action Item 
1. Build the LLM prompt QnA Style (done) and optimizing BOID logic generation (check decision three to guard and make the schedule data easier for LLM)
2. Experiment in Prompt engineering (in progress)
3. Develop script that automatically run multiple model and extracts its conversation
4. Design how to assess model and code performance, then develop script to measure that
5. Experiment with various LLM model both for chat and embedding
5. Fix the docker access

-simplify slot sma misal A dan bedain 1 dan 2
-untuk schedule bikin simpel aja
-tidak perlu  banyak fungsi
-bikin 1 llm aja gak usah 2
-cara testnya, bikin 1 case yang oke dan test
-perlu refine yang example juga
-ikutin cara dari webnya openai, ada cara untuk applynya misal fewshot dll
