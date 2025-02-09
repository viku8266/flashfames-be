from sqlalchemy import Column, Integer, String, Text
import json

from database_config import Base, session, engine


# Define the updated table
class FaceData(Base):
    __tablename__ = 'face'
    id = Column(Integer, primary_key=True, autoincrement=True)
    face_id = Column(String(255), unique=True)
    meta_data = Column(Text)

    def to_dict(self):
        meta_data_json = json.loads(self.meta_data)
        return {
            'id': self.id,
            'face_id': self.face_id,
            'face_image_path': meta_data_json["face_Image_path"].split("/")[-1]
        }

# Create the table in the database
Base.metadata.create_all(engine)

# Function to insert data into the database
def insert_data(face_id, face_Image_path):
    meta_data = {"face_Image_path": face_Image_path}
    meta_data_json = json.dumps(meta_data)  # Convert dictionary to JSON string
    new_data = FaceData(face_id=face_id, meta_data=meta_data_json)
    session.add(new_data)
    session.commit()
    return new_data

# Function to fetch data from the database
def fetch_data():
    return session.query(FaceData).all()

# Function to update data in the database
def update_data(data_id, new_face_id, new_meta_data):
    data = session.query(FaceData).filter(FaceData.id == data_id).first()
    if data:
        data.face_id = new_face_id
        data.meta_data = new_meta_data
        session.commit()

# Function to delete data from the database
def delete_data(data_id):
    data = session.query(FaceData).filter(FaceData.id == data_id).first()
    if data:
        session.delete(data)
        session.commit() 