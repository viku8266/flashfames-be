import faiss
import pickle
import os


class FaissDataStore:
    """
    FaissDataStore is a class that implements a data store using Faiss.
    """
    # convert the class to a singleton class        
    def __new__(cls, dimention, disk_path):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FaissDataStore, cls).__new__(cls)
            base_index = faiss.IndexFlatL2(dimention)  # Create a base index
            cls.instance._index = faiss.IndexIDMap2(base_index)  # Wrap it with IndexIDMap2
            cls.instance.disk_path = disk_path
            if os.path.exists(cls.instance.disk_path):
                cls.instance.load_faiss_data_store()
        return cls.instance
        
    def __init__(self, dimention, disk_path):
        base_index = faiss.IndexFlatL2(dimention)  # Create a base index
        self._index = faiss.IndexIDMap2(base_index)  # Wrap it with IndexIDMap2
        self.disk_path = disk_path
        if os.path.exists(self.disk_path):
            self.load_faiss_data_store()

    def add(self, data, ids):
        idx = self._index.add_with_ids(data, ids)
        self.save_faiss_data_store()
        return idx

    def search(self, data):
        return self._index.search(data, 1)

    def save_faiss_data_store(self):
        with open(self.disk_path, 'wb') as f:
            pickle.dump(self._index, f)

    def load_faiss_data_store(self):
        with open(self.disk_path, 'rb') as f:
            self._index = pickle.load(f)
    
# cerate a method to return the FaissDataStore object  out of the class
    @staticmethod
    def get_faiss_data_store(dimention, disk_path):
        return FaissDataStore(dimention, disk_path + "/faiss_data_store.pkl")
   
