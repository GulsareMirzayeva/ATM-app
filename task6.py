import sqlite3

conn = sqlite3.connect('atm.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS atm (
        pin INT,
        balance REAL
    )
''')

cursor.execute("INSERT INTO atm (pin, balance) VALUES ('1234', 1000.00)")
conn.commit()


while True:
    print("1. Balansı yoxla")
    print("2. Kartdan Pul Çıxar")
    print("3. Karta Mədaxil et")
    print("4. Pin dəyiş")
    print("5. Çıxış")

    choice = input("GULSARE, Zəhmət olmasa əmri seçin: ")

    if choice == '1':
        pin = input("PIN-i daxil edin: ")
        cursor.execute("SELECT balance FROM atm WHERE pin = ?", (pin,))
        result = cursor.fetchone()
        if result:
            print(f"Balansınız: {result[0]} AZN")
        else:
            print("PIN yanlışdır. Yenidən cəhd edin.")
    
    elif choice == '2':
        pin = input("PIN-i daxil edin: ")
        amount = float(input("Çıxarılacaq məbləği daxil edin: "))
        cursor.execute("SELECT balance FROM atm WHERE pin = ?", (pin,))
        result = cursor.fetchone()
        if result:
            balance = result[0]
            if balance >= amount:
                new_balance = balance - amount
                cursor.execute("UPDATE atm SET balance = ? WHERE pin = ?", (new_balance, pin))
                conn.commit()
                print(f"{amount} AZN uğurla çıxarıldı. Yeni balans: {new_balance} AZN")
            else:
                print("Balansınız kifayət qədər deyil.")
        else:
            print("PIN yanlışdır. Yenidən cəhd edin.")

    elif choice == '3':
        pin = input("PIN-i daxil edin: ")
        amount = float(input("Məbləği daxil edin: "))
        cursor.execute("SELECT balance FROM atm WHERE pin = ?", (pin,))
        result = cursor.fetchone()
        if result:
            balance = result[0]
            new_balance = balance + amount
            cursor.execute("UPDATE atm SET balance = ? WHERE pin = ?", (new_balance, pin))
            conn.commit()
            print(f"{amount} AZN uğurla əlavə edildi. Yeni balans: {new_balance} AZN")
        else:
            print("PIN yanlışdır. Yenidən cəhd edin.")
    elif choice == '4':
        current_pin = input("Hazırkı PIN-i daxil edin: ")
        new_pin = input("Yeni PIN-i daxil edin: ")
        cursor.execute("SELECT * FROM atm WHERE pin = ?", (current_pin,))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE atm SET pin = ? WHERE pin = ?", (new_pin, current_pin))
            conn.commit()
            print("PIN uğurla dəyişdirildi.")
        else:
            print("Hazırkı PIN yanlışdır. Yenidən cəhd edin.")             

    elif choice == '5':
        print("Programdan çıxılır.")
        break

conn.close()
