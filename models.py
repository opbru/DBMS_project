from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'USER'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(150), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    computer_type = db.Column(db.String(50), db.ForeignKey('COMPUTER_TYPE.name'), nullable=True)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class Component(db.Model):
    __tablename__ = 'component'
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    
    def as_dict(self):
        return {
            "name": self.name,
            "price": self.price
        }

class CPU(db.Model):
    __tablename__ = 'CPU'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    component_ID = db.Column(db.Integer, db.ForeignKey('component.ID'), nullable=False)
    socket = db.Column(db.String(50), nullable=False)
    watt = db.Column(db.String(50), nullable=False)
    benchmark = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    
    def as_dict(self):
        component = Component.query.get(self.component_ID)
        return {
            "name": self.name,
            "price": component.price,
            "benchmark": self.benchmark
        }
    
class MB(db.Model):
    __tablename__ = 'MB'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    component_ID = db.Column(db.Integer, db.ForeignKey('component.ID'), nullable=False)
    socket = db.Column(db.String(50), nullable=False)
    form_factor = db.Column(db.String(50), nullable=False)
    interface = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    
    def as_dict(self):
        component = Component.query.get(self.component_ID)
        return {
            "name": self.name,
            "price": component.price
        }
    
class RAM(db.Model):
    __tablename__ = 'RAM'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    component_ID = db.Column(db.Integer, db.ForeignKey('component.ID'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    channel = db.Column(db.String(50), nullable=False)
    interface = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    
    def as_dict(self):
        component = Component.query.get(self.component_ID)
        return {
            "name": self.name,
            "price": component.price
        }
    
class SSD(db.Model):
    __tablename__ = 'SSD'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    component_ID = db.Column(db.Integer, db.ForeignKey('component.ID'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    interface = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)

    def as_dict(self):
        component = Component.query.get(self.component_ID)
        return {
            "name": self.name,
            "price": component.price
        }
        
class HDD(db.Model):
    __tablename__ = 'HDD'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    component_ID = db.Column(db.Integer, db.ForeignKey('component.ID'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    
    def as_dict(self):
        component = Component.query.get(self.component_ID)
        return {
            "name": self.name,
            "price": component.price
        }
    
class GPU(db.Model):
    __tablename__ = 'GPU'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    component_ID = db.Column(db.Integer, db.ForeignKey('component.ID'), nullable=False)
    memory = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Float, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    benchmark = db.Column(db.Integer, nullable=False)
    
    def as_dict(self):
        component = Component.query.get(self.component_ID)
        return {
            "name": self.name,
            "price": component.price,
            "benchmark": self.benchmark
        }
        
class CHASSIS(db.Model):
    __tablename__ = 'CHASSIS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    component_ID = db.Column(db.Integer, db.ForeignKey('component.ID'), nullable=False)
    GPU_size = db.Column(db.Float, nullable=False)
    mb_form_factor = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    
    def as_dict(self):
        component = Component.query.get(self.component_ID)
        return {
            "name": self.name,
            "price": component.price
        }

class PSU(db.Model):
    __tablename__ = 'PSU'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    component_ID = db.Column(db.Integer, db.ForeignKey('component.ID'), nullable=False)
    watt = db.Column(db.String(50), nullable=False)
    module = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    
    def as_dict(self):
        component = Component.query.get(self.component_ID)
        return {
            "name": self.name,
            "price": component.price
        }
    
class COMPUTER_TYPE(db.Model):
    __tablename__ = 'COMPUTER_TYPE'
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    cpu_ratio = db.Column(db.Float)
    mb_ratio = db.Column(db.Float)
    ram_ratio = db.Column(db.Float)
    ssd_ratio = db.Column(db.Float)
    hdd_ratio = db.Column(db.Float)
    gpu_ratio = db.Column(db.Float)
    chassis_ratio = db.Column(db.Float)
    psu_ratio = db.Column(db.Float)
    
class UserSelections(db.Model):
    __tablename__ = 'UserSelections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False)
    component_type = db.Column(db.String(50), nullable=False)
    component_id = db.Column(db.Integer, nullable=False)

    


