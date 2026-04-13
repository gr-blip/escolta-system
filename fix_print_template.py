path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_print.html'
content = open(path, encoding='utf-8').read()

BLOCO = """
  <!--  DESPESAS / CREDITOS  -->
  {% if despesas %}
  <div class="card">
    <div class="card-header">
      <svg width="13" height="13" fill="none" viewBox="0 0 14 14"><rect x="1" y="3" width="12" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/><path d="M4 7h2M8 7h2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
      Despesas / Créditos
    </div>
    <div class="card-body" style="padding:0">
      <table class="op-table" style="width:100%">
        <thead>
          <tr>
            <th>Tipo</th>
            <th>Natureza</th>
            <th>Descrição</th>
            <th>Data</th>
            <th style="text-align:right;padding-right:16px">Valor</th>
          </tr>
        </thead>
        <tbody>
          {% for d in despesas %}
          <tr>
            <td class="sit">{{ d.get_tipo_display }}</td>
            <td>
              {% if d.natureza == 'credito' %}
              <span class="badge badge-green">Crédito</span>
              {% else %}
              <span class="badge badge-red">Despesa</span>
              {% endif %}
            </td>
            <td style="color:var(--text3)">{{ d.descricao|default:"" }}</td>
            <td>{{ d.ocorrido_em|date:"d/m/Y H:i" }}</td>
            <td class="num" style="text-align:right;padding-right:16px">R$ {{ d.valor }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
  {% endif %}

  <!--  ASSINATURAS DIGITAIS  -->
  {% if assinaturas %}
  <div class="card">
    <div class="card-header">
      <svg width="13" height="13" fill="none" viewBox="0 0 14 14"><path d="M2 10c2-3 4-5 6-4s1 4-1 4 3-4 5-6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
      Assinaturas Digitais
    </div>
    <div class="card-body">
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px">
        {% for tipo_val, tipo_label in assinatura_tipos_lista %}
        {% if tipo_val in assinaturas %}
        {% with a=assinaturas|get_item:tipo_val %}
        <div style="border:1px solid var(--border);border-radius:8px;overflow:hidden;background:var(--bg3)">
          <div style="padding:6px 10px;font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.06em;border-bottom:1px solid var(--border);background:var(--bg4)">
            {{ tipo_label }}
          </div>
          <div style="background:#fff;padding:8px;text-align:center">
            <img src="{{ a.imagem.url }}" alt="Assinatura {{ tipo_label }}" style="max-height:80px;max-width:100%;object-fit:contain">
          </div>
          <div style="padding:6px 10px;font-size:11px;color:var(--text2);border-top:1px solid var(--border)">
             {{ a.nome }}<br>
            <span style="font-size:10px;color:var(--text3)">{{ a.criado_em|date:"d/m/Y H:i" }}</span>
          </div>
        </div>
        {% endwith %}
        {% endif %}
        {% endfor %}
      </div>
    </div>
  </div>
  {% endif %}

"""

rodape = '  <div class="rodape">ATENCIOSAMENTE'

if rodape in content:
    content = content.replace(rodape, BLOCO + '  <div class="rodape">ATENCIOSAMENTE')
    open(path, 'w', encoding='utf-8').write(content)
    print('OK template')
else:
    print('ERRO - rodape nao encontrado')
