import faiss
import numpy as np

faiss_index = None
job_id_map = []

def build_faiss_index(job_vectors, job_ids):
    global faiss_index, job_id_map
    dim = job_vectors.shape[1] # dimension of the vectors
    faiss_index = faiss.IndexFlatL2(dim)
    faiss_index.add(job_vectors.astype(np.float32))
    job_id_map = job_ids
    

def get_top_jobs(user_vector, top_k=5):
    D, I = faiss_index.search(user_vector.astype(np.float32), top_k+10)
    return [job_id_map[i] for i in I[0]]