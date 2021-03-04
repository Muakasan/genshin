from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk, amp_react_mult

# Strongly based on Zakharov's sheets https://docs.google.com/spreadsheets/d/1RAz3jx4x1ThWED8XWg8GKIf73RjPrZrnSukYZUCSRU8/edit#gid=383481181
# DM High HP should be 15262, Homa 17311 
'''
4pc Crimson Witch		
HP%, Pyro%, Crit Rate/Crit Damage		
E + N4 x 4 + Q
(80+21)/60*4 = 6.733
'''

'''
Hero Level	80
Enemy Level	80
Enemy Elem Res	10.0%
Enemy Phys Res	10.0%
'''

'''
Determine best NA combo (N4), 21 frames for dash cancel (determined it was n4)
na_mv = [.6447, .6635, .8394, .9026, .9415, 1.1819]

na_frames = [14, 25, 51, 80, 116, 184]
for i in range(6):
    print(sum(na_mv[:i+1])/(na_frames[i]+21)*60)
'''
NA_MV = [.6447, .6635, .8394, .9026, .9415, 1.1819]
charge_mv = 1.8695
skill_mv = .896
low_hp_burst_mv = 4.994
high_hp_burst_mv = 3.9952

# Frames counted by Artesians and JinJinx
skill_cast_time = 30/60 
burst_cast_time = 99/60 

n3c_time = 110/60
n3c_burst_casts = 4
n3c_casts = 5

resist_down = 0

low_hp = 1 # 0 when HP > 50% , 1 when HP is  < 50%
use_bennet = 0 # 0 when excluding bennet atk buff, 1 when including

cw_avg_stacks = 1
dm_1_opp = .5
liyue_chars = 3.0
vv_stacks = 4
dbane_passive_uptime = 1
a4_uptime = 1
base_hp = 13721

hp_to_atk = .0506

