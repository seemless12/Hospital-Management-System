import streamlit as st
import re
import requests

BASE_URL = "https://seenless-patient-fastapi-server.hf.space/"  # your FastAPI backend

st.subheader("➕ Add New Patient")

# Inputs
name = st.text_input("Name")
if name and not re.match(r'^[a-zA-Z\s]+$', name):
    st.error("Invalid name — only letters and spaces allowed")

age = st.number_input("Age", min_value=1, max_value=100)

gender = st.selectbox("Gender", ["Male", "Female"])

blood_type = st.text_input("Blood Type (e.g. A+, O-)")
if blood_type and len(blood_type) > 3:
    st.error("Invalid blood type — maximum 3 characters (e.g. A+)")

contact_phone = st.text_input("Contact Phone")
if contact_phone and not re.match(r'^[0-9\-]{4,15}$', contact_phone):
    st.error("Invalid phone number — only digits and '-' allowed")

contact_email = st.text_input("Contact Email (optional)")
if contact_email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact_email):
    st.error("Invalid email address")

doctor_assigned = st.text_input("Doctor Assigned", placeholder="Enter name only (Dr. will be added automatically)")
if doctor_assigned:
    doctor_assigned = "Dr " + doctor_assigned.strip()

medical_history = st.text_area(
    "Medical History (comma separated)",
    placeholder="e.g. Diabetes, Hypertension"
)

# Submit Button
if st.button("Create Patient"):
    if not name or not re.match(r'^[a-zA-Z\s]+$', name):
        st.warning("Please enter a valid name.")
    elif len(blood_type) > 3:
        st.warning("Please enter a valid blood type (max 3 chars).")
    elif not re.match(r'^[0-9\-]{4,15}$', contact_phone):
        st.warning("Please enter a valid phone number.")
    elif contact_email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact_email):
        st.warning("Please enter a valid email.")
    else:
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
            st.error(f"❌ Server error: {res.json().get('detail')}")


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





