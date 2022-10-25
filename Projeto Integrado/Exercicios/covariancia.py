#!/usr/bin/env python
# coding: utf-8

# # Covariância

# A covariância é dada por:

# $$
# CoV(X,Y) = \frac{1}{n-1}\sum_{i=1}^{n}{(x_{i}-\bar{x})(y_{i}-\bar{y})}
# $$

# ## TAREFA

# **[01]** Implemente a função a seguir sem o uso de bibliotecas externas. **Não pode usar import**, mas você pode criar outras funções (e.g., a média) para auxiliar na função `cov`.

# In[1]:


# Exemplos de X e Y
x = [1, 2, 3, 4, 5]
y = [3, 4, 5, 6, 3]


def cov(x, y):
    """
    Calcula e retorna (não imprime na tela) a covariância entre duas distribuições
    """
    assert len(x) == len(y)
    multiplier = 1 / (len(x) - 1)
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    return multiplier * sum([(x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x))])


cov(x, y)
# **[02]** Crie uma matriz de covariância (2x2) para duas distribuições x, y:
# 
# ```
#   CoV(x,x)  CoV(x,y)
#   CoV(y,x)  CoV(y,y)
# ```

# In[ ]:


def matriz_cov(x, y):
    """
  Retorna (não imprime na tela) a matriz de covariância entre duas distribuições
  """
    assert len(x) == len(y)
    return [[cov(x, x), cov(x, y)], [cov(y, x), cov(y, y)]]

matriz_cov(x, y)


