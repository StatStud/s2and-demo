import random

def generate_signatures():
  with open('data/papers.json') as f:
    papers = json.load(f)
  signatures = {}
  author_id_set = set()
  for paper_id, paper in papers.items():
    for author in paper['authors']:
      author_id = random.randint(1000000, 9999999)
      while author_id in author_id_set:
        author_id = random.randint(1000000, 9999999)
      author_id_set.add(author_id)
      signature_id = len(signatures)
      given_block = author['author_name'].split()[0][0].lower()
      last_name = author['author_name'].split()[-1].lower()
      block = given_block + ' ' + last_name
      author_info = {
        'given_block': given_block + ' ' + last_name,
        'block': block,
        'position': author['position'],
        'first': author['author_name'].split()[0],
        'middle': ' '.join(author['author_name'].split()[1:-1]) or None,
        'last': last_name,
        'suffix': None,
        'affiliations': [],
        'email': None
      }
      signatures[str(signature_id)] = {
        'author_id': author_id,
        'paper_id': int(paper_id),
        'signature_id': str(signature_id),
        'author_info': author_info
      }
  with open('data/signatures.json', 'w') as f:
    json.dump(signatures, f, indent=4)
  return 2
