from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo
from app.models import to_dict, StatusEnum

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data.get('title') or data.get('status') not in StatusEnum._value2member_map_:
        return jsonify({"error": "Invalid data"}), 400

    task = {
        "title": data['title'],
        "description": data.get('description'),
        "status": data['status'],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "user": current_user
    }

    result = mongo.db.tasks.insert_one(task)
    task["_id"] = result.inserted_id
    return jsonify(to_dict(task)), 201


@task_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({'username': current_user})

    tasks = mongo.db.tasks.find() if user.get("role") == "admin" else mongo.db.tasks.find({"user": current_user})
    return jsonify([to_dict(task) for task in tasks])


@task_bp.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({'username': current_user})

    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)}) if user.get(
        "role") == "admin" else mongo.db.tasks.find_one({"_id": ObjectId(task_id), "user": current_user})

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    updated_fields = {key: data[key] for key in data if
                      key in ["title", "description", "status"] and key in StatusEnum._value2member_map_}
    updated_fields["updated_at"] = datetime.utcnow()

    mongo.db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": updated_fields})
    task.update(updated_fields)
    return jsonify(to_dict(task))


@task_bp.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({'username': current_user})

    result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id)}) if user.get(
        "role") == "admin" else mongo.db.tasks.delete_one({"_id": ObjectId(task_id), "user": current_user})

    return jsonify({"message": "Task deleted"}) if result.deleted_count else jsonify({"error": "Task not found"}), 404
