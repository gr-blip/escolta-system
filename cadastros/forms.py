from django import forms
from .models import Agente, Viatura, Rastreador, Armamento, Cliente, Colete, FuncionarioPatrimonial


class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        exclude = ['criado_em', 'atualizado_em']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Roberto Souza de Jesus'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs={'placeholder': '0000000'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(62) 99999-0000'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'cnh': forms.TextInput(attrs={'placeholder': '00000000000'}),
            'cnh_validade': forms.DateInput(attrs={'type': 'date'}),
            'cnv': forms.TextInput(attrs={'placeholder': '00000/0000'}),
            'cnv_validade': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observacoes sobre o agente...'}),
        }


class ViaturaForm(forms.ModelForm):
    class Meta:
        model = Viatura
        exclude = ['criado_em', 'atualizado_em']
        widgets = {
            'marca_modelo': forms.TextInput(attrs={'placeholder': 'Ex: VW Polo'}),
            'ano': forms.TextInput(attrs={'placeholder': '2024'}),
            'cor': forms.TextInput(attrs={'placeholder': 'Ex: Cinza'}),
            'placa': forms.TextInput(attrs={'placeholder': 'SEO-3C73'}),
            'frota': forms.TextInput(attrs={'placeholder': 'Codigo interno'}),
            'mct_id': forms.TextInput(attrs={'placeholder': '2261451'}),
            'renavam': forms.TextInput(attrs={'placeholder': '00000000000'}),
            'chassi': forms.TextInput(attrs={'placeholder': '9BWZZZ...'}),
            'crlv_validade': forms.DateInput(attrs={'type': 'date'}),
            'seguro_validade': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Manutencoes, equipamentos instalados...'}),
        }


class RastreadorForm(forms.ModelForm):
    class Meta:
        model = Rastreador
        exclude = ['criado_em', 'atualizado_em']
        widgets = {
            'marca': forms.TextInput(attrs={'placeholder': 'Ex: SASCAR'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Ex: SASCAR Full'}),
            'numero_serie': forms.TextInput(attrs={'placeholder': 'SER-00000'}),
        }


class ArmamentoForm(forms.ModelForm):
    class Meta:
        model = Armamento
        exclude = ['criado_em', 'atualizado_em']
        widgets = {
            'marca': forms.TextInput(attrs={'placeholder': 'Ex: Taurus, Glock'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Ex: PT840, G17'}),
            'calibre': forms.TextInput(attrs={'placeholder': 'Ex: .40 S&W, 9mm'}),
            'numero_serie': forms.TextInput(attrs={'placeholder': 'TQ000000'}),
            'numero_cano': forms.TextInput(attrs={'placeholder': 'Numero do cano'}),
            'registro_cr': forms.TextInput(attrs={'placeholder': 'Nr de registro'}),
            'registro_validade': forms.DateInput(attrs={'type': 'date'}),
            'data_aquisicao': forms.DateInput(attrs={'type': 'date'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # 'ativo' é excluído propositalmente: o template não renderiza esse
        # campo e, sem ele no POST, Django salvaria como False (checkbox
        # não marcado). A toggle de ativo/inativo é feita pela view dedicada
        # cliente_inativar. Default do model (True) prevalece no cadastro.
        exclude = ['criado_em', 'atualizado_em', 'ativo']
        widgets = {
            'razao_social': forms.TextInput(attrs={'placeholder': 'Ex: Bayer SA BCS'}),
            'cnpj': forms.TextInput(attrs={'placeholder': '00.000.000/0000-00'}),
            'inscricao_estadual': forms.TextInput(attrs={'placeholder': 'Inscricao estadual'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Rua, numero, bairro'}),
            'cidade_uf': forms.TextInput(attrs={'placeholder': 'Goiania / GO'}),
            'cep': forms.TextInput(attrs={'placeholder': '00000-000'}),
        }


class ColeteForm(forms.ModelForm):
    class Meta:
        model = Colete
        exclude = ['criado_em', 'atualizado_em']
        widgets = {
            'marca':     forms.TextInput(attrs={'placeholder': 'Ex: BLINTEC'}),
            'numeracao': forms.TextInput(attrs={'placeholder': 'Ex: 442 15206'}),
            'validade':  forms.DateInput(attrs={'type': 'date'}),
        }


class FuncionarioPatrimonialForm(forms.ModelForm):
    class Meta:
        model = FuncionarioPatrimonial
        exclude = ['criado_em', 'atualizado_em']
        widgets = {
            'nome':            forms.TextInput(attrs={'placeholder': 'Ex: Jose Silva Santos'}),
            'cpf':             forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'rg':              forms.TextInput(attrs={'placeholder': '0000000'}),
            'telefone':        forms.TextInput(attrs={'placeholder': '(62) 99999-0000'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'cnh':             forms.TextInput(attrs={'placeholder': '00000000000'}),
            'cnh_validade':    forms.DateInput(attrs={'type': 'date'}),
            'cnv':             forms.TextInput(attrs={'placeholder': '00000/0000'}),
            'cnv_validade':    forms.DateInput(attrs={'type': 'date'}),
            'posto_trabalho':  forms.TextInput(attrs={'placeholder': 'Ex: Portaria Condominio Alpha'}),
            'data_admissao':   forms.DateInput(attrs={'type': 'date'}),
            'registro_drt':    forms.TextInput(attrs={'placeholder': 'Nr DRT/MTE'}),
            'observacoes':     forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observacoes sobre o funcionario...'}),
        }
