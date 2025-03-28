import streamlit as st
import hashlib

# Initialize an empty hospital ledger (a dictionary where keys are patient names)
hospital_ledger_advanced = {}

# Function to generate a hash for the visit record
def generate_hash(patient_name, treatment, cost, date_of_visit):
    visit_string = f"{patient_name}{treatment}{cost}{date_of_visit}"
    return hashlib.sha256(visit_string.encode()).hexdigest()

# Function to add or update patient visits (optimized)
def add_patient_visit_advanced(patient_name, treatment, cost, date_of_visit):
    # Check if the patient already exists
    patient_name = patient_name.lower()
    if patient_name in hospital_ledger_advanced:
        st.success(f"Updating visit record for {patient_name}.")
    else:
        st.success(f"Adding new visit record for {patient_name}.")

    # Generate a hash for this visit record
    visit_hash = generate_hash(patient_name, treatment, cost, date_of_visit)

    # Create a dictionary for the visit with the hash
    visit = {
        "treatment": treatment,
        "cost": cost,
        "date_of_visit": date_of_visit,
        "visit_hash": visit_hash  # Store the hash to verify data integrity
    }

    # Add the visit to the patient's list of visits (using a dictionary)
    if patient_name not in hospital_ledger_advanced:
        hospital_ledger_advanced[patient_name] = []

    hospital_ledger_advanced[patient_name].append(visit)
    st.info(f"Visit added for {patient_name} on {date_of_visit} for treatment {treatment} costing ${cost}.")
    st.text_area("Visit hash:", visit_hash, height=50)

# Function to apply the theme based on mode
def apply_theme(dark_mode):
    if dark_mode:
        st.markdown(
            """
            <style>
                body {
                    background-color: #2b2b2b;
                    color: #e1e1e1;
                }
                .css-1v0mbdj {
                    background-color: #003366;
                }
                .stButton>button {
                    background-color: #003366;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input, .stSelectbox select {
                    background-color: #333333;
                    color: white;
                    border: none;
                }
                .stMarkdown {
                    color: #e1e1e1;
                }
                .stTextInput, .stTextArea, .stNumberInput, .stDateInput, .stSelectbox {
                    border-radius: 5px;
                }
                .stButton>button:hover {
                    background-color: #005bb5;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
                body {
                    background-color: #f0f0f0;
                    color: #333333;
                }
                .css-1v0mbdj {
                    background-color: #004080;
                }
                .stButton>button {
                    background-color: #004080;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input, .stSelectbox select {
                    background-color: white;
                    color: #333333;
                    border: 1px solid #004080;
                }
                .stMarkdown {
                    color: #333333;
                }
                .stTextInput, .stTextArea, .stNumberInput, .stDateInput, .stSelectbox {
                    border-radius: 5px;
                }
                .stButton>button:hover {
                    background-color: #005bb5;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

# Set the page configuration
st.set_page_config(page_title="Hospital Ledger System", layout="wide")

# Sidebar for theme toggle
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)

# Apply theme based on the toggle value
apply_theme(dark_mode)

# Main content of the app
st.title("Hospital Ledger System")

# Sidebar to switch between tabs
selected_tab = st.selectbox("Choose an action", ["Add Visit", "Search Patient"])

if selected_tab == "Add Visit":
    st.header("Add New Patient Visit")
    
    # Inputs for patient visit details (organize them in columns for a cleaner look)
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Enter the patient's name", placeholder="John Doe")
        treatment = st.text_input("Enter the treatment received", placeholder="Treatment description")
    with col2:
        cost = st.number_input("Enter the cost of the treatment (₹)", min_value=0.0, format="%.2f")
        date_of_visit = st.date_input("Enter the date of visit")

    # Button to add the visit
    if st.button("Add Visit"):
        if patient_name and treatment and cost and date_of_visit:
            add_patient_visit_advanced(patient_name, treatment, cost, str(date_of_visit))
        else:
            st.warning("Please fill all fields!")

elif selected_tab == "Search Patient":
    st.header("Search for Patient Visits")
    
    # Input field for searching patient name
    search_patient = st.text_input("Enter patient name to search for", placeholder="John Doe").lower()

    if search_patient:
        if search_patient in hospital_ledger_advanced:
            st.write(f"Visit records for {search_patient}:")
            for visit in hospital_ledger_advanced[search_patient]:
                st.markdown(f"**Treatment:** {visit['treatment']}")
                st.markdown(f"**Cost:** ${visit['cost']}")
                st.markdown(f"**Date of Visit:** {visit['date_of_visit']}")
                st.markdown(f"**Visit Hash:** {visit['visit_hash']}")
                st.write("---")
        else:
            st.error(f"Patient {search_patient} not found in the ledger.")
