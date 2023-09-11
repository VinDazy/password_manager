from dependencies import *
import pickle
import hashlib
import os
import base64



st.set_page_config(page_title="Password Manager",layout="wide", page_icon="media/icon.png")
st.title("Password Manager")

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
global_email = None

def create_unique_code(password):
    # Generate a random salt
    salt = os.urandom(16)

    # Hash the password using a cryptographic hash function (SHA-256)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    # Combine the salt and password hash to create a unique code
    unique_code = salt + password_hash

    # Convert the unique code to a hexadecimal representation
    unique_code_hex = unique_code.hex()

    return unique_code_hex[:10]
def login():
    try:
            users = fetch_users()
            emails = []
            usernames = []
            passwords = []

            for user in users:
                emails.append(user['key'])
                usernames.append(user['username'])
                passwords.append(user['password'])

            credentials = {'usernames': {}}
            for index in range(len(emails)):
                credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

            Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=0)
            email, authentication_status,username = Authenticator.login(':green[Login]', 'main')
            info, info1 = st.columns(2)

            if not authentication_status:
                df.drop(df.index, inplace=True)
                sign_up()

            if username:
                if username in usernames:
                    if authentication_status:
                        # let User see app
                        st.sidebar.subheader(f'Welcome {username}')
                        st.sidebar.image('media/welcome.gif')
                        Authenticator.logout('Log Out', 'sidebar')
                        data=display()
                        global global_email
                        global_email=email
                        cipher_suite = Fernet(key)
                        if data is not None:
                            password=data['Password']
                            password_bytes = password.encode('utf-8')
                            encrypted_password = cipher_suite.encrypt(password_bytes)
                            encrypted_password_base64 = base64.b64encode(encrypted_password).decode('utf-8')
                            insert_password(password_id=create_unique_code(password),user_id=email,domain=data['Domain'],password_length=data['Password_Length'],password=encrypted_password_base64)
                            
                    elif not authentication_status:
                        with info:
                            st.error('Incorrect Password or username')
                    else:
                        with info:
                            st.warning('Please feed in your credentials')
                else:
                    with info:
                        st.warning('Username does not exist, Please Sign up')


    except Exception as e:
        st.write(e)



login()

def return_email():
    return global_email
print("(home)email is :",return_email())
###############################################



email = return_email()



file_path = "email.pickle"

with open(file_path, 'wb') as file:
    pickle.dump(email, file)
