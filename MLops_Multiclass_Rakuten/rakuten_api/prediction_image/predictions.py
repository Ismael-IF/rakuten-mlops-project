import os
import requests
from datetime import datetime
import time


time.sleep(28)

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

# User account used for model predictions tests :
client_email_user = 'johndoe@example.com'
client_secret_user = 'secret2'

user_account = {'username':client_email_user,
                'password': client_secret_user
               }

time.sleep(1)
token_request = requests.post(url='http://{address}:{port}/token'.format(address=api_address,port=api_port), 
                                headers=headers, 
                                data=user_account)
time.sleep(2)

token = token_request.json()['access_token']
#token

# Add the token to subsequent requests
headers['Authorization'] = 'Bearer ' + token

test_title =  '''
**********************************************************************************************
                                     Models tests - {date_test}
                                                   START 
**********************************************************************************************
'''
test_title =  test_title.format(date_test = date_test)
print(test_title)

# Request #1 START =========================================================================================
designation_text_1 = "Figurine Minnie Robe Jaune Et Chaussure Rose"
description_text_1 = "quelques petit éclats de peinture sur gant nez et oreille blanc"
real_class_1 = 1280
real_label_1 = 'toys for children'

data_text_1 = {'designation': designation_text_1 ,
              'description': description_text_1 }

time.sleep(1)
response_1 = requests.post(url='http://{address}:{port}/predict_with_text_Conv1D/'.format(address=api_address,port=api_port), 
                           headers=headers,
                           data=data_text_1)                         
time.sleep(4)

output_1 = '''
====================================================================
    Predictions test #1 using Conv1D TEXT BASED MODEL - results
====================================================================

request done at "predict_with_text_Conv1D"
| username = 'johndoe@example.com'
| password = 'secret2'
| Rakuten product designation = '{designation_text_1}'                
| Rakuten product description = '{description_text_1}'  


expected result code = {status_code}
expected Predicted class result =  {real_class_1}
expected Predicted label result = "{real_label_1}"
expected Precision  = 100

actual result code = {status_code}
actual Predicted class result = {predicted_class}
actual Predicted label result = "{predicted_label}"
actual Precision  = {precision}

==> Code result = {test_status}
==> Prediction result = {prediction_status}

'''

# Response code status
status_code = response_1.status_code

# Request response data
results_1 = response_1.json()
#results_1

predicted_class = results_1["predicted_class"]
predicted_label = results_1["predicted_label"]
precision = results_1["precision"]

# Setting test results
if status_code == 200 :
    test_status = 'SUCCESS'
    if predicted_class == real_class_1:    
        prediction_status = 'SUCCESS'
    else: 
        prediction_status = 'FAILURE'
    
elif status_code != 200:
    score_status = 'FAILURE'

output_1 =  output_1.format(designation_text_1=designation_text_1,
                            description_text_1=description_text_1,
                            real_class_1=real_class_1,
                            real_label_1=real_label_1,
                            status_code=status_code,
                            test_status=test_status,
                            predicted_class=predicted_class,
                            predicted_label=predicted_label,
                            precision=precision,
                            prediction_status=prediction_status)

print(output_1)

# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)
        file.write(test_title)
        file.write(output_1)
else : 
     print("An error occurred when tring to save LOGs!")
#Request #1 END =========================================================================================

#Request #2 START =========================================================================================
designation_text_2 = "Revue Fémina 2004 Couverture Sharon Stone"
description_text_2 = None
real_class_2 = 2403
real_label_2 = 'children books and magazines'

data_text_2 = {'designation': designation_text_2 ,
              'description': description_text_2 }

time.sleep(1)
response_2 = requests.post(url='http://{address}:{port}/predict_with_text_SimpleDN/'.format(address=api_address,port=api_port), 
                           headers=headers ,
                           data=data_text_2)                          
time.sleep(4)


output_2 = '''
====================================================================
    Predictions test #2 using Simple DNN TEXT BASED MODEL - results
====================================================================

request done at "predict_with_text_SimpleDN"
| username = 'johndoe@example.com'
| password = 'secret2'
| Rakuten product designation = '{designation_text_2}'               
| Rakuten product description = '{description_text_2}'  


expected result code = {status_code}
expected Predicted class result =  {real_class_2}
expected Predicted label result = '{real_label_2}'
expected Precision  = 100

actual result code = {status_code}
actual Predicted class result = {predicted_class}
actual Predicted label result = '{predicted_label}'
actual Precision  = {precision}

==> Code result = {test_status}
==> Prediction result = {prediction_status}

'''

# Response code status
status_code = response_2.status_code

# Request response data
results_2 = response_2.json()
#results_2

