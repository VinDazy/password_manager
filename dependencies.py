import streamlit as st
import streamlit_authenticator as stauth
from keys import db_user_tab_key,db_password_tab_key
import datetime
from deta import Deta
import re 
import pandas as pd
import random



DETA_KEY = db_user_tab_key
DETA_PASS_KEY = db_password_tab_key

deta = Deta(DETA_KEY)
deta_pass = Deta(DETA_PASS_KEY)



db = deta.Base('user')
db_pass = deta_pass.Base('password')





def insert_password(password_id,user_id,domain,password_length,password):
    #user_id=user_email 
    return db_pass.put({'Password_id':password_id,
                        'User_Email':user_id,
                        'Password':password,
                        'Password_Domain':domain,
                        'Password_length':password_length
                        })


def insert_user(email, username, password):
    """
    Inserts Users into the DB
    :param email:
    :param username:
    :param password:
    :return User Upon successful Creation:
    """
    date_joined = str(datetime.datetime.now())

    return db.put({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})


def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items


def get_user_emails():
    """
    Fetch User Emails
    :return List of user emails:
    """
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    """
    Fetch Usernames
    :return List of user usernames:
    """
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames


def validate_email(email):
    """
    Check Email Validity
    :param email:
    :return True if email is valid else False:
    """
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    """
    Checks Validity of userName
    :param username:
    :return True if username is valid else False:
    """

    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False


def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        # Add User to DB
                                        hashed_password = stauth.Hasher([password2]).generate()
                                        insert_user(email, username, hashed_password[0])
                                        st.success('Account created successfully!!')
                                        st.balloons()
                                    else:
                                        st.warning('Passwords Do Not Match')
                                else:
                                    st.warning('Password is too Short')
                            else:
                                st.warning('Username Too short')
                        else:
                            st.warning('Username Already Exists')

                    else:
                        st.warning('Invalid Username')
                else:
                    st.warning('Email Already exists!!')
            else:
                st.warning('Invalid Email')

        btn1, bt2, btn3, btn4, btn5 = st.columns(5)

        with btn3:
            st.form_submit_button('Sign Up')


def generate_password(lower, upper, special, number):
    lowercase_chars = 'abcdefghijklmnopqrstuvwxyz'
    uppercase_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    special_chars = '!@#$%^&*()_+-/.,'
    digit_chars = '0123456789'

    # Create lists for each character type
    lowercase_list = [random.choice(lowercase_chars) for _ in range(lower)]
    uppercase_list = [random.choice(uppercase_chars) for _ in range(upper)]
    special_list = [random.choice(special_chars) for _ in range(special)]
    number_list = [random.choice(digit_chars) for _ in range(number)]

    # Concatenate the lists and shuffle to form the password
    password_list = lowercase_list + uppercase_list + special_list + number_list
    random.shuffle(password_list)
    password = ''.join(password_list)
    return password

def input_info():
    data = {}
    input_form = st.form(key="input", clear_on_submit=False)
    domain = input_form.text_input("Password Domain")
    input_form.markdown("---")
    username = input_form.text_input("Domain Username")
    input_form.markdown("---")
    input_form.subheader("Desired password length")
    pass_length = input_form.slider("🔐", min_value=8, max_value=100)
    input_form.markdown("---")
    special = input_form.slider("Special characters", min_value=0, max_value=100)
    lower = input_form.slider("Lower case characters", min_value=0, max_value=100)
    upper = input_form.slider("Upper case characters", min_value=0, max_value=100)
    number = input_form.slider("Numbers", min_value=0, max_value=100)
    verify = input_form.form_submit_button("Generate")
    summ = lower + upper + number + special
    if verify:
        if domain == '' or username == '':
            input_form.warning("Please verify username and/or domain name input ")
        elif summ != pass_length:
            input_form.error("Please verify password composition", icon="🚨")
        else:
            password = generate_password(lower, upper, special, number)
            input_form.success("Composition done successfully", icon="✅")
            data = {
                "Domain": domain,
                "Username": username,
                "Password": password,
                "Password_Length": summ
            }
            return data



df = pd.DataFrame()
def display():
    insert, output = st.columns(2)
    
    with insert:
        data = input_info()
        if data:
            global df
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    
    with output:
        if not df.empty:
            st.subheader("Generated Passwords :")
            st.write(df)
    return data


    






