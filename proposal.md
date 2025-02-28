# Project Proposal: Question-Answering Slackbot for DSAN Slack Channel

## Overview: 
Effective communication and knowledge sharing are essential in the DSAN Slack workspace, where students, faculty, and TAs frequently exchange information. However, repetitive questions about coursework, deadlines, coding issues, and general program guidelines often arise, leading to inefficiencies in information retrieval and response time.
To address this, we will develop a Question-Answering Slackbot that provides intelligent, context-aware responses by leveraging Retrieval-Augmented Generation (RAG) techniques. This Slackbot will enhance productivity by efficiently retrieving relevant information from Slack conversation history, ensuring users receive accurate and timely answers without waiting for human intervention.
By implementing advanced RAG-based retrieval techniques, we aim to improve the bot’s ability to understand and respond to user queries with high precision. Our solution will be seamlessly integrated into a Slack channel, enabling interactive and automated support for the DSAN community.

### Through this project, we will achieve:
1. Preprocessing and storing Slack messages in a vector database.
2. Implementing multiple RAG techniques for enhanced retrieval.
3. Deploying a fully functional Slackbot that supports multi-turn conversations.
4. Optionally generating synthetic Slack data to improve performance in edge cases.

## Technical Implementation:

### A. Data Processing & Storage

1. Load and preprocess Slack JSON data 
Our primary data source will be anonymized Slack conversation history, which will serve as the foundation for training and fine-tuning our retrieval model. However, real-world Slack data may have limitations, such as incomplete coverage of potential queries or unbalanced representation of topics.
To address these challenges, we will generate synthetic Slack conversations in Slack’s JSON format, which includes key attributes such as user messages, timestamps, and thread structures. This synthetic data will help improve the bot’s robustness by simulating diverse user interactions, edge cases, and rarely asked questions. By incorporating both real and synthetic data, we aim to enhance the model’s ability to generalize across a wide range of queries and provide more accurate responses.

2. Store processed data in a vector database (e.g., FAISS) for efficient retrieval.

3. Example data: 
- https://huggingface.co/datasets/m-a-p/CodeCriticBench
- Load the dataset and question (questions), and answer (answers); use public and private to vlildate the answer 
- Enhance the model performance on processing coding-based questions 
- https://huggingface.co/datasets/math-ai/StackMathQA
- Load the dataset and Q (questions) and A (answers). 
- Enhance the model performance on Math Questions
- https://huggingface.co/datasets/PrimeIntellect/stackexchange-question-answering
- Load the dataset and extract prompt (questions) and gold_standard_solution (answers).
- Enhance the model performance on Q&A

### B. Retrieval-Augmented Generation (RAG) Pipeline
The Slackbot will implement three advanced RAG techniques from the following list:
1. Query Rewriting:
- Rewriting user queries to improve retrieval accuracy.
2. Query Decomposition:
- Breaks complex queries into smaller, more manageable sub-queries.
3. Graph RAG:
- Builds a knowledge graph from Slack conversations, connecting related topics and FAQs.
- Uses graph-based retrieval to enhance relevance beyond keyword-based search.
4. Ensemble Retriever:
- Combines multiple retrieval methods (e.g., dense vector search + BM25 keyword search).
- Merges results using ranking or fusion techniques.
- Hybrid Search (Dense + Sparse Retrieval):
- Uses a combination of vector embeddings (semantic search) and BM25 retrieval for improved accuracy.

### C. Slackbot Integration
- Implement the Slackbot using Slack’s API and event handling.
- Enable real-time query handling by fetching and processing messages.
- Ensure multi-turn conversation support by tracking context within a thread.
- Allow users to provide feedback (e.g., thumbs up/down) to refine response quality.
