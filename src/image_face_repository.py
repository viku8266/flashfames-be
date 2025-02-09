from sqlalchemy import Column, Integer, ForeignKey
from database_config import Base, engine, session

# Define the mapping table for image_id and face_id
class ImageFaceMapping(Base):
    __tablename__ = 'image_face_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    face_id = Column(Integer, ForeignKey('face.id'))

# Create the table in the database
Base.metadata.create_all(engine)

# Function to insert data into the mapping table
def insert_mapping(image_id, face_id):
    new_mapping = ImageFaceMapping(image_id=image_id, face_id=face_id)
    session.add(new_mapping)
    session.commit()
    return new_mapping.id

def fetch_image_ids_by_face_ids(face_ids):
    mappings = session.query(ImageFaceMapping).filter(ImageFaceMapping.face_id.in_(face_ids)).all()
    return [mapping.image_id for mapping in mappings] 