from typing import Union, List

from fastapi import FastAPI

from app.services.pinterest_service import PinterestService


class App:
    app = FastAPI()

    def get_application(self):
        return self.app

    @staticmethod
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @staticmethod
    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}

    @staticmethod
    @app.get('/get/category')
    def get_query_category():
        return [
            category_name for category_name in PinterestService.query_category_dict.keys()]

    @staticmethod
    @app.get('/get/{category_name}/group')
    def get_query_group(category: str):
        return [
            group_name for group_name in PinterestService.query_category_dict[category].keys()]

    @staticmethod
    @app.get('/get/{category_name}/{group_name}/name')
    def get_query_name(category: str, group: str):
        return PinterestService.query_category_dict[category][group]

    @staticmethod
    @app.get('/search/board/{query_name}')
    def get_search_board_id(query: str):
        _pinterest_service = PinterestService()
        _pinterest_service.search(query=query, num_pins=100, scope='boards')
        return _pinterest_service.board_id_list

    @staticmethod
    @app.get('/get/board/{board_id}')
    def get_images_using_board_id(board_id: str):
        _pinterest_service = PinterestService()
        _pinterest_service.get_board_feed_orig_images(
            board_id=board_id, page_size=100)
        return _pinterest_service.image_info_list


app = App().get_application()
