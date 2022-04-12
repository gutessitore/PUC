#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
from math import e, log, sqrt

MULHER = 0
HOMEM = 1

def medidas(gênero):
    """
    As medidas retornam nesta ordem:
    média_peso, sigma_peso, média_altura, sigma_altura
    """
    if (gênero == MULHER):
        return (57.9, 8.89, 163.4, 6.55)
    elif (gênero == HOMEM):
        return (76.3, 12.62, 176.8, 6.91)

def eh_obeso(imc):
    # Se maior que 30, a pessoa é obesa
    return 0 if imc < 30 else 1

def imc(peso, altura):
    return peso / altura**2

def criar_amostra(tam_amostra, tipo_ap="reg_log"):
    # Médias para homens e mulheres de 23 anos de idade de Andaluzia
    médias_homens = (76.3, 12.62, 176.8, 6.91)
    médias_mulheres = (57.9, 8.89, 163.4, 6.55)
    qtd_max_por_genero = tam_amostra // 2
    HOMEM = 1
    MULHER = 0
    if (tipo_ap == "reg_log"):
        #homens = normalizar(criar_grupo(médias_homens, HOMEM, qtd_max_por_genero))
        homens = criar_grupo_reg_log(médias_homens, HOMEM, qtd_max_por_genero)
        mulheres = criar_grupo_reg_log(médias_mulheres, MULHER, qtd_max_por_genero)
        return homens + mulheres
    elif (tipo_ap=="reg_lin"):
        homens = criar_grupo_reg_linear(médias_homens, HOMEM, qtd_max_por_genero)
        mulheres = criar_grupo_reg_linear(médias_mulheres, MULHER, qtd_max_por_genero)
        return homens + mulheres

def criar_grupo_reg_linear(médias, gênero, n_max_pessoas):
    max_por_grupo = n_max_pessoas // 2
    qtd_obesos, qtd_não_obesos = 0, 0
    lst_pessoas = []
    while (qtd_obesos + qtd_não_obesos < 2 * max_por_grupo):
        mp = criar_pessoa(médias)
        eh_pes_obesa = eh_obeso(imc(mp[0], mp[1]/100))
        if (eh_pes_obesa and qtd_obesos < max_por_grupo):
            lst_pessoas.append([1, round(mp[0], 1), round(mp[1], 1)])
            qtd_obesos += 1

        if (not eh_pes_obesa and qtd_não_obesos < max_por_grupo):
            lst_pessoas.append([1, round(mp[0], 1), round(mp[1], 1)])
            qtd_não_obesos += 1
    if (len(lst_pessoas) < n_max_pessoas):
        mp = criar_pessoa(médias)
        lst_pessoas.append([1, round(mp[0], 1), round(mp[1], 1)])
    return lst_pessoas


def criar_grupo_reg_log(médias, gênero, n_max_pessoas):
    max_por_grupo = n_max_pessoas // 2
    qtd_obesos, qtd_não_obesos = 0, 0
    lst_pessoas = []
    while (qtd_obesos + qtd_não_obesos < 2 * max_por_grupo):
        mp = criar_pessoa(médias)
        eh_pes_obesa = eh_obeso(imc(mp[0], mp[1]/100))
        if (eh_pes_obesa and qtd_obesos < max_por_grupo):
            lst_pessoas.append([gênero, round(mp[0], 1), round(mp[1], 1), 1])
            qtd_obesos += 1

        if (not eh_pes_obesa and qtd_não_obesos < max_por_grupo):
            lst_pessoas.append([gênero, round(mp[0], 1), round(mp[1], 1), 0])
            qtd_não_obesos += 1
    if (len(lst_pessoas) < n_max_pessoas):
        mp = criar_pessoa(médias)
        tipo = 1 if eh_obeso(imc(mp[0], mp[1]/100)) else 0
        lst_pessoas.append([gênero, round(mp[0], 1), round(mp[1], 1), tipo])
    return lst_pessoas

def criar_pessoa(medidas):
    media_peso, sigma_peso, media_altura, sigma_altura = medidas
    peso = np.random.normal(media_peso, sigma_peso)
    altura = np.random.normal(media_altura, sigma_altura)
    return peso, altura

def preparar_amostra(amostra):
    amostra_prep = []
    medH = medidas(HOMEM)
    medM = medidas(MULHER)
    for linha in amostra:
        viés = 1
        gênero = linha[0]
        if (gênero == HOMEM):
            m_peso, s_peso = medH[0], medH[1]
            m_alt, s_alt = medH[2], medH[3]
        elif (gênero == MULHER):
            m_peso, s_peso = medM[0], medM[1]
            m_alt, s_alt = medM[2], medM[3]
        else:
            continue
        peso = padronizar([linha[1]], m_peso, s_peso)[0]
        altura = padronizar([linha[2]], m_alt, s_alt)[0]
        classe = linha[3]
        amostra_prep.append([viés, peso, altura, classe])
    return amostra_prep

def normalizar(dist):
    min_x, max_x = min(dist), max(dist)
    return [(x - min_x)/(max_x - min_x) for x in dist]

def padronizar_ms(dist, media, sigma):
    return [(x - media)/sigma for x in dist]

def padronizar(dist):
    m = média(dist)
    s = sigma(dist)
    return [(x - m)/s for x in dist]

def média(dist):
    return sum(dist) / len(dist)

def sigma(dist):
    m = média(dist)
    return sqrt(sum([(x - m)**2 for x in dist]))

# Função hipótese, sigmóide
def h(instância, betas):
    z = 0
    for i in range(len(betas)):
        z += betas[i] * instância[i]
    return 1 / (1 + np.exp(-z))

def escores(amostra, model_coef):
    TP, TN, FP, FN = 0, 0, 0, 0
    for instância in amostra:
        y = instância[-1]
        y_pred = h(instância, model_coef)
        if int(round(y_pred)) == 1:
            if (y == 1):
                TP += 1
            else:
                FP += 1
        else:
            if (y == 1):
                FN += 1
            else:
                TN += 1
    acc = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, acc, precision, recall
