import streamlit as st
import json
import datetime
import threading

# List of workers
workers = [
    "Afrim", "Dorentin", "Mirjeta", "Loredan", "Fjoralb", "Adil", "Laura",
    "Anita", "Mustafa", "Argenita", "Agon", "Albin", "Astriti", "Erina", "Dren",
    "Aida", "Kushtrim", "Besfort", "Fitimi", "Rinor", "Fisnik"
]

# Load or initialize parking lot status from a JSON file
PARKING_LOTS_FILE = "parking_lots.json"

def load_parking_lots():
    try:
        with open(PARKING_LOTS_FILE, "r") as file:
            content = file.read()
            if content:
                return json.loads(content)
            else:
                return {f"Lot {i + 1}": None for i in range(10)}
    except FileNotFoundError:
        return {f"Lot {i + 1}": None for i in range(10)}

def save_parking_lots(parking_lots):
    with open(PARKING_LOTS_FILE, "w") as file:
        json.dump(parking_lots, file)

def reset_parking_lots():
    # Reset parking lots at 20:35 every day
    now = datetime.datetime.now()
    reset_time = datetime.datetime(now.year, now.month, now.day, 17, 35, 0)

    if now >= reset_time:
        return {f"Lot {i + 1}": None for i in range(10)}
    return None

# Initialize parking lot status
parking_lots = load_parking_lots()

def reset_parking_lots_daily():
    global parking_lots
    while True:
        reset_result = reset_parking_lots()
        if reset_result:
            parking_lots = reset_result
            save_parking_lots(parking_lots)
            st.success("Parking lots reset at 20:35 every day.")
        # Sleep for 1 hour before checking again
        threading.Event().wait(3600)

# Start the thread for daily reset
reset_thread = threading.Thread(target=reset_parking_lots_daily)
reset_thread.start()

def parking_app():
    global parking_lots  # Make parking_lots a global variable

    st.title("Tive Kosovo Parking App")

    # Display current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Current Time: {current_time}, parking lots will be reset every day at 17:30!")

    # Main content
    # st.write("Welcome to the Parking App!")

    # Display available parking lots
    st.subheader("Available Parking Lots")
    available_lots = [lot for lot, status in parking_lots.items() if status is None]
    selected_lot = st.selectbox("Select Parking Lot", available_lots)

    # Dropdown for worker selection
    worker_name = st.selectbox("Select Worker", workers, index=0)

    # Checkbox for agreement
    agreement_checkbox = st.checkbox("Pasha baxhanakun s'po e rezervoj para se me parku kerrin!")

    # Book parking lot if the checkbox is checked
    if agreement_checkbox and st.button("Parked the car!"):
        parking_lots[selected_lot] = worker_name
        save_parking_lots(parking_lots)
        st.success(f"{worker_name} successfully parked {selected_lot}.")
    elif not agreement_checkbox and st.button("Parked the car!"):
        st.warning("Check the box!")

    # Display booked parking lots
    st.subheader("Full Parking Lots")
    booked_lots = {lot: worker for lot, worker in parking_lots.items() if worker is not None}
    if not booked_lots:
        st.info("No parking lots have been booked yet.")
    else:
        for lot, worker in booked_lots.items():
            st.write(f"{lot}: Booked by {worker}")

# Run the app
if __name__ == "__main__":
    parking_app()
