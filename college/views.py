from django.shortcuts import render,redirect
import os
import numpy as np
import pickle
from .colleges import college_list,school_loc_list
from .models import MyProfile,CollegeData
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


gender_list = ['Female', 'Male']
school_type = ['Home-Schooled','Parochial','Private','Public']

ib = ['No','Yes']
ethnicity_list = ['African','American','Asian','Black','Caucacian','European','Hispanic','Jewish','Middle East','Others','Pacific Islander','Russia','South American','White']
major_list = ['Arts and Humanities','Business','Health and Medicine','Multi Interdisciplinary Studies','Others','Public and Social Services','Science Math and Technology','Social Sciences','Trades Personal Services','Undecided']
rank_list = ['Top 10%','Top 25%','Top 50%','Top 75%','Top 100%']
sat_from_list = ['Multiple Tests','Single Test']
colleges = list(range(1390))


# Loading models
model = os.path.join(BASE_DIR,'xgb_reg_model.pkl')
scaler = os.path.join(BASE_DIR,'scaler.pkl')

clf = pickle.load(open(model, "rb"))
std = pickle.load(open(scaler, "rb"))


def prediction(year,gender,major,ethnicity,gpa_w,hs_loc,hs_type,ib_candidate,class_rank,
                sub_eng_h,sub_mat_h,sub_sci_h,sub_oth_h,sub_hist_h,sub_arts_h,sub_ele_h,
                sat_math,sat_ebread,sat_wrt_lng,sat_scores_from,act_comp):
    # Loading models
    model = os.path.join(BASE_DIR,'xgb_reg_model.pkl')
    scaler = os.path.join(BASE_DIR,'scaler.pkl')

    
    clf = pickle.load(open(model, "rb"))
    
    std = pickle.load(open(scaler, "rb"))
    pb_scores = []

    for clg in colleges:
        data = [year,gender,major,ethnicity,gpa_w,hs_loc,hs_type,ib_candidate,class_rank,
                sub_eng_h,sub_mat_h,sub_sci_h,sub_oth_h,sub_hist_h,sub_arts_h,sub_ele_h,
                sat_math,sat_ebread,sat_wrt_lng,sat_scores_from,act_comp,clg]

            

        #print(data)
        data = [[float(i) for i in data]]
            
        data = std.transform(data)
                
        prediction = clf.predict(data)[0]
        proba_score = abs(round(prediction*100,2))

        if proba_score >=99:
            proba_score = 99
                
        pb_scores.append(int(proba_score))

    college = [ college_list[x]  for x in colleges ]

    pb_scores,college = zip(*sorted(zip( pb_scores,college))) #sorting
   
    
    n_top = 5

    high_scores,high_clgs = list(pb_scores[-n_top:]),list(college[-n_top:])

    hc_ids = []
    for c_id in list(college[-n_top:]):
        hc_ids.append(college_list.index(c_id))
    

    low_scores,low_clgs = list(pb_scores[:n_top]), list(college[:n_top])
    lc_ids = []
    for c_id in list(college[:n_top]):
        lc_ids.append(college_list.index(c_id))

    high_chances = zip(high_clgs, high_scores,hc_ids)
    low_chances = zip(low_clgs, low_scores,lc_ids)
    

    return high_chances,low_chances



