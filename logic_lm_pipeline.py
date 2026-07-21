import os
import janus_swi as janus
from openai import OpenAI

client = OpenAI()  # reads API key from OPENAI_API_KEY environment variable

# Load our Task 4 knowledge base
janus.consult("foodchain.pl")

def stage1_problem_formulation(question):
    """LLM translates natural language question into a Prolog query."""
    prompt = f"""You are translating natural language questions into Prolog queries.
The knowledge base uses these predicates:
- eats(X, Y): X eats Y directly
- food_chain(X, Y): X is connected to Y through some chain of eating (direct or indirect)

Translate the following question into a single valid Prolog query.
Only output the query itself, ending with a period. No explanation, no code fences.

Question: {question}
Prolog query:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    query = response.choices[0].message.content.strip()
    # strip any accidental code fences or extra text
    query = query.replace("```prolog", "").replace("```", "").strip()
    return query

def stage2_symbolic_reasoning(query):
    """Run the Prolog query against our KB using Janus. Returns (success, result, error)."""
    try:
        results = list(janus.query(query.rstrip('.')))
        success = len(results) > 0
        return success, results, None
    except Exception as e:
        return False, None, str(e)

def stage3_result_interpretation(question, query, success, results):
    """LLM translates the raw Prolog result back into a natural language answer."""
    prompt = f"""A user asked: "{question}"
We translated this into the Prolog query: {query}
The Prolog engine returned: {"TRUE (solution found)" if success else "FALSE (no solution found)"}
Raw results: {results}

Write a single, natural-language sentence answering the user's original question, based strictly on this result."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def self_refine(question, bad_query, error_message):
    """If the query failed to run, ask the LLM to fix it using the error message."""
    prompt = f"""The following Prolog query caused an error when run:
Query: {bad_query}
Error: {error_message}

The knowledge base uses these predicates:
- eats(X, Y): X eats Y directly
- food_chain(X, Y): X is connected to Y through some chain of eating

Original question: "{question}"

Provide a corrected, valid Prolog query. Only output the query itself, ending with a period."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    query = response.choices[0].message.content.strip()
    query = query.replace("```prolog", "").replace("```", "").strip()
    return query

def logic_lm_pipeline(question):
    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")

    # Stage 1
    query = stage1_problem_formulation(question)
    print(f"[Stage 1 - Problem Formulation] Generated query: {query}")

    # Stage 2
    success, results, error = stage2_symbolic_reasoning(query)

    # Self-refinement if there was an error
    if error:
        print(f"[Self-Refinement] Solver error: {error}")
        query = self_refine(question, query, error)
        print(f"[Self-Refinement] Corrected query: {query}")
        success, results, error = stage2_symbolic_reasoning(query)

    print(f"[Stage 2 - Symbolic Reasoning] Success: {success}, Results: {results}")

    # Stage 3
    answer = stage3_result_interpretation(question, query, success, results)
    print(f"[Stage 3 - Result Interpretation] Answer: {answer}")

    return success, answer


if __name__ == "__main__":
    test_questions = [
        "Does a fox eat a rabbit?",
        "Does a fox eat grass?",
        "Is there a food chain connecting a wolf to grass?",
        "Is there a food chain connecting an eagle to grass?",
        "Does a bear eat a snake?",
        "Is there a food chain connecting a bear to grass?",
    ]

    for q in test_questions:
        logic_lm_pipeline(q)
