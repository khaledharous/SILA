import qrcode
import csv
from PIL import Image

with open('students.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0  

    for row in reader:
        first_name = row['first_name'].strip()
        last_name = row['last_name'].strip()
        reg_number = row['reg_number'].strip()
        
        if not first_name or not last_name or not reg_number:
            print("⚠️ Missing row of data:", row)
            continue
        
        qr_data = f"First name: {first_name}\nLast name: {last_name}\nRegistration number: {reg_number}"
        qr = qrcode.make(qr_data)
        file_name = f"{reg_number}.png"
        qr.save(file_name)

        print(f"✅ QR code generated: {first_name} {last_name} → {file_name}")
        count += 1

print(f"\n🧾 Total QR codes generated: {count}")



 