@login_required(login_url='login',redirect_field_name='userform')
def userform(request):
    if request.method =='POST':
        try:
            if request.POST.get('hs_loc').isdigit():   
                hs_loc = request.POST.get('hs_loc')
            else:
                hs_loc = school_loc_list.index(request.POST.get('hs_loc'))
            
            if request.POST.get('gender').isdigit():
                gender = request.POST.get('gender')
            
            else:
                gender = gender_list.index(request.POST.get('gender'))


            if request.POST.get('hs_type').isdigit():

                hs_type = request.POST.get('hs_type')
            else:
                hs_type = school_type.index(request.POST.get('hs_type'))

            if request.POST.get('hs_loc').isdigit():
                hs_loc = request.POST.get('hs_loc')
            else:
                hs_loc = school_loc_list.index(request.POST.get('hs_loc'))

            
            if request.POST.get('ib_candidate').isdigit():
                ib_candidate = request.POST.get('ib_candidate')
            else:
                ib_candidate = ib.index(request.POST.get('ib_candidate'))

            if request.POST.get('ethnicity').isdigit():
                ethnicity = request.POST.get('ethnicity')
            else:
                ethnicity = ethnicity_list.index(request.POST.get('ethnicity'))

            
            if request.POST.get('major').isdigit():
                major = request.POST.get('major')
            else:
                major = major_list.index(request.POST.get('major'))

            if request.POST.get('class_rank').isdigit():
                class_rank = request.POST.get('class_rank')
            else:
                class_rank = rank_list.index(request.POST.get('class_rank'))
            
            if request.POST.get('sat_scores_from').isdigit():
                sat_scores_from = request.POST.get('sat_scores_from')
            else:
                sat_scores_from = sat_from_list.index(request.POST.get('sat_scores_from'))
            
            
            year = int(request.POST.get('year'))

            gpa_w = float(request.POST.get('gpa_w'))

            sub_eng_h = float(request.POST.get('sub_eng_h')) #ubject Honors
            sub_mat_h = float(request.POST.get('sub_mat_h'))
            sub_sci_h = float(request.POST.get('sub_sci_h'))
            sub_oth_h = float(request.POST.get('sub_oth_h'))
            sub_hist_h = float(request.POST.get('sub_hist_h'))
            sub_arts_h = float(request.POST.get('sub_arts_h'))
            sub_ele_h = float(request.POST.get('sub_ele_h'))

            act_comp = float(request.POST.get('act_comp')) #AT

            sat_math = float(request.POST.get('sat_math')) # subjects
            sat_ebread = float(request.POST.get('sat_ebread'))
            sat_wrt_lng = float(request.POST.get('sat_wrt_lng'))  

            

            
            high_chances,low_chances = prediction(float(year),float(gender),float(major),float(ethnicity),float(gpa_w),float(hs_loc),float(hs_type),float(ib_candidate),float(class_rank),
                    sub_eng_h,sub_mat_h,sub_sci_h,sub_oth_h,sub_hist_h,sub_arts_h,sub_ele_h,
                    sat_math,sat_ebread,sat_wrt_lng,float(sat_scores_from),act_comp)

            context = {
                'high_chances': high_chances,
                'low_chances': low_chances,
                }
        except:
            messages.info(request,'Something missed in the data, Please fill all the required details..')
            return redirect('userform')
        
        if CollegeData.objects.filter(user=request.user).exists():
            clg = CollegeData.objects.get(user=request.user)
            clg.user=request.user
            clg.gender =gender_list[int(gender)]
            clg.school_type = school_type[int(hs_type)]
            clg.school_location = school_loc_list[int(hs_loc)]
            clg.is_ib_candidate = ib[int(ib_candidate)]
            clg.ethnicity = ethnicity_list[int(ethnicity)]
            clg.class_rank = rank_list[int(class_rank)]
            clg.major = major_list[int(major)]
            clg.passout_year = year
            clg.weighted_gpa = gpa_w
            clg.sub_ele_h = sub_ele_h
            clg.sub_eng_h = sub_eng_h
            clg.sub_arts_h = sub_arts_h
            clg.sub_hist_h = sub_hist_h
            clg.sub_mat_h = sub_mat_h
            clg.sub_oth_h = sub_oth_h
            clg.sub_sci_h = sub_sci_h
            clg.sat_math = sat_math
            clg.sat_ebread = sat_ebread
            clg.sat_wrt_lng = sat_wrt_lng
            clg.sat_scores_from = sat_from_list[int(sat_scores_from)]
            clg.act_comp = act_comp
            clg.save()
            return redirect('dashboard')

        else:
            user = CollegeData(user=request.user,gender=gender_list[int(gender)],school_type=school_type[int(hs_type)],school_location=school_loc_list[int(hs_loc)],is_ib_candidate=ib[int(ib_candidate)],ethnicity=ethnicity_list[int(ethnicity)],major=major_list[int(major)],class_rank=rank_list[int(class_rank)],
                            passout_year=year,weighted_gpa=gpa_w,sub_eng_h=sub_eng_h,sub_mat_h=sub_mat_h,sub_sci_h=sub_sci_h,sub_oth_h=sub_oth_h,sub_hist_h=sub_hist_h,sub_arts_h=sub_arts_h,sub_ele_h=sub_ele_h,sat_math=sat_math,sat_ebread=sat_ebread,sat_wrt_lng=sat_wrt_lng,sat_scores_from=sat_from_list[int(sat_scores_from)],act_comp=act_comp)
            user.save()


        
        return redirect('dashboard')
    else:
        try:
            college_data = CollegeData.objects.get(user=request.user)
            context = {
                'college_data':college_data,
                
                }
            return render(request,'userform.html',context)
        except:
            return render(request,'userform.html')


    
    

@login_required(login_url='login',redirect_field_name='dashboard')
def dashboard(request):
    #print(10*'---',request.user)
    try:
        college_data = CollegeData.objects.get(user=request.user)
        gender = gender_list.index(college_data.gender)
        hs_type = school_type.index(college_data.school_type)

        hs = college_data.school_location

        if hs.isalpha():
                hs_loc = school_loc_list.index(hs)
        else:
            hs_loc = school_loc_list[int(hs)]
            hs_loc = school_loc_list.index(hs_loc)

        ib_candidate = ib.index(college_data.is_ib_candidate)
        ethnicity = ethnicity_list.index(college_data.ethnicity)
        major = major_list.index(college_data.major)
        class_rank = rank_list.index(college_data.class_rank)
        year = college_data.passout_year
        gpa_w = college_data.weighted_gpa

        sub_eng_h = college_data.sub_eng_h
        sub_mat_h = college_data.sub_mat_h
        sub_sci_h = college_data.sub_sci_h
        sub_oth_h = college_data.sub_oth_h
        sub_hist_h = college_data.sub_hist_h
        sub_arts_h = college_data.sub_arts_h
        sub_ele_h = college_data.sub_ele_h

        sat_math = college_data.sat_math
        sat_ebread = college_data.sat_ebread
        sat_wrt_lng = college_data.sat_wrt_lng
        sat_scores_from = sat_from_list.index(college_data.sat_scores_from)

        act_comp = college_data.act_comp

        high_chances,low_chances = prediction(year,gender,major,ethnicity,gpa_w,hs_loc,hs_type,ib_candidate,class_rank,
                            sub_eng_h,sub_mat_h,sub_sci_h,sub_oth_h,sub_hist_h,sub_arts_h,sub_ele_h,
                            sat_math,sat_ebread,sat_wrt_lng,sat_scores_from,act_comp)

        context = {
                    'high_chances': high_chances,
                    'low_chances': low_chances,
                    }
        
        return render(request,'dashboard_2.html',context)

    except CollegeData.DoesNotExist:
        context={
                'message':'No data for this user',
            }

        return render(request,'dashboard_2.html',context)




