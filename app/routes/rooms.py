from flask import render_template, request, redirect, url_for, flash, jsonify
from app.routes import main
from models.room import Room

@main.route('/rooms')
def list_rooms():
    """Display all rooms."""
    rooms = Room.get_all()
    return render_template('rooms/list.html', rooms=rooms)

@main.route('/rooms/add', methods=['GET', 'POST'])
def add_room():
    """Add new room."""
    if request.method == 'GET':
        return render_template('rooms/add.html')

    try:
        room_data = {
            'room_number': request.form['room_number'],
            'room_type': request.form['room_type'],
            'capacity': int(request.form['capacity']),
            'price_per_night': float(request.form['price_per_night']),
            'description': request.form.get('description', '')
        }

        Room.create(room_data)
        flash('اتاق با موفقیت اضافه شد', 'success')
        return redirect(url_for('main.list_rooms'))

    except ValueError as e:
        flash(f'خطا در اعتبارسنجی: {str(e)}', 'error')
        return redirect(url_for('main.add_room'))
    except Exception as e:
        flash(f'خطا در اضافه کردن اتاق: {str(e)}', 'error')
        return redirect(url_for('main.add_room'))

@main.route('/rooms/<int:room_id>')
def view_room(room_id):
    """View room details."""
    room = Room.get_by_id(room_id)
    if not room:
        flash('اتاق یافت نشد', 'error')
        return redirect(url_for('main.list_rooms'))
    return render_template('rooms/detail.html', room=room)

@main.route('/rooms/<int:room_id>/edit', methods=['GET', 'POST'])
def edit_room(room_id):
    """Edit room."""
    if request.method == 'GET':
        room = Room.get_by_id(room_id)
        if not room:
            flash('اتاق یافت نشد', 'error')
            return redirect(url_for('main.list_rooms'))
        return render_template('rooms/edit.html', room=room)

    try:
        room_data = {
            'room_number': request.form['room_number'],
            'room_type': request.form['room_type'],
            'capacity': int(request.form['capacity']),
            'price_per_night': float(request.form['price_per_night']),
            'is_available': 1 if 'is_available' in request.form else 0,
            'description': request.form.get('description', '')
        }

        Room.update(room_id, room_data)
        flash('اتاق با موفقیت به‌روزرسانی شد', 'success')
        return redirect(url_for('main.list_rooms'))

    except Exception as e:
        flash(f'خطا در به‌روزرسانی: {str(e)}', 'error')
        return redirect(url_for('main.edit_room', room_id=room_id))

@main.route('/rooms/<int:room_id>/delete', methods=['POST'])
def delete_room(room_id):
    """Delete room."""
    try:
        Room.delete(room_id)
        flash('اتاق با موفقیت حذف شد', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f'خطا در حذف: {str(e)}', 'error')
    return redirect(url_for('main.list_rooms'))

@main.route('/api/rooms/available')
def api_available_rooms():
    """API endpoint for available rooms."""
    arrival = request.args.get('arrival_date')
    departure = request.args.get('departure_date')
    rooms = Room.get_available(arrival, departure)
    return jsonify([dict(r) for r in rooms])
