import streamlit as st
import requests
import re

BASE_URL = "https://seenless-patient-fastapi-server.hf.space/"

st.set_page_config(page_title="Patient Management System", layout="centered")

st.title("🏥 Patient Management Dashboard")

# Sidebar Navigation
menu = ["Add Patient", "View All", "Sort Patients", "Update Patient", "Delete Patient"]
choice = st.sidebar.selectbox("Navigation", menu)

# --------------------------------------------------
# 🔹 ADD PATIENT SECTION
# --------------------------------------------------
if choice == "Add Patient":
    st.subheader("➕ Add New Patient")

    # Input Fields
    name = st.text_input("Full Name")
    if name and not re.match(r'^[a-zA-Z\s]+$', name):
        st.error("Invalid name — only letters and spaces allowed.")

    age = st.number_input("Age", min_value=1, max_value=100, value=1)

    gender = st.selectbox("Gender", ["Male", "Female"])

    blood_type = st.text_input("Blood Type (e.g. A+, O-)")
    if blood_type and len(blood_type) > 3:
        st.error("Invalid blood type — max 3 characters (e.g. A+).")

    contact_phone = st.text_input("Contact Phone")
    if contact_phone and not re.match(r'^[0-9\-]{4,15}$', contact_phone):
        st.error("Invalid phone number — only digits and '-' allowed.")

    contact_email = st.text_input("Contact Email (optional)")
    if contact_email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact_email):
        st.error("Invalid email address format.")

    doctor_assigned = st.text_input("Doctor Assigned")
    medical_history = st.text_area("Medical History (comma separated)", placeholder="e.g. Diabetes, Hypertension")

    # Submit Button
    if st.button("Create Patient"):
        # Validate before sending
        if not name or not re.match(r'^[a-zA-Z\s]+$', name):
            st.warning("⚠️ Please enter a valid name.")
        elif blood_type and len(blood_type) > 3:
            st.warning("⚠️ Blood type must be at most 3 characters.")
        elif not re.match(r'^[0-9\-]{4,15}$', contact_phone):
            st.warning("⚠️ Please enter a valid contact number.")
        elif contact_email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact_email):
            st.warning("⚠️ Please enter a valid email address.")
        else:
            # Prepare data
            data = {
                "name": name,
                "age": age,
                "gender": gender,
                "blood_type": blood_type,
                "contact_phone": contact_phone,
                "contact_email": contact_email or None,
                "Medical_History": [x.strip() for x in medical_history.split(",")] if medical_history else None,
                "doctor_assigned": doctor_assigned,
            }

            res = requests.post(f"{BASE_URL}/create_patients", json=data)
            if res.status_code == 200:
                st.success("✅ Patient added successfully!")
            else:
                try:
                    st.error(f"❌ {res.json().get('detail', 'Server error')}")
                except:
                    st.error("❌ Something went wrong while creating patient.")

# --------------------------------------------------
# 🔹 VIEW ALL PATIENTS
# --------------------------------------------------
elif choice == "View All":
    st.subheader("📋 All Patients")
    res = requests.get(f"{BASE_URL}/patients")
    if res.status_code == 200:
        patients = res.json()
        st.dataframe(patients)
    else:
        st.error("⚠️ Could not load patients.")

# --------------------------------------------------
# 🔹 SORT PATIENTS
# --------------------------------------------------
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
            st.error(res.json().get("detail", "Something went wrong."))

# --------------------------------------------------
# 🔹 UPDATE PATIENT
# --------------------------------------------------
elif choice == "Update Patient":
    st.subheader("✏️ Update Patient Info")
    patient_id = st.text_input("Enter Patient ID")

    st.markdown("### Update Fields")

    new_name = st.text_input("New Name (optional)")
    new_age = st.number_input("New Age", min_value=1, max_value=100, value=1)
    new_gender = st.selectbox("New Gender", ["", "Male", "Female"])
    new_blood_type = st.text_input("New Blood Type (optional)")
    new_phone = st.text_input("New Contact Phone (optional)")
    new_email = st.text_input("New Contact Email (optional)")
    new_medical_history = st.text_area("New Medical History (comma-separated, optional)")
    new_doctor = st.text_input("New Doctor Assigned (optional)")

    if st.button("Update"):
        update_data = {}

        if new_name:
            update_data["name"] = new_name
        if new_age != 1:
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
                    st.error(f"❌ {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"⚠️ Request failed: {e}")

# --------------------------------------------------
# 🔹 DELETE PATIENT
# --------------------------------------------------
elif choice == "Delete Patient":
    st.subheader("🗑️ Delete Patient")
    patient_id = st.text_input("Enter Patient ID to Delete")

    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/delete_patient/{patient_id}")
        if res.status_code == 200:
            st.success("✅ Patient deleted successfully!")
        else:
            st.error(f"❌ {res.json().get('detail', 'Something went wrong')}")
