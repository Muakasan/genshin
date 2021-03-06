from utils import calc_dmg, calc_dmg_obj, calc_avg_crit_dmg_obj, AttrObj, DmgTag, calc_tot_atk, amp_react_mult
from jean import n1c_dps, eeeeq_dps
from artifact_optimizer import perf_art_optim
from artifacts import MainstatType, SubstatType

# Strongly based on Zakharov's sheets https://docs.google.com/spreadsheets/d/1RAz3jx4x1ThWED8XWg8GKIf73RjPrZrnSukYZUCSRU8/edit#gid=383481181
# 90/90 weapon
hod_uptime = 1
rancour_stacks = 4
alley_uptime = 1
iron_sting_stacks = 2
blackcliff_stacks = 3
skyward_uptime = 1
summit_stacks = 5

hod_attr= AttrObj(base_atk=401, crit_dmg=.469, crit_rate=hod_uptime*.28) # R5 TODO is multiplying correct here?

rancour_attr = AttrObj(base_atk=565, dmg_bonus={DmgTag.PHYS: .345}, atk_pct=rancour_stacks*.04, def_pct=rancour_stacks*.04)
alley_flash_attr = AttrObj(base_atk=620, dmg_bonus={DmgTag.ALL: .12*alley_uptime}, em=55)
favonius_attr = AttrObj(base_atk=454, er=.613) # doesn't take into account of passive
flute_attr = AttrObj(base_atk=510, atk_pct=.413) # TODO handle passive
sac_sword_attr = AttrObj(base_atk=454, er=.613) # doesn't take into account of passive
lions_roar_attr = AttrObj(base_atk=510, atk_pct=.413) # ignores passive
iron_string_attr = AttrObj(base_atk=510, em=165, dmg_bonus={DmgTag.ALL: .06*iron_sting_stacks})
blackcliff_attr = AttrObj(base_atk=565, crit_dmg=.368, atk_pct=.12*blackcliff_stacks)
black_sword_attr = AttrObj(base_atk=510, crit_rate=.276, dmg_bonus={DmgTag.NORMAL: .2, DmgTag.CHARGED: .2})
festering_attr = AttrObj(base_atk=510, er=.459, dmg_bonus={DmgTag.SKILL: .32}) # R5 TODO take into account skill crit rate

skyward_attr = AttrObj(base_atk=608, er=.551, crit_rate=.04) # TODO handle passive
aquila_attr = AttrObj(base_atk=674, dmg_bonus={DmgTag.PHYS: .413}, atk_pct=.2) # TODO handle passive
summit_shaper_attr = AttrObj(base_atk=608, atk_pct=.496 + .04*summit_stacks) # No shield
pjc_attr = AttrObj(base_atk=542, crit_rate=.441, hp_pct=.2) # TODO handle passive


cr_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_rate=.311, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)
cd_main_stats = AttrObj(flat_atk=311, hp_pct=.466, crit_dmg=.622, dmg_bonus={DmgTag.PYRO: .466}, flat_hp=4780)

artifact_no_substats = AttrObj()

bsc2glad2_set_effects = AttrObj(dmg_bonus={DmgTag.PHYS: .25}, atk_pct=.18)
vv_set_effects = AttrObj(dmg_bonus={DmgTag.ANEMO: .15}) # Doesn't account for resist down

wt_attr = AttrObj(base_atk=401, crit_rate=.221, dmg_bonus={DmgTag.NORMAL: .48}) # white tassel R5, lvl 90/90
bt_attr = AttrObj(base_atk=354, hp_pct=.469) # black tassel, lvl 90/90, assuming not slimes

if __name__ == '__main__':
    # (weapon attributes, artifacts, is it homa?)
    weapons = {
        "White Tassel (R5)": (wt_attr, cr_main_stats, False, False),
        "Black Tassel": (bt_attr, cr_main_stats, False, False),
        "Deathmatch (2 Enemies)": (dm_2enem_attr, cr_main_stats, False, False), 
        "Deathmatch (Solo)": (dm_solo_attr, cr_main_stats, False, False), 
        "DBane": (db_attr, cr_main_stats, False, False),
        "DBane R5": (db5_attr, cr_main_stats, False, False),
        "DBane (no bonus)": (db_bonusless_attr, cr_main_stats, False, False),
        "Vortex Vanquisher (5 stacks, No Shield)": (vv_attr, cr_main_stats, False, False), 
        "Vortex Vanquisher (5 stacks, Shield)": (vv_shield_attr, cr_main_stats, False, False), 
        "Homa": (homa_attr, cr_main_stats, True, False),
        "Jade Winged Spear (0 stacks)": (pjws0_attr, cr_main_stats, False, False),
        "Jade Winged Spear (6 stacks)": (pjws6_attr, cr_main_stats, False, False),
        "Jade Winged Spear (7 stacks)": (pjws7_attr, cr_main_stats, False, False),
        "Lithic Spear (2 Liyue)": (lithic2_attr, cr_main_stats, False, False),
        "Lithic Spear (4 Liyue)": (lithic4_attr, cr_main_stats, False, False),
        "Lithic Spear (R5) (2 Liyue)": (lithic2_5_attr, cr_main_stats, False, False),
        "Lithic Spear (R5) (4 Liyue)": (lithic4_5_attr, cr_main_stats, False, False),
        "Blackcliff (0 stacks)": (bc0_attr, cr_main_stats, False, False),
        "Blackcliff (3 stacks)": (bc3_attr, cr_main_stats, False, False),
        "Skyward Spine": (sspine, cr_main_stats, False, True),
    }
    low_hp = 1 # 0 when HP > 50% , 1 when HP is  < 50%
    for weapon_name, weapon in weapons.items():
        weapon_attr, artifact_main_stats, is_homa, is_sspine = weapon
        n3c_burst_dps, _, _, _ = n3cq_dps(weapon_attr, artifact_main_stats, artifact_substats, artifact_set_effects, char_attr=char_attr, talent=8, vape=True, vape_bonus=.15, low_hp=low_hp, is_homa=is_homa, is_sspine=is_sspine)
        print(weapon_name, "(Mainstats Only):", n3c_burst_dps)

        weapon_attr, artifact_main_stats, is_homa, is_sspine = weapon
        dps_func = lambda art_mains, art_subs: n3cq_dps(weapon_attr, art_mains, art_subs, artifact_set_effects, char_attr=char_attr, talent=8, vape=True, vape_bonus=.15, low_hp=low_hp, is_homa=is_homa, is_sspine=is_sspine, supress=True)
        highest_dps, highest_mainstat_attr, highest_substat_attr, highest_substat_dist, highest_tot_attr = perf_art_optim(dps_func, 
            sandss=[MainstatType.HP_PCT], goblets=["PYRO"], circlets=[MainstatType.CRIT_DMG, MainstatType.CRIT_RATE], 
            substats=[SubstatType.CRIT_RATE, SubstatType.CRIT_DMG, SubstatType.EM, SubstatType.HP_PCT])
        print(weapon_name, "(Perfect Subs):", highest_dps)
        print("Substats:\n", highest_substat_attr)
        print("Main Stats:\n",  highest_mainstat_attr)
        print("Total Stats:\n", highest_tot_attr)

        print()
