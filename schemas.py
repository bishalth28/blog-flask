from marshmallow import Schema, fields
class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.Str(required = True)
    password = fields.Str(required = True, load_only=True)
    
class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    author_id = fields.Int(dump_only=True)
