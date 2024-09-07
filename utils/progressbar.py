from tqdm import tqdm as original_tqdm

def tqdm(*args, **kwargs):
    return original_tqdm(*args, leave=False, ascii=True, **kwargs)