predicted_class = results_2["predicted_class"]
predicted_label = results_2["predicted_label"]
precision = results_2["precision"]

# Setting test results
if status_code == 200 :
    test_status = 'SUCCESS'
    if predicted_class == real_class_2:    
        prediction_status = 'SUCCESS'
    else: 
        prediction_status = 'FAILURE'
    
elif status_code != 200:
    score_status = 'FAILURE'

    
output_2 =  output_2.format(designation_text_2=designation_text_2,
                            description_text_2=description_text_2,
                            real_class_2=real_class_2,
                            real_label_2=real_label_2,
                            status_code=status_code,
                            test_status=test_status,
                            predicted_class=predicted_class,
                            predicted_label=predicted_label,
                            precision=precision,
                            prediction_status=prediction_status)


print(output_2)

# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)      
        file.write(output_2)
else : 
     print("An error occurred when tring to save LOGs!")
#Request #2 END =========================================================================================

headers = {}
 
# Add the token to subsequent requests
headers['Authorization'] = 'Bearer ' + token

#Request #3 START ========================================================================================
image_name_1 = './image_samples/image_1164498572_product_2786150067.jpg'
real_class_3 = 2583
real_label_3 = 'piscine spa'

#image_name_1 = './image_samples/image_862500067_product_102168018.jpg'
#real_class_3 = 1160
#real_label_3 = 'playing cards'

image_file = [('image_file', (image_name_1, open(image_name_1, 'rb'),
            'image/jpeg'))]


time.sleep(1)
response_3 = requests.post(url='http://{address}:{port}/predict_with_image_Xception/'.format(address=api_address,port=api_port), 
                           headers=headers ,
                           files=image_file)
time.sleep(4)                       


output_3 = '''
====================================================================
    Predictions test #3 using Xception IMAGE BASED MODEL - results
====================================================================

request done at "predict_with_image_Xception"
| username = 'johndoe@example.com'
| password = 'secret2'
| Rakuten product image name = '{image_name_1}'                
  

expected result code = {status_code}
expected Predicted class result =  {real_class_3}
expected Predicted label result = '{real_label_3}'
expected Precision  = 100

actual result code = {status_code}
actual Predicted class result = {predicted_class}
actual Predicted label result = '{predicted_label}'
actual Precision  = {precision}

==> Code result = {test_status}
==> Prediction result = {prediction_status}

'''

# Response code status
status_code = response_3.status_code

# Request response data
results_3 = response_3.json()
#results_3

predicted_class = results_3["predicted_class"]
predicted_label = results_3["predicted_label"]
precision = results_3["precision"]

# Setting test results
if status_code == 200 :
    test_status = 'SUCCESS'
    if predicted_class == real_class_3:    
        prediction_status = 'SUCCESS'
    else: 
        prediction_status = 'FAILURE'
    
elif status_code != 200:   
    score_status = 'FAILURE'

output_3 =  output_3.format(image_name_1=image_name_1,                           
                            real_class_3=real_class_3,
                            real_label_3=real_label_3,
                            status_code=status_code,
                            test_status=test_status,
                            predicted_class=predicted_class,
                            predicted_label=predicted_label,
                            precision=precision,
                            prediction_status=prediction_status)


print(output_3)

# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)       
        file.write(output_3)
else : 
     print("An error occurred when tring to save LOGs!")
#Request #3 END ===========================================================================================

#Request #4 START =========================================================================================
image_name_2 = './image_samples/image_862500067_product_102168018.jpg'
real_class_4 = 1160
real_label_4 = 'playing cards'


image_file = [('image_file', (image_name_2, open(image_name_2, 'rb'),
            'image/jpeg'))]


time.sleep(1)
response_4 = requests.post(url='http://{address}:{port}/predict_with_image_Inception/'.format(address=api_address,port=api_port), 
                           headers=headers ,
                           files=image_file)
time.sleep(4)                        

print(image_file)


output_4 = '''
====================================================================
    Predictions test #4 using Inception IMAGE BASED MODEL - results
====================================================================

request done at "predict_with_image_Inception"
| username = 'johndoe@example.com'
| password = 'secret2'
| Rakuten product image name = '{image_name_2}'                
  

expected result code = {status_code}
expected Predicted class result =  {real_class_4}
expected Predicted label result = '{real_label_4}'
expected Precision  = 100

actual result code = {status_code}
actual Predicted class result = {predicted_class}
actual Predicted label result = '{predicted_label}'
actual Precision  = {precision}

==> Code result = {test_status}
==> Prediction result = {prediction_status}

'''

# Response code status
status_code = response_4.status_code

# Request response data
results_4 = response_4.json()
#results_4

