# main.py

import dockingBays as db

# Function to print docking bays information
def print_docking_bays():
    print("Docking Bays:")
    for bay in db.docking_bays:
        print(f"Bay {bay['bay_id']} - Size: {bay['size']}, Schedule: {bay['schedule']}")

# Function to print incoming ships information
def print_incoming_ships():
    print("\nIncoming Ships:")
    for ship in db.incoming_ships:
        print(f"Ship {ship['ship_name']} - Size: {ship['size']}, Arrival: {ship['arrival_time']}, Departure: {ship['departure_time']}")

def get_bay_times(index: int):
    times = []
    for ship in db.docking_bays[index]['schedule']:
        times.append((int(ship[0][0:2]), int(ship[1][0:2])))
    return times

def get_incoming_ship_times(name: str):
    for ship in db.incoming_ships:
        if ship['ship_name'].lower() == name.lower():
            return [int(ship['arrival_time'][0:2]), int(ship['departure_time'][0:2])]
    return ""

def compare_times(bay_times: list, ship_times: list):
    if len(bay_times) == 0:
        return True
    for times in bay_times:
        if times[0] == ship_times[0] or ship_times[0] < times[0] and ship_times[1] > times[0]:
            return False
    return True

def check_repeats(schedule: list, ship_check: list):
    for bay in schedule:
        for ship in bay['ships']:
            if ship[2] == ship_check[2]:
                return False
    return True

def create_schedule():
    schedule = []
    for bay in db.docking_bays:
        schedule.append({'bay': f'Bay {bay['bay_id']}', 'ships': bay['schedule']})
    return schedule

def sort_times(bay_times: list, ship_times: list):
    index = 0
    for i in range(0, len(bay_times)):
            if bay_times[i][1] <= ship_times[0]:
                index = i+1
    return index
        
def available_bays(schedule: list):
    for i in range(0, len(db.docking_bays)):
        for ship in db.incoming_ships:
            bay_times = get_bay_times(db.docking_bays[i]['bay_id']-1)
            ship_times = get_incoming_ship_times(ship['ship_name'])
            if not compare_times(bay_times, ship_times):
                continue
            if not check_repeats(schedule, (ship['arrival_time'], ship['departure_time'], ship['ship_name'])):
                continue
            if db.docking_bays[i]['size'] == ship['size']:
                schedule[i]['ships'].insert(sort_times(bay_times, ship_times), (ship['arrival_time'], ship['departure_time'], ship['ship_name']))
    return schedule

# Main function
def main():
    print_docking_bays()
    print_incoming_ships()
    
    # TODO: Implement the docking scheduler logic here
    schedule = create_schedule()
    schedule = available_bays(schedule)
    bays = []
    for i in schedule:
        statement = f"{i['bay']}\n"
        for j in i['ships']:
            statement += f"{j[2]} - {j[0]} to {j[1]}\n"
        bays.append(statement)
    for bay in bays:
        print(bay)
    
    # Levels 1 to 4 and the bonus can be implemented below
    

if __name__ == "__main__":
    main()
