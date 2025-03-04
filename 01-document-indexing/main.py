import os
from whoosh.index import create_in, open_dir, FileIndex
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.qparser import QueryParser

BOOKS_DIR = "books"


class IX():
    """
    IX holds all information and methods used for indexing and querying t1rough
    the documents.
    """
    ix: FileIndex

    schema: Schema = Schema(
        path=ID(stored=True),
        line=NUMERIC(stored=True),
        content=TEXT(stored=True),
    )

    query_parser = QueryParser("content", schema)

    def __init__(self, index_dir: str = "ix_cache", books_dir: str = "books") -> None:
        self.__load_ix(index_dir)
        self.__load_books(books_dir)

    def __load_ix(self, index_dir: str) -> None:
        """
        initializes a new whoosh index instance.
        """

        # If the index directory already exists, just open it and return.
        if os.path.exists(index_dir):
            self.ix = open_dir(index_dir, schema=self.schema)
            return

        # Create the index directory.
        os.mkdir(index_dir)

        # Create the index instance.
        self.ix = create_in(index_dir, self.schema)
        return

    def __load_books(self, books_dir: str) -> None:
        """
        loads all "new" books inside the books folder one by one.
        """
        # Create a searcher instance
        with self.ix.searcher() as searcher:

            # Loop through files inside the books_dir.
            for file in os.listdir(books_dir):
                path = f"{books_dir}/{file}"

                # Check if the file already loaded.
                results = searcher.find("path", path)
                if len(results) > 0:
                    continue

                # Load the file as it's new.
                print(f"Loading '{path}'...")
                self.load_book(f"{books_dir}/{file}")

    def load_book(self, path: str) -> None:
        """
        opens and reads the file content line by line, then writes and commits
        it to the index instance.
        """
        writer = self.ix.writer()

        with open(path, encoding="utf-8") as f:
            for line, content in enumerate(f.readlines()):
                writer.add_document(
                    path=path,
                    line=line,
                    content=content.removesuffix("\n"),
                )

        writer.commit(merge=True)


if __name__ == "__main__":
    print("Loading the index instance...")
    print("This may take a few minutes on first run...")

    # initialize the IX instance.
    ix = IX()

    print("Index instance loaded!")

    # Create a new searcher instance
    with ix.ix.searcher() as searcher:

        # An infinite loop for searches.
        while True:
            # example input: dog AND cat
            query_text = input("\nEnter your query (enter 'q' to exit): ")

            # Break the loop if the user wants to quit.
            if query_text == "q":
                break

            # Parse the query_text.
            query = ix.query_parser.parse(query_text)

            # Search the parsed query using the searcher instance we've made.
            results = searcher.search(query)

            print(f"\n{len(results)} results where found:")

            # Print top 10< results one by one.
            for index, res in enumerate(results):
                print(f"{index+1}. {res["path"]
                                    }:{res["line"]}\t{res["content"]}")
