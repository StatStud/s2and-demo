import json
import pickle
import numpy as np
from transformers import AutoTokenizer, AutoModel
import os
from s2and.consts import PROJECT_ROOT_PATH
import argparse



def process_papers(input_file, output_file, data_dir):
  
  # define data dir
  dataset_name = data_dir
  DATA_DIR = os.path.join(PROJECT_ROOT_PATH, 'data', dataset_name)
  papers_path =os.path.join(DATA_DIR, dataset_name + "_papers.json")
  
  # load model and tokenizer
  tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
  model = AutoModel.from_pretrained('allenai/specter')

  # read papers from input file
  with open(input_file, 'r') as f:
    data = json.load(f)


  # extract title and abstract fields from the data
  papers = []
  paper_ids = []
  for key, paper_data in data.items():
    title = paper_data['title']
    abstract = paper_data.get('abstract', '')
    paper_ids.append(paper_data['paper_id'])
    papers.append({'title': title, 'abstract': abstract})
     
  title_abs = [d['title'] + tokenizer.sep_token + (d.get('abstract') or '') for d in papers]

  # preprocess the input
  inputs = tokenizer(title_abs, padding=True, truncation=True, return_tensors="pt", max_length=512)
  result = model(**inputs)

  # take the first token in the batch as the embedding
  embeddings = result.last_hidden_state[:, 0, :].detach().numpy()
   

  # create tuple with embeddings and paper ids
  #embeddings_with_ids = (embeddings,paper_ids)
  embeddings_with_ids = tuple((embeddings, paper_ids))

  # save tuple as pickle file
  with open(output_file, 'wb') as f:
    pickle.dump(embeddings_with_ids, f)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Process papers')
  parser.add_argument('input_file', help='Path to input JSON file')
  parser.add_argument('output_file', help='Path to output pickle file')
  parser.add_argument('data_dir', help='Path to data')
  args = parser.parse_args()

  process_papers(args.input_file, args.output_file, args.data_dir)
