from flask import request,render_template,redirect,url_for
from flask import current_app as app
from application.models import*
from flask_bcrypt import Bcrypt
import datetime
bcrypt = Bcrypt()

'''Admin Details and Code to add admin to database
it was used to set the first record in the database to be of Admin'''
'''admin_email="kavish2k@gmail.com"
admin_pass="kps123"
admin_pass_hashed = bcrypt.generate_password_hash(admin_pass).decode('utf-8')
admin_user=User(user_email=admin_email,user_password=admin_pass_hashed,user_role='Admin')
db.session.add(admin_user)
db.session.commit()'''

service_type_list=['Cleaning','Electrical','Plumbing','Carpentry','Painting','Appliance Installation','Appliance Service','Pest Control']

'''Login Page'''
@app.route('/',methods=["GET","POST"])
def login():
    if request.method=='GET':
        return render_template('login.html')
    
    elif request.method=='POST':
        email=str(request.form['email'])
        password=str(request.form['password'])
        y=User.query.filter(User.user_email==email).first() #Access the User table to fetch user object whose email exists in the table
        if y:
            if y.user_role=="Admin": #Admin Login
                return redirect('/admin/home')
            elif y.user_role=="Customer":  #Customer Login
                hashed_pass=bcrypt.check_password_hash(y.user_password,password)
                if hashed_pass: #Checking for correct password, if incorrect, then redirect back to login page
                    customer=Customer.query.filter(Customer.customer_email==email).first()
                    cid=customer.customer_id
                    return redirect (url_for('customer_home',customer_id=cid))
                else:
                    return redirect('/')
            else: #Professional Login
                hashed_pass=bcrypt.check_password_hash(y.user_password,password)
                if hashed_pass:
                    p=Professional.query.filter(Professional.pro_email==email).first()
                    pid=p.pro_id
                    return redirect(url_for('pro_home',pro_id=pid))
                else:
                    return redirect('/')
        else: #If incorrect email, then redirect back to login page
            return redirect('/')

           

@app.route('/register/customer',methods=["GET","POST"])
def customer_reg():
    if request.method=='GET':
        return render_template('register_customer.html')
    
    elif request.method=='POST':
        try:
            c_name=str(request.form['fullname'])
            c_phone=int(request.form['c_contact_no'])
            c_email=str(request.form['email'])
            c_pass=str(request.form['password'])
            c_add=str(request.form['address'])
            c_pin=int(request.form['pincode'])
            c_pass_hashed = bcrypt.generate_password_hash(c_pass).decode('utf-8') #Hashing the password, before storing in database
            if len(str(c_phone))!=10 or '@' not in c_email: #Backend Validation to check if phone number has exactly 10 digits and email contains @
                return redirect ('/')
            c_data=Customer.query.filter(Customer.customer_email==c_email).first()
            if c_data: #If customer already exists or a new customer uses an already existing email, redirect back to login page
                return redirect('/')
            else:
                new_customer=Customer(customer_name=c_name, customer_contact_no=c_phone, customer_email=c_email, customer_password=c_pass_hashed, customer_address=c_add, customer_pincode=c_pin,customer_status='Active')
                db.session.add(new_customer)
                db.session.commit()
                new_user=User(user_email=c_email, user_password=c_pass_hashed, user_role="Customer")
                db.session.add(new_user)
                db.session.commit()
                c_data=Customer.query.filter(Customer.customer_email==c_email).first()
                cid=c_data.customer_id
                return redirect(url_for('customer_home',customer_id=cid))
        except ValueError: #Backend Validation to check make sure that form has recieved correct inputs, if not then redirect back to login page
            return redirect('/')
            


