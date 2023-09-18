import sqlite3
conn = sqlite3.connect('hotel.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE guests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        is_foreign TEXT,              -- مسافر داخلی یا خارجی
        relation,                     -- رابطه
        nationality TEXT,             -- ملیت
        name TEXT,                    -- نام
        last_name TEXT,               -- نام خانوادگی
        father_name TEXT,             -- نام پدر
        national_id TEXT,             -- کد ملی (فقط برای مسافران داخلی)
        passport_number TEXT,         -- شماره گذرنامه (فقط برای مسافران خارجی)
        gender TEXT,                  -- جنسیت
        date_of_birth TEXT,           -- تاریخ تولد
        phone_number TEXT,            -- تلفن همراه یا ثابت
        arrival_date TEXT,            -- تاریخ ورود
        departure_date TEXT,          -- تاریخ خروج
        residence_unit TEXT,          -- نام واحد اقامتی        
        leader_name TEXT,             -- نام لیدر
        leader_phone TEXT,            -- تلفن لیدر
        occupation TEXT,              -- شغل
        payment_type TEXT,            -- نوع پرداخت
        advance_payment REAL,         -- پیش پرداخت
        balance REAL,                 -- مانده
        total_amount REAL,            -- مبلغ کل
        note TEXT                     -- ملاحظات
    );
''')

conn.commit()
print ("Table created successfully")
conn.close()

