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

    MAX_DIM = 500
    if any(d * (scale / 100) > MAX_DIM for d in [
        model.model_length or 0,
        model.model_width  or 0,
        model.model_height or 0
    ]):
        raise ValueError("Scaled dimensions exceed maximum of 500mm per side")

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

def assign_printer_to_order(db, order, print_time_hours):
    """
    Assigns the order to the printer with least queue time.
    Adds 10% buffer on top of estimated print time (slicer estimate + 10%).
    Updates printer queue.
    Returns estimated completion hours from now.
    """
    from ..models import Printer

    # add 10% buffer to slicer estimate
    buffered_time = float(print_time_hours) * 1.10

    # find printer with least queue
    printers = db.query(Printer).all()
    if not printers:
        raise ValueError("No printers available")

    best_printer = min(printers, key=lambda p: float(p.printer_queue or 0))

    # estimated completion = current queue + buffered print time
    current_queue = float(best_printer.printer_queue or 0)
    estimated_completion = round(current_queue + buffered_time, 2)

    # update printer queue
    best_printer.printer_queue = estimated_completion

    # link order to printer
    order.printer_id = best_printer.printer_id  

    return {
        "printer_id": best_printer.printer_id,
        "printer_name": best_printer.printer_type.printer_name if best_printer.printer_type else None,
        "estimated_hours": estimated_completion,
        "print_time_with_buffer": buffered_time
    }