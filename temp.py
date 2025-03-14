import datetime

FORM_SCHEDULE = [
    (("10:00", "10:30"), "https://forms.gle/form1"),
    (("12:00", "12:30"), "https://forms.gle/form2"),
    (("14:00", "14:30"), "https://forms.gle/form3"),
    (("16:00", "16:30"), "https://forms.gle/form4"),
]

def get_current_form():
    """Returns the correct Google Form URL if the current time falls within a range."""
    now = datetime.datetime.now().strftime("%H:%M")

    for (start_time, end_time), form_url in FORM_SCHEDULE:
        if start_time <= now <= end_time:
            return form_url

    return None

print(get_current_form())