@app.route('/register/pro',methods=["GET","POST"])
def pro_reg():
    if request.method=='GET':
        return render_template('register_professional.html',service_data=service_type_list) #Sending service-types as declared above to allow the professional to register to any one of them. 
    
    elif request.method=='POST':
        try:
            p_name=str(request.form['fullname'])
            p_phone=int(request.form['pro_contact_no'])
            p_email=str(request.form['email'])
            p_pass=str(request.form['password'])
            p_srv_type=str(request.form['service_type'])
            p_yrs=int(request.form['yrs_of_exp'])
            p_pin=int(request.form['pincode'])
            p_pass_hashed = bcrypt.generate_password_hash(p_pass).decode('utf-8') #Hashing the password, before storing in database
            if len(str(p_phone))!=10 or '@' not in p_email: #Backend Validation to check if phone number has exactly 10 digits and email contains @
                return redirect('/')
            pro_data=Professional.query.filter(Professional.pro_email==p_email).first()
            if pro_data: #If pro already exists or a new pro uses an already existing email, redirect back to login page
                return redirect('/')
            else:
                new_pro=Professional(pro_name=p_name, pro_contact_no=p_phone, pro_email=p_email, pro_password=p_pass_hashed, pro_service_type=p_srv_type, pro_exp=p_yrs, pro_pincode=p_pin,pro_status='Pending')
                db.session.add(new_pro)
                db.session.commit()
                return redirect('/')
        except ValueError: #Backend Validation to check make sure that form has recieved correct inputs, if not then redirect back to login page
            return redirect('/')


'''Professional Page Functionality'''
@app.route('/pro/home/<int:pro_id>',methods=["GET"])
def pro_home(pro_id):
    if request.method=='GET':
        p_data=Professional.query.filter(Professional.pro_id==pro_id).first()
        serv_type=p_data.pro_service_type
        pro_stat=p_data.pro_status
        s1=ServiceRequest.query.filter(ServiceRequest.service_status=="Requested").all()
        s2=ServiceRequest.query.filter(ServiceRequest.service_status=="Closed").all()
        s3=ServiceRequest.query.filter(ServiceRequest.service_status=="Accepted").all()
        serv_req_list=[]
        serv_close_list=[]
        serv_acc_list=[]
        for x in s1:
            if x.sr.service_type==serv_type and p_data.pro_pincode==x.cr.customer_pincode and pro_stat=='Active':
                if x.srp is None:
                    serv_req_list.append([x.sr_id,x.sr.service_name,x.sr.service_price,x.cr.customer_name,x.cr.customer_contact_no,x.cr.customer_address,x.cr.customer_pincode,x.date_of_req])
        for y in s2:
            if y.sr.service_type==serv_type and y.srp.pro_id==pro_id:
                serv_close_list.append([y.sr.service_name,y.cr.customer_name,y.cr.customer_address,y.cr.customer_pincode,y.service_remarks,y.date_of_comp,y.service_rating,y.pro_rating])
        for z in s3:
            if z.srp is None:
                serv_acc_list.append(None) 
            else: 
                if z.sr.service_type==serv_type and z.srp.pro_id==pro_id:
                    serv_acc_list.append([z.sr_id,z.sr.service_name,z.sr.service_price,z.cr.customer_name,z.cr.customer_contact_no,z.cr.customer_address,z.cr.customer_pincode])

        return render_template('home_professional.html',pid=pro_id,pro_data=p_data,serv_reqs=serv_req_list,serv_hist=serv_close_list,serv_acc=serv_acc_list)

@app.route('/pro/<int:pro_id>/service/accept/<int:serv_id>',methods=['GET'])
def pro_serv_accept(pro_id,serv_id):
    if request.method=="GET":
        service_hist=ServiceRequest.query.filter((ServiceRequest.pro_id==pro_id)&(ServiceRequest.service_status=='Accepted')).first()
        if service_hist:
            return redirect(url_for('pro_home',pro_id=pro_id))
        service=ServiceRequest.query.filter(ServiceRequest.sr_id==serv_id).first()
        service.pro_id=pro_id
        service.service_status='Accepted'
        db.session.commit()
        return redirect(url_for('pro_home',pro_id=pro_id))

    
@app.route('/pro/profile/<int:pro_id>',methods=["GET","POST"])
def pro_profile(pro_id):
    if request.method=="GET":
        pro_data=Professional.query.filter(Professional.pro_id==pro_id).first()
        return render_template('profile_professional.html',pid=pro_id,pro_data=pro_data,service_data=service_type_list)
    elif request.method=="POST":
        try:
            p_name=str(request.form['fullname'])
            p_phone=int(request.form['pro_contact_no'])
            p_srv_type=str(request.form['service_type'])
            p_yrs=int(request.form['yrs_of_exp'])
            p_pin=int(request.form['pincode'])
            if len(str(p_phone))!=10:
                return redirect(url_for('pro_home',pro_id=pro_id))
            p=Professional.query.filter(Professional.pro_id==pro_id).first()
            p.pro_name=p_name
            p.pro_contact_no=p_phone
            p.pro_service_type=p_srv_type
            p.pro_exp=p_yrs
            p.pro_pincode=p_pin
            db.session.commit()
            return redirect(url_for('pro_home',pro_id=pro_id))
        except ValueError:
            return redirect(url_for('pro_home',pro_id=pro_id))

