CREATE OR REPLACE FUNCTION public.get_embedding_bert_f(
	sentence text)
    RETURNS double precision[]
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
  from sentence_transformers import SentenceTransformer
  import numpy as np
  import plpy
  import os
  import torch
  # Force PyTorch to use only CPU
  if 'model' not in SD:
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    torch.set_num_threads(1)
    device = "cpu" # Explicitly set to CPU to avoid confusion
    # Initialize the model (consider doing this outside the function for efficiency)
    SD['model'] = SentenceTransformer('all-distilroberta-v1').to(device)
    plpy.notice("Model Loaded")
#  else:
#    plpy.notice("Model reused from SD")
  model = SD['model']
  embedding = model.encode([sentence], convert_to_tensor=True)
  embedding_list = embedding[0].tolist()
  return embedding_list
$BODY$;
