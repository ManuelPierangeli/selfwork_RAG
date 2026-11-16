from scanner_cv.ingest import get_collection


def search_context(user_question, n_results=2):
    collection = get_collection()

    results = collection.query(
        query_texts=[user_question],
        n_results=n_results
    )

    source = results["metadatas"][0][0]["source"]
    document = results["documents"][0][0]

    context = f"CONTESTO: nome file {source} ecco il paragrafo piu' significativo: {document}"
    return context


if __name__ == "__main__":
    user_question = "mi serve qualcuno per promuovere il mio prodotto"
    print(search_context(user_question))