import os
import json

import pytest

import run



@pytest.fixture(scope="session")
def app():
    return run.connex_app


@pytest.fixture(scope='module')
def client():
    with app().app.test_client() as c:
        yield c


# @pytest.fixture(scope="session", autouse=True)
# def clean_up():
#     yield
#     default_pets = {
#         "1": {"name": "ginger", "breed": "bengal", "price": 100},
#         "2": {"name": "sam", "breed": "husky", "price": 10},
#         "3": {"name": "guido", "breed": "python", "price": 518},
#     }

#     abs_file_path = os.path.abspath(os.path.dirname(__file__))
#     json_path = os.path.join(abs_file_path, "../", "test_api", "core", "pets.json")
#     with open(json_path, "w") as pet_store:
#         json.dump(default_pets, pet_store, indent=4)
