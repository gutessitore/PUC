
def mae(y: list, y_pred: list):
    """Calcula o erro absoluto médio.

    Args:
        y (list): lista com os valores reais.
        y_pred (list): lista com os valores previstos.

    Returns:
        float: erro absoluto médio.
    """
    return sum([abs(y[i] - y_pred[i]) for i in range(len(y))]) / len(y)


def mape(y: list, y_pred: list, epsilon: float = 1e-30):
    """Calcula o erro percentual médio.

    Args:
        y (list): lista com os valores reais.
        y_pred (list): lista com os valores previstos.
        epsilon (float, optional): valor para evitar divisão por zero. Defaults to 1e-30.

    Returns:
        float: erro percentual médio.
    """
    return sum([abs(y[i] - y_pred[i]) / max(abs(y[i]), epsilon) for i in range(len(y))]) / len(y)


def mse(y: list, y_pred: list):
    """Calcula o erro quadrático médio.

    Args:
        y (list): lista com os valores reais.
        y_pred (list): lista com os valores previstos.

    Returns:
        float: erro quadrático médio.
    """
    return sum([(y[i] - y_pred[i]) ** 2 for i in range(len(y))]) / len(y)


def r2(y: list, y_pred: list):
    """Calcula o coeficiente de determinação.

    Args:
        y (list): lista com os valores reais.
        y_pred (list): lista com os valores previstos.

    Returns:
        float: coeficiente de determinação.
    """
    y_mean = sum(y) / len(y)
    return 1 - sum([(y[i] - y_pred[i]) ** 2 for i in range(len(y))]) / sum([(y[i] - y_mean) ** 2 for i in range(len(y))])


def mediana(l):
    half = len(l) // 2
    l.sort()
    if not len(l) % 2:
        return (l[half - 1] + l[half]) / 2.0
    return l[half]


def medae(y: list, y_pred: list):
    """Calcula o erro absoluto mediano.

    Args:
        y (list): lista com os valores reais.
        y_pred (list): lista com os valores previstos.

    Returns:
        float: erro absoluto mediano.
    """
    return mediana([abs(y[i] - y_pred[i]) for i in range(len(y))])
