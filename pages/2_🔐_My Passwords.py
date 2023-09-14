import streamlit as st
from deta import Deta
import pandas as pd 
import pickle
from dependencies import*
import base64
import time

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
col1,col2,col3,col4,col5,col6,col7,col8=st.columns(8)
delete_account=col8.button("Delete My Account")


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
    if delete_account:
        verify_form=col8.form(key="verify")
        user_check=verify_form.text_input("Verify your Username")
        check=verify_form.form_submit_button("Yes, Delete")
        if user_check==get_username(email=email) and check :
            Delete_Account(email=email)


    with st.sidebar:
        st.image('media/welcome.gif')
        st.success("Displaying Passwords",icon="✅")
    st.write("User Email:", email)
    delete_form=st.form(key="delete",clear_on_submit=True)
    placeholder =delete_form.empty()
    def fetch_user_passwords(email):
        user_data_list = []
        users = db_pass.fetch()

        for user in users.items:
            if user['User_Email'] == email:
                password=user['Password']
                decrypted=cipher_suite.decrypt(password).decode('utf-8')
                new_data = {
                    'Password_id': user['Password_id'],
                    'User_Email': user['User_Email'],
                    'Username':user["Username"],
                    'Password': decrypted,
                    'Password_Domain': user['Password_Domain'],
                    'Password_length': user['Password_length']
                }
                user_data_list.append(new_data)

        # Create a DataFrame from the list of user data dictionaries
        df = pd.DataFrame(user_data_list)
        
        return df
        
    df=fetch_user_passwords(email=email)
    if not df.empty:
        placeholder.write(df)
            
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
                with st.spinner("Deleting Password"):
                    time.sleep(2)
                    
                delete_form.success("Successfuly deleted Password,Please Reload the page")

                
    except Exception as e:
        delete_form.error("An error occured")
        expander=delete_form.expander("More info")
        expander.write(e)


except Exception as e :
    st.error("An error occured, Please try again Later",icon="🚨")
    st.write(e)


