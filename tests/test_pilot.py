"""Integrity tests for the actual pilot and common data failures."""
import copy,importlib.util,json,pathlib,tempfile,unittest
P=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pilot',P/'src/run_pilot.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class PilotTests(unittest.TestCase):
 def setUp(self):self.data=m.load_data(P/'data/pilot.json')
 def check_bad(self,data):
  with tempfile.TemporaryDirectory() as tmp:
   f=pathlib.Path(tmp)/'bad.json';f.write_text(json.dumps(data))
   with self.assertRaises(ValueError):m.load_data(f)
 def test_duplicate_claim_rejected(self):
  self.data[0]['claims'][1]['id']=self.data[0]['claims'][0]['id'];self.check_bad(self.data)
 def test_missing_source_anchor_rejected(self):
  self.data[0]['claims'][0]['source_anchor']='nonexistent evidence';self.check_bad(self.data)
 def test_unanchored_preserved_unit_rejected(self):
  self.data[0]['claims'][0]['summary_evidence']='nonexistent evidence';self.check_bad(self.data)
 def test_omitted_with_evidence_rejected(self):
  c=next(c for c in self.data[0]['claims'] if c['status']=='omitted');c['summary_evidence']='some text';self.check_bad(self.data)
 def test_graph_endpoints_and_degree_identity(self):
  for p in self.data:
   for v in ['source','summary']:
    nodes,edges=m.graph(p,v);ids={n['id'] for n in nodes};self.assertTrue(all(a in ids and b in ids for a,b,_ in edges));s=m.stats(nodes,edges)
    self.assertEqual(sum(int(k)*n for k,n in s['degree_distribution'].items()),2*len(edges))
 def test_summary_graph_exact_saved_alignment(self):
  for p in self.data:
   ids={n['id'] for n in m.graph(p,'summary')[0]};expected={p['id']}|{c['id'] for c in p['claims'] if c['status']=='preserved'};self.assertEqual(ids,expected)
 def test_full_export_and_graphml(self):
  import xml.etree.ElementTree as ET
  with tempfile.TemporaryDirectory() as tmp:
   result=m.run(P/'data/pilot.json',tmp,False)
   self.assertEqual(result['totals'],dict(papers=3,selected_units=30,preserved=20,omitted=10))
   for p in self.data:
    for v in ['source','summary']:
     f=pathlib.Path(tmp)/(p['id']+'_'+v+'.graphml');tree=ET.parse(f);self.assertEqual(len(tree.findall('.//{*}node')),m.stats(*m.graph(p,v))['nodes'])
   for f in ['interactive_graphs.html','validation_log.md','annotation_review.csv','graph_statistics.csv']:self.assertTrue((pathlib.Path(tmp)/f).is_file())
if __name__=='__main__':unittest.main()
