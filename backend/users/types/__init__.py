from ariadne import load_schema_from_path
import os

user_type_schema = load_schema_from_path(
    os.path.join(os.getcwd(), "backend/users/types"))
