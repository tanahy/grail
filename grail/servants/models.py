from django.db import models

import json, requests
import numpy as np
import pandas as pd

class_rel = requests.get("https://api.atlasacademy.io/export/JP/NiceClassRelation.json").json()
attrib_rel = requests.get("https://api.atlasacademy.io/export/JP/NiceAttributeRelation.json").json()
class_rates = requests.get("https://api.atlasacademy.io/export/JP/NiceClassAttackRate.json").json()
card_data = requests.get("https://api.atlasacademy.io/export/JP/NiceCard.json").json()
card_details = requests.get("https://api.atlasacademy.io/export/JP/NiceCard.json").json()

class Servant(models.Model):
    uid = models.IntegerField()
    servant_id = models.IntegerField()
    name = models.CharField(max_length=32)
    server = models.CharField(max_length=3)
    className = models.CharField(max_length=12)
    traits = models.ForeignKey(Trait, on_delete=None)
    atk = models.IntegerField()
    skills = models.ForeignKey(Skill)
    noble_phantasm = models.ForeignKey(NoblePhantasm)
    gender = models.CharField(max_length=12)
    attribute = models.CharField(max_length=12)
    face = models.URLField()
    
    #Have to check if this is the proper way to populate with non database attributes
    def __init__(self):
        self.attack_mod = []
        self.def_mod = []

    update_date = {}

    class Meta:
        unique_together = (('servant_id', 'server'),)

    def set_servant_data(self, data = None):
        if data is None:
            data = requests.get(f"https://api.atlasacademy.io/nice/{self.server}/servant/{self.servant_id}").json()
        self.uid = data['id']
        self.servant_id = data['collectionNo']
        self.name = data['name']
        self.attribute = data['attribute']
        self.className = data['className']
        self.gender = data['gender']
        for trait in data['traits']:
            self.
        self.atk = data['atkMax']
        self.skills = data['skills']
        self.noble_phantasm = NoblePhantasm(data['noblePhantasms'])
        self.face = data['extraAssets']['faces']['4']
                
        for skill in servant_data['skills']:
            uid = skill['id']
            name = skill['name']
            for function in skill['functions']:
                func_uid = function['funcId']
                func_type = function['funcType']
                func_target_type = function['funcTargetType']
                for buff on function['buffs']:
                    buff_uid = buff['id']
                    buff_type = buff['type'] 
        
        NP_strength_list = [NP['strengthStatus'] for NP in servant_data['noblePhantasms']]

        for NP in servant_data['noblePhantasms']:
            if NP['strengthStatus'] == max(NP_strength_list):
                name = NP['name']
                card_type = NP['card']
                
                NoblePhantasm(name = name, card_type = card_type, data = NP)

    @staticmethod
    def set_all_servants_data():
        for server in ['JP','NA']:
            #self.update_date_NA = requests.head("https://api.atlasacademy.io/export/NA/nice_servant.json").headers['Last-Modified']
            r = requests.get(f"https://api.atlasacademy.io/export/{server}/nice_servant.json")
            data = r.json()
            for servant_data in data:
                servant = Servant(servant_id = servant_data['collectionNo'], server = server).set_servant_data(servant_data)
            Servant.update_date[server] = r.headers['Last-Modified']

class Trait(models.Model):
    id = models.IntegerField(max_length=12, primary_key=True)
    name = models.CharField(max_length=32)
    users = models.ManyToManyField(Servant, on_delete=models.CASCADE)

