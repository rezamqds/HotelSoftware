#fp app made by @rezamqds

from flask import Flask, request, render_template
import os, sqlite3 , webbrowser # , connection



# os.path.join(os.getcwd()
# static_directory = os.path.join(os.getcwd(), 'static')
# form_dir = os.path.join(static_directory, 'form.html')



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/test')
# def test():
#     return render_template('t.html',name = "reza")





@app.route('/data_entry')

def fill_form():
    return render_template('form.html')

    # if connection.is_internet_available():
    #     return render_template('form.html')
    # else:
    #     # importance to chnage dir in every pc if not using join map !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #     webbrowser.open("/home/xxx/Desktop/HotelSoftware/templates/form.html")
    #     return render_template('index.html')






@app.route('/add_guest', methods=['POST', 'GET'])
def add_guest():
    if request.method == 'POST':
        if request.form['is_foreign'] == "FALSE":
            form_data = {
                'is_foreign': 'FALSE',
                'nationality': '',
                'name': request.form['name'],
                'last_name': request.form['last_name'],
                'father_name': request.form['father_name'],
                'national_id': request.form['national_id'],
                'passport_number': '',
                'gender': '',
                'date_of_birth': request.form['date_of_birth'],
                'phone_number': request.form['phone_number'],
                'leader_name': '',
                'leader_phone': '',
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
        else:
            form_data = {
                'is_foreign': 'TRUE',
                'nationality': request.form['nationality'],
                'name': request.form['foreign_name'],
                'last_name': request.form['foreign_last_name'],
                'father_name': '',
                'national_id': '',
                'passport_number': request.form['passport_number'],
                'gender': request.form['gender'],
                'date_of_birth': request.form['f_date_of_birth'],
                'phone_number': request.form['f_phone_number'],
                'leader_name': request.form['leader_name'],
                'leader_phone': request.form['leader_phone'],
                'arrival_date': request.form['f_arrival_date'],
                'departure_date': request.form['f_departure_date'],
                'occupation': '',
                'residence_unit': request.form['f_residence_unit'],
                'payment_type': request.form['f_payment_type'],
                'advance_payment': request.form['f_advance_payment'],
                'balance': request.form['f_balance'],
                'total_amount': request.form['f_total_amount'],
                'note': request.form['f_note'],
                }

        # print(form_data)

        # Connect to the database
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()

        # Insert data into the "guests" table
        insert_query = """
        INSERT INTO guests (is_foreign, nationality, name, last_name, father_name, national_id, passport_number, gender, date_of_birth, phone_number, leader_name, leader_phone, arrival_date, departure_date, occupation, residence_unit, payment_type, advance_payment, balance, total_amount, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            form_data['is_foreign'], form_data['nationality'], form_data['name'], form_data['last_name'], form_data['father_name'],
            form_data['national_id'], form_data['passport_number'], form_data['gender'], form_data['date_of_birth'],
            form_data['phone_number'], form_data['leader_name'], form_data['leader_phone'], form_data['arrival_date'],
            form_data['departure_date'], form_data['occupation'], form_data['residence_unit'], form_data['payment_type'],
            form_data['advance_payment'], form_data['balance'], form_data['total_amount'], form_data['note']
        ))

        conn.commit()
        conn.close()

        # return "Guest added successfully!"

    # return render_template('add_guest.html')
    return render_template('result.html', name=form_data["name"] , lname=form_data["last_name"])


@app.route('/list', methods=['GET'])
def get_guests():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guests")
    guests = c.fetchall()
    return render_template('list.html', guests=guests)


if __name__ == '__main__':
    app.run(debug=True)