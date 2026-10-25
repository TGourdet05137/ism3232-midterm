"""Print the Harvest Table Catering event report."""

from business_rules import (
    calculate_event_total,
    format_event_line,
    largest_event,
    needs_second_chef,
    needs_manager_signoff,
    total_booked,
)

events = [
    {"client": "Finch Law", "guest_price": 18.00, "guests": 20, "nonprofit": False},
    {"client": "Garden Club", "guest_price": 22.00, "guests": 40, "nonprofit": True},
    {"client": "Hilltop Gym", "guest_price": 30.00, "guests": 120, "nonprofit": False},
    {"client": "Island Pantry", "guest_price": 25.00, "guests": 150, "nonprofit": True},
    {"client": "Juniper Spa", "guest_price": 16.00, "guests": 30, "nonprofit": False},
    {"client": "Kettle Works", "guest_price": 20.00, "guests": 80, "nonprofit": False},
    {"client": "Lumen Labs", "guest_price": 15.00, "guests": 81, "nonprofit": False},
    {"client": "Marlow Gala", "guest_price": 70.00, "guests": 50, "nonprofit": True},
]


def main() -> None:
    """Print the report title, one line per event, and the summary."""
    print("Harvest Table Catering Event Report")

    event_count = 0
    signoff_count = 0
    second_chef_count = 0

    for event in events:
        total = calculate_event_total(
            event["guest_price"], event["guests"], event["nonprofit"]
        )
        signoff = needs_signoff(total)
        second_chef = needs_second_chef(event["guests"], total)

    print(format_event_line(event["client"], total, signoff, second_chef))

    event_count += 1
    if signoff:
        signoff_count += 1
    if second_chef:
        second_chef_count += 1

    booked = total_booked(events)
    average = booked / event_count


print(f"Events: {event_count}")
print(f"Total booked: ${booked:.2f}")
print(f"Average event total: ${average:.2f}")
print(f"Largest event total: {largest_event(events)}")
print(f"Sign-offs needed: {signoff_count}")
print(f"Second chefs needed: {second_chef_count}")


main()
