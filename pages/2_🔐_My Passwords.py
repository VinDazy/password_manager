import streamlit as st
from deta import Deta
import pandas as pd 
import pickle
from dependencies import Fernet,key,delete_passowrd
import base64

st.set_page_config(page_title="Password Manager",layout="wide", page_icon="media/icon.png")
st.title("Manage Passwords")

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
cipher_suite = Fernet(key)

try :
    file_path = "email.pickle"
    

    try:
        # Open the pickle file in binary read mode
        with open(file_path, 'rb') as file:
            # Load the data from the pickle file
            email = pickle.load(file)
            #print(f"Read email from pickle file: {email}")
    except FileNotFoundError:
        print(f"Pickle file '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    with st.sidebar:
        st.image('media/welcome.gif')
        st.success("Displaying Passwords",icon="✅")
    st.write("User Email:", email)
    delete_form=st.form(key="delete",clear_on_submit=True)
    def fetch_user_passwords(email):
        user_data_list = []
        users = db_pass.fetch()

        for user in users.items:
            if user['User_Email'] == email:
                password=user['Password']
                decoded_encrypted_password = base64.b64decode(password)
                decrypted_password_bytes = cipher_suite.decrypt(decoded_encrypted_password,ttl=7200)
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
        
        return df
        
    df=fetch_user_passwords(email=email)
    if not df.empty:
        delete_form.write(df)
            
    else:
        delete_form.write("No passwords found for this user.")
        delete_form.markdown("---")
    
    fetch_user_passwords(email=email)
    st.markdown("---")
    
    pass_id=delete_form.text_input("Password ID")
    submit=delete_form.form_submit_button("Delete Password")
    try :
        if submit:
            if not pass_id :
                raise ValueError("Valid Password ID is required")
            else:
                delete_passowrd(password_id=pass_id)
                delete_form.success("Successfuly deleted Password")
    except Exception as e:
        delete_form.error("An error occured")
        expander=delete_form.expander("More info")
        expander.write(e)


except Exception as e :
    st.error("An error occured, Please try again Later",icon="🚨")
    st.write(e)


