import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime 
from datetime import date



#load the model 
model = pickle.load(open('rf_model.pkl','rb')) 

def calculate_dob(dob) :
    
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)) 

def scale_amount(amount,max_val,min_val) :
    
    '''convert the amount which is in thousend to lakhs and then perform min max scaling
    
    Arguments :
        amount -- amounto to be scaled , type str must convert it to a type of float
        max_val -- max_val used during min_max scaling
        min_val -- min_val used during min_max scaling
    Returns :
        amount_scaled : Scaled amount between 0 and 1
    '''
    #amount_in_lakhs = (float(amount)) / 100000.0

    scaled_std = (float(amount) - min_val) / ( max_val - min_val)
    #amount_scaled = scaled_std * (max_val - min_val) + min_val

    return scaled_std

def preprocessing_input(d) :

    '''Dob is an instances of datetime object 
    
    Arguments : 
        dob -- dob object
    Returns : 
        age
    '''
    purpose_le = {"Bussiness":0,"Car":1,"Domestic Appliences":2,"Education":3,"Furniture/Equipment":4,
    "Radio/Tv":5,"Repairs":6,"Vacation/Others":7}

    saving_accounts_le = {"Little":0,"Moderate":1,"Quite Rich":3,"Rich":2}
    education_type_le = {"Higher Education":0,"Incomplete Higher":1,"Lower Secondary":2,"Secondary/Secondary Special":3}
    job_le = {'Grade A':0, 'Grade B':1,'Grade C':2,'Grade D':3}
    gender_le = {"Male":1,"Female":0}
    income_type_le = {"Commercial associate":0,"Pensioner":1,"State Pensioner":3,"Public Servent":3}

    feature_list = []
    for key, val in d.items() :
        if key == 'dob' :
            feature_list.append(calculate_dob(val))
        elif key == 'job' :
            feature_list.append(job_le[val])
        elif key == 'income_type' :
            feature_list.append(income_type_le[val])
        elif key == 'saving_account' :
            feature_list.append(saving_accounts_le[val])
        elif key == 'education_type' :
            feature_list.append(education_type_le[val])
        elif key == 'sex' :
            feature_list.append(gender_le[val])
        elif key == 'purpose' :
            feature_list.append(purpose_le[val])
        elif key == 'credit_amount' :
            feature_list.append(scale_amount(val,max_val=18424.0,min_val=250.0))
        elif key == 'income':
            feature_list.append(scale_amount(val,max_val=765000.0,min_val=31500.0))
        else :
            feature_list.append(val)


        

    return feature_list

def check_for_empty_feilds(d) :

    '''check for any feilds left empty by users
    Arguments : 
        d -- dictionary containing key and user supplied values
    Returns : 
        bool -- true if contain empty values and false if not
    '''

    #since income,children count can be zero we can leave this part as 0 but all
    #other feilds must be supplied by user

    vals = [val for key,val in d.items() if key != 'children_count']

    return all(vals)

def make_prediction(d) :

    '''Function to make prediction 
    
    Arguments : 
        d -- dictionary conatining values for dob,gender,job,housing,saving account,checking account
        credit amount,duration,purpose
    Returns : 
        output -- predicted value
    '''
    features =[float(feature) for feature in preprocessing_input(d)]
    features = np.array([features])

    output = model.predict_proba(features)[0]
    return output

        
def main():
  st.markdown("<h1 style='text-align: center; color: White;background-color:#e84343'>Credit risk modelling</h1>", unsafe_allow_html=True)

  features = {} 

  features['dob'] = st.date_input(label = "Enter your dob",min_value=datetime(1910,12,12), value=datetime(1995,9,1))
  features['sex'] = st.radio(label = "Enter your gender", options=("Male","Female"))
  features['job'] = st.selectbox(label = "Job",options=("","Grade A","Grade B",\
      "Grade C","Grade D")) 
  features['saving_account'] = st.selectbox(label = "Saving account",options=("","Little","Moderate","Rich","Quite Rich"))
  features['credit_amount'] = st.number_input(label="Credit Amount(In Lakhs)",min_value=0)
  features['purpose'] = st.selectbox(label = "Purpose",options=("","Car","Furniture/Equipment","Radio/Tv","Domestic Appliences",\
      "Repairs","Education","Bussiness","Vacation/Others"))
  features['income'] = st.number_input(label="Income",min_value=0)
  features['children_count'] = st.number_input(label="Children count",min_value=0,max_value=10)
  features['income_type'] = st.selectbox(label = "Income Type",options=("","Commercial associate","Pensioner","State Pensioner","Public Servent"))
  
  features['education_type'] = st.selectbox(label = "Education Type",options=("","Higher Education","Incomplete Higher","Lower Secondary", "Secondary/Secondary Special"))
 
   
  prediction = ""
  if st.button(label="Predict") :
      #check for any empty values 
      if check_for_empty_feilds(features) :
        st.write(features)
        prediction = make_prediction(features)
        st.write(prediction)

        if np.argmax(prediction) == 1 :
            st.success("Risk : GOOD {} %".format(round(prediction[1]*100,2)))
        else :
            st.success("Risk : BAD {} %".format(round(prediction[0]*100,2)))
      else :
        st.error('All feilds are required!')
        st.write(features)
    

if __name__ == "__main__" :
     main()
