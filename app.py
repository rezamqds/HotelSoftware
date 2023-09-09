# import sqlite3
# conn = sqlite3.connect('hotel.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE IF NOT EXISTS guests
#                (first_name TEXT, last_name TEXT, national_id TEXT,
#                 phone_number TEXT, nationality TEXT, amount_paid REAL)''')
# conn.commit()
# conn.close()


from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/guest_fill_form')
def fill_form():
   return render_template('guestFillForm.html')



@app.route('/add_guest', methods=['POST'])
def add_guest():

    # دریافت اطلاعات از فرم
    form_data = {
        'is_foreign': request.form['is_foreign'],
        'nationality': request.form['nationality'],
        'name': request.form['name'],
        'last_name': request.form['last_name'],
        'father_name': request.form['father_name'],
        'national_id': request.form['national_id'],
        'passport_number': request.form['passport_number'],
        'gender': request.form['gender'],
        'date_of_birth': request.form['date_of_birth'],
        'phone_number': request.form['phone_number'],
        'leader_name': request.form['leader_name'],
        'leader_phone': request.form['leader_phone'],
        'arrival_date': request.form['arrival_date'],
        'departure_date': request.form['departure_date'],
        'occupation': request.form['occupation'],
        'residence_unit': request.form['residence_unit'],
        'payment_type': request.form['payment_type'],
        'advance_payment': request.form['advance_payment'],
        'balance': request.form['balance'],
        'total_amount': request.form['total_amount'],
        'note': request.form['note'],
    }

    # اتصال به پایگاه داده
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # دستور SQL برای افزودن رکورد به جدول "guests"
    insert_query = """
    INSERT INTO guests (is_foreign, nationality, name, last_name, father_name, national_id, passport_number, gender, date_of_birth, phone_number, leader_name, leader_phone, arrival_date, departure_date, occupation, residence_unit, payment_type, advance_payment, balance, total_amount, note)
    VALUES (:is_foreign, :nationality, :name, :last_name, :father_name, :national_id, :passport_number, :gender, :date_of_birth, :phone_number, :leader_name, :leader_phone, :arrival_date, :departure_date, :occupation, :residence_unit, :payment_type, :advance_payment, :balance, :total_amount, :note)
    """

    # اجرای دستور SQL با استفاده از دیکشنری داده‌ها
    cursor.execute(insert_query, form_data)

    # ذخیره تغییرات و بستن اتصال به پایگاه داده
    conn.commit()
    conn.close()


#    # get data
#     is_foreign = request.form['is_foreign'] # mandatory
#     nationality = request.form['nationality'] # show if foreign
#     name = request.form['name'] # show both
#     last_name = request.form['last_name'] # show both
#     father_name = request.form['father_name'] # just for internals
#     national_id = request.form['national_id'] # just for internals
#     passport_number = request.form['passport_number'] # just for foreign
#     gender = request.form['gender'] # just for foreign
#     date_of_birth = request.form['date_of_birth'] # show both
#     phone_number = request.form['phone_number'] # show both
#     leader_name = request.form['leader_name'] # just for foreign
#     leader_phone = request.form['leader_phone'] # just for foreign
#     arrival_date = request.form['arrival_date'] # show both
#     departure_date = request.form['departure_date'] # show both
#     occupation = request.form['occupation'] # show both
#     residence_unit = request.form['residence_unit'] # show both
#     payment_type = request.form['payment_type'] # show both
#     advance_payment = request.form['advance_payment'] # show both
#     balance = request.form['balance'] # show both
#     total_amount = request.form['total_amount'] # show both
#     note = request.form['note'] # show both

#     # # save data on db
#     # conn = sqlite3.connect('hotel.db')
#     # c = conn.cursor()
#     # c.execute("INSERT INTO guests (is_foreign, nationality, first_name, last_name, father_name, national_id, passport_number, gender, birth_date, phone_number, leader_name, leader_phone, entry_date, exit_date, occupation, residence_unit, payment_type, advance_payment, balance, total_amount, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (is_foreign, nationality, first_name, last_name, father_name, national_id, passport_number, gender, birth_date, phone_number, leader_name, leader_phone, entry_date, exit_date, occupation, residence_unit, deposit_type, advance_payment, balance, total_amount, notes))
#     # conn.commit()
#     # conn.close()


    
    return render_template('result.html', name=form_data["name"] , lname=form_data["last_name"])





@app.route('/list', methods=['GET'])
def get_guests():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guests")
    guests = c.fetchall()
    return render_template('guests.html', guests=guests)



if __name__ == '__main__':
    app.run(debug=True)

