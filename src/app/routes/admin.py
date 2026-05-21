from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import date
from ..database import get_db
from ..models import (User, Filament, Printer, PrinterType, OrderHeader, OrderDetail, Model, Tag, ModelTag, ModelFilament, FilamentPrinter)
from ..services.stock_service import get_low_stock_filaments, is_low_stock
from ..utils.decorators import require_admin

admin_bp = Blueprint("admin", __name__)

# dashboard
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@require_admin
def get_dashboard():
    try:
        with get_db() as db:
            active_orders = db.query(OrderHeader).filter(OrderHeader.order_status.in_(["Pending", "Printing"])).count()
            total_orders = db.query(OrderHeader).filter(OrderHeader.order_status != "Cart").count()

            low_stock = get_low_stock_filaments(db, Filament)

            total_printers = db.query(Printer).count()
            busy_printers = db.query(OrderHeader).filter_by(order_status="Printing").count()
            free_printers = total_printers - busy_printers

            return jsonify({
                "active_orders": active_orders,
                "total_orders": total_orders,
                "low_stock_count": len(low_stock),
                "low_stock_items": low_stock,
                "total_printers": total_printers,
                "free_printers": max(free_printers, 0)
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# filaments
@admin_bp.route("/filaments", methods=["GET"])
@jwt_required()
@require_admin
def get_filaments():
    try:
        with get_db() as db:
            filaments = db.query(Filament).all()
            return jsonify([
                {
                    "filament_id": f.filament_id,
                    "material_name": f.material_name,
                    "color_hex": f.color_hex,
                    "quantity_in_stock": f.quantity_in_stock,
                    "manufacturer": f.manufacturer,
                    "filament_price": float(f.filament_price),
                    "more_wear_and_tear": float(f.more_wear_and_tear) if f.more_wear_and_tear else None,
                    "finish_filament": f.finish_filament,
                    "is_low_stock": is_low_stock(f.quantity_in_stock or 0)
                }
                for f in filaments
            ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/filaments", methods=["POST"])
@jwt_required()
@require_admin
def add_filament():
    data = request.get_json()
    required = ["material_name", "filament_price"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
    try:
        with get_db() as db:
            filament = Filament(
                material_name = data["material_name"],
                color_hex = data.get("color_hex"),
                quantity_in_stock = data.get("quantity_in_stock", 0),
                manufacturer = data.get("manufacturer"),
                filament_price = data["filament_price"],
                more_wear_and_tear = data.get("more_wear_and_tear"),
                finish_filament = data.get("finish_filament")
            )
            db.add(filament)
            db.flush()
            return jsonify({
                "message":     "Filament added",
                "filament_id": filament.filament_id
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/filaments/<int:filament_id>", methods=["PUT"])
@jwt_required()
@require_admin
def update_filament(filament_id):
    data = request.get_json()
    try:
        with get_db() as db:
            filament = db.query(Filament).filter_by(filament_id=filament_id).first()
            if not filament:
                return jsonify({"error": "Filament not found"}), 404
            if data.get("material_name") is not None: filament.material_name = data["material_name"]
            if data.get("color_hex") is not None: filament.color_hex = data["color_hex"]
            if data.get("quantity_in_stock")  is not None: filament.quantity_in_stock = data["quantity_in_stock"]
            if data.get("manufacturer") is not None: filament.manufacturer = data["manufacturer"]
            if data.get("filament_price") is not None: filament.filament_price = data["filament_price"]
            if data.get("more_wear_and_tear") is not None: filament.more_wear_and_tear = data["more_wear_and_tear"]
            if data.get("finish_filament") is not None: filament.finish_filament = data["finish_filament"]
            return jsonify({"message": "Filament updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/filaments/<int:filament_id>", methods=["DELETE"])
@jwt_required()
@require_admin
def delete_filament(filament_id):
    try:
        with get_db() as db:
            filament = db.query(Filament).filter_by(filament_id=filament_id).first()
            if not filament:
                return jsonify({"error": "Filament not found"}), 404
            db.delete(filament)
            return jsonify({"message": "Filament deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# printers
@admin_bp.route("/printers", methods=["GET"])
@jwt_required()
@require_admin
def get_printers():
    try:
        with get_db() as db:
            printers = db.query(Printer).all()
            result = []
            for p in printers:
                # 1. Gather all filament IDs linked to this specific printer
                printer_filament_ids = [link.filament_id for link in p.filament_links if link.filament_id]
                
                # 2. Query active orders matching ANY of this printer's filaments
                active_order = None
                if printer_filament_ids:
                    active_order = db.query(OrderHeader).filter_by(
                        order_status="Printing"
                    ).join(OrderDetail).filter(
                        OrderDetail.filament_id.in_(printer_filament_ids) # Fixed attribute reference
                    ).first()
                
                result.append({
                    "printer_id": p.printer_id,
                    "printer_name": p.printer_type.printer_name if p.printer_type else None,
                    "max_size": p.printer_type.max_size if p.printer_type else None,
                    "filaments": [
                        {
                            "filament_id": link.filament.filament_id,
                            "material_name": link.filament.material_name,
                            "color_hex": link.filament.color_hex
                        }
                        for link in p.filament_links
                        if link.filament
                    ],
                    "printer_queue": p.printer_queue or 0,
                    "status": "Printing" if active_order else "Available",
                    "current_order": active_order.order_header_id if active_order else None
                })
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/printers", methods=["POST"])
@jwt_required()
@require_admin
def add_printer():
    data = request.get_json()
    if data.get("printer_type_id") is None:
        return jsonify({"error": "printer_type_id is required"}), 400
    try:
        with get_db() as db:
            printer_type = db.query(PrinterType).filter_by(
                printer_type_id=data["printer_type_id"]
            ).first()
            if not printer_type:
                return jsonify({"error": "Printer type not found"}), 404

            printer = Printer(
                printer_type_id = data["printer_type_id"],
                printer_queue   = 0
            )
            db.add(printer)
            db.flush()

            # link filaments
            from ..models import FilamentPrinter
            for filament_id in data.get("filament_ids", []):
                filament = db.query(Filament).filter_by(filament_id=filament_id).first()
                if filament:
                    db.add(FilamentPrinter(
                        printer_id=printer.printer_id,
                        filament_id=filament_id
                    ))

            return jsonify({
                "message":    "Printer added",
                "printer_id": printer.printer_id
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/printers/<int:printer_id>", methods=["DELETE"])
@jwt_required()
@require_admin
def delete_printer(printer_id):
    try:
        with get_db() as db:
            printer = db.query(Printer).filter_by(printer_id=printer_id).first()
            if not printer:
                return jsonify({"error": "Printer not found"}), 404
            db.delete(printer)
            return jsonify({"message": "Printer deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# orders
@admin_bp.route("/orders", methods=["GET"])
@jwt_required()
@require_admin
def get_all_orders():
    try:
        with get_db() as db:
            orders = db.query(OrderHeader).filter(OrderHeader.order_status != "Cart").all()
            return jsonify([
                {
                    "order_id": o.order_header_id,
                    "order_date": str(o.order_date),
                    "order_status": o.order_status,
                    "payment_status": o.payment_status,
                    "total_price": float(o.total_price),
                    "tracking_number": o.order_tracking_number,
                    "user_id": o.user_id,
                    "username": o.user.username if o.user else None,
                    "items": [
                        {
                            "model": d.model.model_name if d.model else None,
                            "quantity": d.order_quantity,
                            "filament": d.filament.material_name if d.filament else None
                        }
                        for d in o.details
                    ]
                }
                for o in orders
            ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/orders/<int:order_id>", methods=["PUT"])
@jwt_required()
@require_admin
def update_order(order_id):
    data = request.get_json()
    valid_statuses = ["Pending", "Printing", "Shipped", "Completed", "Cancelled"]
    try:
        with get_db() as db:
            order = db.query(OrderHeader).filter_by(order_header_id=order_id).first()
            if not order:
                return jsonify({"error": "Order not found"}), 404
            if data.get("order_status"):
                if data["order_status"] not in valid_statuses:
                    return jsonify({"error": f"Invalid status. Must be one of: {valid_statuses}"}), 400
                order.order_status = data["order_status"]
            if data.get("order_tracking_number") is not None:
                order.order_tracking_number = data["order_tracking_number"]
            if data.get("payment_status") is not None:
                order.payment_status = data["payment_status"]
            return jsonify({"message": "Order updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# models
@admin_bp.route("/models", methods=["GET"])
@jwt_required()
@require_admin
def get_all_models():
    try:
        with get_db() as db:
            models = db.query(Model).all()
            return jsonify([
                {
                    "model_id": m.model_id,
                    "model_name": m.model_name,
                    "model_length": m.model_length,
                    "model_width": m.model_width,
                    "model_height": m.model_height,
                    "model_description": m.model_description,
                    "print_time_hours": float(m.print_time_hours) if m.print_time_hours else None,
                    "tags": [
                        link.tag.tag_name for link in m.tag_links
                    ],
                    "filaments": [
                        {
                            "filament_id": link.filament.filament_id,
                            "material_name": link.filament.material_name
                        }
                        for link in m.filament_links
                    ]
                }
                for m in models
            ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/models", methods=["POST"])
@jwt_required()
@require_admin
def add_model():
    data = request.get_json()
    required = ["model_name", "model_length", "model_width", "model_height", "print_time_hours"]
    for field in required:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400
    try:
        with get_db() as db:
            model = Model(
                model_name = data["model_name"],
                model_length = data["model_length"],
                model_width = data["model_width"],
                model_height = data["model_height"],
                model_description = data.get("model_description"),
                print_time_hours = data["print_time_hours"],
                printer_id = data.get("printer_id")
            )
            db.add(model)
            db.flush()

            # link tags
            for tag_id in data.get("tag_ids", []):
                tag = db.query(Tag).filter_by(tag_id=tag_id).first()
                if tag:
                    db.add(ModelTag(model_id=model.model_id, tag_id=tag_id))

            # link filaments
            for filament_id in data.get("filament_ids", []):
                filament = db.query(Filament).filter_by(filament_id=filament_id).first()
                if filament:
                    db.add(ModelFilament(model_id=model.model_id, filament_id=filament_id))

            return jsonify({
                "message":  "Model added",
                "model_id": model.model_id
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/models/<int:model_id>", methods=["PUT"])
@jwt_required()
@require_admin
def update_model(model_id):
    data = request.get_json()
    try:
        with get_db() as db:
            model = db.query(Model).filter_by(model_id=model_id).first()
            if not model:
                return jsonify({"error": "Model not found"}), 404
            if data.get("model_name") is not None: model.model_name = data["model_name"]
            if data.get("model_length") is not None: model.model_length = data["model_length"]
            if data.get("model_width") is not None: model.model_width = data["model_width"]
            if data.get("model_height") is not None: model.model_height = data["model_height"]
            if data.get("model_description") is not None: model.model_description = data["model_description"]
            if data.get("print_time_hours") is not None: model.print_time_hours = data["print_time_hours"]
            return jsonify({"message": "Model updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/models/<int:model_id>", methods=["DELETE"])
@jwt_required()
@require_admin
def delete_model(model_id):
    try:
        with get_db() as db:
            model = db.query(Model).filter_by(model_id=model_id).first()
            if not model:
                return jsonify({"error": "Model not found"}), 404
            db.delete(model)
            return jsonify({"message": "Model deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# users
@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@require_admin
def get_all_users():
    try:
        with get_db() as db:
            users = db.query(User).all()
            return jsonify([
                {
                    "user_id": u.user_id,
                    "username": u.username,
                    "full_name": u.full_name,
                    "email": u.email,
                    "phone_number": u.phone_number,
                    "city": u.city,
                    "province": u.province,
                    "is_admin": u.is_admin
                }
                for u in users
            ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/users/<int:user_id>/make-admin", methods=["PUT"])
@jwt_required()
@require_admin
def make_admin(user_id):
    try:
        with get_db() as db:
            user = db.query(User).filter_by(user_id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            user.is_admin = True
            return jsonify({"message": f"{user.username} is now an admin"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/users/<int:user_id>/remove-admin", methods=["PUT"])
@jwt_required()
@require_admin
def remove_admin(user_id):
    try:
        with get_db() as db:
            user = db.query(User).filter_by(user_id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            user.is_admin = False
            return jsonify({"message": f"{user.username} admin access removed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@require_admin
def delete_user(user_id):
    try:
        with get_db() as db:
            user = db.query(User).filter_by(user_id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            db.delete(user)
            return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# printer types
@admin_bp.route("/printer-types", methods=["GET"])
@jwt_required()
@require_admin
def get_printer_types():
    try:
        with get_db() as db:
            types = db.query(PrinterType).all()
            return jsonify([
                {
                    "printer_type_id": t.printer_type_id,
                    "printer_name": t.printer_name,
                    "max_size": t.max_size
                }
                for t in types
            ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/printer-types", methods=["POST"])
@jwt_required()
@require_admin
def add_printer_type():
    data = request.get_json()
    required = ["printer_name", "max_size"]
    for field in required:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400
    try:
        with get_db() as db:
            printer_type = PrinterType(
                printer_name = data["printer_name"],
                max_size = data["max_size"]
            )
            db.add(printer_type)
            db.flush()
            return jsonify({
                "message": "Printer type added",
                "printer_type_id": printer_type.printer_type_id
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@admin_bp.route("/orders/<int:order_id>", methods=["DELETE"])
@jwt_required()
@require_admin
def delete_order(order_id):
    try:
        with get_db() as db:
            order = db.query(OrderHeader).filter_by(
                order_header_id=order_id
            ).first()
            if not order:
                return jsonify({"error": "Order not found"}), 404
            if order.order_status != "Cancelled":
                return jsonify({"error": "Only cancelled orders can be deleted"}), 400
            # Delete order details first
            for detail in order.details:
                db.delete(detail)
            db.delete(order)
            return jsonify({"message": "Order deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500