import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import mannwhitneyu
from os import path


def Normalization(Matrix):
    max_len = 0
    for v in Matrix:
        max_len = max(max_len, len(v))
    for v in Matrix:
        while len(v) < max_len:
            value = v[0]
            v.insert(0, value)
    return Matrix


def draw_convergence(CMAES_ave, DE_ave, ES_ave, GA_ave, hybridDE_ave, x_CMAES, x_DE, x_ES, x_GA, x_hybridDE, func_num,
                     p_value, move, FEs, best_point):

    this_path = path.realpath(__file__)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.semilogy(x_CMAES, CMAES_ave, label='CMA-ES', linestyle=':')
    plt.semilogy(x_DE, DE_ave, label='DE', linestyle=':')
    plt.semilogy(x_ES, ES_ave, label='ES', linestyle=':')
    plt.semilogy(x_GA, GA_ave, label='GA', linestyle=':', color='cyan')
    plt.semilogy(x_hybridDE, hybridDE_ave, label='hybridDE', color='red')
    plt.scatter(x_GA[len(x_GA)-1], best_point, label='best Solution')

    # plt.plot(x_CMAES, CMAES_ave, label='CMA-ES', linestyle=':')
    # plt.plot(x_DE, DE_ave, label='DE', linestyle=':')
    # plt.plot(x_ES, ES_ave, label='ES', linestyle=':')
    # plt.plot(x_GA, GA_ave, label='GA', linestyle=':', color='cyan')
    # plt.plot(x_hybridDE, hybridDE_ave, label='hybridDE', color='red')
    font_title = {'size': 18}
    font = {'size': 16}
    plt.title('$f_' + '{' + str(func_num) + '}$ in GTOPX Suite', font_title)
    plt.xlabel('Fitness evaluation times', font)
    plt.ylabel('Fitness', font)
    plt.legend()
    if p_value < 0.05:
        if p_value < 0.01:
            plt.text(FEs, move, "**", fontdict={'size': 14, 'color': 'red'})
        else:
            plt.text(FEs, move, "*", fontdict={'size': 14, 'color': 'red'})
    plt.savefig(
       path.dirname(this_path) + '/data/pic/' + 'f' + str(func_num))
    plt.show()


def ave(array):
    result = []
    for i in range(len(array[0])):
        result.append(np.mean(array[:, i]))
    return result


def final(method, name):
    method_final = method[:, len(method[0]) - 1]
    print(name, 'final: ', '%e' % np.mean(method_final), '±', '%e' % np.std(method_final, ddof=1))
    return method_final


def Holm(DE_ave, ES_ave, GA_ave, hybridDE_a_ave, hybridDE_w_ave, RS_ave, test):
    result = {'DE_ES': test(DE_ave, ES_ave)[1], 'DE_GA': test(DE_ave, GA_ave)[1],
              'DE_A_hybridDE': test(DE_ave, hybridDE_a_ave)[1], 'DE_W_hybridDE': test(DE_ave, hybridDE_w_ave)[1],
              'DE_RS': test(DE_ave, RS_ave)[1], 'ES_GA': test(ES_ave, GA_ave)[1],
              'ES_A_hybridDE': test(ES_ave, hybridDE_a_ave)[1], 'ES_W_hybridDE': test(ES_ave, hybridDE_w_ave)[1],
              'ES_RS': test(ES_ave, RS_ave)[1], 'GA_A_hybridDE': test(GA_ave, hybridDE_a_ave)[1],
              'GA_W_hybridDE': test(GA_ave, hybridDE_w_ave)[1], 'GA_RS': test(GA_ave, RS_ave)[1],
              'A_hybridD_W_hybridDE': test(hybridDE_a_ave, hybridDE_w_ave)[1], 'A_hybridDE_RS': test(hybridDE_a_ave, RS_ave)[1],
              'W_hybridDE_RS': test(hybridDE_w_ave, RS_ave)[1],
              }
    result = dict(sorted(result.items(), key=lambda d: d[1]))
    flag = len(result)
    for (k, v) in result.items():
        result[k] = v * flag
        flag -= 1
    return result


def increase(ave):
    for i in range(len(ave)-1):
        if ave[i+1] > ave[i]:
            ave[i+1] = ave[i]
    return ave


if __name__ == '__main__':

    DE = []
    ES = []
    GA = []
    hybridDE_a = []
    hybridDE_w = []
    RS = []

    DE = np.array(DE)
    ES = np.array(ES)
    GA = np.array(GA)
    hybridDE_a = np.array(hybridDE_a)
    hybridDE_w = np.array(hybridDE_w)
    RS = np.array(RS)

    DE_ave = ave(DE)
    ES_ave = ave(ES)
    GA_ave = ave(GA)
    hybridDE_a_ave = ave(hybridDE_a)
    hybridDE_w_ave = ave(hybridDE_w)
    RS_ave = ave(RS)

    DE_final = final(DE, "DE")
    ES_final = final(ES, "ES")
    GA_final = final(GA, "GA")
    hybridDE_a_final = final(hybridDE_a, "hybridDE with averaging")
    hybridDE_w_final = final(hybridDE_w, "hybridDE with weighting")
    RS_final = final(RS, "RS")
    print(Holm(DE_final, ES_final, GA_final, hybridDE_a_final, hybridDE_w_final, RS_final, mannwhitneyu))
    #     if cons == 0:
    #     CMAES_ave = increase(CMAES_ave)
    #     DE_ave = increase(DE_ave)
    #     ES_ave = increase(ES_ave)
    #     GA_ave = increase(GA_ave)
    #     hybridDE_ave = increase(hybridDE_ave)
    # x_CMAES = np.linspace(0, FEs, len(CMAES_ave))
    # x_DE = np.linspace(0, FEs, len(DE_ave))
    # x_ES = np.linspace(0, FEs, len(ES_ave))
    # x_GA = np.linspace(0, FEs, len(GA_ave))
    # x_hybridDE = np.linspace(0, FEs, len(hybridDE_ave))
    # print('p_value: ', p_value)
    # draw_convergence(CMAES_ave, DE_ave, ES_ave, GA_ave, hybridDE_ave, x_CMAES, x_DE, x_ES,
    #                  x_GA, x_hybridDE, func_num, p_value, move, FEs, best_point)