@app.route('/pro/search/<int:pro_id>',methods=['GET','POST'])
def pro_search(pro_id):
    if request.method=="GET":
        options=['ServiceRequests']
        return render_template('search_professional.html',data=options,pid=pro_id)
    elif request.method=="POST":
        search_q=request.form['search_q']
        table=request.form['search_cat']
        options=['ServiceRequests']
        if search_q and table:
            if table=='ServiceRequests':
                data=ServiceRequest.query.filter((ServiceRequest.pro_id==pro_id)&(ServiceRequest.service_rating==search_q)|(ServiceRequest.date_of_comp==search_q)|(ServiceRequest.date_of_req==search_q)|(ServiceRequest.pro_rating==search_q)|(ServiceRequest.service_status==search_q)).all()
                cols=ServiceRequest.__table__.columns.keys()
                cols.remove('pro_id')
                return render_template('search_professional.html',data=options,dtable=data,data_cols=cols,table_name=table,pid=pro_id)
            else:
                pass
        elif table:
            data=ServiceRequest.query.filter((ServiceRequest.pro_id==pro_id)).all()
            cols=ServiceRequest.__table__.columns.keys()
            cols.remove('pro_id')
            return render_template('search_professional.html',data=options,dtable=data,data_cols=cols,table_name=table,pid=pro_id)
        else:
            return redirect(url_for('pro_search',pro_id=pro_id))
        
@app.route('/pro/summary/<int:pro_id>',methods=['GET'])
def pro_summary(pro_id):
    ratings=[]
    labels_ratings=['1 Star','2 Stars','3 Stars','4 Stars','5 Stars']
    labels_service=['Accepted','Requested','Closed','Cancelled']
    for x in range(1,6):
        pro_ratings=ServiceRequest.query.filter((ServiceRequest.pro_id==pro_id)&(ServiceRequest.pro_rating==x)).count()
        ratings.append(pro_ratings)
    accepted=ServiceRequest.query.filter((ServiceRequest.pro_id==pro_id) & (ServiceRequest.service_status=='Accepted')).count()
    requested=ServiceRequest.query.filter((ServiceRequest.pro_id==pro_id) & (ServiceRequest.service_status=='Requested')).count()
    closed=ServiceRequest.query.filter((ServiceRequest.pro_id==pro_id) & (ServiceRequest.service_status=='Closed')).count()
    cancelled=ServiceRequest.query.filter((ServiceRequest.pro_id==pro_id) & (ServiceRequest.service_status=='Cancelled')).count()
    service_data=[accepted,requested,closed,cancelled]
    return render_template('summary_professional.html',pid=pro_id,data_ratings=ratings,labels_ratings=labels_ratings,data_service=service_data,labels_service=labels_service)



'''Customer Page Functionality''' 
@app.route('/customer/home/<int:customer_id>',methods=["GET","POST"])
def customer_home(customer_id):
    if request.method=="GET":
        service_type=[]
        serv_hist_list=[]
        service=Service.query.all()
        for x in service:
            if x.service_type not in service_type:
                service_type.append(x.service_type)
        customer_data=Customer.query.filter(Customer.customer_id==customer_id).first()
        c_stat=customer_data.customer_status
        service_history=ServiceRequest.query.filter(ServiceRequest.customer_id==customer_id).all()
        for x in service_history:
            if x.srp is None:
                serv_hist_list.append([x.sr_id,x.sr.service_type,x.sr.service_name,None,None,None,x.date_of_req,x.service_status,x.service_rating,x.pro_rating])
            else:
                serv_hist_list.append([x.sr_id,x.sr.service_type,x.sr.service_name,x.srp.pro_name,x.srp.pro_exp,x.srp.pro_contact_no,x.date_of_req,x.service_status,x.service_rating,x.pro_rating])
        return render_template('home_customer.html',c_id=customer_id,c_data=customer_data,s_data=service_type,serv_hist=serv_hist_list,status=c_stat)
    
    
