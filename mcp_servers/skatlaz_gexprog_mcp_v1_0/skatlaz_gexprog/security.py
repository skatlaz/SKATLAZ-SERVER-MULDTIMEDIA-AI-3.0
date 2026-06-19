import re

def quick_code_audit(code: str):
    warnings=[]
    patterns={
        'eval(': 'Uso de eval pode ser perigoso.',
        'exec(': 'Uso de exec pode executar código arbitrário.',
        'shell=True': 'shell=True pode permitir command injection.',
        'password=': 'Possível senha hardcoded.',
        'api_key': 'Possível API key hardcoded.',
        'SECRET_KEY': 'Possível secret key hardcoded.',
    }
    for p,msg in patterns.items():
        if p in code:
            warnings.append(msg)
    if re.search(r'http://[^\s]+', code): warnings.append('URL HTTP sem TLS encontrada.')
    return {'warnings': warnings, 'ok': not warnings}
