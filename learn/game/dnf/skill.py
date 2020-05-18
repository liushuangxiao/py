# coding=utf-8


def show_attack(major, equipment_attack, weapon_mastery, other, intensify):
    """
    面板攻击力
    :param major: major 主属性 力量或智力
    :param equipment_attack: 总 物理/魔法 攻击力 （武器上显示的物理攻击力、附魔物理攻击力、称号／宠物／光环／辅助装备等部位加的物理攻击力的总和，技能提供的物攻也是）
    :param weapon_mastery: 武器精通
    :param other: 魂链、光兵等增加基础攻击力
    :param intensify: 无视 物理/魔法 攻击力
    :return:
    """
    ba = basic_attack(major, equipment_attack, weapon_mastery, other)
    return ba + intensify


def basic_attack(major, equipment_attack, weapon_mastery, other):
    """
    普通/技能 基础攻击力
    :param major: major 主属性 力量或智力
    :param equipment_attack: array 总 物理/魔法 攻击力 （武器上显示的物理攻击力、附魔物理攻击力、称号／宠物／光环／辅助装备等部位加的物理攻击力的总和，技能提供的物攻也是）
    :param weapon_mastery: 武器精通
    :param other: 魂链、光兵等增加基础攻击力
    :param intensify: 无视 物理/魔法 攻击力
    :return:
    """
    count = 0
    for atk in equipment_attack:
        count += atk
    return count * (float(major) / 250.0) * (1 + weapon_mastery + (other or 0))


def skill_damage(basic_atk, intensify, element, skill, buff, tp, defense, element_defense):
    """
    计算技能伤害
    :param basic_atk: 基础 物理/魔法 攻击力
    :param intensify: 无视 物理/魔法 攻击力
    :param element: 无视 物理/魔法 攻击力
    :param skill: 技能百分比数值
    :param buff: 角色增伤buff合计（装备）
    :param tp:
    :param defense: 物理/魔法 防御力
    :param element_defense: 属性抗性
    :return:
    """
    defense_p = 1
    if defense and defense > 0:
        defense_p = defense / (100 * 200 + defense)
    return (
                   basic_atk * tp * (1 - defense_p) * (1.05 + (element - element_defense) * 0.0045) +
                   intensify
           ) * skill * buff


def count_buff(critical, final, attack, skill, attach, element_attach, element):
    tmp = 1.0
    for c in critical:
        tmp += c
    result = 1.5 * tmp

    tmp = 1.0
    for c in final:
        tmp += c
    result *= tmp

    tmp = 1.0
    for c in attack:
        tmp += c
    result *= tmp

    tmp = 1.0
    for c in attach:
        tmp += c
    attach_all = tmp * 1.015

    tmp = 1.0
    for c in element_attach:
        tmp += c
    attach_all += tmp * (1.05 + element * 0.0045) * 1.015

    result *= attach_all

    normal_attack = result

    tmp = 1.0
    for c in skill:
        tmp *= (c + 1.0)
    skill_attack = result * tmp

    return normal_attack, skill_attack
