"""Business rules for Harvest Table Catering"""

MEDIUM_EVENT_GUESTS = 25
LARGE_EVENT_GUESTS = 100
NO_DISCOUNT = 0.0
STANDARD_DISCOUNT = 0.05
NONPROFIT_DISCOUNT = 0.12
SERVICE_FEE = 75.0
SERVICE_FEE_LIMIT = 500.0
SIGNOFF_LIMIT = 2500.0
SECOND_CHEF_GUESTS = 80
SECOND_CHEF_TOTAL = 3000.0


def calculate_food_cost(guest_price: float, guests: int) -> float:
    """Return the food cost before any discount."""
    return guest_price * guests


def get_event_discount(guests: int, nonprofit: bool = False) -> float:
    """Return the discount rate as a decimal for the guest count."""
    if guests >= LARGE_EVENT_GUESTS and nonprofit:
        return NONPROFIT_DISCOUNT
    if guests >= MEDIUM_EVENT_GUESTS:
        return STANDARD_DISCOUNT
    return NO_DISCOUNT


def calculate_event_total(
    guest_price: float, guests: int, nonprofit: bool = False
) -> float:
    """Return the discounted food cost plus the service fee when it applies."""
    food_cost = calculate_food_cost(guest_price, guests)
    discount = get_event_discount(guests, nonprofit)
    discounted = food_cost * (1 - discount)
    if discounted <= SERVICE_FEE_LIMIT:
        return discounted + SERVICE_FEE
    return discounted


def needs_signoff(total: float) -> bool:
    """Return True when the event total needs a manager's sign-off."""
    return total > SIGNOFF_LIMIT


def needs_second_chef(guests: int, total: float) -> bool:
    """Return True when the event needs a second chef."""
    return guests > SECOND_CHEF_GUESTS or total >= SECOND_CHEF_TOTAL


def total_booked(events: list) -> float:
    """Return the sum of the event totals for every event in the list."""
    booked = 0.0
    for event in events:
        booked += calculate_event_total(
            event["guest_price"], event["guests"], event.get("nonprofit", False)
        )
    return booked


def largest_event(events: list) -> str:
    """Return the client with the largest event total, first one on a tie."""
    best_client = ""
    best_total = 0.0
    found_any = False
    for event in events:
        total = calculate_event_total(
            event["guest_price"], event["guests"], event.get("nonprofit", False)
        )
        if not found_any or total > best_total:
            best_client = event["client"]
            best_total = total
            found_any = True
    return best_client


def format_event_line(
    client: str, total: float, signoff: bool, second_chef: bool
) -> str:
    """Return one report line for an event."""
    signoff_text = "yes" if signoff else "no"
    chef_text = "yes" if second_chef else "no"
    return (
        f"{client}: ${total:.2f} | sign-off: {signoff_text} | second chef: {chef_text}"
    )