@app.route('/customer/<int:customer_id>/book/<string:service_type>',methods=["GET"])
def customer_booking(customer_id,service_type):
    if request.method=="GET":
        serv_hist_list=[]
        customer_data=Customer.query.filter(Customer.customer_id==customer_id).first()
        data=Service.query.filter(Service.service_type==service_type).all()
        service_history=ServiceRequest.query.filter(ServiceRequest.customer_id==customer_id).all()
        for x in service_history:
            if x.srp is None:
                serv_hist_list.append([x.sr_id,x.sr.service_type,x.sr.service_name,None,None,None,x.date_of_req,x.service_status,x.service_rating,x.pro_rating])
            else:
                serv_hist_list.append([x.sr_id,x.sr.service_type,x.sr.service_name,x.srp.pro_name,x.srp.pro_exp,x.srp.pro_contact_no,x.date_of_req,x.service_status,x.service_rating,x.pro_rating])
        return render_template('services_booking.html',service=data, c_id=customer_id, c_data=customer_data,serv_hist=serv_hist_list)
    
@app.route('/customer/<int:customer_id>/booked/<int:service_id>',methods=["GET"])
def customer_serv_booked(customer_id,service_id):
    if request.method=="GET":
        d=datetime.datetime.now()
        day=d.day
        month=d.month
        year=d.year
        date=str(day)+"-"+str(month)+"-"+str(year)
        service_hist=ServiceRequest.query.filter((ServiceRequest.customer_id==customer_id)&(ServiceRequest.service_id==service_id)&(ServiceRequest.service_status=='Requested')).first()
        if service_hist is not None:
            return redirect (url_for('customer_home',customer_id=customer_id))
        service=ServiceRequest(service_id=service_id, customer_id=customer_id, date_of_req=date,service_status="Requested")
        db.session.add(service)
        db.session.commit()
        return redirect (url_for('customer_home',customer_id=customer_id))

@app.route('/customer/profile/<int:customer_id>',methods=['GET','POST'])
def customer_profile(customer_id):
    if request.method=="GET":
        customer_data=Customer.query.filter(Customer.customer_id==customer_id).first()
        return render_template('profile_customer.html',c_id=customer_data.customer_id,data=customer_data)
    
    elif request.method=="POST":
        try:
            c_name=str(request.form['fullname'])
            c_phone=int(request.form['c_contact_no'])
            c_add=str(request.form['address'])
            c_pin=int(request.form['pincode'])
            if len(str(c_phone))!=10:
                return redirect (url_for('customer_home',customer_id=customer_id))
            else:
                c=Customer.query.filter(Customer.customer_id==customer_id).first()
                c.customer_name=c_name
                c.customer_contact_no=c_phone
                c.customer_address=c_add
                c.customer_pincode=c_pin
                db.session.commit()
                return redirect (url_for('customer_home',customer_id=customer_id))
        except ValueError:
            return redirect (url_for('customer_home',customer_id=customer_id))

@app.route('/customer/<int:customer_id>/service/close/<int:sr_id>',methods=["GET","POST"])
def service_close(customer_id,sr_id):
    if request.method=="GET":
        d=datetime.datetime.now()
        day=d.day
        month=d.month
        year=d.year
        date=str(day)+"-"+str(month)+"-"+str(year)
        s=ServiceRequest.query.filter(ServiceRequest.sr_id==sr_id).first()
        s.date_of_comp=date
        db.session.commit()
        serv_req=ServiceRequest.query.filter(ServiceRequest.sr_id==sr_id).all()
        serv_req_data=[]
        for x in serv_req:
            serv_req_data.append([x.sr_id,x.sr.service_type,x.sr.service_name,x.sr.service_price,x.sr.service_duration,x.date_of_req,x.date_of_comp,x.srp.pro_name,x.srp.pro_contact_no])
        return render_template('service_remarks.html',data=serv_req_data,c_id=customer_id)
        
    elif request.method=="POST":
        s_rating=int(request.form['inlineRadioOptions'])
        p_rating=int(request.form['inlineRadioOptions_pro'])
        s_review=str(request.form['service_rev'])
        s=ServiceRequest.query.filter(ServiceRequest.sr_id==sr_id).first()
        s.service_rating=s_rating
        s.pro_rating=p_rating
        s.service_remarks=s_review
        s.service_status="Closed"
        db.session.commit()
        return redirect (url_for('customer_home',customer_id=customer_id))
    

