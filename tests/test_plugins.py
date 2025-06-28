import pytest
from app.plugins import ruby_plugin

# --- Ruby Plugin Tests ---
def test_ruby_plugin_good_code():
    code = "class MyClass; end"
    report = ruby_plugin.analyze(code)
    assert not report['issues']
    assert report['metrics']['line_count'] == 1

def test_ruby_plugin_detects_eval():
    code = "eval('puts \'hello\')"
    report = ruby_plugin.analyze(code)
    assert len(report['issues']) == 1
    assert "Use of 'eval'" in report['issues'][0]