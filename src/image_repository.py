import json
from sqlalchemy import Column, Integer, String, Text
from database_config import Base, engine, session
# Define the new table for images
class ImageData(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(String(255), unique=True)
    meta_data = Column(Text)


    # create to dict function
    def to_dict(self):
        meta_data_json = json.loads(self.meta_data)
        return {
            'id': self.id,
            'image_id': self.image_id,
            'image_path': meta_data_json.get('image_path').split('/')[-1]
        }

    #create a function to insert the data into the database
    # 
def insert_data(image_id, image_path, num_of_faces):
    meta_data = {"num_of_faces": num_of_faces, "image_path": image_path}
    meta_data_json = json.dumps(meta_data)  # Convert dictionary to JSON string
    new_data = ImageData(image_id=image_id, meta_data=meta_data_json)
    session.add(new_data)
    session.commit()
    return new_data

def fetch_images_by_ids(image_ids):
    return session.query(ImageData).filter(ImageData.id.in_(image_ids)).all()


def fetch_all_images():
    return session.query(ImageData).all()

def to_dict(self):
    meta_data_json = json.loads(self.meta_data)
    return {
        'id': self.id,
        'image_id': self.image_id,
        'num_of_faces': meta_data_json.get('num_of_faces')
    }

# Create the table in the database
Base.metadata.create_all(engine) 
