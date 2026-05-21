from datetime import date
from ..models import OrderHeader, OrderDetail, Filament, Model
from ..services.pricing import calculate_quote


def get_or_create_cart(db, user_id):
    cart = db.query(OrderHeader).filter_by(
        user_id=user_id,
        order_status="Cart"
    ).first()
    if not cart:
        cart = OrderHeader(
            user_id=user_id,
            order_date=date.today(),
            order_status="Cart",
            shipping_price=10.00,
            total_price=0.00,
            payment_status="Pending"
        )
        db.add(cart)
        db.flush()
    return cart


def calculate_cart_total(db, cart):
    total = sum(
        float(detail.unit_price) * detail.order_quantity
        for detail in cart.details
        if detail.unit_price
    )
    cart.total_price = round(total + float(cart.shipping_price), 2)


def add_item_to_cart(db, user_id, model_id, filament_id, quantity, scale, infill_percent, color_count):
    model = db.query(Model).filter_by(model_id=model_id).first()
    filament = db.query(Filament).filter_by(filament_id=filament_id).first()

    if not model:
        raise ValueError("Model not found")
    if not filament:
        raise ValueError("Filament not found")
    if not model.print_time_hours:
        raise ValueError("Model is missing print time data")

    quote = calculate_quote(
        length = model.model_length,
        width = model.model_width,
        height = model.model_height,
        scale = scale,
        infill_percent = infill_percent,
        filament_price = float(filament.filament_price),
        color_count = color_count,
        print_time_hours = float(model.print_time_hours)
    )
    unit_price = quote["total"]

    cart = get_or_create_cart(db, user_id)

    existing = db.query(OrderDetail).filter_by(
        order_header_id = cart.order_header_id,
        model_id = model_id,
        filament_id = filament_id,
        scale = scale,
        infill_percent = infill_percent
    ).first()

    if existing:
        existing.order_quantity += quantity
    else:
        detail = OrderDetail(
            order_header_id = cart.order_header_id,
            model_id = model_id,
            filament_id = filament_id,
            order_quantity = quantity,
            scale = scale,
            infill_percent = infill_percent,
            unit_price = unit_price
        )
        db.add(detail)

    db.flush()
    calculate_cart_total(db, cart)
    return cart


def remove_item_from_cart(db, user_id, order_detail_id):
    cart = db.query(OrderHeader).filter_by(
        user_id=user_id,
        order_status="Cart"
    ).first()
    if not cart:
        raise ValueError("No active cart found")

    detail = db.query(OrderDetail).filter_by(
        order_detail_id=order_detail_id,
        order_header_id=cart.order_header_id
    ).first()
    if not detail:
        raise ValueError("Item not found in cart")

    db.delete(detail)
    db.flush()
    calculate_cart_total(db, cart)
    return cart


def clear_cart(db, user_id):
    cart = db.query(OrderHeader).filter_by(
        user_id=user_id,
        order_status="Cart"
    ).first()
    if not cart:
        raise ValueError("No active cart found")

    for detail in cart.details:
        db.delete(detail)
    db.flush()
    cart.total_price = float(cart.shipping_price)
    return cart


def deduct_filament_stock(db, order):
    """
    Deducts filament stock when order status changes to Printing.
    """
    for detail in order.details:
        filament = db.query(Filament).filter_by(
            filament_id=detail.filament_id
        ).first()
        model = db.query(Model).filter_by(
            model_id=detail.model_id
        ).first()

        if filament and model and model.model_length:
            try:
                quote = calculate_quote(
                    length = model.model_length,
                    width = model.model_width,
                    height = model.model_height,
                    scale = float(detail.scale),
                    infill_percent = float(detail.infill_percent),
                    filament_price = float(filament.filament_price),
                    color_count = 1,
                    print_time_hours = float(model.print_time_hours)
                )
                grams_needed = quote["material_grams"] * detail.order_quantity
                if filament.quantity_in_stock is not None:
                    filament.quantity_in_stock = max(0, filament.quantity_in_stock - grams_needed)
            except Exception as e:
                print(e)


def assign_printer_to_order(db, order, print_time_hours):
    from ..models import Printer
    buffered_time = float(print_time_hours) * 1.10
    printers = db.query(Printer).all()
    if not printers:
        raise ValueError("No printers available")
    best_printer = min(
        printers,
        key=lambda p: float(p.printer_queue or 0)
    )
    current_queue = float(best_printer.printer_queue or 0)
    estimated_completion = round(current_queue + buffered_time, 2)
    best_printer.printer_queue = estimated_completion
    order.printer_id = best_printer.printer_id
    return {
        "printer_id": best_printer.printer_id,
        "printer_name": best_printer.printer_type.printer_name if best_printer.printer_type else None,
        "estimated_hours": estimated_completion,
        "print_time_with_buffer": buffered_time
    }