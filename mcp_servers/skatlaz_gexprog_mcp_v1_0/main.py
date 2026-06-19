from skatlaz_gexprog.generator import CodeGenerator
from skatlaz_gexprog.packages import PackageExplorer
from skatlaz_gexprog.rag import SimpleRAG
from skatlaz_gexprog.security import quick_code_audit

if __name__ == '__main__':
    gen = CodeGenerator()
    print('=== Skatlaz GexProg MCP v1.0 CLI ===')
    result = gen.create_project(
        prompt='Crie um script Python que leia um CSV e gere resumo estatistico',
        language='python',
        name='csv_stats_demo'
    )
    print(result)
    print('\nPacotes para pandas:')
    print(PackageExplorer().search_all('pandas'))
    print('\nRAG paradigmas:')
    print(SimpleRAG().search('orientação objetos'))
    print('\nAuditoria rapida:')
    print(quick_code_audit('eval(user_input)'))
