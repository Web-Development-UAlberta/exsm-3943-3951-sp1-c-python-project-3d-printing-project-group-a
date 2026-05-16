from flask import Blueprint, request, jsonify
from ..database import get_db
from ..models import Model, Filament, Tag, ModelTag, ModelFilament
from ..services.pricing import calculate_quote
from werkzeug.utils import secure_filename
import os

models_bp = Blueprint("models", __name__)

@models_bp.route("/", methods=["GET"])
def get_models():
    tag_id = request.args.get("tag_id")
    order = request.args.get("order")
    filament_id = request.args.get("filament_id")
    search = request.args.get("search")

    try:
        with get_db() as db:
            query = db.query(Model)
            if search and tag_id and order == "asc" and filament_id:
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).filter(ModelFilament.filament_id == filament_id).filter(Model.model_name.ilike(f'%{search}%')).order_by(Model.model_name.asc())
            elif search and tag_id and order == "desc" and filament_id:
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).filter(ModelFilament.filament_id == filament_id).filter(Model.model_name.ilike(f'%{search}%')).order_by(Model.model_name.desc())
            elif search and tag_id and order == 'asc':
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).filter(Model.model_name.ilike(f'%{search}%')).order_by(Model.model_name.asc()).all()
            elif search and tag_id and order == 'desc':
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).filter(Model.model_name.ilike(f'%{search}%')).order_by(Model.model_name.desc()).all()
            elif search and tag_id and filament_id:
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).filter(ModelFilament.filament_id == filament_id).filter(Model.model_name.ilike(f'%{search}%'))
            elif search and order == 'asc':
                models = query.filter(Model.model_name.ilike(f'%{search}%')).order_by(Model.model_name.asc()).all()
            elif search and order == 'desc':
                models = query.filter(Model.model_name.ilike(f'%{search}%')).order_by(Model.model_name.desc()).all()
            elif search and tag_id:
                models = query.join(ModelTag).filter(ModelTag.tag_id == tag_id).filter(Model.model_name.ilike(f'%{search}%'))
            elif search and filament_id:
                models = query.join(ModelFilament).filter(ModelFilament.filament_id == filament_id).filter(Model.model_name.ilike(f'%{search}%'))
            elif tag_id and order == "asc" and filament_id:
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).filter(ModelFilament.filament_id == filament_id).order_by(Model.model_name.asc())
            elif tag_id and order == "desc" and filament_id:
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).filter(ModelFilament.filament_id == filament_id).order_by(Model.model_name.desc())
            elif tag_id and order == 'asc':
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).order_by(Model.model_name.asc()).all()
            elif tag_id and order == 'desc':
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).order_by(Model.model_name.desc()).all()
            elif tag_id and filament_id:
                models = query.join(ModelTag).join(ModelFilament).filter(ModelTag.tag_id == tag_id).filter(ModelFilament.filament_id == filament_id)
            elif order == 'asc':
                models = query.order_by(Model.model_name.asc()).all()
            elif order == 'desc':
                models = query.order_by(Model.model_name.desc()).all()
            elif tag_id:
                models = query.join(ModelTag).filter(ModelTag.tag_id == tag_id)
            elif filament_id:
                models = query.join(ModelFilament).filter(ModelFilament.filament_id == filament_id)
            elif search:
                models = query.filter(Model.model_name.ilike(f'%{search}%')).all()
            else:
                models = query.all()
            result = []
            for m in models:
                # FORCE LOAD relationships safely
                filaments = [
                    link.filament
                    for link in m.filament_links
                    if link.filament is not None
                ]

                tags = [
                    {"tag_id": link.tag.tag_id, "tag_name": link.tag.tag_name}
                    for link in m.tag_links
                    if link.tag is not None
                ]

                result.append({
                    "model_id": m.model_id,
                    "model_name": m.model_name,
                    "tags": tags,
                    "filaments": [
                        {
                            "filament_id": f.filament_id,
                            "material_name": f.material_name,
                            "color_hex": f.color_hex
                        }
                        for f in filaments
                    ]
                })

            return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@models_bp.route("/<int:model_id>", methods=["GET"])

