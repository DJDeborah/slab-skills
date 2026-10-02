import copy,hashlib,importlib.util,json,tempfile,unittest,csv,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(skill,script):
    path=ROOT/'skills'/skill/'scripts'/(script+'.py');s=importlib.util.spec_from_file_location(script,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def asset(skill,name):return json.loads((ROOT/'skills'/skill/'assets'/name).read_text(encoding='utf-8'))
sig=load('research-significance','audit_significance');gap=load('research-gap','audit_gap');writing=load('research-writing','audit_manuscript');fem=load('fem-explicit-bifurcation','prepare_explicit');energy=load('fem-explicit-bifurcation','audit_history');events=load('fem-explicit-bifurcation','detect_events');branches=load('fem-explicit-bifurcation','branch_benchmarks')
spec=importlib.util.spec_from_file_location('installer',ROOT/'tools'/'install.py');installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)

class SignificanceTests(unittest.TestCase):
    def setUp(self):self.d=asset('research-significance','significance.json')
    def test_prospective_contract(self):self.assertTrue(sig.audit(self.d)['pass'])
    def test_calibration_holdout_leak(self):
        self.d.update(calibration_cases=['G1'],holdout_cases=['G1']);self.assertFalse(sig.audit(self.d)['pass'])
    def test_unbacked_holdout(self):
        self.d['evidence_tier']='holdout';self.assertFalse(sig.audit(self.d)['pass'])
    def test_no_rival_test(self):
        self.d['rivals'][0]['discriminating_test']='';self.assertFalse(sig.audit(self.d)['pass'])
    def test_nonfinite_falsifier(self):
        self.d['falsifier']['threshold']=float('nan');self.assertFalse(sig.audit(self.d)['pass'])
    def test_missing_decision(self):
        self.d['decision']='';self.assertFalse(sig.audit(self.d)['pass'])

class GapTests(unittest.TestCase):
    def setUp(self):
        self.d=asset('research-gap','gap.json')
        with open(ROOT/'skills'/'research-gap'/'assets'/'search-ledger.csv',encoding='utf-8',newline='') as f:self.rows=list(csv.DictReader(f))
    def test_bounded_fixture(self):self.assertTrue(gap.audit(self.d,self.rows)['pass'])
    def test_universal_absence_rejected(self):
        self.d['claim_type']='universal';self.assertFalse(gap.audit(self.d,self.rows)['pass'])
    def test_unknown_citation(self):
        self.d['nearest_studies'][0]['study_id']='INVENTED';self.assertFalse(gap.audit(self.d,self.rows)['pass'])
    def test_missing_source_passage(self):
        self.rows[0]['passage']='';self.assertFalse(gap.audit(self.d,self.rows)['pass'])
    def test_doi_duplicate(self):
        self.rows[0]['doi']='https://doi.org/10.123/ABC';r=dict(self.rows[0],study_id='OTHER',doi='doi:10.123/abc');self.rows.append(r);self.assertFalse(gap.audit(self.d,self.rows)['pass'])
    def test_unknown_not_absence(self):
        self.d['nearest_studies'][0]['assessment']='unknown';r=gap.audit(self.d,self.rows);self.assertTrue(r['pass']);self.assertTrue(any('Unknown' in w for w in r['warnings']))
    def test_future_search(self):
        self.rows[0]['searched_on']='2026-10-03';self.assertFalse(gap.audit(self.d,self.rows)['pass'])

class WritingTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name);(self.base/'evidence.txt').write_text('synthetic measured observable')
        self.d={'claims':[{'id':'C1','status':'supported','evidence_ids':['E1']}],'figures':[{'id':'F1','evidence_ids':['E1']}],'evidence':[{'id':'E1','path':'evidence.txt','role':'numerical-verification','sha256':hashlib.sha256((self.base/'evidence.txt').read_bytes()).hexdigest()}],'required_assets':['C1','F1']};self.text='A bounded result [claim:C1], shown in the comparison [figure:F1].'
    def tearDown(self):self.temp.cleanup()
    def test_traceable_draft(self):self.assertTrue(writing.audit(self.d,self.text,self.base)['pass'])
    def test_dropped_core_figure(self):self.assertFalse(writing.audit(self.d,'Result [claim:C1]',self.base)['pass'])
    def test_hash_tampering(self):
        (self.base/'evidence.txt').write_text('changed');self.assertFalse(writing.audit(self.d,self.text,self.base)['pass'])
    def test_missing_file(self):
        self.d['evidence'][0]['path']='absent.csv';self.assertFalse(writing.audit(self.d,self.text,self.base)['pass'])
    def test_proposal_cannot_support_claim(self):
        self.d['evidence'][0]['role']='proposal';self.assertFalse(writing.audit(self.d,self.text,self.base)['pass'])
    def test_path_escape(self):
        self.d['evidence'][0]['path']='../outside';self.assertFalse(writing.audit(self.d,self.text,self.base)['pass'])

