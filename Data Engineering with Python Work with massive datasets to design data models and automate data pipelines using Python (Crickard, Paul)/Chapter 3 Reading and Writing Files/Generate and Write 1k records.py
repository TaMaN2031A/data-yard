from faker import Faker
import csv


output = open('data.csv', 'w')
writer = csv.writer(output)

fake = Faker()
header = ['name', 'age', 'street', 'city', 'state', 'zip', 'lng', 'lat']
writer.writerow(header)

for _ in range(1000):
    writer.writerow([fake.name(), fake.random_int(min=7, max=120, step=1),
                     fake.street_address(), fake.city(), fake.zipcode(),
                     fake.longitude(), fake.latitude()])

output.close()