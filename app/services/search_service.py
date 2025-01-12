from interfaces import RepositoryInterface

from models_dto import ItemSearchParamsDTO


class SearchService():
    def __init__(
        self,
        repository: RepositoryInterface
    ):
        self.repository = repository
    
    
    async def search_by_tags(self, search_params: ItemSearchParamsDTO) -> list[str]:
        query = self.repository._build_tag_search_query(search_params)
        item_hashes = await self.repository.make_tag_search(query)
        return item_hashes