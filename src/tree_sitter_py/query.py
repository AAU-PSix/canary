from tree_sitter.binding import Query as _Query

class Query:
    def __init__(self, query: _Query) -> None:
        self._query = query
