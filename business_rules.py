"""Pricing rules for Harvest Table Catering."""

SERVICE_FEE = 75.00
FEE_THRESHOLD = 500.00
SIGNOFF_THRESHOLD = 2500.00
CHEF_GUEST_LIMIT = 80
CHEF_TOTAL_THRESHOLD = 3000.00


def food_cost(price_per_guest: float, guests: int) -> float:
    """Rule 1: price per guest times number of guests."""
    return price_per_guest * guests


def service_fee(discounted_total: float) -> float:
    """Rule 2: $75 fee when the discounted cost is $500 or less."""
    return SERVICE_FEE if discounted_total <= FEE_THRESHOLD else 0.00


def event_total(price_per_guest: float, guests: int, is_nonprofit: bool) -> float:
    discounted = discounted_cost(price_per_guest, guests, is_nonprofit)
    return round(discounted + service_fee(discounted), 2)


def needs_manager_signoff(total: float) -> bool:
    """Rule 5: strictly more than $2,500."""
    return total > SIGNOFF_THRESHOLD


def needs_second_chef(guests: int, total: float) -> bool:
    """Rule 6: more than 80 guests OR total of $3,000 or more."""
    return guests > CHEF_GUEST_LIMIT or total >= CHEF_TOTAL_THRESHOLD
