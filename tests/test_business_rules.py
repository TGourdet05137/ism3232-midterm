"""Tests for the Harvest Table Catering business rules."""

from business_rules import (
    calculate_event_total,
    calculate_food_cost,
    format_event_line,
    get_event_discount,
    largest_event,
    needs_second_chef,
    needs_signoff,
    total_booked,
)


def make_event(client, guest_price, guests, nonprofit=False):
    """Build one event dict for a test."""
    return {
        "client": client,
        "guest_price": guest_price,
        "guests": guests,
        "nonprofit": nonprofit,
    }


# calculate_food_cost (rule 1)


def test_food_cost_is_price_times_guests():
    assert round(calculate_food_cost(18.00, 20), 2) == 360.00


def test_food_cost_has_no_discount_applied():
    assert round(calculate_food_cost(30.00, 120), 2) == 3600.00


# get_event_discount (rules 2 and 3)


def test_discount_is_zero_at_24_guests():
    assert get_event_discount(24) == 0.0


def test_discount_is_five_percent_at_25_guests():
    assert get_event_discount(25) == 0.05


def test_discount_is_five_percent_at_99_guests_for_nonprofit():
    assert get_event_discount(99, nonprofit=True) == 0.05


def test_discount_is_twelve_percent_at_100_guests_for_nonprofit():
    assert get_event_discount(100, nonprofit=True) == 0.12


def test_discount_is_five_percent_at_100_guests_when_not_nonprofit():
    assert get_event_discount(100) == 0.05


def test_discount_is_zero_at_24_guests_even_for_nonprofit():
    assert get_event_discount(24, nonprofit=True) == 0.0


def test_nonprofit_flag_defaults_to_false():
    assert get_event_discount(150) == get_event_discount(150, nonprofit=False)


# calculate_event_total (rule 4)


def test_total_adds_fee_when_discounted_cost_is_exactly_500():
    assert round(calculate_event_total(50.00, 10), 2) == 575.00


def test_total_has_no_fee_when_discounted_cost_is_just_over_500():
    assert round(calculate_event_total(50.01, 10), 2) == 500.10


def test_total_adds_fee_to_small_event_with_no_discount():
    assert round(calculate_event_total(18.00, 20), 2) == 435.00


def test_total_applies_five_percent_discount_without_fee():
    assert round(calculate_event_total(22.00, 40), 2) == 836.00


def test_total_uses_discounted_cost_when_deciding_the_fee():
    # 25 guests x $22 = $550, but 5% off makes it $522.50, so no fee.
    assert round(calculate_event_total(22.00, 25), 2) == 522.50


def test_total_fee_applies_when_discount_pulls_cost_to_500_or_less():
    # 25 guests x $21 = $525, 5% off is $498.75, so the fee is added.
    assert round(calculate_event_total(21.00, 25), 2) == 573.75


def test_nonprofit_true_changes_the_total_for_a_100_guest_event():
    regular = calculate_event_total(30.00, 100, nonprofit=False)
    nonprofit = calculate_event_total(30.00, 100, nonprofit=True)
    assert round(regular, 2) == 2850.00
    assert round(nonprofit, 2) == 2640.00


# needs_signoff (rule 5)


def test_signoff_not_needed_at_exactly_2500():
    assert needs_signoff(2500.00) is False


def test_signoff_needed_just_over_2500():
    assert needs_signoff(2500.01) is True


# needs_second_chef (rule 6)


def test_no_second_chef_at_80_guests_when_total_is_low():
    assert needs_second_chef(80, 100.00) is False


def test_second_chef_needed_at_81_guests_when_total_is_low():
    assert needs_second_chef(81, 100.00) is True


def test_second_chef_needed_at_total_of_exactly_3000_with_few_guests():
    assert needs_second_chef(10, 3000.00) is True


def test_no_second_chef_just_under_3000_with_few_guests():
    assert needs_second_chef(10, 2999.99) is False


# total_booked


def test_total_booked_adds_every_event_total():
    events = [
        make_event("A", 18.00, 20),
        make_event("B", 22.00, 40),
        make_event("C", 30.00, 100, nonprofit=True),
    ]
    # 435.00 + 836.00 + 2640.00
    assert round(total_booked(events), 2) == 3911.00


def test_total_booked_of_one_event_is_that_events_total():
    events = [make_event("A", 18.00, 20)]
    assert round(total_booked(events), 2) == 435.00


def test_total_booked_of_empty_list_is_zero():
    assert total_booked([]) == 0.0


# largest_event


def test_largest_event_returns_client_with_biggest_total():
    events = [
        make_event("Small", 18.00, 20),
        make_event("Big", 30.00, 120),
        make_event("Medium", 22.00, 40),
    ]
    assert largest_event(events) == "Big"


def test_largest_event_can_be_the_last_in_the_list():
    events = [make_event("First", 18.00, 20), make_event("Last", 30.00, 120)]
    assert largest_event(events) == "Last"


def test_largest_event_tie_returns_the_one_listed_first():
    events = [
        make_event("Earlier", 20.00, 50),
        make_event("Later", 20.00, 50),
    ]
    assert largest_event(events) == "Earlier"


def test_largest_event_of_empty_list_is_empty_string():
    assert largest_event([]) == ""


# format_event_line


def test_format_line_shows_no_for_false_values():
    line = format_event_line("Finch Law", 435.0, False, False)
    assert line == "Finch Law: $435.00 | sign-off: no | second chef: no"


def test_format_line_shows_yes_for_true_values():
    line = format_event_line("Hilltop Gym", 3420.0, True, True)
    assert line == "Hilltop Gym: $3420.00 | sign-off: yes | second chef: yes"


def test_format_line_shows_each_flag_independently():
    line = format_event_line("Lumen Labs", 1154.25, False, True)
    assert line == "Lumen Labs: $1154.25 | sign-off: no | second chef: yes"


def test_format_line_always_has_two_decimal_places():
    line = format_event_line("Kettle Works", 1520, False, False)
    assert "$1520.00" in line
