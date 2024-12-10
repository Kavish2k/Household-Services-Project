from .database import db

class User(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email=db.Column(db.String(), nullable=False, unique=True)
    user_password=db.Column(db.String(), nullable=False)
    user_role=db.Column(db.String(), db.ForeignKey('role.role_name'), nullable=False)

class Role(db.Model):
    __tablename__="role"
    role_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name=db.Column(db.String(), nullable=False, unique=True)
    role_desc=db.Column(db.String())
    user_role=db.Relationship('User',backref='ur')


class Service(db.Model):
    __tablename__="service"
    service_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_type=db.Column(db.String(), nullable=False)
    service_name=db.Column(db.String(), nullable=False, unique=True)
    service_price=db.Column(db.Integer, nullable=False)
    service_duration=db.Column(db.Integer, nullable=False)
    service_desc=db.Column(db.String())
    service_req=db.Relationship('ServiceRequest',backref='sr',cascade='delete')

class Customer(db.Model):
    __tablename__="customer"
    customer_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name=db.Column(db.String(), nullable=False)
    customer_contact_no=db.Column(db.Integer, nullable=False)
    customer_email=db.Column(db.String(), nullable=False, unique=True)
    customer_password=db.Column(db.String(),nullable=False)
    customer_address=db.Column(db.String(),nullable=False)
    customer_pincode=db.Column(db.Integer,nullable=False)
    customer_status=db.Column(db.String())
    customer_req=db.Relationship('ServiceRequest',backref='cr')

class Professional(db.Model):
    __tablename__="professional"
    pro_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    pro_name=db.Column(db.String(), nullable=False)
    pro_contact_no=db.Column(db.Integer)
    pro_email=db.Column(db.String(), nullable=False, unique=True)
    pro_password=db.Column(db.String(), nullable=False)
    pro_service_type=db.Column(db.String(), nullable=False)
    pro_exp=db.Column(db.Integer, nullable=False)
    pro_pincode=db.Column(db.Integer, nullable=False)
    pro_status=db.Column(db.String())
    serv_req_pro=db.Relationship('ServiceRequest',backref='srp')
    


class ServiceRequest(db.Model):
    __tablename__="servicerequest"
    sr_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id=db.Column(db.Integer, db.ForeignKey('service.service_id'))
    customer_id=db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    pro_id=db.Column(db.Integer, db.ForeignKey('professional.pro_id'))
    date_of_req=db.Column(db.String(), nullable=False)
    date_of_comp=db.Column(db.String())
    service_status=db.Column(db.String(), nullable=False)
    service_remarks=db.Column(db.String())
    service_rating=db.Column(db.Integer)
    pro_rating=db.Column(db.Integer)
    
    












