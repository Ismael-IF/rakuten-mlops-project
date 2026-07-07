import os
import requests
from datetime import datetime
import time


time.sleep(18)

date_test = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
log_fname =  '/home/data/api_tests.log'

# API IP
api_address = 'fastApi_rakuten'

# API port
api_port = 8000

headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
} 

# Request #1 START =========================================================================================
client_email_admin_user = 'admin_account1@example.com'
client_secret_admin_user = 'adminsecret1'

admin_account = {'username':client_email_admin_user,
                'password':client_secret_admin_user
               }

time.sleep(1)
token_request_1 = requests.post(url='http://{address}:{port}/token'.format(address=api_address, port=api_port), 
                                headers=headers, 
                                data=admin_account)
time.sleep(1)

token_1 = token_request_1.json()['access_token']


# Add the token to subsequent requests
headers['Authorization'] = 'Bearer ' + token_1

account_to_delete = 'clementinemandarine@example.com'  

time.sleep(1)
response_1 = requests.delete(url='http://{address}:{port}/Admin/delete_user/'.format(address=api_address, port=api_port) + account_to_delete , 
                                headers=headers)                   
time.sleep(2)

test_title =  '''

**********************************************************************************************
**********************************************************************************************
                                     Authorization tests - {date_test}
                                                   START 
**********************************************************************************************
'''
test_title =  test_title.format(date_test = date_test)
print(test_title)


output_1 = '''
===========================================================================
    Authorization test #1 - user deletion test with Admin account- results
===========================================================================

request done at "/Admin/delete_user/"
| username = 'admin_account1@example.com'
| password = 'adminsecret1'
| user account deletion with email = 'clementinemandarine@example.com'


expected result = 204
actual restult = {status_code}

==>  {test_status}

'''


# Response code status
status_code = response_1.status_code

# Setting test result
if status_code == 204:
    test_status = 'SUCCESS'
    
elif  status_code == 404:
    test_status = 'Inconclusive(data to delete not found)'
    
else:
    test_status = 'FAILURE'
    
output_1 =  output_1.format(status_code=status_code, test_status=test_status)
print(output_1)


# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)
        file.write(test_title)
        file.write(output_1)
else : 
     print("An error occurred when tring to save LOGs!")
        
        
# Request #1 END =========================================================================================
client_email_user = 'alicewonderson@example.com'
client_secret_user = 'secret1'

user_account = {'username':client_email_user,
                'password':client_secret_user
               }
               
time.sleep(1)
token_request_2 = requests.post(url='http://{address}:{port}/token'.format(address=api_address, port=api_port), 
                                headers=headers, 
                                data=user_account)
time.sleep(1)

token_2 = token_request_2.json()['access_token']
token_2

# Add the token to subsequent requests
headers['Authorization'] = 'Bearer ' + token_2

account_to_delete = 'johndoe@example.com'  

time.sleep(1)
response_2 = requests.delete(url='http://{address}:{port}/Admin/delete_user/'.format(address=api_address, port=api_port) + account_to_delete , 
                                headers=headers)                    
time.sleep(2)

# Request #2 START =========================================================================================
output_2 = '''
===========================================================================
    Authorization test #2 - user deletion test with user account- results
===========================================================================
request done at "/Admin/delete_user/"
| username = 'alicewonderson@example.com'
| password = 'secret1'
| user account deletion with email = 'johndoe@example.com'


expected result = 403
actual restult = {status_code}

==>  {test_status}

'''


# Response code status
status_code = response_2.status_code

# Setting test result
if status_code == 403:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
output_2 =  output_2.format(status_code=status_code, test_status=test_status)
print(output_2)


test_end = '''
**********************************************************************************************
                                     Authorization tests 
                                               END
**********************************************************************************************
'''

# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)
        file.write(output_2)
        file.write(test_end)
else : 
     print("An error occurred when tring to save LOGs!")
     
print(test_end)
# Request #2 END =========================================================================================