@app.route('/customer/<int:customer_id>/service/cancel/<int:sr_id>',methods=["GET"])
def service_cancel(customer_id,sr_id):
    if request.method=="GET":
        s=ServiceRequest.query.filter(ServiceRequest.sr_id==sr_id).first()
        s.service_status="Cancelled"
        db.session.commit()
        return redirect (url_for('customer_home',customer_id=customer_id))

@app.route('/customer/search/<int:customer_id>',methods=["GET","POST"])
def customer_search(customer_id):
    if request.method=="GET":
        options=['Services','ServiceRequests']
        return render_template('search_customer.html',data=options,c_id=customer_id)
    elif request.method=="POST":
        search_q=request.form['search_q']
        table=request.form['search_cat']
        options=['Services','ServiceRequests']
        if search_q and table:
            if table=="Services":
                service_data=Service.query.filter((Service.service_type==search_q)|(Service.service_name==search_q)|(Service.service_price==search_q)|(Service.service_duration==search_q)).all()
                cols=Service.__table__.columns.keys()
                return render_template('search_customer.html',data=options,dtable=service_data,data_cols=cols,table_name=table,c_id=customer_id)
            elif table=="ServiceRequests":
                data=ServiceRequest.query.filter((ServiceRequest.customer_id==customer_id)&(ServiceRequest.service_rating==search_q)|(ServiceRequest.date_of_comp==search_q)|(ServiceRequest.date_of_req==search_q)|(ServiceRequest.pro_rating==search_q)|(ServiceRequest.service_status==search_q)).all()
                cols=ServiceRequest.__table__.columns.keys()
                cols.remove('customer_id')
                return render_template('search_customer.html',data=options,dtable=data,data_cols=cols,table_name=table,c_id=customer_id)
        elif table:
            if table=="Services":
                service_data=Service.query.all()
                cols=Service.__table__.columns.keys()
                return render_template('search_customer.html',data=options,dtable=service_data,data_cols=cols,table_name=table,c_id=customer_id)
            elif table=="ServiceRequests":
                data=ServiceRequest.query.filter(ServiceRequest.customer_id==customer_id).all()
                cols=ServiceRequest.__table__.columns.keys()
                cols.remove('customer_id')
                return render_template('search_customer.html',data=options,dtable=data,data_cols=cols,table_name=table,c_id=customer_id)
        else:
            return redirect(url_for('customer_search',customer_id=customer_id))

@app.route('/customer/summary/<int:customer_id>',methods=['GET'])
def customer_summary(customer_id):
    ratings_service=[]
    ratings_pro=[]
    labels_service=['1 Star','2 Stars','3 Stars','4 Stars','5 Stars']
    labels_pro=['1 Star','2 Stars','3 Stars','4 Stars','5 Stars']
    for x in range(1,6):
        customer_ratings=ServiceRequest.query.filter((ServiceRequest.customer_id==customer_id)&(ServiceRequest.service_rating==x)).count()
        ratings_service.append(customer_ratings)
    for x in range(1,6):
        c_ratings=ServiceRequest.query.filter((ServiceRequest.customer_id==customer_id)&(ServiceRequest.pro_rating==x)).count()
        ratings_pro.append(c_ratings)
    return render_template('summary_customer.html',c_id=customer_id,data_pro_ratings=ratings_pro,labels_pro_ratings=labels_pro,data_service=ratings_service,labels_service=labels_service)
    

'''Admin Page Functionality'''
@app.route('/admin/home',methods=["GET","POST"])
def admin_home():
    if request.method=="GET":
        serv_hist_list=[]
        services_data=Service.query.all()
        pro_data=Professional.query.filter(Professional.pro_status=='Pending').all()
        service_reqs=ServiceRequest.query.all()
        for x in service_reqs:
            if x.srp is None:
                serv_hist_list.append([x.sr_id,x.sr.service_name,None,None,x.date_of_req,x.service_status])
            else:
                serv_hist_list.append([x.sr_id,x.sr.service_name,x.srp.pro_name,x.srp.pro_contact_no,x.date_of_req,x.service_status])
        return render_template('home_admin.html',service=services_data, pro=pro_data,serv_reqs=serv_hist_list)


