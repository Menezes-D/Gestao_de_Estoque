import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLACHEMY_DATABASE_URI = 'mysql+pymysql://root2:usbw@localhost/test'