import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='python',
        database='hotel_system'
    )

def get_booking_by_room(room_number):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
        SELECT b.booking_id, c.customer_name, r.room_number, b.check_in, b.check_out
        FROM booking b
        JOIN hotel_customers c ON b.customer_id = c.customer_id
        JOIN rooms r ON b.room_id = r.room_id
        WHERE r.room_number = %s
    """
    cursor.execute(query, (room_number,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

def delete_booking(booking_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "DELETE FROM booking WHERE booking_id = %s"
    cursor.execute(query, (booking_id,))
    conn.commit()

    cursor.close()
    conn.close()

# ---- Main Program ----
room_input = input("Enter Room Number: ")

booking = get_booking_by_room(room_input)

if booking:
    print("\n--- Booking Details ---")
    print(f"Booking ID : {booking[0]}")
    print(f"Customer   : {booking[1]}")
    print(f"Room No    : {booking[2]}")
    print(f"Check-In   : {booking[3]}")
    print(f"Check-Out  : {booking[4]}")
    
    checkout = input("\nDo you want to check out this room? (yes/no): ").lower()
    if checkout == 'yes':
        delete_booking(booking[0])
        print("✅ Guest checked out successfully.")
    else:
        print("ℹ️  Checkout canceled.")
else:
    print("❌ No booking found for that room.")
