import re
from app import db
from app.models.customer import Customer
from datetime import datetime
from flask import request, Blueprint, make_response, jsonify
import requests
import os
from app.models.video import Video
from app.models.rental import Rental


videos_bp = Blueprint(
    "videos", __name__, url_prefix="/videos")
customers_bp = Blueprint(
    "customers", __name__, url_prefix="/customers")
rentals_bp = Blueprint(
    "rentals", __name__, url_prefix="/rentals")


# ----------------------------
# WAVE 1 - CUSTOMER ENDPOINTS
# ----------------------------

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customer_index():
    customers = Customer.query.all()
    customers_response = [(customer.to_json()) for customer in customers]
    return make_response(jsonify(customers_response), 200)


@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()
    if "name" in request_body and "postal_code" in request_body and "phone" in request_body:
        new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            registered_at=datetime.now()
        )
        db.session.add(new_customer)
        db.session.commit()
        customer_response = {"id": new_customer.customer_id}
        return jsonify(customer_response), 201
        # return jsonify(new_customer.to_json()), 201
    return make_response({"details": "You must include a name, postal code, and phone number"}, 400)


@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("Customer does not exist", 404)
    return jsonify(customer.to_json()), 200


@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    form_data = request.get_json()
    if customer is None:
        return make_response("Customer does not exist", 404)
    elif "name" in form_data and "postal_code" in form_data and "phone" in form_data:
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]
        db.session.commit()
        return jsonify(customer.to_json()), 200
        # JSON DICTIONARY !why dis only one
    return make_response({"details": "Bad Request"}, 400)


@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("Customer does not exist", 404)
    db.session.delete(customer)
    db.session.commit()
    # return jsonify(customer.to_json()), 200
    customer_response = {"id": customer.customer_id}
    return jsonify(customer_response), 200


# --------------------------
# WAVE 1 - VIDEO ENDPOINTS
# --------------------------

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def video_index():
    videos = Video.query.all()
    videos_response = [(video.to_dict()) for video in videos]
    return make_response(jsonify(videos_response), 200)


@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():
    request_body = request.get_json()
    if "title" in request_body and "release_date" in request_body and "total_inventory" in request_body:
        new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"],
            available_inventory=request_body["total_inventory"]
        )
        db.session.add(new_video)
        db.session.commit()
        # video_response = {"id": new_video.video_id}
        return jsonify({"id": new_video.video_id}), 201
        # return jsonify(new_video.to_dict()), 201
    return make_response({"details": "You must include a title, release date, and total inventory"}, 400)


@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return make_response("Video does not exist", 404)
    return jsonify(video.to_dict()), 200


@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    video = Video.query.get(video_id)
    form_data = request.get_json()
    if video is None:
        return make_response("Video does not exist", 404)
    elif "title" in form_data and "release_date" in form_data and "total_inventory" in form_data:
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]
        db.session.commit()
        return jsonify(video.to_dict()), 200
    return make_response("Bad Request", 400)


@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return make_response("Video does not exist", 404)
    db.session.delete(video)
    db.session.commit()
    # return jsonify(video.to_dict()), 200
    # video_response = {"id": video.video_id}
    return jsonify({"id": video.video_id}), 200


# ----------------------------------
# WAVE 2 - (mostly) RENTAL ENDPOINTS
# ----------------------------------

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def checking_out():
    request_body = request.get_json()
    # INT ??? (the order).
    try:
        video_id = int(request_body["video_id"])
        customer_id = int(request_body["customer_id"])
    except ValueError or KeyError:
        return make_response({"details": "The customer or video does not exist"}, 400)
    video = Video.query.get_or_404(request_body["video_id"])
    customer = Customer.query.get_or_404(request_body["customer_id"])
    if video.available_inventory < 1:
        return make_response({"details": "This video doesn't have any current available inventory"}, 400)
    elif "customer_id" in request_body and "video_id" in request_body:
        # date = Rental.date_due()
        new_rental = Rental(
            customer_id=request_body["customer_id"],
            video_id=request_body["video_id"],
        )
        customer.videos_checked_out_count += 1
        video.available_inventory -= 1
        db.session.add_all([new_rental, video, customer])
        db.session.commit()
        return ({
            "customer_id": customer.customer_id,
            "video_id": video.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory
        }, 200)
    return make_response({"details": "Invalid required request body parameters"}, 400)


@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def checking_in():
    request_body = request.get_json()
    video = Video.query.get_or_404(request_body["video_id"])
    customer = Customer.query.get_or_404(request_body["customer_id"])
    if "customer_id" in request_body and "video_id" in request_body:
        customer.videos_checked_out_count -= 1
        video.available_inventory += 1
        ###
        rental = Rental.query.filter_by(
            video_id=request_body["video_id"], customer_id=request_body["customer_id"]).one_or_none()
        if rental is None:
            return make_response({"details": "The video and customer do not match a current rental"}, 400)
        db.session.delete(rental)
        db.session.add_all([video, customer])
        db.session.commit()
        return ({
            "customer_id": customer.customer_id,
            "video_id": video.video_id,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory
        }), 200
    # if video is None or customer is None:
    #     return make_response({"details": "The customer or video does not exist"}, 404)
    return make_response({"details": "Invalid required request body parameters"}, 400)


@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_videos_of_customer(customer_id):
    # request_body = request.get_json()
    rentals = Rental.query.filter(Rental.customer_id == customer_id).all()
    if rentals is None:
        return make_response({"details": "Customer does not exist"}, 404)
    list_of_rentals = []
    for rental in rentals:
        video = Video.query.get(rental.video_id)
        list_of_rentals.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date})
    return jsonify(list_of_rentals), 200


@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customers_of_video(video_id):
    rentals = Rental.query.filter(Rental.video_id == video_id).all()
    if rentals is None:
        return make_response({"details": "Video does not exist"}, 404)
    list_of_customers = []
    for rental in rentals:
        customer = Customer.query.get(rental.customer_id)
        list_of_customers.append({
            "due_date": rental.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": int(customer.postal_code)})
    return jsonify(list_of_customers), 200
