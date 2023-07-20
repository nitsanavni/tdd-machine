import subprocess

def test_e2e_fizzbuzz():
    result = subprocess.run(['python', 'fizzbuzz.py', '3'], capture_output=True)
    assert result.stdout == b'Fizz
'
