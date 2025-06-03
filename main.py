from src.vector_db import get_vector_db


def main():
    print("Hello from soreq!")
    vector_db = get_vector_db()
    print(f"Vector database initialized: {vector_db}")


if __name__ == "__main__":
    main()
