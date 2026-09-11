from flask import render_template, request, redirect, url_for, flash
from app.routes import main
from models.guest import Guest
from models.room import Room
from utils.digits import to_number

@main.route('/')
def home():
    """Home page."""
    return render_template('index.html')

@main.route('/data_entry')
def fill_form():
    """Guest registration form."""
    rooms = Room.get_available()
    return render_template('form.html', rooms=rooms)

@main.route('/add_guest', methods=['POST'])
def add_guest():
    """Process guest registration with validation."""
    try:
        # Validate required fields
        required_fields = ['name', 'last_name', 'arrival_date', 'departure_date', 'is_foreign']
        for field in required_fields:
            if not request.form.get(field):
                flash(f'فیلد {field} الزامی است', 'error')
                return redirect(url_for('main.fill_form'))

        # Determine if foreign guest
        is_foreign = request.form['is_foreign'] == 'TRUE'

        # Build guest data based on type
        if is_foreign:
            guest_data = {
                'is_foreign': 'خارجی',
                'nationality': request.form.get('nationality', ''),
                'name': request.form['foreign_name'],
                'last_name': request.form['foreign_last_name'],
                'father_name': '',
                'national_id': '',
                'passport_number': request.form.get('passport_number', ''),
                'gender': request.form.get('gender', ''),
                'date_of_birth': request.form.get('f_date_of_birth', ''),
                'phone_number': request.form.get('f_phone_number', ''),
                'leader_name': request.form.get('leader_name', ''),
                'leader_phone': request.form.get('leader_phone', ''),
                'arrival_date': request.form['f_arrival_date'],
                'departure_date': request.form['f_departure_date'],
                'occupation': '',
                'residence_unit': request.form.get('f_residence_unit', ''),
                'room_id': request.form.get('f_room_id'),
                'payment_type': request.form.get('f_payment_type', ''),
                'advance_payment': to_number(request.form.get('f_advance_payment')),
                'balance': to_number(request.form.get('f_balance')),
                'total_amount': to_number(request.form.get('f_total_amount')),
                'note': request.form.get('f_note', ''),
                'is_companion': 0,
                'primary_guest_id': None
            }
        else:
            guest_data = {
                'is_foreign': 'ایرانی',
                'nationality': 'ایرانی',
                'name': request.form['name'],
                'last_name': request.form['last_name'],
                'father_name': request.form.get('father_name', ''),
                'national_id': request.form.get('national_id', ''),
                'passport_number': '',
                'gender': '',
                'date_of_birth': request.form.get('date_of_birth', ''),
                'phone_number': request.form.get('phone_number', ''),
                'leader_name': '',
                'leader_phone': '',
                'arrival_date': request.form['arrival_date'],
                'departure_date': request.form['departure_date'],
                'occupation': request.form.get('occupation', ''),
                'residence_unit': request.form.get('residence_unit', ''),
                'room_id': request.form.get('room_id'),
                'payment_type': request.form.get('payment_type', ''),
                'advance_payment': to_number(request.form.get('advance_payment')),
                'balance': to_number(request.form.get('balance')),
                'total_amount': to_number(request.form.get('total_amount')),
                'note': request.form.get('note', ''),
                'is_companion': 0,
                'primary_guest_id': None
            }

        # Create main guest
        guest_id = Guest.create(guest_data)

        # Handle companions
        companion_count = int(request.form.get('companion_count', 0) or 0)
        for i in range(1, companion_count + 1):
            companion_name = request.form.get(f'companion-name-{i}', '')
            companion_last_name = request.form.get(f'companion-lastname-{i}', '')
            companion_relation = request.form.get(f'companion-rel-{i}', '')
            companion_national_id = request.form.get(f'companion-national-id-{i}', '')
            companion_gender = request.form.get(f'companion-gender-{i}', '')

            if companion_name and companion_last_name:  # Only add if name provided
                companion_data = {
                    'is_foreign': guest_data['is_foreign'],
                    'nationality': guest_data['nationality'],
                    'name': companion_name,
                    'last_name': companion_last_name,
                    'father_name': '',
                    'national_id': companion_national_id if not is_foreign else '',
                    'passport_number': companion_national_id if is_foreign else '',
                    'gender': companion_gender,
                    'date_of_birth': '',
                    'phone_number': '',
                    'leader_name': '',
                    'leader_phone': '',
                    'arrival_date': guest_data['arrival_date'],
                    'departure_date': guest_data['departure_date'],
                    'occupation': '',
                    'room_id': guest_data['room_id'],
                    'payment_type': '',
                    'advance_payment': 0,
                    'balance': 0,
                    'total_amount': 0,
                    'note': (
                        f"↑↑↑ {companion_relation} - {guest_data['name']} "
                        f"{guest_data['last_name']} با شناسه : "
                        f"{guest_data['national_id']} {guest_data['passport_number']}"
                    ),
                    'is_companion': 1,
                    'primary_guest_id': guest_id
                }
                Guest.create(companion_data)

        # Update room availability if room assigned
        if guest_data.get('room_id'):
            Room.update_availability(guest_data['room_id'], 0)

        flash('مسافر با موفقیت ثبت شد', 'success')
        return render_template(
            'result.html',
            name=guest_data['name'],
            lname=guest_data['last_name'],
        )

    except ValueError as e:
        flash(f'خطا در اعتبارسنجی: {str(e)}', 'error')
        return redirect(url_for('main.fill_form'))
    except Exception as e:
        flash(f'خطا در ثبت مسافر: {str(e)}', 'error')
        return redirect(url_for('main.fill_form'))

