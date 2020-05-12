# -*- coding: UTF-8 -*-

import numpy


def forward(transition_probability, emission_probability, pi, obs_seq):
    """
    :param transition_probability :transition_probability 是状态转移矩阵
    :param emission_probability: emission_probability 是发射矩阵
    :param pi: pi是初始状态概率
    :param obs_seq: obs_seq是观察状态序列
    :return: 返回结果
    """
    transition_probability = numpy.array(transition_probability)
    emission_probability = numpy.array(emission_probability)
    pi = numpy.array(pi)

    colNum = len(obs_seq)
    rowNum = transition_probability.shape[0]

    result = numpy.zeros((rowNum, colNum))
    result[:, 0] = pi * numpy.transpose(emission_probability[:, obs_seq[0]])

    for i in range(1, colNum):
        for n in range(rowNum):  # n是代表隐藏状态的
            print()
            result[n, i] = numpy.dot(result[:, i - 1], transition_probability[:, n]) * emission_probability[
                n, obs_seq[i]]  # 对应于公式,前面是对应相乘
            print(numpy.dot(result[:, i - 1], transition_probability[:, n]))
    return result


def backward(transition_probability, emission_probability, pi, obs_seq):
    """
    :param transition_probability :transition_probability 是状态转移矩阵
    :param emission_probability: emission_probability 是发射矩阵
    :param pi: pi是初始状态概率
    :param obs_seq: obs_seq是观察状态序列
    :return: 返回结果
    """
    transition_probability = numpy.array(transition_probability)
    emission_probability = numpy.array(emission_probability)
    pi = numpy.array(pi)

    colNum = len(obs_seq)
    rowNum = transition_probability.shape[0]

    result = numpy.zeros((rowNum, colNum))
    result[:, -1] = 1

    for i in reversed(range(colNum - 1)):
        for n in range(rowNum):  # n是代表隐藏状态的
            result[n, i] = numpy.sum(result[:, i + 1] * transition_probability[n, :] * emission_probability[:, obs_seq[i + 1]])  # 对应于公式,前面是对应相乘
    return result


transition_probability = [[0.7, 0.3], [0.4, 0.6]]
emission_probability = [[0.5, 0.4, 0.1], [0.1, 0.3, 0.6]]
pi = [0.6, 0.4]
# transition_probability = [[0.5, 0.3, 0.2], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]]
# emission_probability = [[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]]
# pi = [0.2, 0.4, 0.4]
obs_seq = [0, 1]
result = forward(transition_probability, emission_probability, pi, obs_seq)

rowNum = numpy.array(transition_probability).shape[0]
colNum = len(obs_seq)

res_forward = 0
for i in range(rowNum):  # 将最后一列相加就得到了我们最终的结果
    res_forward += result[i][colNum - 1]  # 求和于最后一列

emission_probability = numpy.array(emission_probability)
result = backward(transition_probability, emission_probability, pi, obs_seq)

res_backword = 0
res_backward = numpy.sum(pi * result[:, 0] * emission_probability[:, obs_seq[0]])

print("res_backward = {}".format(res_backward))
print("res_forward = {}".format(res_forward))
