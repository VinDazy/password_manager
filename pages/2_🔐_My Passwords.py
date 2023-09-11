import streamlit as st
from deta import Deta
import pandas as pd 
import pickle
from dependencies import *



st.set_page_config(page_title="Password Manager",layout="wide", page_icon="media/icon.png")
st.title("User Passwords")

st.markdown("""
<style>
.css-eh5xgm.e1ewe7hr3    
{
            visibility : hidden;
}
.css-cio0dv.e1g8pov61
            {
            visibility : hidden;
            }
</style>
""", unsafe_allow_html=True)

DETA_PASS_KEY = st.secrets["db_password_tab_key"]

deta_pass = Deta(DETA_PASS_KEY)

db_pass = deta_pass.Base('password')

try :
    file_path = "email.pickle"

    try:
        # Open the pickle file in binary read mode
        with open(file_path, 'rb') as file:
            # Load the data from the pickle file
            email = pickle.load(file)
            print(f"Read email from pickle file: {email}")
    except FileNotFoundError:
        print(f"Pickle file '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    with st.sidebar:
        st.image('media/welcome.gif')
        st.success("Displaying Passwords",icon="✅")
    def fetch_user_passwords(email):
        user_data_list = []
        users = db_pass.fetch()

        for user in users.items:
            if user['User_Email'] == email:
                encrypted_password=user['Password']
                decrypted_password_bytes = cipher_suite.decrypt(encrypted_password)
                decrypted_password = decrypted_password_bytes.decode('utf-8')
                new_data = {
                    'Password_id': user['Password_id'],
                    'User_Email': user['User_Email'],
                    'Password': decrypted_password,
                    'Password_Domain': user['Password_Domain'],
                    'Password_length': user['Password_length']
                }
                user_data_list.append(new_data)

        # Create a DataFrame from the list of user data dictionaries
        df = pd.DataFrame(user_data_list)
        
        # Display the data in a Streamlit web app
        st.write("User Email:", email)
        
        if not df.empty:
            st.write(df)
            
        else:
            st.write("No passwords found for this user.")

    fetch_user_passwords(email=email)
except:
    st.error("Please Log in first")


