from fastapi import Query


class PaginationQuery:
    def __init__(self, page: int = 0, limit: int = Query(50, le=100)) -> None:
        self.page = page
        self.limit = limit
