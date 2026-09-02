def calculate_mileage(distance, fuel):
    if fuel > 0:
        return distance / fuel
    return 0


def calculate_cost(fuel, price):
    return fuel * price


def efficiency_category(mileage):
    if mileage >= 20:
        return "Excellent"
    elif mileage >= 15:
        return "Good"
    else:
        return "Low"