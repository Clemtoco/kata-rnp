from flask_restx import Api
from .stack_ns import api as stack_ns_api

api = Api(
    # app,
    version="1.0",
    title="RPN Kata API Doc",
    description="A RPN API documentation for CA-CIB kata",
    doc="/doc/",
    prefix="/rnp",
)
api.add_namespace(stack_ns_api)