cr_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
em_cr_main_stats = AttrObj(flat_atk=311, em=187, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
em_cd_main_stats = AttrObj(flat_atk=311, em=187, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)

artifact_substats = AttrObj(flat_atk=50, atk_pct=.149, crit_rate=.198, crit_dmg=.396, em=99, er=.275, flat_hp=762, hp_pct=.249, flat_def=59, def_pct=.186)
artifact_set_effects = AttrObj(dmg_bonus={DmgTag.PYRO: .15 + .15*.5*cw_avg_stacks}) # cw
#artifact_set_effects = AttrObj(dmg_bonus={DmgTag.NORMAL: .4}) # bolide 100% shield uptime

#archaic_attr = AttrObj(base_atk=565, atk_pct=.276) # archaic, lvl 90/90, phys procs later
wt_attr = AttrObj(base_atk=401, crit_rate=.221, dmg_bonus={DmgTag.NORMAL: .48}) # white tassel R5, lvl 90/90
bt_attr = AttrObj(base_atk=354, hp_pct=.469) # black tassel, lvl 90/90, assuming not slimes
dm_attr = AttrObj(base_atk=454, crit_rate=.368, atk_pct=.16+.08*dm_1_opp) # deathmatch R1, lvl 90/90
homa_attr = AttrObj(base_atk=608, hp_pct=.2, crit_dmg=.662) # Homa R1, lvl 90/90
pjws0_attr = AttrObj(base_atk=674, crit_rate=.221) # Jade Winged Spear R1, 0 stacks, lvl 90/90
pjws7_attr = AttrObj(base_atk=674, crit_rate=.221, atk_pct=.224, dmg_bonus={DmgTag.PYRO: .12}) # Jade Winged Spear R1, 7 stacks, lvl 90/90, remember to change from PYRO if not all abilies/attacks are pyro
vv_attr = AttrObj(base_atk=608, atk_pct=.496 + vv_stacks*.04) 
vv_shield_attr = AttrObj(base_atk=608, atk_pct=.496 + vv_stacks*2*.04)
db_attr = AttrObj(base_atk=454, em=221, dmg_bonus={DmgTag.PYRO: .20*dbane_passive_uptime}) 
db_bonusless_attr = AttrObj(base_atk=454, em=221)

def n3cq_dps(weapon_attr, artifact_main_stats, artifact_substats, artifact_set_effects, vape=True, vape_bonus=0, low_hp=0, is_homa=False, use_bennet=0):
    char_attr = AttrObj(base_atk=94, crit_rate=.05, crit_dmg=.788, dmg_bonus={DmgTag.PYRO: low_hp*.33}) #crit dmg ascension stat, a4
    tot_attr = char_attr + weapon_attr + artifact_main_stats + artifact_substats + artifact_set_effects
    tot_hp = calc_tot_atk(base_hp, tot_attr.hp_pct, tot_attr.flat_hp)
    
    # Adds additional flat attack from e skill and homa passive
    skill_flat_atk = tot_hp*hp_to_atk
    if skill_flat_atk > 4*tot_attr.base_atk:
        print('Exceeds atk limit')
    tot_attr.flat_atk += skill_flat_atk
    if is_homa:
        tot_attr.flat_atk += .008*tot_hp + .01*low_hp*tot_hp # only for homa
    
    # Hail's Puretao
    # Bennet baseatk 80/80 169, 90/90 191, t6: 78.4, t8: 90, t10: 101
    # Festering 510 90/90 Favonius 454
    bennet_base_atk = 169 + 510
    bennet_atk_bonus = bennet_base_atk * .784
    tot_attr.flat_atk += bennet_atk_bonus * use_bennet
    
    n1_mv, n2_mv, n3_mv, _, _, _ = NA_MV

    vape_mult = 1
    if vape:
        vape_mult = amp_react_mult(is_strong=False, em=tot_attr.em, bonus=vape_bonus) # vape, bonus from CW
    
    charge_dmg = calc_avg_crit_dmg_obj(tot_attr, charge_mv, [DmgTag.PYRO, DmgTag.CHARGED], enemy_resist_pct=.1-resist_down)*vape_mult
    n1_dmg = calc_avg_crit_dmg_obj(tot_attr, n1_mv, [DmgTag.PYRO, DmgTag.CHARGED], enemy_resist_pct=.1-resist_down)*vape_mult
    n23_dmg = calc_avg_crit_dmg_obj(tot_attr, n2_mv + n3_mv, [DmgTag.PYRO, DmgTag.CHARGED], enemy_resist_pct=.1-resist_down)

    n3c_dmg = charge_dmg + n1_dmg + n23_dmg 

    skill_dmg = calc_avg_crit_dmg_obj(tot_attr, skill_mv, [DmgTag.PYRO, DmgTag.SKILL], enemy_resist_pct=.1-resist_down)*1 # 1 blood blossom

    burst_dmg = calc_avg_crit_dmg_obj(tot_attr, low_hp_burst_mv if low_hp else high_hp_burst_mv, [DmgTag.PYRO, DmgTag.BURST], enemy_resist_pct=.1-resist_down)*vape_mult

    #tot_n3c_dmg = n3c_dmg*n3c_casts + skill_dmg  
    tot_n3c_burst_dmg = n3c_dmg*n3c_burst_casts + skill_dmg + burst_dmg

    n3c_burst_dur = burst_cast_time + skill_cast_time + n3c_burst_casts*n3c_time
    #n3c_dur = skill_cast_time + n3c_casts*n3c_time

    n3c_burst_dps = tot_n3c_burst_dmg/n3c_burst_dur
    return n3c_burst_dps, tot_n3c_burst_dmg, n3c_burst_dur
    #n3c_dps = tot_n3c_dmg/n3c_dur

if __name__ == '__main__':
    # (weapon attributes, artifacts, is it homa?)
    weapons = {
        "White Tassel": (wt_attr, cr_main_stats, False),
        "Black Tassel": (bt_attr, cr_main_stats, False),
        "Deathmatch (Solo 50% time)": (dm_attr, cd_main_stats, False), 
        "Deathmatch (EM Sands) (Solo 50% time)": (dm_attr, em_cd_main_stats, False), 
        "DBane": (db_attr, cr_main_stats, False),
        "DBane (no bonus)": (db_bonusless_attr, cr_main_stats, False),
        "Vortex Vanquisher": (vv_attr, cr_main_stats, False), 
        "Vortex Vanquisher (Shield)": (vv_shield_attr, cr_main_stats, False), 
        "Homa": (homa_attr, cr_main_stats, True),
        "Jade Winged Spear (0 stacks)": (pjws0_attr, cr_main_stats, False),
        "Jade Winged Spear (7 stacks)": (pjws7_attr, cr_main_stats, False)
    }

    for weapon_name, weapon in weapons.items():
        print(weapon_name)
        weapon_attr, artifact_main_stats, is_homa = weapon
        n3c_burst_dps, _, _ = n3cq_dps(weapon_attr, artifact_main_stats, artifact_substats, artifact_set_effects, vape_bonus=.15, low_hp=low_hp, is_homa=is_homa, use_bennet=use_bennet)
        print("N3C Burst DPS:", n3c_burst_dps)
        #print("N3C DPS:", n3c_dps)
        print()