@app.route("/admin/service_create",methods=["GET","POST"])
def admin_new_service():
    if request.method=='GET':
        return render_template('service_create.html',service_data=service_type_list)
    
    elif request.method=='POST':
        try:
            s_type=str(request.form['service_type'])
            s_name=str(request.form['service_name'])
            s_price=int(request.form['service_price'])
            s_duration=int(request.form['service_duration'])
            s_desc=str(request.form['service_desc'])
            data=Service.query.filter((Service.service_type==s_type)&(Service.service_name==s_name)).first()
            if data:
                return redirect('/admin/service_create')
            new_service=Service(service_type=s_type, service_name=s_name, service_price=s_price, service_duration=s_duration, service_desc=s_desc)
            db.session.add(new_service)
            db.session.commit()
            return redirect('/admin/home')
        except ValueError:
            return redirect('/admin/service_create')
            
@app.route('/admin/service_update/<int:service_id>',methods=["GET","POST"])
def service_update(service_id):
    if request.method=="GET":
        service_data=Service.query.filter(Service.service_id==service_id).first()
        return render_template('service_update.html',data=service_data,service_data=service_type_list)
    
    elif request.method=="POST":
        try:
            s_type=str(request.form['service_type'])
            s_name=str(request.form['service_name'])
            s_price=int(request.form['service_price'])
            s_duration=int(request.form['service_duration'])
            s_desc=str(request.form['service_desc'])
            updated_service=Service.query.filter(Service.service_id==service_id).first()
            updated_service.service_type=s_type
            updated_service.service_name=s_name
            updated_service.service_price=s_price
            updated_service.service_duration=s_duration
            updated_service.service_desc=s_desc
            db.session.commit()
            return redirect('/admin/home')
        except ValueError:
            return redirect('/admin/home')

@app.route("/admin/service_delete/<int:service_id>",methods=["GET"])
def service_delete(service_id):
    delete_service=Service.query.filter(Service.service_id==service_id).first()
    db.session.delete(delete_service)
    db.session.commit()
    return redirect('/admin/home')

@app.route("/admin/pro/approve/<int:pro_id>",methods=["GET"])
def pro_approve(pro_id):
    pro_data=Professional.query.filter(Professional.pro_id==pro_id).first()
    pro_data.pro_status='Active'
    db.session.commit()
    p_data=Professional.query.filter(Professional.pro_id==pro_id).first()
    p_email=p_data.pro_email
    p_password=p_data.pro_password
    new_user=User(user_email=p_email, user_password=p_password, user_role="Professional")
    db.session.add(new_user)
    db.session.commit()
    return redirect('/admin/home')

@app.route("/admin/pro/reject/<int:pro_id>",methods=["GET"])
def pro_reject(pro_id):
    p_data=Professional.query.filter(Professional.pro_id==pro_id).first()
    db.session.delete(p_data)
    db.session.commit()
    return redirect('/admin/home')

@app.route('/admin/service/<int:service_id>',methods=["GET"])
def service_details(service_id):
    serv_data=Service.query.filter(Service.service_id==service_id).all()
    return render_template('service_details.html',serv_data=serv_data)

@app.route('/admin/pro_details/<int:pro_id>',methods=["GET"])
def pro_details(pro_id):
    pro_data=Professional.query.filter(Professional.pro_id==pro_id).all()
    return render_template('professional_details.html',pro_data=pro_data)



@app.route('/admin/service_req/<int:sr_id>',methods=["GET"])
def service_req_details(sr_id):
    serv_req_data=ServiceRequest.query.filter(ServiceRequest.sr_id==sr_id).all()
    for y in serv_req_data:
        stat=y.service_status
    data=[]
    for x in serv_req_data:
        if x.srp is None:
                data.append([x.sr_id, x.customer_id, x.cr.customer_name, x.sr.service_type, x.sr.service_name, None, None, x.date_of_req, None, x.service_status,None,None,None])
        else:
            data.append([x.sr_id, x.customer_id, x.cr.customer_name, x.sr.service_type, x.sr.service_name, x.srp.pro_name, x.srp.pro_contact_no, x.date_of_req, x.date_of_comp, x.service_status,x.service_remarks,x.service_rating,x.pro_rating])

    return render_template('service_request_details.html',serv_req_data=data,status=stat)