class NoblePhantasm(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    card_type = models.CharField(max_length=32)
    functions = models.ForeignKey()

    def __init__(self, data):
        value_array = np.empty((5,5))
        for function_data in data['functions']:
            self.functions = NPFunction(function_data)


class NPFunction(models.Model):
    uid = models.IntegerField()
    func_type = models.CharField(max_length=12)
    buffs = models.CharField(max_length=128)
    func_target_type = models.CharField(max_length=32)
    values = models.TextField()


    def __init__(self, data):
        self.uid = data['funcId']
        self.func_type = data['funcType']
        self.func_target_type = data['funcTargetType']
        self.buffs = ','.join([buff['name'] for buff in data['buffs']])
            for i in range(5):
                OC = 'svals'
                if i > 0:
                    OC += str(i+1)
                for j,NP_level in enumerate(NP[OC]):
                    value_array[j,i] = NP_level['Value']


class Card:
    def __init__(self, card_type, servant, is_NP = False):
        self.type = card_type
        self.servant = senvant
        self.is_NP = is_NP

        if self.servant.NoblePhantasm.type != self.type and self.is_NP:
            raise ValueError("Card type doesn't match servant's Noble Phantasm.")
        if self.type not in card_data.keys():
            raise ValueError("Card type not registered.")

def turn_damage_calc(card_list, enemies, **kwargs):
    '''
    Per turn damage calculation routine
    Missing features:
    - Check same servant for consecutive attacks so as to not switch enemies
    - Guts
    - Overkill bug (buster damage)
    - Overgauge
    - Don't count overkill/overgauge damage?
    '''
    first_card = card_list[0]
    type_chain = all([card.type == first_card.type for card in card_list])
    if all([card.servant == card_list[0].servant for card in card_list]):
        card_list.append(Card('extra', card_list[0].servant, False))
    damage = 0

    for i, card in enumerate(card_list):
        card_turn = i+1
        enemies_hp = np.array([enemy['hp'] for enemy in enemies])
        if card.is_NP and servant.NP.func_target_type == 'AoE':
            for j in len(enemies):
                card_damage = card_damage_calc(card, card_turn, enemies[j], first_card = first_card, card_turn = i, type_chain = type_chain)
                enemies_hp[j] -= card_damage
                damage += card_damage
        else:
            card_damage = card_damage_calc(card, card_turn, enemies[0], first_card = first_card, card_turn = i, type_chain = type_chain)
            enemies_hp[0] -= card_damage
            damage += card_damage

        
        enemies = enemies[enemies_hp > 0]
    
    return damage, enemies

def card_damage_calc(card, card_turn, enemy, first_card, critical_hit = False, **kwargs):
    '''
    Source for the formula: https://blogs.nrvnqsr.com/entry.php/3309-How-is-damage-calculated   
    damage = [servantAtk * npDamageMultiplier * classAtkBonus * triangleModifier * attributeModifier * randomModifier * 0.23 * (1 + atkMod - defMod) * criticalModifier * extraCardModifier * (firstCardBonus + cardDamageValue * (1 + cardMod)) * (1 - specialDefMod) * {1 + powerMod + selfDamageMod + (critDamageMod * isCrit) + (npDamageMod * isNP)} * {1 + ((superEffectiveModifier - 1) * isSuperEffective)}] + dmgPlusAdd + selfDmgCutAdd + (servantAtk * busterChainMod)
    Missing features:
    - check status for effective damage modifier
    '''
    servant = card.servant
    random_mod = 1.1 #random.random((.9,1.1))

    base_damage = servant.attack * class_rates[servant.className] / 1000 * class_rel[servant.className][enemy.className] / 1000 * attrib_rel[servant.attrib][enemy.attrib] * random_mod * .23 

    atk_def_mod = 1
    if servant.atk_mod:
        for atk_mod in servant.atk_mod:
            if atk_mod.type is 'raw_atk':
                at_def_mod += atk_mod.value / 1000
    if enemy.def_mod:
        for def_mod in enemy.def_mod:    
            if not any([atk_mod.name is 'defensePierce' for atk_mod in servant.atk_mod]) or def_mod.value < 0:
                atk_def_mod -= def_mod.value / 1000
    
    base_damage *= atk_def_mod

    card_mods = card_details[card.type][str(card_turn)]['adjustAtk'] / 1000 * (1 + card_mod)
    if first_card.type == 'buster' and not card.is_NP:
        card_mods += .5
    
    base_damage *= card_mods 

    if critical_hit:
        base_damage *= 2

    if card.type == 'extra':
        if type_chain:
            base_damage *= 3.5
        else:
            base_damage *= 2

    if enemy.special_def_mod:
        base_damage *= 1 - enemy.special_def_mod.value / 1000

    misc_mod = 1
    if servant.power_mod:
        for mod in servant.power_mod:
            misc_mod += mod.value
    if enemy.self_damage_mod:
        for mod in enemy.self_damage_mod:
            misc_mod += mod.value
    if critical_hit:
        misc_mod += servant.crit_damage_mod

    base_damage *= misc_mod

    if card.is_NP:
        base_damage *= servant.NP.np_damage_multiplier
        misc_mods += servant.NP.np_damage_mod
        #have to check if this is cumulative or not:
        for function in servant.Np.functions:
            if function.target and (function.target in enemy.traits or function.target in enemy.status):
                base_damage *= servant.NP.supereffective_mod
    flat_damage = 0
    for mod in servant.attack_mod:
        if mod.type == 'damagePlusAdd':
            flat_damage += mod.value
    for mod in enemy.def_mod:
        if mod.type == 'selfDamageCutAdd':
            flat_damage += mod.value
            
    if type_chain and first_card.type == 'buster':
        flat_damage += .2 * servant.attack
    
    damage = base_damage + flat_damage

    return damage

