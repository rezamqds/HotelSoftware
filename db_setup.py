import sqlite3
conn = sqlite3.connect('hotel.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE guests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        is_foreign BOOLEAN NOT NULL,  -- مسافر داخلی یا خارجی (TRUE یا FALSE)
        nationality TEXT,             -- ملیت
        first_name TEXT NOT NULL,     -- نام
        last_name TEXT NOT NULL,      -- نام خانوادگی
        father_name TEXT,             -- نام پدر
        national_id TEXT,             -- کد ملی (فقط برای مسافران داخلی)
        passport_number TEXT,         -- شماره گذرنامه (فقط برای مسافران خارجی)
        gender TEXT,                  -- جنسیت
        birth_date DATE,              -- تاریخ تولد
        phone_number TEXT NOT NULL,   -- تلفن همراه یا ثابت
        address TEXT                  -- ادرس
        entry_date DATE,              -- تاریخ ورود
        exit_date DATE,               -- تاریخ خروج
        accommodation_unit TEXT,      -- نام واحد اقامتی        
        leader_name TEXT,             -- نام لیدر
        leader_phone TEXT,            -- تلفن لیدر
        
        occupation TEXT,              -- شغل

        pay_type TEXT,                -- نوع پرداخت
        advance_payment REAL,         -- پیش پرداخت
        balance REAL,                 -- مانده
        total_amount REAL,            -- مبلغ کل
        notes TEXT                    -- ملاحظات
    );
''')

c.execute('''CREATE TABLE companions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_id INTEGER,           -- شناسه مسافر مرتبط
    first_name TEXT NOT NULL,   -- نام
    last_name TEXT NOT NULL,    -- نام خانوادگی
    national_id TEXT,           -- کد ملی
    relationship TEXT,          -- نسبت
    birth_date DATE,            -- تاریخ تولد
    gender TEXT                 -- جنسیت
); ''')

conn.commit()
print ("Table created successfully")
conn.close()