@app.route('/admin/search',methods=["GET","POST"])
def admin_search():
    if request.method=="GET":
        options=['Services','ServiceRequests','Professionals','Customers','Users']
        return render_template('search_admin.html',data=options)
    
    elif request.method=="POST":
        search_q=request.form['search_q']
        table=request.form['search_cat']
        options=['Services','ServiceRequests','Professionals','Customers','Users']
        if search_q and table:
            if table=="Services":
                dt=db.session.query(Service).filter((Service.service_id==search_q)|(Service.service_duration==search_q)|(Service.service_type==search_q)|(Service.service_name==search_q)|(Service.service_price==search_q)).all()
                data_cols=Service.__table__.columns.keys()
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=dt,table_name=table)
            elif table=="ServiceRequests":
                dt=db.session.query(ServiceRequest).filter((ServiceRequest.sr_id==search_q)|(ServiceRequest.service_rating==search_q)|(ServiceRequest.pro_rating==search_q)|(ServiceRequest.service_status==search_q)|(ServiceRequest.date_of_comp==search_q)|(ServiceRequest.date_of_req==search_q)).all()
                data_cols=ServiceRequest.__table__.columns.keys()
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=dt,table_name=table)
            elif table=="Professionals":
                dt=db.session.query(Professional).filter((Professional.pro_status!='Pending')&(Professional.pro_id==search_q)|(Professional.pro_service_type==search_q)|(Professional.pro_exp==search_q)|(Professional.pro_status==search_q)|(Professional.pro_pincode==search_q)|(Professional.pro_name==search_q)).all()
                data_cols=Professional.__table__.columns.keys()
                data_cols.remove('pro_email')
                data_cols.remove('pro_password')
                sr=ServiceRequest.query.all()
                ratings={}
                avg=[]
                for y in sr:
                    if y.pro_id in ratings:
                        ratings[y.pro_id].append(y.pro_rating)
                    else:
                        ratings[y.pro_id] = [y.pro_rating]
                for pro in dt:
                    if pro.pro_id in ratings:
                        valid_ratings = [r for r in ratings[pro.pro_id] if r is not None]
                        
                        if len(valid_ratings) > 0:
                            avg_rating = sum(valid_ratings) / len(valid_ratings)
                        else:
                            avg_rating = 0.0
                    else:
                        avg_rating = 0.0

                    avg.append([pro.pro_id, avg_rating])
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=dt,table_name=table,ratings=avg)
            elif table=="Customers":
                dt=db.session.query(Customer).filter((Customer.customer_id==search_q)|(Customer.customer_pincode==search_q)|(Customer.customer_contact_no==search_q)|(Customer.customer_name==search_q)|(Customer.customer_status==search_q)).all()
                data_cols=Customer.__table__.columns.keys()
                data_cols.remove('customer_email')
                data_cols.remove('customer_password')
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=dt,table_name=table)  
            else:
                data_table=db.session.query(User).filter((User.user_id==search_q)|(User.user_email==search_q)|(User.user_role==search_q)).all()
                data_cols=User.__table__.columns.keys()
                data_cols.remove('user_password')
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=data_table,table_name=table)

        elif table:
            if table=="Services":
                data_table=Service.query.all()
                data_cols=Service.__table__.columns.keys()
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=data_table,table_name=table)
            elif table=="ServiceRequests":
                data_table=ServiceRequest.query.all()
                data_cols=ServiceRequest.__table__.columns.keys()
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=data_table,table_name=table)
            elif table=="Professionals":
                dt=Professional.query.filter(Professional.pro_status!='Pending').all()
                data_cols=Professional.__table__.columns.keys()
                data_cols.remove('pro_email')
                data_cols.remove('pro_password')
                sr=ServiceRequest.query.all()
                ratings={}
                avg=[]
                for y in sr:
                    if y.pro_id in ratings:
                        ratings[y.pro_id].append(y.pro_rating)
                    else:
                        ratings[y.pro_id] = [y.pro_rating]
                for pro in dt:
                    if pro.pro_id in ratings:
                        valid_ratings = [r for r in ratings[pro.pro_id] if r is not None]
                        
                        if len(valid_ratings) > 0:
                            avg_rating = sum(valid_ratings) / len(valid_ratings)
                        else:
                            avg_rating = 0.0
                    else:
                        avg_rating = 0.0

                    avg.append([pro.pro_id, avg_rating])
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=dt,table_name=table,ratings=avg)
            elif table=='Customers':
                data_table=Customer.query.all()
                data_cols=Customer.__table__.columns.keys()
                data_cols.remove('customer_email')
                data_cols.remove('customer_password')
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=data_table,table_name=table)
            else:
                data_table=User.query.all()
                data_cols=User.__table__.columns.keys()
                data_cols.remove('user_password')
                return render_template('search_admin.html',data=options,data_cols=data_cols,dtable=data_table,table_name=table)
        else:
            return redirect('/admin/search')

