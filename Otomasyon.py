import mysql.connector
from datetime import datetime, timedelta

#** MYSQL VERİ TABANI BAĞLANTISI
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin123",
    database="Kütüphane"
)

#** ÖĞRENCİ EKLEME FONKSİYONU
def add_student():
    name = input("İsim: ")
    surname = input("Soyisim: ")
    date_of_birth = input("Doğum Tarihi (YYYY-MM-DD): ")
    email = input("E-posta: ")

    cursor = connection.cursor()
    query = "INSERT INTO students (name, surname, date_of_birth, email) VALUES (%s, %s, %s, %s)"
    values = (name, surname, date_of_birth, email)

    try:
        cursor.execute(query, values)
        connection.commit()
        print("Öğrenci başarıyla eklendi.")

    except mysql.connector.Error as error:
        print("Hata:", error)

#** RENT_ALLOWED DEĞERİNİ KONTROL ETME FONKSİYONU
def check_rent_allowed(student_id):
    cursor = connection.cursor()
    query = "SELECT rent_allowed FROM students WHERE student_id = %s"
    values = (student_id,)

    try:
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result is not None:
            rent_allowed = result[0]
            return rent_allowed == 1

    except mysql.connector.Error as error:
        print("Hata:", error)

    finally:
        cursor.close()

    return False

#!! Yazım aşamasında karmaşıklığı önlemek için fonksiyonları aşamalara böldüm
#*** KİTAP KİRALAMA EYLEMİNDE VERİ TABANI İŞLEMLERİ FONKSİYONU
def rent_book(student_id, book_id):
    if check_rent_allowed(student_id):
        cursor = connection.cursor()
        query = "INSERT INTO student_rented_books (student_id, book_id) VALUES (%s, %s)"
        values = (student_id, book_id)

        try:
            cursor.execute(query, values)
            connection.commit()

            update_query = "UPDATE students SET rent_allowed = 0 WHERE student_id = %s"
            update_values = (student_id,)
            cursor.execute(update_query, update_values)
            connection.commit()

            print("Kitap kiralandı.")

        except mysql.connector.Error as error:
            print("Hata:", error)

        finally:
            cursor.close()
    else:
        print("Kitap kiralama işlemine izin verilmiyor. Öğrenci kiralama limitine ulaşmış olabilir.")

#** KİTAP KİRALAMA FONKSİYONU
def rent_book_from_user():
    student_id = input("Öğrenci ID'sini girin: ")
    book_id = input("Kitap ID'sini girin: ")

    if check_rent_allowed(student_id):
        rent_book(student_id, book_id)
    else:
        print("Kitap kiralama işlemine izin verilmiyor. Öğrenci kiralama limitine ulaşmış olabilir.")

#** ÖĞRENCİDEN BİLGİLERİ ALARAK KİTAP KİRALAMA FONKSİYONU
def rent_book_from_user():
    student_id = input("Öğrenci ID'sini girin: ")
    book_id = input("Kitap ID'sini girin: ")

    rent_book(student_id, book_id)

#** KİTAP İADE FONKSİYONU
def return_book(student_id, book_id):
    cursor = connection.cursor()
    query = "UPDATE student_rented_books SET actual_return_date = CURDATE() WHERE student_id = %s AND book_id = %s"
    values = (student_id, book_id)
    cursor.execute(query, values)
    connection.commit()
    print("Kitap iade edildi.")
    
    # rent_allowed Değerini 1 Olarak Güncelle
    update_query = "UPDATE students SET rent_allowed = 1 WHERE student_id = %s"
    update_values = (student_id,)
    cursor.execute(update_query, update_values)
    connection.commit()
    print("Rent allowed değeri güncellendi.")

#** ÖĞRENCİDEN BİLGİLERİ ALARAK KİTAP İADE ETME FONKSİYONU
def return_book_from_user():
    student_id = input("Öğrenci ID'si: ")
    book_id = input("İade edilecek kitap ID'si: ")
    return_book(student_id, book_id)

#** KİTAP EKLEME FONKSİYONU
def add_book(name, author, publish_date):
    cursor = connection.cursor()
    query = "INSERT INTO books (name, author, publish_date) VALUES (%s, %s, %s)"
    values = (name, author, publish_date)
    cursor.execute(query, values)
    connection.commit()
    print("Kitap başarıyla eklendi.")

#** ÖĞRENCİDEN BİLGİLERİ ALARAK KİTAP EKLEME FONKSİYONU
def add_book_from_user():
    name = input("Kitap adını girin: ")
    author = input("Yazarını girin: ")
    publish_date = input("Yayınlanma tarihini girin (YYYY-AA-GG): ")
    add_book(name, author, publish_date)

#** KİTAP LİSTESİ FONKSİYONU
def list_books():
    cursor = connection.cursor()
    query = "SELECT * FROM books"
    cursor.execute(query)
    books = cursor.fetchall()
    for book in books:
        book_id = book[0]
        name = book[1]
        author = book[2]
        publish_date = book[3]
        print(f"ID: {book_id}, Kitap İsmi: {name}, Yazar: {author}, Yayınlanma Tarihi: {publish_date}")

#** ÖĞRENCİ LİSTESİ FONKSİYONU
def list_students():
    cursor = connection.cursor()
    query = "SELECT * FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    if len(students) == 0:
        print("Öğrenci listesi boş.")
    else:
        for student in students:
            student_id = student[0]
            name = student[1]
            surname = student[2]
            date_of_birth = student[3]
            email = student[4]
            rent_allowed = student[5]
            print(f"ID: {student_id}, İsim: {name}, Soyisim: {surname}, Doğum Tarihi: {date_of_birth}, E-posta: {email}, Kitap Hakkı: {rent_allowed}")

#** ANA MENÜ
def show_menu():
    print("----------------------------- Kütüphane Menüsü -----------------------------")
    print("Yapmak istediğiniz işlemi seçiniz:\n")
    print("0) Öğrenci listesi\n")
    print("1) Öğrenci kayıt\n")
    print("2) Kitap listesini görüntüleyin\n")
    print("3) Kitap kiralayın\n")
    print("4) Kitap iade edin\n")
    print("5) Kitap bağışı\n")
    print("6) Çıkış\n")

#** SEÇİM
def handle_choice(choice):
    if choice == "0":
        list_students()
    if choice == "1":
        add_student()
    elif choice == "2":
        list_books()
    elif choice == "3":
        rent_book_from_user()
    elif choice == "4":
        return_book_from_user()
    elif choice == "5":
        add_book_from_user()
    elif choice == "6":
        exit()

#** ANA DÖNGÜ
while True:
    show_menu()
    choice = input("seçiminiz: ")
    handle_choice(choice)