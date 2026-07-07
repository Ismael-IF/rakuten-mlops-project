import os
import requests
from datetime import datetime
import time


#wait for the api to be launched
print('\n \n Wait until API is finished starting...')
time.sleep(10)
print('\n \n starting completed')

date_test = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
log_fname =  '/home/data/api_tests.log' 

# API IP
api_address = 'fastApi_rakuten'

# API port
api_port = 8000

headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
} 

# Request #1 START =========================================================================================
# User #1  - Admin account
client_email_user_1 = 'admin_account1@example.com'
client_secret_user_1 = 'adminsecret1'

    
data_user_1 = {'username':client_email_user_1,
               'password':client_secret_user_1
              }
              
time.sleep(1)             
response_1 = requests.post(url='http://{address}:{port}/token'.format(address=api_address, port=api_port), 
                                headers=headers, 
                                data=data_user_1)
time.sleep(1)

test_title =  '''
**********************************************************************************************
                                     Authentication tests - {date_test}
                                                   START 
**********************************************************************************************
'''
test_title =  test_title.format(date_test = date_test)
print(test_title)



output_1 = '''
==================================
    Authentication test #1 results
==================================

request done at "/token"
| username = 'admin_account1@example.com'
| password = adminsecret1'

expected result = 200
actual restult = {status_code}

==>  {test_status}

'''


# Response code status
status_code = response_1.status_code

# Setting test result
if status_code == 200:
    test_status = 'SUCCESS'
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

# Request #2 START =======================================================================================
# User #2  - user account
client_email_user_2 = 'alicewonderson@example.com'
client_secret_user_2 = 'secret1'

    
data_user_2 = {'username':client_email_user_2,
               'password':client_secret_user_2
              }
              
time.sleep(1)               
response_2 = requests.post(url='http://{address}:{port}/token'.format(address=api_address, port=api_port), 
                                headers=headers, 
                                data=data_user_2)
time.sleep(1)
  
output_2 = '''
==================================
    Authentication test #2 results
==================================

request done at "/token"
| username = 'alicewonderson@example.com'
| password = 'secret1'

expected result = 200
actual restult = {status_code}

==>  {test_status}

'''


# Response code status
status_code = response_2.status_code

# Setting test result
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
output_2 =  output_2.format(status_code=status_code, test_status=test_status)
print(output_2)


# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)
        file.write(output_2)
else : 
     print("An error occurred when tring to save LOGs!")
# Request #2 END =========================================================================================

# Request #3 START =======================================================================================
# User #3  - user account
client_email_user_3 = 'johndoe@example.com'
client_secret_user_3 = 'password'

    
data_user_3 = {'username':client_email_user_3,
               'password':client_secret_user_3
              }
              
time.sleep(1)                
response_3 = requests.post(url='http://{address}:{port}/token'.format(address=api_address, port=api_port), 
                                headers=headers, 
                                data=data_user_3)
time.sleep(1) 

output_3 = '''
==================================
    Authentication test #3 results
==================================

request done at "/token"
| username = 'johndoe@example.com'
| password = 'password'

expected result = 401
actual restult = {status_code}

==>  {test_status}

'''


# Response code status
status_code = response_3.status_code

# Setting test result
if status_code == 401:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
output_3 =  output_3.format(status_code=status_code, test_status=test_status)
print(output_3)


test_end = '''
**********************************************************************************************
                                     Authentication tests 
                                               END
**********************************************************************************************
'''

# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)        
        file.write(output_3)
        file.write(test_end)
else : 
     print("An error occurred when tring to save LOGs!")
     
print(test_end)
# Request #3 END =========================================================================================