predicted_class = results_4["predicted_class"]
predicted_label = results_4["predicted_label"]
precision = results_4["precision"]

# Setting test results
if status_code == 200 :
    test_status = 'SUCCESS'
    if predicted_class == real_class_4:    
        prediction_status = 'SUCCESS'
    else: 
        prediction_status = 'FAILURE'
    
elif status_code != 200:
    score_status = 'FAILURE'

output_4 =  output_4.format(image_name_2=image_name_2,                           
                            real_class_4=real_class_4,
                            real_label_4=real_label_4,
                            status_code=status_code,
                            test_status=test_status,
                            predicted_class=predicted_class,
                            predicted_label=predicted_label,
                            precision=precision,
                            prediction_status=prediction_status)


print(output_4)

# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)
        file.write(output_4)
else : 
     print("An error occurred when tring to save LOGs!")
#Request #4 END =========================================================================================

#Request #5 START =======================================================================================
#designation_text_3 = "Black Rock Shooter Tv Animation Figurine Figma Dead Master 16 Cm"
#description_text_3 =  None
#image_name_3 = './image_samples/image_955830017_product_220445101.jpg'
#real_class_5 = 1140
#real_label_5 = 'figurines and Toy Pop'


designation_text_3 = "3-in-1 Manuel Tube Cintreuse application dans le remplacement des lignes de frein Tube de travail tools 1385"
description_text_3 =  "3-in-1 manuel Tube Tube Bender application dans le remplacement des lignes de frein Tube de travail électrique automobile Caractéristiques: cintreuse de tube pour le tube de 90 degrés ou à 180 degrés de flexion conception à trois fentes fonctionne pour 6/8/10 mm tubes et tuyaux poignée ergonomique  correspond à vos mains confortablement et facile à contrôler Convient aux tubes de cuivre des tuyaux en aluminium et les tubes en acier à paroi mince une large application dans le remplacement des lignes de frein travail du tube des champs électriques de l&#39;automobile etc. spécifications: Matériel: alliage d&#39;aluminium angle de flexion maximale: 180 degres de diamètre Bend: 6/8/10 mm poids: 03350 kg taille du produit: 2030 x 590 x 400 cm / 799 x 232 x 157 pouces poids du paquet: 0.3500 kg taille du paquet: 2100 x 700 x 500 cm / 827 x 276 x 197 pouces Contenu de l&#39;emballage: 1 x Tube Bender"
image_name_3 = './image_samples/image_1314429107_product_4202302612.jpg'
real_class_5 = 2585
real_label_5 = 'gardening and DIY'


data_text_3 = {'designation': designation_text_3 ,
              'description': description_text_3 }                          
                           
image_file = [('image_file', (image_name_3, open(image_name_3, 'rb'),
          'image/jpeg'))]


time.sleep(1)
response_5 = requests.post(url='http://{address}:{port}/predict_with_text_and_image_Conv1D_SimpleDNN_Xception/'.format(address=api_address,port=api_port), 
                           headers=headers ,
                           data=data_text_3,
                           files=image_file)       
time.sleep(3)

output_5= '''
=========================================================================================================
    Predictions test #5 using TEXT and IMAGE - BIMODAL : Conv1D & Simple DNN & Xception Results - results
=========================================================================================================

request done at "predict_with_text_and_image_Conv1D_SimpleDNN_Xception"
| username = 'johndoe@example.com'
| password = 'secret2'
| Rakuten product designation = '{designation_text_3}'                
| Rakuten product description = '{description_text_3}'
| Rakuten product image name = '{image_name_3}'                
  

expected result code = {status_code}
expected Predicted class result =  {real_class_5}
expected Predicted label result = '{real_label_5}'
expected Precision  = 100

actual result code = {status_code}
actual Predicted class result = {predicted_class}
actual Predicted label result = '{predicted_label}'
actual Precision  = {precision}

==> Code result = {test_status}
==> Prediction result = {prediction_status}

'''

# Response code status
status_code = response_5.status_code

# Request response data
results_5 = response_5.json()
#results_5

predicted_class = results_5["predicted_class"]
predicted_label = results_5["predicted_label"]
precision = results_5["precision"]

# Setting test results
if status_code == 200 :
    test_status = 'SUCCESS'
    if predicted_class == real_class_5:    
        prediction_status = 'SUCCESS'
    else: 
        prediction_status = 'FAILURE'
    
elif status_code != 200:
    score_status = 'FAILURE'

output_5 =  output_5.format(designation_text_3=designation_text_3,                           
                            description_text_3=description_text_3,
                            image_name_3=image_name_3,
                            real_class_5=real_class_5,
                            real_label_5=real_label_5,
                            status_code=status_code,
                            test_status=test_status,
                            predicted_class=predicted_class,
                            predicted_label=predicted_label,
                            precision=precision,
                            prediction_status=prediction_status)