class FEMTests(unittest.TestCase):
    def setUp(self):self.c=asset('fem-explicit-bifurcation','beam-explicit.json')
    def test_bc_registration(self):
        deck,r=fem.prepare(self.c);self.assertEqual(r['regions']['TIP'],[21]);self.assertAlmostEqual(r['expected_small_deflection_tip_reaction_N'],-0.0525);self.assertIn('*Dynamic, Explicit',deck)
    def test_empty_selection(self):
        self.c['regions']['ROOT']['bbox']=[1,2,1,2]
        with self.assertRaisesRegex(ValueError,'selects'):fem.prepare(self.c)
    def test_duplicate_bc(self):
        self.c['constraints'].append(copy.deepcopy(self.c['constraints'][0]))
        with self.assertRaisesRegex(ValueError,'conflicting'):fem.prepare(self.c)
    def test_wrong_physical_boundary(self):
        self.c['regions']['ROOT']['bbox']=[4.999,5.001,-0.01,0.01]
        with self.assertRaisesRegex(ValueError,'ROOT at'):fem.prepare(self.c)
    def test_wrong_units(self):
        self.c['units']='SI'
        with self.assertRaisesRegex(ValueError,'units'):fem.prepare(self.c)
    def test_unphysical_density(self):
        self.c['material']['density']=-1
        with self.assertRaisesRegex(ValueError,'density'):fem.prepare(self.c)
    def test_written_input_hash(self):
        with tempfile.TemporaryDirectory() as t:
            p=subprocess.run([sys.executable,str(ROOT/'skills/fem-explicit-bifurcation/scripts/prepare_explicit.py'),str(ROOT/'skills/fem-explicit-bifurcation/assets/beam-explicit.json'),'--out',t],capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr);r=json.loads((Path(t)/'registration.json').read_text());self.assertEqual(hashlib.sha256((Path(t)/'beam_explicit.inp').read_bytes()).hexdigest(),r['input_sha256'])
    def history(self,ke=0.001):
        return {'completed':True,'history':[{'time':t,'U2':-0.1*t/.25,'RF2':-.0525*t/.25,'ALLIE':t,'ALLKE':ke*t,'ALLAE':0.0} for t in (0.0,.125,.25)]}
    def test_energy_positive_control(self):self.assertTrue(energy.audit(self.history(),self.c)['pass'])
    def test_inertia_failure(self):self.assertFalse(energy.audit(self.history(1.0),self.c)['pass'])
    def test_noncompleted_job(self):
        d=self.history();d['completed']=False;self.assertFalse(energy.audit(d,self.c)['pass'])
    def test_zero_energy_mask(self):
        d=self.history()
        for r in d['history']:r['ALLIE']=0.0
        self.assertFalse(energy.audit(d,self.c)['pass'])
    def test_nonfinite_history(self):
        d=self.history();d['history'][1]['ALLKE']=float('nan');self.assertFalse(energy.audit(d,self.c)['pass'])
    def test_exact_branch_oracle(self):
        r=branches.compute();self.assertTrue(r['pass']);self.assertTrue(any(x['lambda']==0 and x['tangent']==0 for x in r['pitchfork']));self.assertIn('no FE branch',r['scope'])
    def test_force_event_not_bifurcation(self):
        r=events.detect([{'time':i,'RF2':f} for i,f in enumerate([1,1,1,.6,.6,.6])],{'window_samples':2,'force_drop_fraction':.2});self.assertTrue(r['events']);self.assertIn('no equilibrium bifurcation',r['scope'])
    def test_no_drop_control(self):self.assertEqual(events.detect([{'time':i,'RF2':i+1} for i in range(6)],{})['events'],[])
    def test_opening_persistence(self):
        rows=[{'time':i,'RF2':1,'angle':v} for i,v in enumerate([0,.2,0,.2,.2,.2])];r=events.detect(rows,{'opening_field':'angle','opening_threshold':.1,'persistence_samples':3});self.assertEqual(r['events'][0]['time'],3)

class InstallationTests(unittest.TestCase):
    def test_install_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            dest=Path(t)/'.agents/skills';paths=installer.install(ROOT/'skills',dest,installer.NAMES);self.assertEqual(len(paths),len(installer.NAMES));self.assertTrue((dest/'fem-explicit-bifurcation/scripts/prepare_explicit.py').is_file())
            with self.assertRaises(FileExistsError):installer.install(ROOT/'skills',dest,installer.NAMES)
    def test_no_partial_install_on_conflict(self):
        with tempfile.TemporaryDirectory() as t:
            dest=Path(t);(dest/'research-gap').mkdir()
            with self.assertRaises(FileExistsError):installer.install(ROOT/'skills',dest,installer.NAMES)
            self.assertFalse((dest/'research-significance').exists())
    def test_duplicate_selection(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):installer.install(ROOT/'skills',Path(t),['research-gap','research-gap'])

if __name__=='__main__':unittest.main()
