from flask_restx import Namespace, Resource, fields

from core.crud.stack_crud import StackCRUD
from core.models import Stack
from marshmallow import Schema, post_load
from marshmallow.fields import UUID, List, String

api = Namespace("stack", description="stack CRUD operations")
stack_crud = StackCRUD()

stack_doc = api.model(
    "Stack",
    {
        "id": fields.String(
            required=False, readonly=True, description="The stack unique identifier"
        ),
        "content": fields.List(
            fields.String(required=True, description="The stack content")
        ),
    },
)
operand_doc = api.model(
    "Operand",
    {
        "operand": fields.String(
            required=False, description="Operand to push in the stack"
        ),
    },
)


class StackSchema(Schema):
    id = UUID(required=False)
    content = List(String(), required=False)
    operand = String(required=False)

    @post_load
    def make_stack(self, data, **kwargs):
        return Stack(**data)


@api.route("/")
class StackListResource(Resource):
    @api.doc("list_stack")
    @api.marshal_list_with(stack_doc)
    def get(self):
        """List all stack"""
        stack_schema = StackSchema(many=True)
        return stack_schema.dump(stack_crud.stacks)

    @api.doc("create_stack")
    @api.expect(stack_doc)
    @api.marshal_with(stack_doc, code=201)
    def post(self):
        """Create a new stack"""
        stack_schema = StackSchema()
        stack = stack_schema.load(api.payload)
        print(stack)
        return stack_schema.dump(stack_crud.create(stack=stack)), 201


@api.route("/<stack_id>")
@api.response(404, "Stack not found")
class StackResource(Resource):
    @api.doc("get_stack")
    @api.marshal_with(stack_doc)
    def get(self, stack_id: str):
        """Fetch a given stack"""
        stack_schema = StackSchema()
        stack = stack_crud.get(stack_id)
        if stack is None:
            api.abort(404)
        return stack_schema.dump(stack)

    @api.doc("delete_stack")
    @api.response(204, "Stack deleted")
    def delete(self, stack_id: str):
        """Delete a stack given its identifier"""
        stack_schema = StackSchema()
        return stack_schema.dump(stack_crud.delete(stack_id)), 204

    @api.expect(operand_doc)
    @api.marshal_with(stack_doc)
    @api.response(202, "Stack updated")
    def post(self, stack_id: str):
        """Update a stack given its identifier"""
        stack_schema = StackSchema()
        stack = None
        try:
            stack = stack_crud.update(stack_id, stack_schema.load(api.payload))
        except ValueError as ve:
            api.abort(422, str(ve))

        if stack is None:
            api.abort(404)

        return (
            stack_schema.dump(stack),
            202,
        )
