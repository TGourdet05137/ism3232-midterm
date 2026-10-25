ISM3232 Midterm: Harvest Table Catering

Tatyana Gourdet
source/bin/python3
10/25/2026

I had to write six business rules and a report that the owner of Harvest Table Catering could read.or each event it works out the final total from the price per guest, the number of guests, and whether the client is a registered nonprofit.It also flags which events need a manager's sign-off or a second chef, and then prints a report with one line per event and a short summary of the whole list.
Rule 1: returns the cost of food before any discount. Rule 2 and 3: Returns it as a decimal. Rule 4: The discounted cost, service fee and event total are included in what is returned. Rule 5: If the event needs a sign-off it returns as True, if not False. Rule 6: if the event needs a second chef it is returned a true.
cd ~/ism3232-midterm source .venv/bin/activate pip install -r requirements.txt python3 main.py
ruff format . ruff check . pytest -v
around 27
I did not use AI on my ism3232-midterm exam.
