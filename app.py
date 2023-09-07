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

   # get data
    is_foreign = request.form['is_foreign']
    nationality = request.form['nationality']
    if nationality == "foreign":
        nationality = request.form['newNationality']
        # print (nationality,"its check point for testing 8888888888#@@!")
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    father_name = request.form['father_name']
    national_id = request.form['national_id']
    passport_number = request.form['passport_number']
    gender = request.form['gender']
    birth_date = request.form['birth_date']
    phone_number = request.form['phone_number']
    leader_name = request.form['leader_name']
    leader_phone = request.form['leader_phone']
    entry_date = request.form['entry_date']
    exit_date = request.form['exit_date']
    occupation = request.form['occupation']
    accommodation_unit = request.form['accommodation_unit']
    pay_type = request.form['pay_type']
    advance_payment = request.form['advance_payment']
    balance = request.form['balance']
    total_amount = request.form['total_amount']
    notes = request.form['notes']

    # save data on db
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("INSERT INTO guests (is_foreign, nationality, first_name, last_name, father_name, national_id, passport_number, gender, birth_date, phone_number, leader_name, leader_phone, entry_date, exit_date, occupation, accommodation_unit, pay_type, advance_payment, balance, total_amount, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (is_foreign, nationality, first_name, last_name, father_name, national_id, passport_number, gender, birth_date, phone_number, leader_name, leader_phone, entry_date, exit_date, occupation, accommodation_unit, deposit_type, advance_payment, balance, total_amount, notes))
    conn.commit()
    conn.close()

    return render_template('result.html', name=first_name , lname=last_name)





@app.route('/list', methods=['GET'])
def get_guests():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guests")
    guests = c.fetchall()
    return render_template('guests.html', guests=guests)



if __name__ == '__main__':
    app.run(debug=True)