@login_required(login_url='login',redirect_field_name='dashboard')
def college(request,c_id):

    score = int(c_id.split('&')[1])
    c_id = int(c_id.split('&')[0])
    
    college = college_list[c_id]

    college_data = CollegeData.objects.get(user=request.user)

    gender = gender_list.index(college_data.gender)
    hs_type = school_type.index(college_data.school_type)

    
    hs = college_data.school_location
    
    if hs.isalpha():
        hs_loc = school_loc_list.index(hs)
    else:
        hs_loc = school_loc_list[int(hs)]
        hs_loc = school_loc_list.index(hs_loc)

    #hs_loc = school_loc_list.index(college_data.school_location)
    ib_candidate = ib.index(college_data.is_ib_candidate)
    ethnicity = ethnicity_list.index(college_data.ethnicity)
    major = major_list.index(college_data.major)
    class_rank = rank_list.index(college_data.class_rank)
    year = college_data.passout_year
    gpa_w = college_data.weighted_gpa


    sub_eng_h = float(college_data.sub_eng_h)
    sub_mat_h = float(college_data.sub_mat_h)
    sub_sci_h = float(college_data.sub_sci_h)
    sub_oth_h = float(college_data.sub_oth_h)
    sub_hist_h = float(college_data.sub_hist_h)
    sub_arts_h = float(college_data.sub_arts_h)
    sub_ele_h = float(college_data.sub_ele_h)

    sat_math = float(college_data.sat_math)
    sat_ebread = float(college_data.sat_ebread)
    sat_wrt_lng = float(college_data.sat_wrt_lng)
    sat_scores_from = sat_from_list.index(college_data.sat_scores_from)

    act_comp = college_data.act_comp

    if request.method =='POST':
        sub_mat_h_new = int(request.POST.get('sub_mat_h'))
        sub_sci_h_new = int(request.POST.get('sub_sci_h'))
        sub_hist_h_new = int(request.POST.get('sub_hist_h'))
        sub_arts_h_new = int(request.POST.get('sub_arts_h'))
        sub_ele_h_new = int(request.POST.get('sub_ele_h'))
        sub_eng_h_new = int(request.POST.get('sub_eng_h'))
        sub_oth_h_new = int(request.POST.get('sub_oth_h'))

        data = np.array([[year,gender,major,ethnicity,gpa_w,hs_loc,hs_type,ib_candidate,class_rank,
                sub_eng_h_new,sub_mat_h_new,sub_sci_h_new,sub_oth_h_new,sub_hist_h_new,sub_arts_h_new,sub_ele_h_new,
                sat_math,sat_ebread,sat_wrt_lng,sat_scores_from,act_comp,c_id]])

            
        data = std.transform(data)
                
        prediction = clf.predict(data)[0]
        new_score = round(prediction*100,2)

        if new_score >=99:
            new_score = 99

        #print('New score:',score)
                
        context ={
            'college': college,
            'c_id': c_id,
            'new_score':new_score,
            'score':score,
            'sat_math':sub_mat_h,
            'sat_sci':sub_sci_h,
            'sat_hist':sub_hist_h,
            'sat_art':sub_arts_h,
            'sat_ele':sub_ele_h,
            'sat_eng':sub_eng_h,
            'sat_oth':sub_oth_h,

            'sub_mat_h_new' : sub_mat_h_new,
            'sub_sci_h_new' : sub_sci_h_new,
            'sub_hist_h_new' : sub_hist_h_new,
            'sub_arts_h_new' : sub_arts_h_new,
            'sub_ele_h_new' : sub_ele_h_new,
            'sub_eng_h_new' : sub_eng_h_new,
            'sub_oth_h_new' : sub_oth_h_new,
        
        }  
  
    else:
        context ={
        'college': college,
        'c_id': c_id,
        'score':score,
        'sat_math':sub_mat_h,
        'sat_sci':sub_sci_h,
        'sat_hist':sub_hist_h,
        'sat_art':sub_arts_h,
        'sat_ele':sub_ele_h,
        'sat_eng':sub_eng_h,
        'sat_oth':sub_oth_h,
        }   
    return render(request,'UniversityCheck.html',context)





