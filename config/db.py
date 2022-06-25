from sqlalchemy import create_engine,MetaData
engine = create_engine("mysql+pymysql://root:Gitsum123$@localhost/test")
meta=MetaData()
con=engine.connect()