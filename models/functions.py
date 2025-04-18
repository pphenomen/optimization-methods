import numpy as np

FUNCTIONS = {
    "sphere": lambda x, y: x**2 + y**2,
    "himmelblau": lambda x, y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2,
    "rastrigin": lambda x, y: 20 + x**2 - 10*np.cos(2*np.pi*x) + y**2 - 10*np.cos(2*np.pi*y),
    "booth": lambda x, y: (x + 2*y - 7)**2 + (2*x + y - 5)**2,
    "matyas": lambda x, y: 0.26*(x**2 + y**2) - 0.48*x*y,
    "rosenbrock": lambda x, y: 100 * (y - x**2)**2 + (1 - x)**2,
    "beale": lambda x, y: (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2,
    "goldstein_price": lambda x, y: (1 + ((x + y + 1)**2) * (19 - 14*x + 3*x**2 - 14*y + 6*x*y + 3*y**2)) * (30 + ((2*x - 3*y)**2) * (18 - 32*x + 12*x**2 + 48*y - 36*x*y + 27*y**2)),
    "bukin_n6": lambda x, y: 100 * np.sqrt(np.abs(y - 0.01*x**2)) + 0.01 * np.abs(x),
    "ackley": lambda x, y: -20*np.exp(-0.2*np.sqrt(0.5*(x**2+y**2))) - np.exp(0.5*np.cos(2*np.pi*x) + np.cos(2*np.pi*y)) + np.e + 20
}

FUNCTION_NAMES = {
    "sphere": "Функция Сферы",
    "himmelblau": "Функция Химмельблау",
    "rastrigin": "Функция Растригина",
    "booth": "Функция Бута",
    "matyas": "Функция Матьяса",
    "rosenbrock": "Функция Розенброка",
    "beale": "Функция Била",
    "goldstein_price": "Функция Гольдштейна-Прайса",
    "bukin_n6": "Функция Букина N6",
    "ackley": "Функция Экли"
}