print(output_5)

# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)
        file.write(output_5)
else : 
     print("An error occurred when tring to save LOGs!")
#Request #5 END ===========================================================================================

#Request #6 START =========================================================================================
designation_text_4 = "Black Rock Shooter Tv Animation Figurine Figma Dead Master 16 Cm"
description_text_4 =  None
image_name_4 = './image_samples/image_955830017_product_220445101.jpg'
real_class_6 = 1140
real_label_6 = 'figurines and Toy Pop'

#designation_text_4 = "3-in-1 Manuel Tube Cintreuse application dans le remplacement des lignes de frein Tube de travail tools 1385"
#description_text_4 =  "3-in-1 manuel Tube Tube Bender application dans le remplacement des lignes de frein Tube de travail électrique automobile Caractéristiques: cintreuse de tube pour le tube de 90 degrés ou à 180 degrés de flexion conception à trois fentes fonctionne pour 6/8/10 mm tubes et tuyaux poignée ergonomique  correspond à vos mains confortablement et facile à contrôler Convient aux tubes de cuivre des tuyaux en aluminium et les tubes en acier à paroi mince une large application dans le remplacement des lignes de frein travail du tube des champs électriques de l&#39;automobile etc. spécifications: Matériel: alliage d&#39;aluminium angle de flexion maximale: 180 degres de diamètre Bend: 6/8/10 mm poids: 03350 kg taille du produit: 2030 x 590 x 400 cm / 799 x 232 x 157 pouces poids du paquet: 0.3500 kg taille du paquet: 2100 x 700 x 500 cm / 827 x 276 x 197 pouces Contenu de l&#39;emballage: 1 x Tube Bender"
#image_name_4 = './image_samples/image_1314429107_product_4202302612.jpg'
#real_class_6 = 2585
#real_label_6 = 'gardening and DIY'


data_text_4 = {'designation': designation_text_4 ,
              'description': description_text_4 }                          
                           
image_file = [('image_file', (image_name_4, open(image_name_4, 'rb'),
          'image/jpeg'))]


time.sleep(1)
response_6 = requests.post(url='http://{address}:{port}/predict_with_text_and_image_Conv1D_SimpleDNN_Inception/'.format(address=api_address,port=api_port), 
                           headers=headers ,
                           data=data_text_4,
                           files=image_file)
time.sleep(3)

output_6= '''
===================================================================================================
    Predictions test #6 using TEXT and IMAGE - BIMODAL : Conv1D & Simple DNN & Inception - results 
===================================================================================================

request done at "predict_with_text_and_image_Conv1D_SimpleDNN_Inception"
| username = 'johndoe@example.com'
| password = 'secret2'
| Rakuten product designation = '{designation_text_4}'                
| Rakuten product description = '{description_text_4}'
| Rakuten product image name = '{image_name_4}'                
  

expected result code = {status_code}
expected Predicted class result = {real_class_6}
expected Predicted label result = '{real_label_6}'
expected Precision  = 100

actual result code = {status_code}
actual Predicted class result = {predicted_class}
actual Predicted label result = '{predicted_label}'
actual Precision={precision}

==> Code result = {test_status}
==> Prediction result = {prediction_status}

'''

# Response code status
status_code = response_6.status_code

# Request response data
results_6 = response_6.json()
#results_6

predicted_class = results_6["predicted_class"]
predicted_label = results_6["predicted_label"]
precision = results_6["precision"]

# Setting test results
if status_code == 200 :
    test_status = 'SUCCESS'
    if predicted_class == real_class_6:    
        prediction_status = 'SUCCESS'
    else: 
        prediction_status = 'FAILURE'
    
elif status_code != 200:
    score_status = 'FAILURE'

output_6 =  output_6.format(designation_text_4=designation_text_4,                           
                            description_text_4=description_text_4,
                            image_name_4=image_name_4,
                            real_class_6=real_class_6,
                            real_label_6=real_label_6,
                            status_code=status_code,
                            test_status=test_status,
                            predicted_class=predicted_class,
                            predicted_label=predicted_label,
                            precision=precision,
                            prediction_status=prediction_status)


print(output_6)

test_end ='''
**********************************************************************************************
                                           Models tests 
                                               END
**********************************************************************************************
'''

# Print logs in a file
if os.environ.get('LOG') == '1':
    with open(log_fname, 'a') as file:
        print("LOGs saved on",  log_fname)
        file.write(output_6)
        file.write(test_end)
else : 
     print("An error occurred when tring to save LOGs!")
print(test_end)
#Request #6 END =========================================================================================