@app.route('/admin/pro/block/<int:pro_id>',methods=['GET'])
def pro_block(pro_id):
    if request.method=="GET":
        serv_data=ServiceRequest.query.filter(ServiceRequest.pro_id==pro_id).all()
        if serv_data:
            for x in serv_data:
                if x.service_status=='Accepted':
                    x.service_status='Cancelled'
                    db.session.commit()
            pro_data=Professional.query.filter(Professional.pro_id==pro_id).first()
            pro_data.pro_status='Blocked'
            db.session.commit()
            return redirect('/admin/search')
        else:
            pro_data=Professional.query.filter(Professional.pro_id==pro_id).first()
            pro_data.pro_status='Blocked'
            db.session.commit()
            return redirect('/admin/search')
            
@app.route('/admin/pro/unblock/<int:pro_id>',methods=['GET'])
def pro_unblock(pro_id):
    if request.method=="GET":
        pro_data=Professional.query.filter(Professional.pro_id==pro_id).first()
        pro_data.pro_status='Active'
        db.session.commit()
        return redirect('/admin/search')

@app.route('/admin/customer/block/<int:customer_id>',methods=['GET'])
def customer_block(customer_id):
    if request.method=="GET":
        serv_data=ServiceRequest.query.filter(ServiceRequest.customer_id==customer_id).all()
        if serv_data:
            for x in serv_data:
                if x.service_status=='Requested':
                    x.service_status='Cancelled'
                    db.session.commit()
                elif x.service_status=='Accepted':
                    x.service_status='Cancelled'
                    db.session.commit()
                else:
                    pass
            c_data=Customer.query.filter(Customer.customer_id==customer_id).first()
            c_data.customer_status='Blocked'
            db.session.commit()
            return redirect('/admin/search')
        else:
            c_data=Customer.query.filter(Customer.customer_id==customer_id).first()
            c_data.customer_status='Blocked'
            db.session.commit()
            return redirect('/admin/search')
@app.route('/admin/customer/unblock/<int:customer_id>',methods=['GET'])
def customer_unblock(customer_id):
    if request.method=="GET":
        c_data=Customer.query.filter(Customer.customer_id==customer_id).first()
        c_data.customer_status='Active'
        db.session.commit()
        return redirect('/admin/search')

@app.route('/admin/summary',methods=['GET'])
def admin_summary():
    if request.method=="GET":
        data_ratings=[]
        for x in range(1,6):
            serv_ratings=ServiceRequest.query.filter(ServiceRequest.service_rating==x).count()
            data_ratings.append(serv_ratings)
        labels_ratings=['1 Star','2 Stars','3 Stars','4 Stars','5 Stars']
        labels_service=['Accepted','Requested','Closed','Cancelled']
        accepted=ServiceRequest.query.filter(ServiceRequest.service_status=='Accepted').count()
        requested=ServiceRequest.query.filter(ServiceRequest.service_status=='Requested').count()
        closed=ServiceRequest.query.filter(ServiceRequest.service_status=='Closed').count()
        cancelled=ServiceRequest.query.filter(ServiceRequest.service_status=='Cancelled').count()
        service_data=[accepted,requested,closed,cancelled]
        return render_template('summary_admin.html',data_ratings=data_ratings,labels_ratings=labels_ratings,data_service=service_data,labels_service=labels_service)
    
