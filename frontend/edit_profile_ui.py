import streamlit as st

def edit_profile_ui():
    st.markdown("### ✏️ Edit Your Details")

    # Load current details from session_state
    current_name = st.session_state.get("name", "")
    current_age = st.session_state.get("age", None)
    current_username = st.session_state.username

    # ✅ Convert age to int if possible, otherwise default to 25 (or 0)
    try:
        current_age = int(current_age) if current_age not in (None, "", "None") else 25
    except ValueError:
        current_age = 25

    new_name = st.text_input("Full Name", value=current_name)
    new_age = st.number_input("Age", min_value=0, max_value=120, value=current_age)
    new_username = st.text_input("Username", value=current_username)
    # new_password = st.text_input("New Password", type="password")


    if st.button("✅ Save Changes", use_container_width=True):
        # Update values
        st.session_state.username = new_username
        st.session_state.name = new_name
        st.session_state.age = new_age
        # TODO: Add password update logic if stored in backend

        st.success("✅ Profile updated!")
        st.session_state.page = "main"
        st.rerun()

    if st.button("⬅️ Back to Home", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()