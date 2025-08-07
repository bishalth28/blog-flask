from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.post import PostModel
from schemas import PostSchema

blp = Blueprint("Posts", "posts", description="Operations on blog posts")

@blp.route("/posts")
class PostList(MethodView):
    @blp.response(200, PostSchema(many=True))
    def get(self):
        posts = PostModel.query.all()
        return posts

    @jwt_required()
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def post(self, post_data):
        user_id = get_jwt_identity()
        post = PostModel(
            title=post_data["title"],
            description=post_data["description"],
            author_id=int(user_id)
        )
        db.session.add(post)
        db.session.commit()
        return post

@blp.route("/posts/<int:post_id>")
class Post(MethodView):
    @blp.response(200, PostSchema)
    def get(self, post_id):
        post = PostModel.query.get_or_404(post_id)
        return post

    @jwt_required()
    @blp.arguments(PostSchema)
    def put(self, post_data, post_id):
        user_id = get_jwt_identity()
        post = PostModel.query.get_or_404(post_id)
        if post.author_id != int(user_id):
            abort(403, message="Not authorized to edit this post")

        post.title = post_data["title"]
        post.description = post_data["description"]
        db.session.commit()
        return post

    @jwt_required()
    def delete(self, post_id):
        user_id = get_jwt_identity()
        post = PostModel.query.get_or_404(post_id)
        if post.author_id != int(user_id):
            abort(403, message="Not authorized to delete this post")

        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}, 200
