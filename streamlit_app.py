import streamlit as st
import requests
import re

BASE_URL = "https://seenless-patient-fastapi-server.hf.space/"

st.set_page_config(page_title="Patient Management System", layout="centered")

st.title("Patient Management Dashboard")

# Sidebar Navigation
menu = ["Add Patient", "View All", "Sort Patients", "Update Patient", "Delete Patient"]
choice = st.sidebar.selectbox("Navigation", menu)

# --------------------------------------------------
# 🔹 ADD PATIENT SECTION (Improved Inline Validation)
# --------------------------------------------------
if choice == "Add Patient":
    st.subheader("➕ Add New Patient")

    # Input fields
    name = st.text_input("Full Name")
    name_error = st.empty()

    age = st.number_input("Age", min_value=1, max_value=100, value=1)
    age_error = st.empty()

    gender = st.selectbox("Gender", ["Male", "Female"])

    blood_type = st.text_input("Blood Type (e.g. A+, O-)")
    blood_error = st.empty()

    contact_phone = st.text_input("Contact Phone")
    phone_error = st.empty()

    contact_email = st.text_input("Contact Email (optional)")
    email_error = st.empty()

    doctor_assigned = st.text_input("Doctor Assigned")
    doctor_error = st.empty()

    medical_history = st.text_area(
        "Medical History (comma separated)",
        placeholder="e.g. Diabetes, Hypertension"
    )

    # Create button
    if st.button("Create Patient"):
        valid = True

        #  Validate Name
        if not name.strip():
            name_error.markdown('<p style="color:red;"> Name cannot be empty.</p>', unsafe_allow_html=True)
            valid = False
        elif not re.match(r'^[a-zA-Z\s]+$', name):
            name_error.markdown('<p style="color:red;"> Invalid name — letters only.</p>', unsafe_allow_html=True)
            valid = False
        else:
            name_error.empty()

        # Validate Age
        if not (1 <= age <= 100):
            age_error.markdown('<p style="color:red;"> Age must be between 1 and 100.</p>', unsafe_allow_html=True)
            valid = False
        else:
            age_error.empty()

        # Validate Blood Type
        if not blood_type.strip():
            blood_error.markdown('<p style="color:red;"> Blood type is required.</p>', unsafe_allow_html=True)
            valid = False
        elif len(blood_type) > 3:
            blood_error.markdown('<p style="color:red;"> Blood type too long (max 3 chars).</p>', unsafe_allow_html=True)
            valid = False
        else:
            blood_error.empty()

        # Validate Phone
        if not contact_phone.strip():
            phone_error.markdown('<p style="color:red;"> Contact phone is required.</p>', unsafe_allow_html=True)
            valid = False
        elif not re.match(r'^[0-9\-]{4,15}$', contact_phone):
            phone_error.markdown('<p style="color:red;"> Invalid phone number format (4–15 digits).</p>', unsafe_allow_html=True)
            valid = False
        else:
            phone_error.empty()

        # Validate Email (only if filled)
        if contact_email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, contact_email):
                email_error.markdown('<p style="color:red;"> Invalid email address.</p>', unsafe_allow_html=True)
                valid = False
            else:
                email_error.empty()
        else:
            email_error.empty()

        # Validate Doctor Assigned
        if not doctor_assigned.strip():
            doctor_error.markdown('<p style="color:red;"> Doctor name cannot be empty.</p>', unsafe_allow_html=True)
            valid = False
        else:
            doctor_error.empty()

        #  Submit to backend only if all are valid
        if valid:
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
                st.success(" Patient added successfully!")
            else:
                try:
                    st.error(f" {res.json().get('detail', 'Server error')}")
                except:
                    st.error(" Something went wrong while creating patient.")



#  VIEW ALL PATIENTS

elif choice == "View All":
    st.subheader("All Patients")
    res = requests.get(f"{BASE_URL}/patients")
    if res.status_code == 200:
        patients = res.json()
        st.dataframe(patients)
    else:
        st.error(" Could not load patients.")


#  SORT PATIENTS

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


# 🔹 UPDATE PATIENT

elif choice == "Update Patient":
    st.subheader(" Update Patient Info")
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
            st.warning(" Please provide at least one field to update.")
        else:
            try:
                res = requests.put(f"{BASE_URL}/patients/{patient_id}", json=update_data)
                if res.status_code == 200:
                    st.success(" Patient updated successfully!")
                else:
                    st.error(f" {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f" Request failed: {e}")

# --------------------------------------------------
# 🔹 DELETE PATIENT
# --------------------------------------------------
elif choice == "Delete Patient":
    st.subheader(" Delete Patient")
    patient_id = st.number_input("Enter Patient ID to Delete")

    if st.button("Delete"):
        if not patient_id.strip():
            st.warning(" Please enter a valid Patient ID.")
        else:
            patient_id = patient_id.strip()  # Clean input
            res = requests.delete(f"{BASE_URL}/delete_patients/{patient_id}")
            try:
                if res.status_code == 200:
                    st.success(" Patient deleted successfully!")
                elif res.status_code == 404:
                    st.error(" Patient not found.")
                else:
                    st.error(f" {res.json().get('detail', 'Something went wrong')}")
            except Exception as e:
                st.error(f" Request failed: {e}")







