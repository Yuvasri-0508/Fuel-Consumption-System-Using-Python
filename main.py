import csv
from fuel_analysis import calculate_mileage, calculate_cost, efficiency_category

vehicles = []
trips = []

vehicle_numbers = set()
EFFICIENCY_LEVELS = ("Excellent", "Good", "Low")


# ---------------- LOAD DATA ----------------

def load_data():

    try:
        with open("vehicles.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                vehicles.append(row)
                vehicle_numbers.add(row["number"])

    except FileNotFoundError:
        pass

    try:
        with open("trips.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:

                row["previous_odometer"] = float(
                    row["previous_odometer"]
                )

                row["current_odometer"] = float(
                    row["current_odometer"]
                )

                row["distance"] = float(row["distance"])
                row["fuel"] = float(row["fuel"])
                row["price"] = float(row["price"])
                row["mileage"] = float(row["mileage"])
                row["cost"] = float(row["cost"])

                trips.append(row)

    except FileNotFoundError:
        pass


# ---------------- SAVE VEHICLE ----------------

def save_vehicle(vehicle):

    file_exists = False

    try:
        with open("vehicles.csv", "r"):
            file_exists = True

    except FileNotFoundError:
        pass

    with open("vehicles.csv", "a", newline="") as file:

        fields = ["number", "name"]

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(vehicle)


# ---------------- SAVE TRIP ----------------

def save_trip(trip):

    file_exists = False

    try:
        with open("trips.csv", "r"):
            file_exists = True

    except FileNotFoundError:
        pass

    with open("trips.csv", "a", newline="") as file:

        fields = [

            "number",
            "date",
            "previous_odometer",
            "current_odometer",
            "distance",
            "fuel",
            "price",
            "mileage",
            "cost"

        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(trip)


# ---------------- ADD VEHICLE ----------------

def add_vehicle():

    number = input(
        "Enter vehicle number: "
    ).upper().strip()

    name = input(
        "Enter vehicle name: "
    ).strip()

    if number == "" or name == "":

        print(
            "Vehicle details cannot be empty!"
        )

        return

    if number in vehicle_numbers:

        print(
            "Vehicle already exists!"
        )

        return

    vehicle = {

        "number": number,
        "name": name

    }

    vehicles.append(vehicle)

    vehicle_numbers.add(number)

    save_vehicle(vehicle)

    print(
        "Vehicle added successfully!"
    )


# ---------------- ADD TRIP ----------------

def add_trip():

    number = input(
        "Enter vehicle number: "
    ).upper().strip()

    if number not in vehicle_numbers:

        print(
            "Vehicle not registered!"
        )

        return

    date = input(
        "Enter date (DD-MM-YYYY): "
    ).strip()

    if date == "":

        print(
            "Date cannot be empty!"
        )

        return

    try:

        previous_odometer = float(
            input(
                "Enter previous odometer reading (km): "
            )
        )

        current_odometer = float(
            input(
                "Enter current odometer reading (km): "
            )
        )

        fuel = float(
            input(
                "Enter fuel used (litres): "
            )
        )

        price = float(
            input(
                "Enter fuel price per litre: "
            )
        )

    except ValueError:

        print(
            "Please enter valid numbers!"
        )

        return

    if current_odometer <= previous_odometer:

        print(
            "Current odometer must be greater than previous odometer!"
        )

        return

    if fuel <= 0 or price <= 0:

        print(
            "Fuel and price must be greater than zero!"
        )

        return


    # Calculate distance using odometer readings

    distance = (
        current_odometer
        - previous_odometer
    )


    # Calculate mileage

    mileage = calculate_mileage(
        distance,
        fuel
    )


    # Calculate fuel cost

    cost = calculate_cost(
        fuel,
        price
    )


    # Create trip dictionary

    trip = {

        "number": number,

        "date": date,

        "previous_odometer":
        previous_odometer,

        "current_odometer":
        current_odometer,

        "distance":
        distance,

        "fuel":
        fuel,

        "price":
        price,

        "mileage":
        mileage,

        "cost":
        cost

    }


    # Add trip to list

    trips.append(trip)


    # Save trip to CSV

    save_trip(trip)


    print(
        "\nTrip added successfully!"
    )

    print(
        "Distance travelled:",
        round(distance, 2),
        "km"
    )

    print(
        "Mileage:",
        round(mileage, 2),
        "km/litre"
    )

    print(
        "Fuel Cost: Rs.",
        round(cost, 2)
    )


    # Abnormal consumption check

    if mileage < 10:

        print(
            "WARNING: Abnormally high fuel consumption!"
        )

    else:

        print(
            "Fuel consumption is normal."
        )


# ---------------- VIEW TRIPS ----------------

def view_trips():

    if len(trips) == 0:

        print(
            "No trip records available."
        )

    else:

        print(
            "\n----- TRIP RECORDS -----"
        )

        for i, trip in enumerate(
            trips,
            start=1
        ):

            print(
                "\nTrip",
                i
            )

            print(
                "Vehicle:",
                trip["number"]
            )

            print(
                "Date:",
                trip["date"]
            )

            print(
                "Previous Odometer:",
                trip["previous_odometer"],
                "km"
            )

            print(
                "Current Odometer:",
                trip["current_odometer"],
                "km"
            )

            print(
                "Distance:",
                trip["distance"],
                "km"
            )

            print(
                "Fuel:",
                trip["fuel"],
                "litres"
            )

            print(
                "Mileage:",
                round(
                    trip["mileage"],
                    2
                ),
                "km/litre"
            )

            print(
                "Cost: Rs.",
                round(
                    trip["cost"],
                    2
                )
            )


# ---------------- MOST EFFICIENT ----------------

def most_efficient_vehicle():

    if len(trips) == 0:

        print(
            "No trip records available."
        )

        return

    best_trip = max(

        trips,

        key=lambda trip:
        trip["mileage"]

    )

    print(
        "\n----- MOST EFFICIENT VEHICLE -----"
    )

    print(
        "Vehicle Number:",
        best_trip["number"]
    )

    print(
        "Mileage:",
        round(
            best_trip["mileage"],
            2
        ),
        "km/litre"
    )

    print(
        "Category:",
        efficiency_category(
            best_trip["mileage"]
        )
    )


# ---------------- LEAST EFFICIENT ----------------

def least_efficient_vehicle():

    if len(trips) == 0:

        print(
            "No trip records available."
        )

        return

    worst_trip = min(

        trips,

        key=lambda trip:
        trip["mileage"]

    )

    print(
        "\n----- LEAST EFFICIENT VEHICLE -----"
    )

    print(
        "Vehicle Number:",
        worst_trip["number"]
    )

    print(
        "Mileage:",
        round(
            worst_trip["mileage"],
            2
        ),
        "km/litre"
    )

    print(
        "Category:",
        efficiency_category(
            worst_trip["mileage"]
        )
    )


# ---------------- GENERATE REPORT ----------------

def generate_report():

    if len(trips) == 0:

        print(
            "No trip records available."
        )

        return


    best_trip = max(

        trips,

        key=lambda trip:
        trip["mileage"]

    )


    worst_trip = min(

        trips,

        key=lambda trip:
        trip["mileage"]

    )


    with open(
        "report.txt",
        "w"
    ) as file:


        file.write(
            "FUEL CONSUMPTION ANALYSIS REPORT\n"
        )

        file.write(
            "=" * 40 + "\n\n"
        )


        file.write(
            "TOTAL TRIPS: "
            + str(len(trips))
            + "\n\n"
        )


        file.write(
            "MOST EFFICIENT VEHICLE\n"
        )

        file.write(
            "Vehicle Number: "
            + best_trip["number"]
            + "\n"
        )

        file.write(
            "Mileage: "
            + str(
                round(
                    best_trip["mileage"],
                    2
                )
            )
            + " km/litre\n\n"
        )


        file.write(
            "LEAST EFFICIENT VEHICLE\n"
        )

        file.write(
            "Vehicle Number: "
            + worst_trip["number"]
            + "\n"
        )

        file.write(
            "Mileage: "
            + str(
                round(
                    worst_trip["mileage"],
                    2
                )
            )
            + " km/litre\n\n"
        )


        file.write(
            "ABNORMAL CONSUMPTION TRIPS\n"
        )


        abnormal_found = False


        for trip in trips:

            if trip["mileage"] < 10:

                file.write(

                    "Vehicle "
                    + trip["number"]

                    + " | Date: "

                    + trip["date"]

                    + " | Mileage: "

                    + str(
                        round(
                            trip["mileage"],
                            2
                        )
                    )

                    + " km/litre\n"

                )

                abnormal_found = True


        if not abnormal_found:

            file.write(
                "No abnormal trips found.\n"
            )


    print(
        "\nReport generated successfully!"
    )

    print(
        "Check the report.txt file."
    )


# ---------------- MENU ----------------
def monthly_fuel_consumption():

    if len(trips) == 0:
        print("No trip records available.")
        return

    monthly_data = {}

    for trip in trips:

        date = trip["date"]

        # Date format: DD-MM-YYYY
        month_year = date[3:]

        if month_year not in monthly_data:

            monthly_data[month_year] = {
                "total_fuel": 0,
                "total_distance": 0,
                "trip_count": 0
            }

        monthly_data[month_year]["total_fuel"] += trip["fuel"]

        monthly_data[month_year]["total_distance"] += trip["distance"]

        monthly_data[month_year]["trip_count"] += 1


    print("\n----- MONTHLY FUEL CONSUMPTION -----")

    for month, data in monthly_data.items():

        average_fuel = (
            data["total_fuel"]
            / data["trip_count"]
        )

        print("\nMonth:", month)

        print(
            "Total Trips:",
            data["trip_count"]
        )

        print(
            "Total Distance:",
            round(
                data["total_distance"],
                2
            ),
            "km"
        )

        print(
            "Total Fuel Used:",
            round(
                data["total_fuel"],
                2
            ),
            "litres"
        )

        print(
            "Average Fuel Consumption:",
            round(
                average_fuel,
                2
            ),
            "litres per trip"
        )
def show_menu():

    while True:

        print(
            "\n----- FUEL CONSUMPTION ANALYSIS SYSTEM -----"
        )

        print(
            "1. Add Vehicle"
        )

        print(
            "2. Add Trip"
        )

        print(
            "3. View Trips"
        )

        print(
            "4. Most Efficient Vehicle"
        )

        print(
            "5. Least Efficient Vehicle"
        )

        print(
            "6. Generate Final Report"
        )

        print(
            "7. Exit"
        )


        choice = input(
            "Enter your choice: "
        )


        if choice == "1":

            add_vehicle()


        elif choice == "2":

            add_trip()


        elif choice == "3":

            view_trips()


        elif choice == "4":

            most_efficient_vehicle()


        elif choice == "5":

            least_efficient_vehicle()


        elif choice == "6":

            generate_report()


        elif choice == "7":
            monthly_fuel_consumption()

        elif choice == "8":
            print("Thank you!")
            break


        else:

            print(
                "Invalid choice!"
            )


# ---------------- START PROGRAM ----------------

load_data()

show_menu()