@main.route('/list')
def get_guests():
    """Display all guests."""
    search = request.args.get('search', '')
    if search:
        guests = Guest.search(search)
    else:
        guests = Guest.get_all()
    return render_template('list.html', guests=guests, search=search)

@main.route('/guest/<int:guest_id>')
def view_guest(guest_id):
    """View guest details with companions."""
    guest_data = Guest.get_by_id(guest_id)
    if not guest_data:
        flash('مسافر یافت نشد', 'error')
        return redirect(url_for('main.get_guests'))
    return render_template('guest_detail.html', data=guest_data)

@main.route('/guest/<int:guest_id>/edit', methods=['GET', 'POST'])
def edit_guest(guest_id):
    """Edit guest information."""
    if request.method == 'GET':
        guest_data = Guest.get_by_id(guest_id)
        if not guest_data:
            flash('مسافر یافت نشد', 'error')
            return redirect(url_for('main.get_guests'))
        rooms = Room.get_available()
        return render_template('edit_guest.html', data=guest_data, rooms=rooms)

    # POST - update guest
    try:
        guest_data = {
            'is_foreign': request.form.get('is_foreign', 'ایرانی'),
            'nationality': request.form.get('nationality', ''),
            'name': request.form['name'],
            'last_name': request.form['last_name'],
            'father_name': request.form.get('father_name', ''),
            'national_id': request.form.get('national_id', ''),
            'passport_number': request.form.get('passport_number', ''),
            'gender': request.form.get('gender', ''),
            'date_of_birth': request.form.get('date_of_birth', ''),
            'phone_number': request.form.get('phone_number', ''),
            'leader_name': request.form.get('leader_name', ''),
            'leader_phone': request.form.get('leader_phone', ''),
            'arrival_date': request.form['arrival_date'],
            'departure_date': request.form['departure_date'],
            'occupation': request.form.get('occupation', ''),
            'room_id': request.form.get('room_id'),
            'payment_type': request.form.get('payment_type', ''),
            'advance_payment': to_number(request.form.get('advance_payment')),
            'balance': to_number(request.form.get('balance')),
            'total_amount': to_number(request.form.get('total_amount')),
            'note': request.form.get('note', '')
        }

        Guest.update(guest_id, guest_data)
        flash('اطلاعات مسافر با موفقیت به‌روزرسانی شد', 'success')
        return redirect(url_for('main.view_guest', guest_id=guest_id))

    except Exception as e:
        flash(f'خطا در به‌روزرسانی: {str(e)}', 'error')
        return redirect(url_for('main.edit_guest', guest_id=guest_id))

@main.route('/guest/<int:guest_id>/delete', methods=['POST'])
def delete_guest(guest_id):
    """Delete guest."""
    try:
        Guest.delete(guest_id)
        flash('مسافر با موفقیت حذف شد', 'success')
    except Exception as e:
        flash(f'خطا در حذف: {str(e)}', 'error')
    return redirect(url_for('main.get_guests'))
