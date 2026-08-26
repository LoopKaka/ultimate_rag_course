from rag_final.src.rag import (generate_llm_answer)

def main():
    print("Welcome to LoopKaka's RAG Course \n\n")

    while True:
        question = input("You: ")

        if question.lower() == 'exit':
            break

        answer = generate_llm_answer(question)
        print("Answer: ", answer , "\n\n")

if __name__ == "__main__":
    main()