def get_model(model_id):
    try:
        with get_db() as db:
            model = db.query(Model).filter_by(model_id=model_id).first()
            if not model:
                return jsonify({"error": "Model not found"}), 404
            
            tags = [
                {"tag_id": link.tag.tag_id, "tag_name": link.tag.tag_name}
                for link in model.tag_links
            ]

            filaments = [
                {
                    "filament_id": link.filament.filament_id,
                    "material_name": link.filament.material_name,
                    "color_hex": link.filament.color_hex,
                    "filament_price": float(link.filament.filament_price),
                    "in_stock": link.filament.quantity_in_stock > 0
                }

                for link in model.filament_links
            ]
            return jsonify({
                "model_id": model.model_id,
                "model_name": model.model_name,
                "model_description": model.model_description,
                "model_length": model.model_length,
                "model_width": model.model_width,
                "model_height": model.model_height,
                "tags": tags,
                "filaments": filaments
            }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@models_bp.route("/upload", methods=["POST"])
def custom_upload():
    CUSTOM_UPLOAD = os.getenv('CUSTOM_UPLOAD')
    ALLOWED_FILE_EXTENSIONS = {'3tl', '3mf'}
    if not os.path.exists(CUSTOM_UPLOAD):
        os.makedirs(CUSTOM_UPLOAD, exist_ok=True)

    def extension_check(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        if file and extension_check(file.filename):
            if file:
                filename = secure_filename(file.filename)
                save_path = os.path.join(CUSTOM_UPLOAD, filename)
                file.save(save_path)
                return jsonify({"message": "File uploaded", "filename": file.filename}), 200
        else:
            return jsonify({"error": "File extension not supported", "filename": file.filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@models_bp.route("/quote", methods=["POST"])
def get_quote():
    data = request.get_json()
    required = ["model_id", "filament_id", "scale", "infill_percent", "color_count"]

    for field in required:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400
        
    if not (1 <= data["scale"] <= 200):
        return jsonify({"error": "Scale must be between 1 and 200"}), 400
    
    if not (1 <= data["infill_percent"] <= 100):
        return jsonify({"error": "Infill must be between 1 and 100"}), 400
    
    if data["color_count"] < 1:
        return jsonify({"error": "color_count must be at least 1"}), 400
    
    try:
        with get_db() as db:
            model = db.query(Model).filter_by(model_id=data["model_id"]).first()
            filament = db.query(Filament).filter_by(filament_id=data["filament_id"]).first()

            if not model:
                return jsonify({"error": "Model not found"}), 404
            
            if not filament:
                return jsonify({"error": "Filament not found"}), 404
            
            if not model.model_length or not model.model_width or not model.model_height:
                return jsonify({"error": "Model is missing dimension data"}), 400
            
            if not model.print_time_hours:
                return jsonify({"error": "Model is missing print time data"}), 400
            
            MAX_DIMENSION_MM = 500
            scaled_length = model.model_length * (data["scale"] / 100)
            scaled_width = model.model_width  * (data["scale"] / 100)
            scaled_height = model.model_height * (data["scale"] / 100)

            if any(d > MAX_DIMENSION_MM for d in [scaled_length, scaled_width, scaled_height]):
                return jsonify({"error": "Scaled dimensions exceed maximum of 500mm per side"}), 400
            
            quote = calculate_quote(
                length = model.model_length,
                width = model.model_width,
                height = model.model_height,
                scale = data["scale"],
                infill_percent = data["infill_percent"],
                filament_price = float(filament.filament_price),
                color_count = data["color_count"],
                print_time_hours = float(model.print_time_hours),
            )

            return jsonify(quote), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500