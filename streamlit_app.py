import streamlit as st
import requests

BASE_URL = "https://seenless-patient-fastapi-server.hf.space/"  # your FastAPI backend URL

st.set_page_config(page_title="Patient Management System", layout="centered")

st.title("🏥 Patient Management Dashboard")

# --- Sidebar Navigation ---
menu = ["Add Patient", "View All", "Sort Patients", "Update Patient", "Delete Patient"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- Add Patient ---
if choice == "Add Patient":
    st.subheader("➕ Add New Patient")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100, value=1)
    gender = st.selectbox("Gender", ["Select", "Male", "Female"])
    blood_type = st.text_input("Blood Type (e.g. A+, O-)")
    contact_phone = st.text_input("Contact Phone")
    contact_email = st.text_input("Contact Email (optional)")
    
    # Doctor name auto prefix
    doctor_assigned = st.text_input("Doctor Assigned (name only)")
    if doctor_assigned and not doctor_assigned.lower().startswith("dr "):
        doctor_assigned = f"Dr {doctor_assigned.strip()}"

    medical_history = st.text_area(
        "Medical History (comma separated)",
        placeholder="e.g. Diabetes, Hypertension"
    )

    if st.button("Create Patient"):
        # --- FRONT-END VALIDATION ---
        if not name.strip():
            st.error("⚠️ Name cannot be empty.")
        elif age <= 0:
            st.error("⚠️ Please enter a valid age.")
        elif gender == "Select":
            st.error("⚠️ Please select a gender.")
        elif not blood_type.strip():
            st.error("⚠️ Blood type is required.")
        elif not contact_phone.strip():
            st.error("⚠️ Contact phone is required.")
        elif not doctor_assigned.strip():
            st.error("⚠️ Doctor name is required.")
        else:
            # Prepare data to send
            data = {
                "name": name,
                "age": age,
                "gender": gender,
                "blood_type": blood_type,
                "contact_phone": contact_phone,
                "contact_email": contact_email or None,
                "Medical_History": [x.strip() for x in medical_history.split(",")] if medical_history else None,
                "doctor_assigned": doctor_assigned
            }

            res = requests.post(f"{BASE_URL}/create_patients", json=data)
            if res.status_code == 200:
                st.success("✅ Patient added successfully!")
            else:
                st.error(f"❌ Error: {res.json().get('detail')}")

# --- View All Patients ---
elif choice == "View All":
    st.subheader("📋 All Patients")
    res = requests.get(f"{BASE_URL}/patients")
    if res.status_code == 200:
        patients = res.json()
        st.dataframe(patients)
    else:
        st.error("Could not load patients.")

# --- Sort Patients ---
elif choice == "Sort Patients":
    st.subheader("🔀 Sort Patients")

    sort_by = st.selectbox("Sort by", ["age", "gender", "blood_type"])
    order = st.radio("Order", ["asc", "desc"])

    if st.button("Sort"):
        res = requests.get(f"{BASE_URL}/sort_patient?sort_by={sort_by}&order={order}")
        if res.status_code == 200:
            sorted_data = res.json().get("sorted_patients", [])
            st.dataframe(sorted_data)
        else:
            st.error(res.json().get("detail", "Something went wrong"))

# --- Update Patient ---
elif choice == "Update Patient":
    st.subheader("✏️ Update Patient Info")
    patient_id = st.text_input("Enter Patient ID")

    st.markdown("### Update the fields you want to change")

    new_name = st.text_input("New Name (optional)")
    new_age = st.number_input("New Age (optional)", min_value=1, max_value=100, value=1)
    new_gender = st.selectbox("New Gender (optional)", ["", "Male", "Female"])
    new_blood_type = st.text_input("New Blood Type (optional)")
    new_phone = st.text_input("New Contact Phone (optional)")
    new_email = st.text_input("New Contact Email (optional)")
    new_medical_history = st.text_area("New Medical History (comma-separated, optional)")
    new_doctor = st.text_input("New Doctor Assigned (optional)")

    if st.button("Update"):
        # Prepare update data
        update_data = {}

        if new_name:
            update_data["name"] = new_name
        if new_age != 1:  # Only include if changed
            update_data["age"] = new_age
        if new_gender:
            update_data["gender"] = new_gender
        if new_blood_type:
            update_data["blood_type"] = new_blood_type
        if new_phone:
            update_data["contact_phone"] = new_phone
        if new_email:
            update_data["contact_email"] = new_email
        if new_medical_history:
            update_data["Medical_History"] = [x.strip() for x in new_medical_history.split(",")]
        if new_doctor:
            update_data["doctor_assigned"] = new_doctor

        if not update_data:
            st.warning("⚠️ Please provide at least one field to update.")
        else:
            try:
                res = requests.put(f"{BASE_URL}/patients/{patient_id}", json=update_data)
                if res.status_code == 200:
                    st.success("✅ Patient updated successfully!")
                else:
                    st.error(f"❌ Error: {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"⚠️ Request failed: {e}")


# --- Delete Patient ---
elif choice == "Delete Patient":
    st.subheader("🗑️ Delete Patient")
    patient_id = st.text_input("Enter Patient ID to Delete")

    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/delete_patient/{patient_id}")
        if res.status_code == 200:
            st.success("✅ Patient deleted successfully!")
        else:
            st.error(f"❌ Error: {res.json().get('detail')}")




