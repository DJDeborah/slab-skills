import copy,hashlib,importlib.util,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1];SD=ROOT/'skills/abaqus-parametric-workflow/scripts'
# Keep the self-contained sweep adapter's namespace isolated from the older test module.
spec=importlib.util.spec_from_file_location('prepare_explicit',SD/'prepare_explicit.py');fem=importlib.util.module_from_spec(spec);spec.loader.exec_module(fem);sys.modules['prepare_explicit']=fem
spec=importlib.util.spec_from_file_location('prepare_sweep',SD/'prepare_sweep.py');plan=importlib.util.module_from_spec(spec);spec.loader.exec_module(plan);sys.modules['prepare_sweep']=plan
spec=importlib.util.spec_from_file_location('run_sweep',SD/'run_sweep.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)

class SweepTests(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((ROOT/'skills/abaqus-parametric-workflow/assets/sweep.json').read_text());self.temp=tempfile.TemporaryDirectory();self.out=Path(self.temp.name)/'study'
    def tearDown(self):self.temp.cleanup()
    def test_plan_frozen_and_no_solver(self):
        d=plan.prepare(self.d,self.out,2);self.assertEqual(len(d['cases']),2);runner.verify_plan(d,self.out);self.assertFalse(runner.run(d,self.out,'missing-abaqus')['solver_launched'])
    def test_stable_ids(self):self.assertEqual([r['case_id'] for r in plan.configurations(self.d,2)],[r['case_id'] for r in plan.configurations(copy.deepcopy(self.d),2)])
    def test_length_reselects_endpoint(self):
        self.d['axes']={'geometry.length':[80,120]};cases=plan.configurations(self.d,2)
        for c in cases:self.assertEqual(c['registration']['regions']['TIP'],[11]);self.assertLess(c['config']['regions']['TIP']['bbox'][0],c['config']['geometry']['length'])
    def test_case_cap(self):
        with self.assertRaisesRegex(ValueError,'exceeds'):plan.configurations(self.d,1)
    def test_unknown_parameter(self):
        self.d['axes']={'wrong.geometry':[1]}
        with self.assertRaisesRegex(ValueError,'unsupported'):plan.configurations(self.d,2)
    def test_duplicate_values(self):
        self.d['axes']={'geometry.width':[1,1.0]}
        with self.assertRaisesRegex(ValueError,'duplicate'):plan.configurations(self.d,2)
    def test_invalid_parameter_before_write(self):
        self.d['axes']={'material.density':[-1]}
        with self.assertRaises(ValueError):plan.prepare(self.d,self.out,2)
        self.assertFalse(self.out.exists())
    def test_changed_input_rejected(self):
        d=plan.prepare(self.d,self.out,2);c=d['cases'][0];p=self.out/c['folder']/(c['case_id']+'.inp');p.write_text('changed')
        with self.assertRaisesRegex(ValueError,'changed'):runner.verify_plan(d,self.out)
    def test_changed_config_rejected(self):
        d=plan.prepare(self.d,self.out,2);(self.out/d['cases'][0]['folder']/'config.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'changed'):runner.verify_plan(d,self.out)
    def test_changed_helper_rejected(self):
        d=plan.prepare(self.d,self.out,2);d['helper_hashes']['run_sweep.py']='incorrect'
        with self.assertRaisesRegex(ValueError,'helper'):runner.verify_plan(d,self.out)
    def test_escape_rejected(self):
        d=plan.prepare(self.d,self.out,2);d['cases'][0]['folder']='../outside'
        with self.assertRaisesRegex(ValueError,'escapes'):runner.verify_plan(d,self.out)
    def test_failed_case_needs_explicit_retry(self):
        d=plan.prepare(self.d,self.out,2);folder=self.out/d['cases'][0]['folder'];runner.dump(folder/'status.json',{'state':'failed','attempt':1})
        with self.assertRaisesRegex(ValueError,'retry-failed'):runner.run(d,self.out,'missing',True,resume=True)
    def test_launcher_zero_without_history_is_failure(self):
        d=plan.prepare(self.d,self.out,2)
        with patch.object(runner,'command',return_value=None):
            with self.assertRaisesRegex(RuntimeError,'no extracted'):runner.run(d,self.out,'fake',True)
        self.assertEqual(json.loads((self.out/d['cases'][0]['folder']/'status.json').read_text())['state'],'failed')
        self.assertEqual(json.loads((self.out/d['cases'][1]['folder']/'status.json').read_text())['state'],'prepared')
    def test_completed_evidence_tamper_rejected(self):
        folder=Path(self.temp.name);p=folder/'history.json';p.write_text('{}');status={'evidence_hashes':{'history.json':plan.sha(p)}};runner.verify_completed(status,folder);p.write_text('modified')
        with self.assertRaisesRegex(ValueError,'evidence changed'):runner.verify_completed(status,folder)
    def test_completed_resume_skips_without_solver(self):
        d=plan.prepare(self.d,self.out,2)
        for c in d['cases']:
            folder=self.out/c['folder'];p=folder/'history.json';p.write_text('{}');runner.dump(folder/'status.json',{'state':'completed','attempt':1,'evidence_hashes':{'history.json':plan.sha(p)}})
        with patch.object(runner,'command',side_effect=AssertionError('solver should not launch')):r=runner.run(d,self.out,'missing',True,resume=True)
        self.assertEqual(r['skipped_completed'],2);self.assertFalse(r['solver_launched'])

if __name__=='__main__':unittest.main()
