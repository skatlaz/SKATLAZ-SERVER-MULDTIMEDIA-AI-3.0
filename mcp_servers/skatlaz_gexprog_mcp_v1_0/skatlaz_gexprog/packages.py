import requests

class PackageExplorer:
    def pypi(self, name):
        r = requests.get(f'https://pypi.org/pypi/{name}/json', timeout=20)
        if r.status_code != 200: return {'found': False, 'source': 'pypi'}
        j = r.json(); info = j.get('info',{})
        return {'found': True, 'source':'pypi','name':info.get('name'),'version':info.get('version'),'summary':info.get('summary'),'url':info.get('package_url')}

    def npm(self, name):
        r = requests.get(f'https://registry.npmjs.org/{name}', timeout=20)
        if r.status_code != 200: return {'found': False, 'source': 'npm'}
        j = r.json(); latest = j.get('dist-tags',{}).get('latest')
        return {'found': True, 'source':'npm','name':j.get('name'),'version':latest,'summary':j.get('description')}

    def rubygems(self, name):
        r = requests.get(f'https://rubygems.org/api/v1/gems/{name}.json', timeout=20)
        if r.status_code != 200: return {'found': False, 'source': 'rubygems'}
        j = r.json(); return {'found': True,'source':'rubygems','name':j.get('name'),'version':j.get('version'),'summary':j.get('info'),'url':j.get('project_uri')}

    def nuget(self, name):
        url = f'https://api.nuget.org/v3-flatcontainer/{name.lower()}/index.json'
        r = requests.get(url, timeout=20)
        if r.status_code != 200: return {'found': False, 'source':'nuget'}
        versions = r.json().get('versions', [])
        return {'found': True, 'source':'nuget','name':name,'version': versions[-1] if versions else None}

    def crates(self, name):
        r = requests.get(f'https://crates.io/api/v1/crates/{name}', timeout=20, headers={'User-Agent':'SkatlazGexProg/1.0'})
        if r.status_code != 200: return {'found': False, 'source':'crates'}
        c = r.json().get('crate',{})
        return {'found': True,'source':'crates','name':c.get('name'),'version':c.get('newest_version'),'summary':c.get('description')}

    def packagist(self, name):
        r = requests.get(f'https://repo.packagist.org/p2/{name}.json', timeout=20)
        return {'found': r.status_code == 200, 'source':'packagist','name':name}

    def search_all(self, name):
        out=[]
        for fn in [self.pypi,self.npm,self.rubygems,self.nuget,self.crates]:
            try: out.append(fn(name))
            except Exception as e: out.append({'found':False,'source':fn.__name__,'error':str(e)})
        return out
