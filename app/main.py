import logging
import traceback
from typing import Union, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.services.pinterest_service import PinterestService
except ImportError:
    # for Deta.sh hadling
    from services.pinterest_service import PinterestService

logger = logging.getLogger(__name__)


class App:
    app = FastAPI()

    def __init__(self):
        origins = [
            'http://localhost:62535',
            'http://localhost:3000',
            '*',
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )

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
    @app.get('/get/categories')
    def get_query_category():
        return [
            category_name for category_name in PinterestService.query_category_dict.keys()]

    @staticmethod
    @app.get('/get/categories/{category_name}')
    def get_query_group(category_name: str):
        return [
            group_name for group_name in PinterestService.query_category_dict[category_name].keys()]

    @staticmethod
    @app.get('/get/categories/{category_name}/group/{group_name}')
    def get_query_name(category_name: str, group_name: str):
        return PinterestService.query_category_dict[category_name][group_name]

    @staticmethod
    @app.get('/search/board/{query}')
    def get_search_board_id(query: str):
        try:
            _pinterest_service = PinterestService()
            _pinterest_service.search(query=query, num_pins=100, scope='boards')
            return _pinterest_service.board_id_list
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            raise e

    @staticmethod
    @app.get('/get/board/{board_id}')
    def get_images_using_board_id(board_id: str):
        try:
            _pinterest_service = PinterestService()
            _pinterest_service.get_board_feed_orig_images(board_id=board_id)
            return _pinterest_service.image_info_list
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            raise e


app = App().get_application()
