import random
import json
import time
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
import copy
import math


class Rarity(Enum):
    COMMON = "Common"
    MAGIC = "Magic"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    MYTHIC = "Mythic"


class ItemType(Enum):
    WEAPON = "Weapon"
    OFFHAND = "Offhand"
    ARMOR = "Armor"
    RING = "Ring"
    AMULET = "Amulet"
    TRINKET = "Trinket"
    CONSUMABLE = "Consumable"
    MATERIAL = "Material"
    QUEST = "Quest"
    RUNE = "Rune"


class PlayerClass(Enum):
    KNIGHT = "Knight"
    PRIESTESS = "Priestess"
    PATHFINDER = "Pathfinder"
    ENGINEER = "Engineer"
    CRUSADER = "Crusader"
    BARBARIAN = "Barbarian"
    GUNSLINGER = "Gunslinger"
    WIZARD = "Wizard"
    SHADOWBLADE = "Shadowblade"
    DRUID = "Druid"


class StatusEffectType(Enum):
    # Damage over time
    POISON = "Poison"
    BURN = "Burn"
    BLEED = "Bleed"
    FREEZE = "Freeze"
    SHOCK = "Shock"

    # Stat modifications
    STRENGTH = "Strength"
    WEAKNESS = "Weakness"
    FORTIFIED = "Fortified"
    VULNERABLE = "Vulnerable"
    SWIFT = "Swift"
    SLOWED = "Slowed"
    FOCUSED = "Focused"
    CONFUSED = "Confused"

    # Special conditions
    STUNNED = "Stunned"
    SLEEPING = "Sleeping"
    BLESSED = "Blessed"
    CURSED = "Cursed"
    REGENERATION = "Regeneration"
    MANA_BURN = "Mana Burn"
    SHIELD = "Shield"
    THORNS = "Thorns"
    LIFESTEAL = "Lifesteal"
    INVISIBLE = "Invisible"
    MARKED = "Marked"
    EMPOWERED = "Empowered"

    # New enhanced effects
    BERSERKER = "Berserker"
    PRECISION = "Precision"
    ELEMENTAL_MASTERY = "Elemental Mastery"
    TIME_DILATION = "Time Dilation"
    SOUL_BURN = "Soul Burn"
    NATURE_BOND = "Nature Bond"


class DifficultyMode(Enum):
    EASY = "Easy"
    NORMAL = "Normal"
    HARD = "Hard"
    NIGHTMARE = "Nightmare"
    APOCALYPSE = "Apocalypse"


class SkillTier(Enum):
    NOVICE = 1
    ADEPT = 2
    EXPERT = 3
    MASTER = 4
    GRANDMASTER = 5


@dataclass
class StatusEffect:
    effect_type: StatusEffectType
    duration: int
    power: int = 0
    description: str = ""
    stacks: int = 1
    max_stacks: int = 5

    def __post_init__(self):
        if not self.description:
            self.description = self.get_default_description()

    def get_default_description(self):
        descriptions = {
            StatusEffectType.POISON: f"Taking {self.power} poison damage per turn (Stacks: {self.stacks})",
            StatusEffectType.BURN: f"Taking {self.power} fire damage per turn",
            StatusEffectType.BLEED: f"Taking {self.power} bleeding damage per turn",
            StatusEffectType.FREEZE: f"Movement and actions slowed, taking {self.power} ice damage",
            StatusEffectType.SHOCK: f"Taking {self.power} lightning damage, chance to spread",
            StatusEffectType.STRENGTH: f"Attack increased by {self.power}",
            StatusEffectType.WEAKNESS: f"Attack decreased by {self.power}",
            StatusEffectType.FORTIFIED: f"Defense increased by {self.power}",
            StatusEffectType.VULNERABLE: f"Defense decreased by {self.power}",
            StatusEffectType.SWIFT: f"Agility increased by {self.power}, dodge chance +{self.power // 2}%",
            StatusEffectType.SLOWED: f"Agility decreased by {self.power}",
            StatusEffectType.FOCUSED: f"Mana efficiency increased by {self.power}%, crit chance +{self.power // 2}%",
            StatusEffectType.CONFUSED: f"Mana costs increased by {self.power}%, miss chance +{self.power}%",
            StatusEffectType.STUNNED: "Cannot act this turn",
            StatusEffectType.SLEEPING: "Cannot act and takes double damage",
            StatusEffectType.BLESSED: f"All stats increased by {self.power}",
            StatusEffectType.CURSED: f"All stats decreased by {self.power}",
            StatusEffectType.REGENERATION: f"Healing {self.power} HP per turn",
            StatusEffectType.MANA_BURN: f"Losing {self.power} mana per turn",
            StatusEffectType.SHIELD: f"Absorbing up to {self.power} damage",
            StatusEffectType.THORNS: f"Reflecting {self.power} damage to attackers",
            StatusEffectType.LIFESTEAL: f"Stealing {self.power}% of damage dealt as health",
            StatusEffectType.INVISIBLE: f"Cannot be targeted, +{self.power}% dodge chance",
            StatusEffectType.MARKED: f"Taking {self.power}% extra damage from all sources",
            StatusEffectType.EMPOWERED: f"All abilities deal {self.power}% extra damage",
            StatusEffectType.BERSERKER: f"Attack +{self.power}%, take +{self.power // 2}% damage",
            StatusEffectType.PRECISION: f"Next {self.power} attacks cannot miss and deal +50% damage",
            StatusEffectType.ELEMENTAL_MASTERY: f"All elemental damage increased by {self.power}%",
            StatusEffectType.TIME_DILATION: f"All cooldowns reduced by {self.power} each turn",
            StatusEffectType.SOUL_BURN: f"Mana and HP burn for {self.power} each turn",
            StatusEffectType.NATURE_BOND: f"Regenerate {self.power} HP and gain +{self.power // 2} to all stats"
        }
        return descriptions.get(self.effect_type, "Unknown effect")


@dataclass
class SkillProgression:
    skill_exp: int = 0
    skill_level: int = 1
    max_skill_level: int = 10
    mastery_points: int = 0
    evolution_path: str = ""

    def gain_exp(self, amount: int):
        self.skill_exp += amount
        exp_needed = self.skill_level * 100

        if self.skill_exp >= exp_needed and self.skill_level < self.max_skill_level:
            self.skill_exp -= exp_needed
            self.skill_level += 1
            self.mastery_points += 1
            return True
        return False


@dataclass
class SkillNode:
    name: str
    unlocked: bool = False
    prerequisites: List[str] = field(default_factory=list)
    description: str = ""
    effect: str = ""


@dataclass
class Skill:
    name: str
    tier: int
    mana_cost: int
    damage: int = 0
    heal: int = 0
    buff_type: str = ""
    buff_value: int = 0
    debuff_type: str = ""
    debuff_value: int = 0
    status_effects: List[StatusEffect] = field(default_factory=list)
    description: str = ""
    unlocked: bool = False
    level_requirement: int = 1
    cooldown: int = 0
    current_cooldown: int = 0
    combo_with: List[str] = field(default_factory=list)

    # Enhanced skill system
    progression: SkillProgression = field(default_factory=SkillProgression)
    skill_type: str = "active"  # active, passive, toggle, channel
    casting_time: int = 0  # turns to cast
    channel_duration: int = 0  # turns to channel
    area_effect: bool = False
    target_type: str = "enemy"  # enemy, self, ally, area
    resource_type: str = "mana"  # mana, energy, rage, focus, soul
    resource_cost: int = 0
    proc_chance: float = 0.0  # chance to trigger on hit/crit
    scaling_stat: str = "attack"  # which stat scales the skill
    elemental_type: str = ""  # fire, ice, lightning, nature, shadow, holy

    # Skill evolution
    can_evolve: bool = False
    evolution_requirements: Dict[str, int] = field(default_factory=dict)
    evolved_form: str = ""

    # Mastery bonuses
    mastery_effects: List[str] = field(default_factory=list)

    def is_ready(self):
        return self.current_cooldown == 0

    def use(self):
        self.current_cooldown = self.cooldown
        # Gain skill experience
        self.progression.gain_exp(random.randint(10, 25))

    def reduce_cooldown(self, amount: int = 1):
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - amount)

    def get_effective_value(self, base_value: int, stat_value: int) -> int:
        """Calculate skill effectiveness based on skill level and scaling stat"""
        skill_multiplier = 1.0 + (self.progression.skill_level - 1) * 0.15
        stat_scaling = 1.0 + (stat_value * 0.02)
        return int(base_value * skill_multiplier * stat_scaling)

    def check_evolution(self) -> bool:
        """Check if skill can evolve"""
        if not self.can_evolve or self.evolved_form:
            return False

        for requirement, needed in self.evolution_requirements.items():
            if requirement == "skill_level" and self.progression.skill_level < needed:
                return False
            elif requirement == "mastery_points" and self.progression.mastery_points < needed:
                return False

        return True


@dataclass
class ClassResource:
    name: str
    current: int
    maximum: int
    regen_rate: int = 0
    decay_rate: int = 0

    def gain(self, amount: int):
        self.current = min(self.maximum, self.current + amount)

    def spend(self, amount: int) -> bool:
        if self.current >= amount:
            self.current -= amount
            return True
        return False

    def process_turn(self):
        """Process resource regeneration/decay"""
        if self.regen_rate > 0:
            self.gain(self.regen_rate)
        if self.decay_rate > 0:
            self.current = max(0, self.current - self.decay_rate)


@dataclass
class ComboChain:
    skills: List[str]
    bonus_damage: int
    bonus_effects: List[StatusEffect] = field(default_factory=list)
    required_sequence: bool = True
    window_turns: int = 3


@dataclass
class Item:
    name: str
    item_type: ItemType
    rarity: Rarity
    value: int
    durability: int = 100
    max_durability: int = 100
    class_requirement: Optional[PlayerClass] = None
    level_requirement: int = 1
    modifiers: Dict[str, int] = field(default_factory=dict)
    status_effects_on_use: List[StatusEffect] = field(default_factory=list)
    status_effects_on_hit: List[StatusEffect] = field(default_factory=list)
    description: str = ""
    enchantment_level: int = 0
    max_enchantment: int = 5
    sockets: int = 0
    socketed_runes: List['Rune'] = field(default_factory=list)
    set_name: str = ""
    set_pieces_required: int = 0


@dataclass
class Rune:
    name: str
    tier: int
    effect_type: str
    effect_value: int
    description: str


@dataclass
class Monster:
    name: str
    level: int
    hp: int
    max_hp: int
    mana: int
    max_mana: int
    attack: int
    defense: int
    agility: int
    skills: List[str]
    rarity: Rarity
    loot_table: List[str] = field(default_factory=list)
    status_effects: Dict[StatusEffectType, StatusEffect] = field(default_factory=dict)
    weaknesses: List[StatusEffectType] = field(default_factory=list)
    resistances: List[StatusEffectType] = field(default_factory=list)
    boss_tier: int = 0  # 0 = normal, 1 = mini-boss, 2 = boss, 3 = world boss


@dataclass
class Achievement:
    name: str
    description: str
    requirement: str
    reward_type: str
    reward_value: int
    completed: bool = False
    progress: int = 0
    target: int = 1


@dataclass
class ComboTracker:
    combo_count: int = 0
    last_skills: List[str] = field(default_factory=list)
    combo_damage_multiplier: float = 1.0
    combo_timer: int = 0
    active_chains: List[ComboChain] = field(default_factory=list)


class GameState:
    def __init__(self):
        self.player = None
        self.current_location = "town"
        self.current_dungeon = None
        self.current_level = 1
        self.current_room = 1
        self.last_shrine_use = None
        self.shop_inventory = {}
        self.last_shop_refresh = None
        self.game_day = 1
        self.difficulty = DifficultyMode.NORMAL
        self.achievements = self.initialize_achievements()
        self.total_monsters_killed = 0
        self.total_gold_earned = 0
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        self.fastest_boss_kill = float('inf')
        self.highest_combo = 0
        self.crafting_recipes = self.initialize_crafting_recipes()
        self.discovered_lore = []
        self.reputation = {"town": 0, "guild": 0, "church": 0, "underground": 0}

    def advance_day(self):
        self.game_day += 1
        if self.last_shop_refresh != self.game_day:
            self.refresh_shops()

    def refresh_shops(self):
        self.last_shop_refresh = self.game_day
        self.shop_inventory = generate_shop_inventory(self.player.level if self.player else 1)

    def initialize_achievements(self):
        return [
            Achievement("First Blood", "Kill your first monster", "kill_monster", "gold", 100),
            Achievement("Monster Hunter", "Kill 100 monsters", "kill_monster", "skill_point", 2, target=100),
            Achievement("Rich Adventurer", "Accumulate 10,000 gold", "earn_gold", "item", 1, target=10000),
            Achievement("Combo Master", "Achieve a 10-hit combo", "combo", "gold", 500, target=10),
            Achievement("Survivor", "Survive with less than 10% HP", "survive_low", "gold", 300),
            Achievement("Speed Demon", "Kill a boss in under 5 turns", "fast_boss", "skill_point", 3),
            Achievement("Perfectionist", "Complete a dungeon without taking damage", "no_damage", "item", 1),
            Achievement("Collector", "Collect 50 unique items", "collect_items", "gold", 1000, target=50),
            Achievement("Skill Master", "Max out any skill to level 10", "max_skill", "skill_point", 5),
            Achievement("Evolution", "Evolve a skill", "evolve_skill", "gold", 2000),
        ]

    def initialize_crafting_recipes(self):
        return {
            "Enhanced Health Potion": {
                "materials": {"Health Potion": 3, "Herb": 2},
                "result": Item("Enhanced Health Potion", ItemType.CONSUMABLE, Rarity.MAGIC, 100,
                               status_effects_on_use=[StatusEffect(StatusEffectType.REGENERATION, 5, 15)],
                               description="Restores 200 HP with strong regeneration")
            },
            "Weapon Enhancement Kit": {
                "materials": {"Iron Ore": 5, "Magic Essence": 2},
                "result": Item("Weapon Enhancement Kit", ItemType.MATERIAL, Rarity.RARE, 250,
                               description="Enhances weapon damage by +5 permanently")
            },
            "Armor Reinforcement Kit": {
                "materials": {"Steel Plate": 3, "Leather": 4},
                "result": Item("Armor Reinforcement Kit", ItemType.MATERIAL, Rarity.RARE, 250,
                               description="Enhances armor defense by +5 permanently")
            }
        }

    def check_achievement(self, achievement_type: str, value: int = 1):
        for achievement in self.achievements:
            if achievement.requirement == achievement_type and not achievement.completed:
                achievement.progress += value
                if achievement.progress >= achievement.target:
                    achievement.completed = True
                    return achievement
        return None


class Player:
    def __init__(self, name: str, player_class: PlayerClass):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.skill_points = 1

        # Base stats
        base_stats = self.get_base_stats()
        self.max_hp = base_stats["hp"]
        self.hp = self.max_hp
        self.max_mana = base_stats["mana"]
        self.mana = self.max_mana
        self.attack = base_stats["attack"]
        self.defense = base_stats["defense"]
        self.agility = base_stats["agility"]
        self.crit_chance = base_stats.get("crit_chance", 5)
        self.crit_damage = base_stats.get("crit_damage", 150)

        self.gold = 500
        self.inventory = {}
        self.equipment = {
            "weapon": None,
            "offhand": None,
            "armor": None,
            "ring1": None,
            "ring2": None,
            "amulet": None,
            "trinket": None
        }

        # Enhanced skill system
        self.skills = self.get_class_skills()
        self.skill_trees = self.initialize_skill_trees()
        self.combo_chains = self.get_combo_chains()
        self.class_resources = self.initialize_class_resources()

        self.buffs = {}
        self.debuffs = {}
        self.status_effects = {}
        self.combo_tracker = ComboTracker()

        # Unlock first tier 1 skill
        for skill_name, skill in self.skills.items():
            if skill.tier == 1:
                skill.unlocked = True
                break

        # Class-specific passive abilities
        self.passive_abilities = self.get_passive_abilities()

    def initialize_class_resources(self):
        """Initialize class-specific resources"""
        resources = {}

        if self.player_class == PlayerClass.BARBARIAN:
            resources["rage"] = ClassResource("Rage", 0, 100, 0, 5)
        elif self.player_class == PlayerClass.PATHFINDER:
            resources["focus"] = ClassResource("Focus", 50, 100, 2, 1)
        elif self.player_class == PlayerClass.ENGINEER:
            resources["energy"] = ClassResource("Energy", 100, 100, 5, 0)
        elif self.player_class == PlayerClass.SHADOWBLADE:
            resources["shadow"] = ClassResource("Shadow Energy", 50, 100, 3, 2)
        elif self.player_class == PlayerClass.CRUSADER:
            resources["holy_power"] = ClassResource("Holy Power", 30, 100, 1, 0)
        elif self.player_class == PlayerClass.DRUID:
            resources["nature_essence"] = ClassResource("Nature Essence", 75, 100, 3, 1)
        elif self.player_class == PlayerClass.GUNSLINGER:
            resources["ammo"] = ClassResource("Ammo", 6, 12, 0, 0)
        elif self.player_class == PlayerClass.WIZARD:
            resources["arcane_power"] = ClassResource("Arcane Power", 25, 100, 2, 0)
        elif self.player_class == PlayerClass.PRIESTESS:
            resources["faith"] = ClassResource("Faith", 40, 100, 2, 0)
        elif self.player_class == PlayerClass.KNIGHT:
            resources["stamina"] = ClassResource("Stamina", 80, 100, 3, 1)

        return resources

    def initialize_skill_trees(self):
        """Initialize skill tree nodes for character progression"""
        trees = {}

        if self.player_class == PlayerClass.KNIGHT:
            trees = {
                "Guardian Path": [
                    SkillNode("Shield Mastery", False, [], "Reduces Shield Bash cooldown by 1", "cooldown_reduction"),
                    SkillNode("Fortress Stance", False, ["Shield Mastery"], "Defense abilities last +2 turns",
                              "duration_boost"),
                    SkillNode("Aegis Protocol", False, ["Fortress Stance"], "Shield effects spread to nearby allies",
                              "area_effect")
                ],
                "Berserker Path": [
                    SkillNode("Rage Building", False, [], "Gain stamina when taking damage", "resource_gain"),
                    SkillNode("Endless Fury", False, ["Rage Building"], "Attack abilities cost -50% stamina",
                              "cost_reduction"),
                    SkillNode("Unstoppable Force", False, ["Endless Fury"], "Cannot be stunned or slowed", "immunity")
                ]
            }
        elif self.player_class == PlayerClass.WIZARD:
            trees = {
                "Elementalist Path": [
                    SkillNode("Spell Fusion", False, [], "Combine elemental effects for bonus damage", "spell_synergy"),
                    SkillNode("Arcane Resonance", False, ["Spell Fusion"], "Spells have 25% chance to not consume mana",
                              "mana_efficiency"),
                    SkillNode("Reality Shaper", False, ["Arcane Resonance"], "All spells gain area effect",
                              "area_mastery")
                ],
                "Time Mage Path": [
                    SkillNode("Temporal Flux", False, [], "Gain Time Dilation when casting spells", "time_magic"),
                    SkillNode("Chrono Lock", False, ["Temporal Flux"], "Can delay spell effects by up to 3 turns",
                              "delayed_cast"),
                    SkillNode("Time Lord", False, ["Chrono Lock"], "Take an extra turn every 5 rounds", "extra_action")
                ]
            }
        elif self.player_class == PlayerClass.PRIESTESS:
            trees = {
                "Holy Path": [
                    SkillNode("Divine Grace", False, [], "Healing spells restore +20% more HP", "healing_boost"),
                    SkillNode("Sacred Bond", False, ["Divine Grace"],
                              "Healing grants temporary shield equal to 50% heal",
                              "heal_shield"),
                    SkillNode("Miracle Worker", False, ["Sacred Bond"], "25% chance to not consume mana on heals",
                              "heal_efficiency")
                ],
                "Battle Cleric Path": [
                    SkillNode("Righteous Fury", False, [], "Gain faith when dealing damage", "faith_on_damage"),
                    SkillNode("Divine Retribution", False, ["Righteous Fury"], "Holy damage +30%, undead take double",
                              "holy_power"),
                    SkillNode("Crusader's Might", False, ["Divine Retribution"], "Attack abilities also heal allies",
                              "battle_healing")
                ]
            }
        elif self.player_class == PlayerClass.PATHFINDER:
            trees = {
                "Marksman Path": [
                    SkillNode("Eagle Eye", False, [], "Critical hit chance +10% on marked targets", "mark_crit"),
                    SkillNode("Perfect Shot", False, ["Eagle Eye"], "First attack each combat cannot miss",
                              "guaranteed_hit"),
                    SkillNode("Death Mark", False, ["Perfect Shot"], "Marked targets take increasing damage over time",
                              "escalating_mark")
                ],
                "Ranger Path": [
                    SkillNode("Nature's Ally", False, [], "Gain focus regeneration in combat", "focus_regen"),
                    SkillNode("Beast Master", False, ["Nature's Ally"], "Summon animal companion for 5 turns",
                              "companion"),
                    SkillNode("Wild Hunt", False, ["Beast Master"], "You and companion gain +50% speed and damage",
                              "hunt_mode")
                ]
            }
        elif self.player_class == PlayerClass.ENGINEER:
            trees = {
                "Inventor Path": [
                    SkillNode("Efficient Design", False, [], "All gadgets cost -20% energy", "energy_efficiency"),
                    SkillNode("Overcharge", False, ["Efficient Design"], "Energy abilities can exceed normal limits",
                              "overcharge"),
                    SkillNode("Perpetual Motion", False, ["Overcharge"], "Regenerate 10 energy per turn permanently",
                              "energy_perpetual")
                ],
                "Demolition Path": [
                    SkillNode("Explosive Expert", False, [], "Trap and bomb damage +30%", "explosive_damage"),
                    SkillNode("Chain Reaction", False, ["Explosive Expert"],
                              "Explosions have 50% chance to trigger again",
                              "chain_explosions"),
                    SkillNode("Scorched Earth", False, ["Chain Reaction"], "All attacks apply burn for 3 turns",
                              "burn_all")
                ]
            }
        elif self.player_class == PlayerClass.CRUSADER:
            trees = {
                "Zealot Path": [
                    SkillNode("Fervor", False, [], "Gain holy power equal to damage dealt / 10", "holy_generation"),
                    SkillNode("Sacred Weapon", False, ["Fervor"], "Weapon attacks deal bonus holy damage",
                              "holy_weapon"),
                    SkillNode("Divine Champion", False, ["Sacred Weapon"], "Cannot drop below 1 HP while blessed",
                              "divine_protection")
                ],
                "Templar Path": [
                    SkillNode("Consecration", False, [], "Create holy ground that heals allies", "consecrate"),
                    SkillNode("Sanctuary", False, ["Consecration"], "Allies gain +20 defense on holy ground",
                              "sanctuary_defense"),
                    SkillNode("Hallowed Ground", False, ["Sanctuary"], "Undead instantly die on holy ground",
                              "holy_ground")
                ]
            }
        elif self.player_class == PlayerClass.BARBARIAN:
            trees = {
                "Fury Path": [
                    SkillNode("Blood for Blood", False, [], "Gain rage equal to damage taken", "rage_from_damage"),
                    SkillNode("Rampage", False, ["Blood for Blood"], "Each kill grants +10% damage for 5 turns",
                              "kill_streak"),
                    SkillNode("Endless Rage", False, ["Rampage"], "Rage no longer decays in combat",
                              "rage_sustain")
                ],
                "Survivor Path": [
                    SkillNode("Thick Skin", False, [], "Reduce all damage taken by 15%", "damage_reduction"),
                    SkillNode("Blood Thirst", False, ["Thick Skin"], "All attacks lifesteal for 20% damage",
                              "lifesteal_all"),
                    SkillNode("Undying Rage", False, ["Blood Thirst"], "Gain 100 rage and full heal when near death",
                              "death_prevention")
                ]
            }
        elif self.player_class == PlayerClass.GUNSLINGER:
            trees = {
                "Sharpshooter Path": [
                    SkillNode("Quick Draw", False, [], "First ability each combat has no cooldown", "quick_start"),
                    SkillNode("Bullet Time", False, ["Quick Draw"], "25% chance to take an extra action",
                              "extra_actions"),
                    SkillNode("Dead Eye", False, ["Bullet Time"], "Critical hits instantly kill enemies below 30% HP",
                              "execute")
                ],
                "Desperado Path": [
                    SkillNode("Fan the Hammer", False, [], "Basic attacks hit twice", "double_tap"),
                    SkillNode("Ricochet", False, ["Fan the Hammer"], "Attacks bounce to nearby enemies",
                              "ricochet"),
                    SkillNode("High Noon", False, ["Ricochet"],
                              "Once per combat, attack all enemies for massive damage",
                              "ultimate_barrage")
                ]
            }
        elif self.player_class == PlayerClass.SHADOWBLADE:
            trees = {
                "Assassin Path": [
                    SkillNode("Lethality", False, [], "Critical strikes apply deadly poison", "crit_poison"),
                    SkillNode("Shadow Strike", False, ["Lethality"], "Attacks from stealth always crit",
                              "stealth_crit"),
                    SkillNode("Death's Shadow", False, ["Shadow Strike"], "Instantly kill enemies below 20% HP",
                              "assassinate")
                ],
                "Trickster Path": [
                    SkillNode("Smoke Screen", False, [], "Gain invisibility when health drops below 50%",
                              "escape_stealth"),
                    SkillNode("Decoy", False, ["Smoke Screen"], "Create illusions that confuse enemies",
                              "illusions"),
                    SkillNode("Master of Shadows", False, ["Decoy"], "All abilities grant 1 turn of invisibility",
                              "perma_stealth")
                ]
            }
        elif self.player_class == PlayerClass.DRUID:
            trees = {
                "Nature Path": [
                    SkillNode("One with Nature", False, [], "Regenerate 5% HP per turn", "nature_regen"),
                    SkillNode("Wild Growth", False, ["One with Nature"], "Healing abilities affect all allies",
                              "group_heal"),
                    SkillNode("Force of Nature", False, ["Wild Growth"], "Summon treants to fight alongside you",
                              "summon_treants")
                ],
                "Shapeshifter Path": [
                    SkillNode("Primal Instincts", False, [], "Gain stats based on current form", "form_bonus"),
                    SkillNode("Fluid Forms", False, ["Primal Instincts"], "Can change forms once per turn",
                              "form_flexibility"),
                    SkillNode("Master Shapeshifter", False, ["Fluid Forms"],
                              "Gain benefits of all forms simultaneously",
                              "all_forms")
                ]
            }

        return trees

    def get_combo_chains(self):
        """Define combo chains for each class"""
        chains = []

        if self.player_class == PlayerClass.KNIGHT:
            chains = [
                ComboChain(["Shield Bash", "Sword Strike"], 15,
                           [StatusEffect(StatusEffectType.VULNERABLE, 2, 15)]),
                ComboChain(["Sword Strike", "Power Attack", "Divine Blade"], 50,
                           [StatusEffect(StatusEffectType.EMPOWERED, 3, 25)])
            ]
        elif self.player_class == PlayerClass.WIZARD:
            chains = [
                ComboChain(["Magic Missile", "Fireball"], 20,
                           [StatusEffect(StatusEffectType.BURN, 3, 15)]),
                ComboChain(["Fireball", "Lightning Bolt", "Meteor"], 75,
                           [StatusEffect(StatusEffectType.ELEMENTAL_MASTERY, 4, 30)])
            ]
        elif self.player_class == PlayerClass.BARBARIAN:
            chains = [
                ComboChain(["Rage Strike", "Berserker Fury"], 25,
                           [StatusEffect(StatusEffectType.BERSERKER, 4, 30)]),
                ComboChain(["Whirlwind", "Blood Frenzy", "Apocalypse Slam"], 100,
                           [StatusEffect(StatusEffectType.LIFESTEAL, 5, 50)])
            ]
        elif self.player_class == PlayerClass.PATHFINDER:
            chains = [
                ComboChain(["Precision Shot", "Hunter's Mark"], 15,
                           [StatusEffect(StatusEffectType.MARKED, 5, 30)]),
                ComboChain(["Precision Shot", "Multi-Shot", "Storm of Arrows"], 60,
                           [StatusEffect(StatusEffectType.PRECISION, 5, 5)])
            ]
        elif self.player_class == PlayerClass.SHADOWBLADE:
            chains = [
                ComboChain(["Shadow Strike", "Poison Blade"], 20,
                           [StatusEffect(StatusEffectType.POISON, 5, 15)]),
                ComboChain(["Shadow Strike", "Shadow Step", "Assassinate"], 80,
                           [StatusEffect(StatusEffectType.SOUL_BURN, 5, 20)])
            ]
        elif self.player_class == PlayerClass.PRIESTESS:
            chains = [
                ComboChain(["Holy Light", "Sacred Shield"], 0,
                           [StatusEffect(StatusEffectType.BLESSED, 5, 15)]),
                ComboChain(["Holy Light", "Divine Strike", "Divine Intervention"], 40,
                           [StatusEffect(StatusEffectType.REGENERATION, 8, 20)])
            ]
        elif self.player_class == PlayerClass.ENGINEER:
            chains = [
                ComboChain(["Shock Trap", "Overclock"], 25,
                           [StatusEffect(StatusEffectType.STUNNED, 2)]),
                ComboChain(["Shock Trap", "Flame Turret", "EMP Blast"], 70,
                           [StatusEffect(StatusEffectType.VULNERABLE, 6, 30)])
            ]
        elif self.player_class == PlayerClass.CRUSADER:
            chains = [
                ComboChain(["Holy Strike", "Consecration"], 20,
                           [StatusEffect(StatusEffectType.BLESSED, 4, 10)]),
                ComboChain(["Holy Strike", "Hammer of Wrath", "Divine Storm"], 90,
                           [StatusEffect(StatusEffectType.BURN, 6, 20)])
            ]
        elif self.player_class == PlayerClass.GUNSLINGER:
            chains = [
                ComboChain(["Quick Shot", "Fan the Hammer"], 25,
                           [StatusEffect(StatusEffectType.PRECISION, 3, 3)]),
                ComboChain(["Quick Shot", "Explosive Shot", "High Noon"], 85,
                           [StatusEffect(StatusEffectType.MARKED, 8, 40)])
            ]
        elif self.player_class == PlayerClass.DRUID:
            chains = [
                ComboChain(["Nature's Touch", "Thorns"], 0,
                           [StatusEffect(StatusEffectType.NATURE_BOND, 5, 15)]),
                ComboChain(["Nature's Touch", "Entangling Roots", "Force of Nature"], 65,
                           [StatusEffect(StatusEffectType.REGENERATION, 10, 15)])
            ]

        return chains

    def get_passive_abilities(self):
        passives = {
            PlayerClass.KNIGHT: {"damage_reduction": 10, "block_chance": 15, "stamina_regen": 3},
            PlayerClass.PRIESTESS: {"healing_bonus": 25, "mana_regen": 3, "faith_on_heal": 5},
            PlayerClass.PATHFINDER: {"dodge_chance": 20, "crit_chance": 10, "focus_on_crit": 10},
            PlayerClass.ENGINEER: {"durability_loss_reduction": 50, "trap_damage_bonus": 30, "energy_efficiency": 20},
            PlayerClass.CRUSADER: {"holy_damage_bonus": 20, "undead_damage_bonus": 30, "holy_power_on_kill": 15},
            PlayerClass.BARBARIAN: {"lifesteal": 15, "rage_on_kill": 20, "rage_on_damage": 5},
            PlayerClass.GUNSLINGER: {"double_strike_chance": 25, "reload_speed": 2, "precision_shots": 15},
            PlayerClass.WIZARD: {"spell_power": 30, "mana_shield": True, "arcane_power_on_cast": 5},
            PlayerClass.SHADOWBLADE: {"stealth_crit_bonus": 50, "poison_chance": 20, "shadow_step": True},
            PlayerClass.DRUID: {"nature_resistance": 30, "companion_summon": True, "nature_bond": 10}
        }
        return passives.get(self.player_class, {})

    def process_class_resources(self):
        """Process class-specific resource regeneration/decay"""
        messages = []

        for resource_name, resource in self.class_resources.items():
            old_value = resource.current
            resource.process_turn()

            if resource.current != old_value:
                if resource.current > old_value:
                    messages.append(f"🔋 {resource.name} regenerated: {resource.current}/{resource.maximum}")
                else:
                    messages.append(f"💨 {resource.name} decayed: {resource.current}/{resource.maximum}")

        return messages

    def check_combo_chains(self, skill_name: str):
        """Check if a skill completes any combo chains"""
        completed_chains = []

        # Add skill to recent history
        self.combo_tracker.last_skills.append(skill_name)
        if len(self.combo_tracker.last_skills) > 5:  # Keep last 5 skills
            self.combo_tracker.last_skills.pop(0)

        # Check each combo chain
        for chain in self.combo_chains:
            if self.is_chain_completed(chain):
                completed_chains.append(chain)

        return completed_chains

    def is_chain_completed(self, chain: ComboChain) -> bool:
        """Check if a combo chain is completed"""
        if len(self.combo_tracker.last_skills) < len(chain.skills):
            return False

        if chain.required_sequence:
            # Check exact sequence
            recent_skills = self.combo_tracker.last_skills[-len(chain.skills):]
            return recent_skills == chain.skills
        else:
            # Check if all skills are present (any order)
            return all(skill in self.combo_tracker.last_skills[-chain.window_turns:] for skill in chain.skills)

    def add_status_effect(self, status_effect: StatusEffect):
        """Add or refresh a status effect with stacking logic"""
        effect_type = status_effect.effect_type

        if effect_type in self.status_effects:
            existing = self.status_effects[effect_type]

            # Stackable damage effects
            if effect_type in [StatusEffectType.POISON, StatusEffectType.BURN,
                               StatusEffectType.BLEED, StatusEffectType.FREEZE]:
                if existing.stacks < existing.max_stacks:
                    existing.stacks += 1
                    existing.power = int(existing.power * (1 + 0.2 * existing.stacks))
                existing.duration = max(existing.duration, status_effect.duration)
            else:
                # Non-stackable effects - refresh duration and update power if stronger
                existing.duration = max(existing.duration, status_effect.duration)
                if status_effect.power > existing.power:
                    existing.power = status_effect.power
        else:
            self.status_effects[effect_type] = status_effect

    def remove_status_effect(self, effect_type: StatusEffectType):
        """Remove a status effect"""
        if effect_type in self.status_effects:
            del self.status_effects[effect_type]

    def process_status_effects(self):
        """Process all status effects at start of turn"""
        effects_to_remove = []
        messages = []

        for effect_type, effect in self.status_effects.items():
            # Skip processing for permanent effects (duration 999)
            if effect.duration == 999:
                continue

            # Process the effect
            if effect_type == StatusEffectType.POISON:
                damage = min(effect.power * effect.stacks, self.hp)
                self.hp -= damage
                messages.append(f"🤢 Poison deals {damage} damage! (Stacks: {effect.stacks})")

            elif effect_type == StatusEffectType.BURN:
                damage = min(effect.power, self.hp)
                self.hp -= damage
                messages.append(f"🔥 Burn deals {damage} damage!")

            elif effect_type == StatusEffectType.BLEED:
                damage = min(effect.power, self.hp)
                self.hp -= damage
                messages.append(f"🩸 Bleeding deals {damage} damage!")

            elif effect_type == StatusEffectType.FREEZE:
                damage = min(effect.power, self.hp)
                self.hp -= damage
                messages.append(f"🧊 Freeze deals {damage} damage and slows you!")

            elif effect_type == StatusEffectType.SHOCK:
                damage = min(effect.power, self.hp)
                self.hp -= damage
                messages.append(f"⚡ Shock deals {damage} damage!")
                # Chance to spread to self (10%)
                if random.random() < 0.1:
                    messages.append(f"⚡ Shock spreads!")

            elif effect_type == StatusEffectType.REGENERATION:
                heal = min(effect.power, self.get_total_stats()["hp"] - self.hp)
                self.hp += heal
                if heal > 0:
                    messages.append(f"💚 Regeneration heals {heal} HP!")

            elif effect_type == StatusEffectType.MANA_BURN:
                mana_loss = min(effect.power, self.mana)
                self.mana -= mana_loss
                if mana_loss > 0:
                    messages.append(f"💜 Mana burn drains {mana_loss} mana!")

            elif effect_type == StatusEffectType.TIME_DILATION:
                # Reduce all cooldowns
                for skill in self.skills.values():
                    skill.reduce_cooldown(effect.power)
                messages.append(f"⏰ Time flows faster - cooldowns reduced by {effect.power}!")

            elif effect_type == StatusEffectType.NATURE_BOND:
                heal = min(effect.power, self.get_total_stats()["hp"] - self.hp)
                self.hp += heal
                if heal > 0:
                    messages.append(f"🌿 Nature bond heals {heal} HP and empowers you!")

            elif effect_type == StatusEffectType.SOUL_BURN:
                damage = min(effect.power, self.hp)
                mana_loss = min(effect.power, self.mana)
                self.hp -= damage
                self.mana -= mana_loss
                messages.append(f"👻 Soul burn: {damage} HP and {mana_loss} MP lost!")

            elif effect_type == StatusEffectType.STUNNED:
                messages.append(f"😵 You are stunned and cannot act!")

            elif effect_type == StatusEffectType.SLEEPING:
                messages.append(f"😴 You are sleeping and cannot act!")

            # Reduce duration (except for permanent effects)
            if effect.duration != 999:
                effect.duration -= 1
                if effect.duration <= 0:
                    effects_to_remove.append(effect_type)

        # Remove expired effects
        for effect_type in effects_to_remove:
            self.remove_status_effect(effect_type)
            effect_name = effect_type.value
            messages.append(f"✨ {effect_name} effect has worn off!")

        # Reduce skill cooldowns (only if not stunned/sleeping)
        if not (StatusEffectType.STUNNED in self.status_effects or
                StatusEffectType.SLEEPING in self.status_effects):
            for skill in self.skills.values():
                skill.reduce_cooldown()

        # Decay combo
        if self.combo_tracker.combo_timer > 0:
            self.combo_tracker.combo_timer -= 1
            if self.combo_tracker.combo_timer == 0:
                if self.combo_tracker.combo_count > 0:
                    messages.append(f"💥 Combo ended at {self.combo_tracker.combo_count} hits!")
                self.combo_tracker.combo_count = 0
                self.combo_tracker.combo_damage_multiplier = 1.0

        # Process class resources
        resource_messages = self.process_class_resources()
        messages.extend(resource_messages)

        return messages

    def can_act(self):
        """Check if player can act this turn"""
        return (StatusEffectType.STUNNED not in self.status_effects and
                StatusEffectType.SLEEPING not in self.status_effects)

    def get_base_stats(self):
        stats = {
            PlayerClass.KNIGHT: {"hp": 150, "mana": 50, "attack": 20, "defense": 25, "agility": 10, "crit_chance": 5,
                                 "crit_damage": 150},
            PlayerClass.PRIESTESS: {"hp": 100, "mana": 100, "attack": 12, "defense": 15, "agility": 15,
                                    "crit_chance": 8, "crit_damage": 140},
            PlayerClass.PATHFINDER: {"hp": 120, "mana": 70, "attack": 18, "defense": 18, "agility": 25,
                                     "crit_chance": 15, "crit_damage": 175},
            PlayerClass.ENGINEER: {"hp": 110, "mana": 80, "attack": 16, "defense": 20, "agility": 12, "crit_chance": 10,
                                   "crit_damage": 160},
            PlayerClass.CRUSADER: {"hp": 140, "mana": 60, "attack": 22, "defense": 22, "agility": 8, "crit_chance": 7,
                                   "crit_damage": 155},
            PlayerClass.BARBARIAN: {"hp": 160, "mana": 40, "attack": 25, "defense": 20, "agility": 15,
                                    "crit_chance": 12, "crit_damage": 180},
            PlayerClass.GUNSLINGER: {"hp": 110, "mana": 70, "attack": 20, "defense": 12, "agility": 30,
                                     "crit_chance": 20, "crit_damage": 200},
            PlayerClass.WIZARD: {"hp": 80, "mana": 120, "attack": 15, "defense": 10, "agility": 18, "crit_chance": 10,
                                 "crit_damage": 170},
            PlayerClass.SHADOWBLADE: {"hp": 105, "mana": 85, "attack": 19, "defense": 14, "agility": 28,
                                      "crit_chance": 18, "crit_damage": 190},
            PlayerClass.DRUID: {"hp": 115, "mana": 90, "attack": 16, "defense": 17, "agility": 20, "crit_chance": 10,
                                "crit_damage": 160}
        }
        return stats.get(self.player_class, stats[PlayerClass.KNIGHT])

    def get_class_skills(self):
        # Enhanced skill database with full implementations for all classes
        skills_db = {
            PlayerClass.KNIGHT: {
                "Shield Bash": Skill("Shield Bash", 1, 10, 15, 0, "", 0, "", 0,
                                     [StatusEffect(StatusEffectType.STUNNED, 1)],
                                     "Stun enemy with your shield", True, 1, cooldown=0,
                                     resource_type="stamina", resource_cost=15, skill_type="active",
                                     target_type="enemy", scaling_stat="defense"),
                "Sword Strike": Skill("Sword Strike", 1, 8, 20, 0, "", 0, "", 0,
                                      [StatusEffect(StatusEffectType.BLEED, 2, 3)],
                                      "Basic sword attack causing bleeding", False, 1, cooldown=0,
                                      combo_with=["Shield Bash"], resource_type="stamina", resource_cost=10,
                                      can_evolve=True, evolution_requirements={"skill_level": 5, "mastery_points": 3}),
                "Defensive Stance": Skill("Defensive Stance", 1, 15, 0, 0, "defense", 10, "", 0,
                                          [StatusEffect(StatusEffectType.FORTIFIED, 3, 10)],
                                          "Increase defense and gain fortification", False, 1, cooldown=2,
                                          skill_type="toggle", resource_type="stamina", resource_cost=20),
                "Power Attack": Skill("Power Attack", 2, 25, 35, 0, "", 0, "", 0,
                                      [StatusEffect(StatusEffectType.VULNERABLE, 2, 5)],
                                      "Powerful sword strike weakening enemy defense", False, 15, cooldown=3,
                                      combo_with=["Sword Strike"], resource_type="stamina", resource_cost=25,
                                      elemental_type="physical"),
                "Guardian's Will": Skill("Guardian's Will", 2, 30, 0, 0, "defense", 20, "", 0,
                                         [StatusEffect(StatusEffectType.SHIELD, 5, 50),
                                          StatusEffect(StatusEffectType.THORNS, 4, 10)],
                                         "Major defense boost with damage shield and thorns", False, 15, cooldown=4,
                                         skill_type="toggle", resource_type="stamina", resource_cost=40),
                "Divine Blade": Skill("Divine Blade", 3, 50, 60, 0, "attack", 15, "", 0,
                                      [StatusEffect(StatusEffectType.BLESSED, 4, 15),
                                       StatusEffect(StatusEffectType.EMPOWERED, 3, 25)],
                                      "Ultimate sword technique with divine blessing", False, 40, cooldown=5,
                                      combo_with=["Power Attack", "Sword Strike"], resource_type="stamina",
                                      resource_cost=60,
                                      elemental_type="holy", area_effect=True)
            },
            PlayerClass.WIZARD: {
                "Magic Missile": Skill("Magic Missile", 1, 15, 16, 0, "", 0, "", 0, [],
                                       "Basic magic attack that never misses", True, 1, cooldown=0,
                                       resource_type="arcane_power", resource_cost=10, skill_type="active",
                                       target_type="enemy", elemental_type="arcane"),
                "Mana Shield": Skill("Mana Shield", 1, 20, 0, 0, "defense", 8, "", 0,
                                     [StatusEffect(StatusEffectType.SHIELD, 4, 25)],
                                     "Magical protection with damage shield", False, 1, cooldown=2,
                                     skill_type="toggle", resource_type="arcane_power", resource_cost=15),
                "Fireball": Skill("Fireball", 1, 25, 20, 0, "", 0, "", 0,
                                  [StatusEffect(StatusEffectType.BURN, 4, 8)],
                                  "Fire spell that burns over time", False, 1, cooldown=0,
                                  combo_with=["Magic Missile"], resource_type="arcane_power", resource_cost=20,
                                  elemental_type="fire", area_effect=True),
                "Lightning Bolt": Skill("Lightning Bolt", 2, 35, 35, 0, "", 0, "", 0,
                                        [StatusEffect(StatusEffectType.SHOCK, 3, 12),
                                         StatusEffect(StatusEffectType.STUNNED, 1)],
                                        "Electric attack that shocks and stuns", False, 15, cooldown=3,
                                        combo_with=["Fireball"], resource_type="arcane_power", resource_cost=30,
                                        elemental_type="lightning", proc_chance=0.3),
                "Teleport": Skill("Teleport", 2, 30, 0, 0, "agility", 12, "", 0,
                                  [StatusEffect(StatusEffectType.SWIFT, 4, 15),
                                   StatusEffect(StatusEffectType.INVISIBLE, 2, 50)],
                                  "Magical movement with invisibility", False, 15, cooldown=4,
                                  skill_type="utility", resource_type="arcane_power", resource_cost=25),
                "Meteor": Skill("Meteor", 3, 80, 100, 0, "", 0, "", 0,
                                [StatusEffect(StatusEffectType.BURN, 8, 20),
                                 StatusEffect(StatusEffectType.STUNNED, 2),
                                 StatusEffect(StatusEffectType.MARKED, 5, 25)],
                                "Ultimate fire magic with massive damage", False, 40, cooldown=6,
                                combo_with=["Lightning Bolt", "Fireball"], resource_type="arcane_power",
                                resource_cost=80,
                                elemental_type="fire", area_effect=True, casting_time=2),
                "Time Warp": Skill("Time Warp", 3, 60, 0, 0, "", 0, "", 0,
                                   [StatusEffect(StatusEffectType.TIME_DILATION, 5, 2)],
                                   "Manipulate time to reduce all cooldowns", False, 35, cooldown=8,
                                   skill_type="utility", resource_type="arcane_power", resource_cost=50)
            },
            PlayerClass.BARBARIAN: {
                "Rage Strike": Skill("Rage Strike", 1, 0, 25, 0, "", 0, "", 0,
                                     [StatusEffect(StatusEffectType.BERSERKER, 3, 15)],
                                     "Powerful attack that builds rage", True, 1, cooldown=0,
                                     resource_type="rage", resource_cost=0, skill_type="active",
                                     scaling_stat="attack"),
                "Berserker Fury": Skill("Berserker Fury", 1, 0, 0, 0, "attack", 20, "", 0,
                                        [StatusEffect(StatusEffectType.BERSERKER, 5, 25),
                                         StatusEffect(StatusEffectType.LIFESTEAL, 5, 20)],
                                        "Enter berserk state with lifesteal", False, 1, cooldown=3,
                                        combo_with=["Rage Strike"], resource_type="rage", resource_cost=30,
                                        skill_type="toggle"),
                "Whirlwind": Skill("Whirlwind", 2, 0, 30, 0, "", 0, "", 0,
                                   [StatusEffect(StatusEffectType.BLEED, 3, 10)],
                                   "Spinning attack hitting all enemies", False, 15, cooldown=4,
                                   resource_type="rage", resource_cost=40, area_effect=True,
                                   can_evolve=True, evolution_requirements={"skill_level": 6}),
                "Blood Frenzy": Skill("Blood Frenzy", 2, 0, 0, 0, "", 0, "", 0,
                                      [StatusEffect(StatusEffectType.LIFESTEAL, 4, 35),
                                       StatusEffect(StatusEffectType.VULNERABLE, 4, 15)],
                                      "Massive lifesteal at cost of defense", False, 20, cooldown=5,
                                      combo_with=["Whirlwind"], resource_type="rage", resource_cost=50),
                "Apocalypse Slam": Skill("Apocalypse Slam", 3, 0, 80, 0, "", 0, "", 0,
                                         [StatusEffect(StatusEffectType.STUNNED, 2),
                                          StatusEffect(StatusEffectType.VULNERABLE, 6, 30)],
                                         "Ultimate ground slam devastating all foes", False, 40, cooldown=6,
                                         combo_with=["Blood Frenzy", "Whirlwind"], resource_type="rage",
                                         resource_cost=80,
                                         area_effect=True, casting_time=1)
            },
            PlayerClass.PATHFINDER: {
                "Precision Shot": Skill("Precision Shot", 1, 12, 18, 0, "", 0, "", 0,
                                        [StatusEffect(StatusEffectType.PRECISION, 3, 2)],
                                        "Accurate shot that improves aim", True, 1, cooldown=0,
                                        resource_type="focus", resource_cost=15, skill_type="active",
                                        scaling_stat="agility"),
                "Hunter's Mark": Skill("Hunter's Mark", 1, 15, 0, 0, "", 0, "", 0,
                                       [StatusEffect(StatusEffectType.MARKED, 8, 25)],
                                       "Mark target for increased damage", False, 1, cooldown=0,
                                       resource_type="focus", resource_cost=20, target_type="enemy"),
                "Evasion": Skill("Evasion", 1, 18, 0, 0, "agility", 15, "", 0,
                                 [StatusEffect(StatusEffectType.SWIFT, 4, 20),
                                  StatusEffect(StatusEffectType.INVISIBLE, 2, 30)],
                                 "Become harder to hit", False, 1, cooldown=3,
                                 skill_type="utility", resource_type="focus", resource_cost=25),
                "Multi-Shot": Skill("Multi-Shot", 2, 30, 15, 0, "", 0, "", 0, [],
                                    "Fire multiple projectiles", False, 15, cooldown=2,
                                    combo_with=["Precision Shot"], resource_type="focus", resource_cost=35,
                                    area_effect=True, scaling_stat="agility"),
                "Nature's Blessing": Skill("Nature's Blessing", 2, 25, 0, 20, "", 0, "", 0,
                                           [StatusEffect(StatusEffectType.NATURE_BOND, 6, 8)],
                                           "Channel nature's power for healing and bonuses", False, 20, cooldown=4,
                                           resource_type="focus", resource_cost=40, skill_type="channel",
                                           channel_duration=3),
                "Storm of Arrows": Skill("Storm of Arrows", 3, 60, 50, 0, "", 0, "", 0,
                                         [StatusEffect(StatusEffectType.PRECISION, 5, 5),
                                          StatusEffect(StatusEffectType.EMPOWERED, 4, 20)],
                                         "Ultimate archery technique", False, 40, cooldown=6,
                                         combo_with=["Multi-Shot", "Precision Shot"], resource_type="focus",
                                         resource_cost=70,
                                         area_effect=True, casting_time=2)
            },
            PlayerClass.SHADOWBLADE: {
                "Shadow Strike": Skill("Shadow Strike", 1, 15, 20, 0, "", 0, "", 0,
                                       [StatusEffect(StatusEffectType.POISON, 3, 6)],
                                       "Attack from shadows with poison", True, 1, cooldown=0,
                                       resource_type="shadow", resource_cost=20, skill_type="active",
                                       scaling_stat="agility", elemental_type="shadow"),
                "Stealth": Skill("Stealth", 1, 20, 0, 0, "", 0, "", 0,
                                 [StatusEffect(StatusEffectType.INVISIBLE, 4, 75)],
                                 "Become invisible to enemies", False, 1, cooldown=3,
                                 resource_type="shadow", resource_cost=25, skill_type="utility"),
                "Poison Blade": Skill("Poison Blade", 1, 12, 0, 0, "", 0, "", 0,
                                      [StatusEffect(StatusEffectType.POISON, 6, 10)],
                                      "Coat weapon with deadly poison", False, 1, cooldown=0,
                                      resource_type="shadow", resource_cost=15, skill_type="toggle",
                                      proc_chance=0.4),
                "Shadow Step": Skill("Shadow Step", 2, 25, 25, 0, "", 0, "", 0,
                                     [StatusEffect(StatusEffectType.SWIFT, 3, 25)],
                                     "Teleport attack from the shadows", False, 15, cooldown=2,
                                     combo_with=["Shadow Strike"], resource_type="shadow", resource_cost=35,
                                     target_type="enemy"),
                "Assassinate": Skill("Assassinate", 2, 40, 60, 0, "", 0, "", 0,
                                     [StatusEffect(StatusEffectType.SOUL_BURN, 4, 15)],
                                     "Attempt to instantly kill marked target", False, 25, cooldown=5,
                                     resource_type="shadow", resource_cost=50, proc_chance=0.25),
                "Shadow Clone": Skill("Shadow Clone", 3, 60, 0, 0, "", 0, "", 0,
                                      [StatusEffect(StatusEffectType.INVISIBLE, 8, 90),
                                       StatusEffect(StatusEffectType.EMPOWERED, 6, 40)],
                                      "Create shadow duplicates to confuse enemies", False, 40, cooldown=7,
                                      combo_with=["Assassinate", "Shadow Step"], resource_type="shadow",
                                      resource_cost=80,
                                      skill_type="summon", casting_time=1)
            },
            PlayerClass.PRIESTESS: {
                "Holy Light": Skill("Holy Light", 1, 12, 0, 25, "", 0, "", 0,
                                    [StatusEffect(StatusEffectType.BLESSED, 3, 5)],
                                    "Heal target with divine light", True, 1, cooldown=0,
                                    resource_type="faith", resource_cost=10, skill_type="active",
                                    target_type="self", scaling_stat="mana", elemental_type="holy"),
                "Sacred Shield": Skill("Sacred Shield", 1, 18, 0, 0, "defense", 10, "", 0,
                                       [StatusEffect(StatusEffectType.SHIELD, 5, 30),
                                        StatusEffect(StatusEffectType.REGENERATION, 4, 5)],
                                       "Divine protection with regeneration", False, 1, cooldown=3,
                                       resource_type="faith", resource_cost=15, skill_type="active"),
                "Purify": Skill("Purify", 1, 15, 0, 0, "", 0, "", 0, [],
                                "Remove all negative status effects", False, 1, cooldown=2,
                                resource_type="faith", resource_cost=20, skill_type="utility",
                                target_type="self"),
                "Divine Strike": Skill("Divine Strike", 2, 30, 30, 0, "", 0, "", 0,
                                       [StatusEffect(StatusEffectType.BURN, 4, 8),
                                        StatusEffect(StatusEffectType.BLESSED, 3, 10)],
                                       "Holy damage that burns undead", False, 15, cooldown=3,
                                       combo_with=["Holy Light"], resource_type="faith", resource_cost=25,
                                       elemental_type="holy", scaling_stat="mana"),
                "Greater Heal": Skill("Greater Heal", 2, 40, 0, 60, "", 0, "", 0,
                                      [StatusEffect(StatusEffectType.REGENERATION, 6, 10),
                                       StatusEffect(StatusEffectType.FORTIFIED, 4, 15)],
                                      "Powerful healing with lasting effects", False, 20, cooldown=4,
                                      resource_type="faith", resource_cost=35, casting_time=1,
                                      target_type="self", scaling_stat="mana"),
                "Divine Intervention": Skill("Divine Intervention", 3, 80, 50, 100, "all", 20, "", 0,
                                             [StatusEffect(StatusEffectType.BLESSED, 10, 25),
                                              StatusEffect(StatusEffectType.SHIELD, 8, 50),
                                              StatusEffect(StatusEffectType.REGENERATION, 10, 15)],
                                             "Ultimate divine blessing and healing", False, 40, cooldown=8,
                                             combo_with=["Greater Heal", "Divine Strike"], resource_type="faith",
                                             resource_cost=60, elemental_type="holy", area_effect=True,
                                             casting_time=2)
            },
            PlayerClass.ENGINEER: {
                "Shock Trap": Skill("Shock Trap", 1, 15, 20, 0, "", 0, "", 0,
                                    [StatusEffect(StatusEffectType.SHOCK, 3, 8),
                                     StatusEffect(StatusEffectType.STUNNED, 1)],
                                    "Deploy electric trap", True, 1, cooldown=0,
                                    resource_type="energy", resource_cost=20, skill_type="active",
                                    elemental_type="lightning"),
                "Repair Bot": Skill("Repair Bot", 1, 20, 0, 15, "defense", 5, "", 0,
                                    [StatusEffect(StatusEffectType.REGENERATION, 5, 5)],
                                    "Deploy healing drone", False, 1, cooldown=3,
                                    resource_type="energy", resource_cost=25, skill_type="summon"),
                "Overclock": Skill("Overclock", 1, 18, 0, 0, "all", 10, "", 0,
                                   [StatusEffect(StatusEffectType.SWIFT, 4, 15),
                                    StatusEffect(StatusEffectType.FOCUSED, 4, 20)],
                                   "Boost all systems temporarily", False, 1, cooldown=4,
                                   resource_type="energy", resource_cost=30, skill_type="toggle"),
                "Flame Turret": Skill("Flame Turret", 2, 35, 35, 0, "", 0, "", 0,
                                      [StatusEffect(StatusEffectType.BURN, 5, 10)],
                                      "Deploy automated flame turret", False, 15, cooldown=3,
                                      combo_with=["Shock Trap"], resource_type="energy", resource_cost=40,
                                      skill_type="summon", elemental_type="fire", area_effect=True),
                "EMP Blast": Skill("EMP Blast", 2, 40, 40, 0, "", 0, "", 0,
                                   [StatusEffect(StatusEffectType.STUNNED, 2),
                                    StatusEffect(StatusEffectType.VULNERABLE, 5, 20)],
                                   "Electromagnetic pulse disables enemies", False, 20, cooldown=5,
                                   resource_type="energy", resource_cost=50, area_effect=True,
                                   elemental_type="lightning"),
                "Mech Suit": Skill("Mech Suit", 3, 80, 0, 0, "all", 30, "", 0,
                                   [StatusEffect(StatusEffectType.SHIELD, 10, 100),
                                    StatusEffect(StatusEffectType.FORTIFIED, 8, 30),
                                    StatusEffect(StatusEffectType.EMPOWERED, 8, 30)],
                                   "Deploy personal mech armor", False, 40, cooldown=8,
                                   combo_with=["EMP Blast", "Flame Turret"], resource_type="energy",
                                   resource_cost=80, skill_type="toggle", casting_time=2)
            },
            PlayerClass.CRUSADER: {
                "Holy Strike": Skill("Holy Strike", 1, 12, 22, 0, "", 0, "", 0,
                                     [StatusEffect(StatusEffectType.BLESSED, 2, 5)],
                                     "Strike with divine power", True, 1, cooldown=0,
                                     resource_type="holy_power", resource_cost=15, skill_type="active",
                                     elemental_type="holy", scaling_stat="attack"),
                "Consecration": Skill("Consecration", 1, 20, 0, 10, "defense", 10, "", 0,
                                      [StatusEffect(StatusEffectType.REGENERATION, 5, 5)],
                                      "Consecrate the ground beneath you", False, 1, cooldown=3,
                                      resource_type="holy_power", resource_cost=20, skill_type="toggle",
                                      area_effect=True, elemental_type="holy"),
                "Divine Shield": Skill("Divine Shield", 1, 25, 0, 0, "defense", 20, "", 0,
                                       [StatusEffect(StatusEffectType.SHIELD, 5, 40),
                                        StatusEffect(StatusEffectType.BLESSED, 4, 10)],
                                       "Divine protection from harm", False, 1, cooldown=4,
                                       resource_type="holy_power", resource_cost=25, skill_type="active"),
                "Hammer of Wrath": Skill("Hammer of Wrath", 2, 35, 45, 0, "", 0, "", 0,
                                         [StatusEffect(StatusEffectType.STUNNED, 2),
                                          StatusEffect(StatusEffectType.VULNERABLE, 4, 15)],
                                         "Throw divine hammer at enemies", False, 15, cooldown=3,
                                         combo_with=["Holy Strike"], resource_type="holy_power", resource_cost=35,
                                         elemental_type="holy", scaling_stat="attack"),
                "Avenging Wrath": Skill("Avenging Wrath", 2, 45, 0, 0, "attack", 25, "", 0,
                                        [StatusEffect(StatusEffectType.EMPOWERED, 6, 30),
                                         StatusEffect(StatusEffectType.SWIFT, 5, 20),
                                         StatusEffect(StatusEffectType.REGENERATION, 6, 8)],
                                        "Sprout divine wings of vengeance", False, 20, cooldown=5,
                                        resource_type="holy_power", resource_cost=50, skill_type="toggle"),
                "Divine Storm": Skill("Divine Storm", 3, 90, 80, 30, "all", 20, "", 0,
                                      [StatusEffect(StatusEffectType.BLESSED, 10, 20),
                                       StatusEffect(StatusEffectType.BURN, 8, 15),
                                       StatusEffect(StatusEffectType.MARKED, 6, 30)],
                                      "Ultimate divine judgment upon all foes", False, 40, cooldown=8,
                                      combo_with=["Avenging Wrath", "Hammer of Wrath"],
                                      resource_type="holy_power", resource_cost=80,
                                      elemental_type="holy", area_effect=True, casting_time=2)
            },
            PlayerClass.GUNSLINGER: {
                "Quick Shot": Skill("Quick Shot", 1, 10, 18, 0, "", 0, "", 0,
                                    [StatusEffect(StatusEffectType.PRECISION, 2, 1)],
                                    "Fast accurate shot", True, 1, cooldown=0,
                                    resource_type="ammo", resource_cost=1, skill_type="active",
                                    scaling_stat="agility"),
                "Fan the Hammer": Skill("Fan the Hammer", 1, 15, 25, 0, "", 0, "", 0,
                                        [StatusEffect(StatusEffectType.VULNERABLE, 3, 10)],
                                        "Rapid fire multiple shots", False, 1, cooldown=2,
                                        resource_type="ammo", resource_cost=3, skill_type="active",
                                        area_effect=True),
                "Smoke Bomb": Skill("Smoke Bomb", 1, 18, 0, 0, "", 0, "", 0,
                                    [StatusEffect(StatusEffectType.INVISIBLE, 3, 50),
                                     StatusEffect(StatusEffectType.SWIFT, 4, 20)],
                                    "Vanish in smoke for repositioning", False, 1, cooldown=3,
                                    skill_type="utility"),
                "Explosive Shot": Skill("Explosive Shot", 2, 30, 40, 0, "", 0, "", 0,
                                        [StatusEffect(StatusEffectType.BURN, 4, 10),
                                         StatusEffect(StatusEffectType.STUNNED, 1)],
                                        "Fire explosive round", False, 15, cooldown=3,
                                        combo_with=["Quick Shot"], resource_type="ammo", resource_cost=2,
                                        elemental_type="fire", area_effect=True),
                "Dead Eye": Skill("Dead Eye", 2, 35, 0, 0, "", 0, "", 0,
                                  [StatusEffect(StatusEffectType.PRECISION, 5, 5),
                                   StatusEffect(StatusEffectType.FOCUSED, 5, 30),
                                   StatusEffect(StatusEffectType.EMPOWERED, 5, 25)],
                                  "Enter focused shooting stance", False, 20, cooldown=5,
                                  skill_type="toggle"),
                "High Noon": Skill("High Noon", 3, 80, 100, 0, "", 0, "", 0,
                                   [StatusEffect(StatusEffectType.MARKED, 10, 50),
                                    StatusEffect(StatusEffectType.PRECISION, 10, 10)],
                                   "Ultimate showdown - hit all enemies", False, 40, cooldown=8,
                                   combo_with=["Dead Eye", "Explosive Shot"], resource_type="ammo",
                                   resource_cost=6, area_effect=True, casting_time=2,
                                   can_evolve=True, evolution_requirements={"skill_level": 7})
            },
            PlayerClass.DRUID: {
                "Nature's Touch": Skill("Nature's Touch", 1, 15, 0, 20, "", 0, "", 0,
                                        [StatusEffect(StatusEffectType.NATURE_BOND, 4, 5)],
                                        "Healing touch of nature", True, 1, cooldown=0,
                                        resource_type="nature_essence", resource_cost=15, skill_type="active",
                                        target_type="self", elemental_type="nature"),
                "Thorns": Skill("Thorns", 1, 18, 0, 0, "defense", 8, "", 0,
                                [StatusEffect(StatusEffectType.THORNS, 999, 12),
                                 StatusEffect(StatusEffectType.FORTIFIED, 4, 10)],
                                "Protective thorns damage attackers", False, 1, cooldown=3,
                                resource_type="nature_essence", resource_cost=20, skill_type="toggle"),
                "Wild Shape": Skill("Wild Shape", 1, 20, 0, 0, "all", 15, "", 0,
                                    [StatusEffect(StatusEffectType.SWIFT, 5, 20),
                                     StatusEffect(StatusEffectType.STRENGTH, 5, 15)],
                                    "Transform into animal form", False, 1, cooldown=4,
                                    resource_type="nature_essence", resource_cost=25, skill_type="toggle"),
                "Entangling Roots": Skill("Entangling Roots", 2, 30, 30, 0, "", 0, "", 0,
                                          [StatusEffect(StatusEffectType.STUNNED, 2),
                                           StatusEffect(StatusEffectType.POISON, 5, 8)],
                                          "Roots entangle and poison enemies", False, 15, cooldown=3,
                                          combo_with=["Nature's Touch"], resource_type="nature_essence",
                                          resource_cost=30, elemental_type="nature"),
                "Rejuvenation": Skill("Rejuvenation", 2, 35, 0, 40, "", 0, "", 0,
                                      [StatusEffect(StatusEffectType.REGENERATION, 8, 12),
                                       StatusEffect(StatusEffectType.NATURE_BOND, 6, 10)],
                                      "Powerful healing over time", False, 20, cooldown=4,
                                      resource_type="nature_essence", resource_cost=40, skill_type="channel",
                                      channel_duration=3, target_type="self"),
                "Force of Nature": Skill("Force of Nature", 3, 90, 70, 50, "all", 25, "", 0,
                                         [StatusEffect(StatusEffectType.NATURE_BOND, 10, 20),
                                          StatusEffect(StatusEffectType.REGENERATION, 10, 15),
                                          StatusEffect(StatusEffectType.EMPOWERED, 8, 30)],
                                         "Call upon nature's full fury", False, 40, cooldown=8,
                                         combo_with=["Rejuvenation", "Entangling Roots"],
                                         resource_type="nature_essence", resource_cost=70,
                                         elemental_type="nature", area_effect=True, casting_time=2)
            }
        }

        # For classes not fully implemented, create enhanced basic skill set
        if self.player_class not in skills_db:
            return {
                "Basic Attack": Skill("Basic Attack", 1, 10, 15, 0, "", 0, "", 0, [],
                                      "Basic attack", True, 1, cooldown=0, skill_type="active"),
                "Defend": Skill("Defend", 1, 15, 0, 0, "defense", 10, "", 0,
                                [StatusEffect(StatusEffectType.FORTIFIED, 3, 10)],
                                "Defensive stance", False, 1, cooldown=2, skill_type="toggle"),
                "Power Strike": Skill("Power Strike", 2, 30, 35, 0, "", 0, "", 0, [],
                                      "Powerful attack", False, 15, cooldown=3, can_evolve=True),
                "Ultimate": Skill("Ultimate", 3, 60, 80, 0, "all", 15, "", 0,
                                  [StatusEffect(StatusEffectType.BLESSED, 5, 15)],
                                  "Ultimate ability", False, 40, cooldown=5, area_effect=True)
            }

        return skills_db[self.player_class]

    def level_up(self):
        if self.exp >= self.exp_to_next:
            self.level += 1
            self.skill_points += 1

            # Enhanced stat increases based on class
            class_growth = {
                PlayerClass.KNIGHT: {"hp": 15, "mana": 5, "attack": 3, "defense": 4, "agility": 1},
                PlayerClass.WIZARD: {"hp": 8, "mana": 12, "attack": 2, "defense": 2, "agility": 2},
                PlayerClass.BARBARIAN: {"hp": 18, "mana": 3, "attack": 4, "defense": 3, "agility": 2},
                PlayerClass.PATHFINDER: {"hp": 10, "mana": 7, "attack": 3, "defense": 2, "agility": 3},
                PlayerClass.SHADOWBLADE: {"hp": 12, "mana": 8, "attack": 3, "defense": 2, "agility": 4},
                PlayerClass.PRIESTESS: {"hp": 9, "mana": 11, "attack": 2, "defense": 3, "agility": 2},
                PlayerClass.ENGINEER: {"hp": 11, "mana": 9, "attack": 3, "defense": 3, "agility": 2},
                PlayerClass.CRUSADER: {"hp": 14, "mana": 6, "attack": 4, "defense": 4, "agility": 1},
                PlayerClass.GUNSLINGER: {"hp": 10, "mana": 7, "attack": 4, "defense": 2, "agility": 4},
                PlayerClass.DRUID: {"hp": 13, "mana": 10, "attack": 2, "defense": 3, "agility": 3}
            }

            growth = class_growth.get(self.player_class, {"hp": 10, "mana": 5, "attack": 2, "defense": 2, "agility": 1})

            self.max_hp += growth["hp"] + (self.level * 2)
            self.max_mana += growth["mana"] + self.level
            self.attack += growth["attack"]
            self.defense += growth["defense"]
            self.agility += growth["agility"]

            # Increase crit stats slightly
            if self.level % 5 == 0:
                self.crit_chance += 1
                self.crit_damage += 5

            # Enhance class resources
            for resource in self.class_resources.values():
                resource.maximum += 10

            # Full heal on level up
            self.hp = self.max_hp
            self.mana = self.max_mana

            # Clear negative status effects
            negative_effects = [StatusEffectType.POISON, StatusEffectType.BURN,
                                StatusEffectType.BLEED, StatusEffectType.FREEZE,
                                StatusEffectType.WEAKNESS, StatusEffectType.VULNERABLE,
                                StatusEffectType.SLOWED, StatusEffectType.CONFUSED,
                                StatusEffectType.STUNNED, StatusEffectType.SLEEPING,
                                StatusEffectType.CURSED, StatusEffectType.MANA_BURN]

            for effect_type in negative_effects:
                if effect_type in self.status_effects:
                    self.remove_status_effect(effect_type)

            self.exp -= self.exp_to_next
            self.exp_to_next = int(self.exp_to_next * 1.15)
            return True
        return False

    def get_total_stats(self):
        total_stats = {
            "hp": self.max_hp,
            "mana": self.max_mana,
            "attack": self.attack,
            "defense": self.defense,
            "agility": self.agility,
            "crit_chance": self.crit_chance,
            "crit_damage": self.crit_damage
        }

        # Add equipment bonuses
        for slot, item in self.equipment.items():
            if item:
                for stat, value in item.modifiers.items():
                    if stat in total_stats:
                        total_stats[stat] += value

                # Add rune bonuses
                for rune in item.socketed_runes:
                    if rune.effect_type in total_stats:
                        total_stats[rune.effect_type] += rune.effect_value

        # Add buff bonuses
        for buff, value in self.buffs.items():
            if buff in total_stats:
                total_stats[buff] += value
            elif buff == "all":
                for stat in total_stats:
                    total_stats[stat] += value

        # Add status effect modifiers
        for effect_type, effect in self.status_effects.items():
            if effect_type == StatusEffectType.STRENGTH:
                total_stats["attack"] += effect.power
            elif effect_type == StatusEffectType.WEAKNESS:
                total_stats["attack"] = max(1, total_stats["attack"] - effect.power)
            elif effect_type == StatusEffectType.FORTIFIED:
                total_stats["defense"] += effect.power
            elif effect_type == StatusEffectType.VULNERABLE:
                total_stats["defense"] = max(0, total_stats["defense"] - effect.power)
            elif effect_type == StatusEffectType.SWIFT:
                total_stats["agility"] += effect.power
            elif effect_type == StatusEffectType.SLOWED:
                total_stats["agility"] = max(1, total_stats["agility"] - effect.power)
            elif effect_type == StatusEffectType.BLESSED:
                for stat in ["attack", "defense", "agility", "hp", "mana"]:
                    if stat in total_stats:
                        total_stats[stat] += effect.power
            elif effect_type == StatusEffectType.CURSED:
                for stat in ["attack", "defense", "agility"]:
                    if stat in total_stats:
                        total_stats[stat] = max(1, total_stats[stat] - effect.power)
            elif effect_type == StatusEffectType.FOCUSED:
                total_stats["crit_chance"] += effect.power // 2
            elif effect_type == StatusEffectType.EMPOWERED:
                total_stats["attack"] = int(total_stats["attack"] * (1 + effect.power / 100))
            elif effect_type == StatusEffectType.BERSERKER:
                total_stats["attack"] = int(total_stats["attack"] * (1 + effect.power / 100))
            elif effect_type == StatusEffectType.PRECISION:
                total_stats["crit_chance"] += 50  # Precision shots have high crit
            elif effect_type == StatusEffectType.NATURE_BOND:
                for stat in ["attack", "defense", "agility"]:
                    if stat in total_stats:
                        total_stats[stat] += effect.power // 2

        return total_stats

    def get_effective_resource_cost(self, skill: Skill):
        """Calculate effective resource cost considering status effects and passives"""
        cost = skill.resource_cost

        # Apply focused effect for mana
        if skill.resource_type == "mana" and StatusEffectType.FOCUSED in self.status_effects:
            reduction = self.status_effects[StatusEffectType.FOCUSED].power
            cost = max(1, int(cost * (100 - reduction) / 100))

        # Apply confused effect for mana
        if skill.resource_type == "mana" and StatusEffectType.CONFUSED in self.status_effects:
            increase = self.status_effects[StatusEffectType.CONFUSED].power
            cost = int(cost * (100 + increase) / 100)

        # Class-specific cost reductions
        if self.player_class == PlayerClass.ENGINEER and skill.resource_type == "energy":
            cost = int(cost * 0.8)  # 20% energy efficiency

        return cost

    def calculate_damage(self, base_damage, is_skill=False, skill_name="", skill=None):
        """Calculate final damage with all modifiers"""
        damage = base_damage

        # Apply skill scaling if provided
        if skill and skill.scaling_stat:
            stat_value = self.get_total_stats().get(skill.scaling_stat, 0)
            damage = skill.get_effective_value(damage, stat_value)

        # Apply combo multiplier
        if self.combo_tracker.combo_count > 0:
            damage = int(damage * self.combo_tracker.combo_damage_multiplier)

        # Apply elemental mastery
        if skill and skill.elemental_type and StatusEffectType.ELEMENTAL_MASTERY in self.status_effects:
            bonus = self.status_effects[StatusEffectType.ELEMENTAL_MASTERY].power
            damage = int(damage * (1 + bonus / 100))

        # Apply precision (guaranteed crit for next X attacks)
        force_crit = False
        if StatusEffectType.PRECISION in self.status_effects:
            precision = self.status_effects[StatusEffectType.PRECISION]
            if precision.power > 0:  # power indicates remaining precision attacks
                force_crit = True
                precision.power -= 1
                if precision.power <= 0:
                    self.remove_status_effect(StatusEffectType.PRECISION)

        # Apply crit chance
        crit_chance = self.get_total_stats()["crit_chance"]
        if force_crit or random.randint(1, 100) <= crit_chance:
            damage = int(damage * self.get_total_stats()["crit_damage"] / 100)
            crit = True
        else:
            crit = False

        # Apply empowered bonus
        if StatusEffectType.EMPOWERED in self.status_effects:
            damage = int(damage * (1 + self.status_effects[StatusEffectType.EMPOWERED].power / 100))

        # Apply berserker bonus
        if StatusEffectType.BERSERKER in self.status_effects:
            damage = int(damage * (1 + self.status_effects[StatusEffectType.BERSERKER].power / 100))

        return damage, crit


def generate_shop_inventory(player_level: int):
    inventory = {}

    # Weapon shop with level-appropriate items
    inventory["weapons"] = []
    for _ in range(8):
        rarity_roll = random.randint(1, 100)
        if rarity_roll <= 50:
            rarity = Rarity.COMMON
        elif rarity_roll <= 75:
            rarity = Rarity.MAGIC
        elif rarity_roll <= 90:
            rarity = Rarity.RARE
        elif rarity_roll <= 97:
            rarity = Rarity.EPIC
        elif rarity_roll <= 99:
            rarity = Rarity.LEGENDARY
        else:
            rarity = Rarity.MYTHIC

        level_range = max(1, player_level - 5), player_level + 3
        item_level = random.randint(*level_range)
        item = generate_item(ItemType.WEAPON, rarity, item_level)
        inventory["weapons"].append(item)

    # Armor shop
    inventory["armor"] = []
    for _ in range(6):
        rarity_roll = random.randint(1, 100)
        if rarity_roll <= 50:
            rarity = Rarity.COMMON
        elif rarity_roll <= 75:
            rarity = Rarity.MAGIC
        elif rarity_roll <= 90:
            rarity = Rarity.RARE
        elif rarity_roll <= 97:
            rarity = Rarity.EPIC
        else:
            rarity = Rarity.LEGENDARY

        level_range = max(1, player_level - 5), player_level + 3
        item_level = random.randint(*level_range)
        item = generate_item(ItemType.ARMOR, rarity, item_level)
        inventory["armor"].append(item)

    # Accessories
    inventory["accessories"] = []
    for _ in range(10):
        rarity_roll = random.randint(1, 100)
        if rarity_roll <= 45:
            rarity = Rarity.COMMON
        elif rarity_roll <= 70:
            rarity = Rarity.MAGIC
        elif rarity_roll <= 85:
            rarity = Rarity.RARE
        elif rarity_roll <= 95:
            rarity = Rarity.EPIC
        else:
            rarity = Rarity.LEGENDARY

        item_type = random.choice([ItemType.RING, ItemType.AMULET, ItemType.TRINKET])
        level_range = max(1, player_level - 5), player_level + 3
        item_level = random.randint(*level_range)
        item = generate_item(item_type, rarity, item_level)
        inventory["accessories"].append(item)

    # Enhanced potions and consumables
    inventory["potions"] = [
        Item("Health Potion", ItemType.CONSUMABLE, Rarity.COMMON, 25,
             status_effects_on_use=[StatusEffect(StatusEffectType.REGENERATION, 3, 5)],
             description="Restores 50 HP and grants regeneration"),
        Item("Mana Potion", ItemType.CONSUMABLE, Rarity.COMMON, 30,
             description="Restores 50 Mana"),
        Item("Greater Health Potion", ItemType.CONSUMABLE, Rarity.MAGIC, 75,
             status_effects_on_use=[StatusEffect(StatusEffectType.REGENERATION, 5, 8)],
             description="Restores 150 HP and grants strong regeneration"),
        Item("Greater Mana Potion", ItemType.CONSUMABLE, Rarity.MAGIC, 85,
             description="Restores 150 Mana"),
        Item("Elixir of Strength", ItemType.CONSUMABLE, Rarity.RARE, 150,
             status_effects_on_use=[StatusEffect(StatusEffectType.STRENGTH, 6, 20),
                                    StatusEffect(StatusEffectType.EMPOWERED, 4, 15)],
             description="Grants powerful strength and empowerment"),
        Item("Elixir of Defense", ItemType.CONSUMABLE, Rarity.RARE, 150,
             status_effects_on_use=[StatusEffect(StatusEffectType.FORTIFIED, 6, 20),
                                    StatusEffect(StatusEffectType.SHIELD, 5, 30)],
             description="Grants powerful defense and shield"),
        Item("Smoke Bomb", ItemType.CONSUMABLE, Rarity.MAGIC, 100,
             status_effects_on_use=[StatusEffect(StatusEffectType.INVISIBLE, 3, 75)],
             description="Grants temporary invisibility"),
        Item("Blessing Potion", ItemType.CONSUMABLE, Rarity.EPIC, 300,
             status_effects_on_use=[StatusEffect(StatusEffectType.BLESSED, 8, 15),
                                    StatusEffect(StatusEffectType.REGENERATION, 6, 10)],
             description="Grants divine blessing and regeneration"),
        Item("Berserker Draught", ItemType.CONSUMABLE, Rarity.RARE, 200,
             status_effects_on_use=[StatusEffect(StatusEffectType.STRENGTH, 5, 25),
                                    StatusEffect(StatusEffectType.LIFESTEAL, 5, 20),
                                    StatusEffect(StatusEffectType.VULNERABLE, 5, 10)],
             description="Massive power at the cost of defense"),
        Item("Phoenix Feather", ItemType.CONSUMABLE, Rarity.LEGENDARY, 500,
             status_effects_on_use=[StatusEffect(StatusEffectType.REGENERATION, 10, 20),
                                    StatusEffect(StatusEffectType.BLESSED, 10, 20)],
             description="Revives with full HP when you would die (auto-use)"),
        Item("Time Crystal", ItemType.CONSUMABLE, Rarity.EPIC, 400,
             status_effects_on_use=[StatusEffect(StatusEffectType.TIME_DILATION, 3, 3)],
             description="Speeds up time, reducing all cooldowns faster"),
        Item("Nature's Essence", ItemType.CONSUMABLE, Rarity.RARE, 250,
             status_effects_on_use=[StatusEffect(StatusEffectType.NATURE_BOND, 8, 12)],
             description="Connect with nature for healing and stat bonuses")
    ]

    # Runes shop (enhanced feature)
    inventory["runes"] = []
    rune_types = [
        ("Power Rune", "attack", [5, 8, 12]),
        ("Guard Rune", "defense", [5, 8, 12]),
        ("Swift Rune", "agility", [3, 5, 8]),
        ("Life Rune", "hp", [20, 35, 50]),
        ("Spirit Rune", "mana", [15, 25, 40]),
        ("Critical Rune", "crit_chance", [3, 5, 8]),
        ("Devastation Rune", "crit_damage", [10, 20, 30])
    ]

    for _ in range(6):
        rune_data = random.choice(rune_types)
        tier = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        rune = Rune(
            name=f"{rune_data[0]} T{tier}",
            tier=tier,
            effect_type=rune_data[1],
            effect_value=rune_data[2][tier - 1],
            description=f"Adds +{rune_data[2][tier - 1]} {rune_data[1]}"
        )
        price = 100 * tier * tier
        rune_item = Item(rune.name, ItemType.RUNE,
                         [Rarity.COMMON, Rarity.MAGIC, Rarity.RARE][tier - 1],
                         price, description=rune.description)
        rune_item.rune_data = rune
        inventory["runes"].append(rune_item)

    return inventory


def generate_item(item_type: ItemType, rarity: Rarity, level: int = 1):
    # Enhanced item generation with more variety

    prefixes = {
        "weapon": ["Ancient", "Blazing", "Frozen", "Venomous", "Divine", "Cursed", "Ethereal",
                   "Draconic", "Infernal", "Crystal", "Shadow", "Lightning", "Vampiric"],
        "armor": ["Reinforced", "Enchanted", "Guardian's", "Mystic", "Titan's", "Spectral",
                  "Regenerating", "Fortress", "Adamantine", "Runic"],
        "accessory": ["Glowing", "Blessed", "Arcane", "Primal", "Celestial", "Void", "Eternal"]
    }

    base_names = {
        ItemType.WEAPON: ["Sword", "Axe", "Mace", "Staff", "Bow", "Dagger", "Spear", "Hammer"],
        ItemType.ARMOR: ["Mail", "Plate", "Robes", "Leather", "Scale", "Chainmail"],
        ItemType.RING: ["Ring", "Band", "Signet", "Loop"],
        ItemType.AMULET: ["Amulet", "Pendant", "Necklace", "Medallion"],
        ItemType.TRINKET: ["Trinket", "Charm", "Talisman", "Relic"]
    }

    suffixes = ["of Power", "of Wisdom", "of the Phoenix", "of Storms", "of the Void",
                "of Destruction", "of Light", "of Darkness", "of the Dragon", "of Eternity"]

    # Generate name
    prefix_type = "weapon" if item_type == ItemType.WEAPON else "armor" if item_type == ItemType.ARMOR else "accessory"
    prefix = random.choice(prefixes[prefix_type])
    base = random.choice(base_names.get(item_type, ["Item"]))
    suffix = random.choice(suffixes) if rarity.value in [Rarity.RARE.value, Rarity.EPIC.value, Rarity.LEGENDARY.value,
                                                         Rarity.MYTHIC.value] else ""

    name = f"{prefix} {base} {suffix}".strip()

    # Calculate base value
    rarity_multipliers = {
        Rarity.COMMON: 1.0,
        Rarity.MAGIC: 1.5,
        Rarity.RARE: 2.5,
        Rarity.EPIC: 4.0,
        Rarity.LEGENDARY: 6.0,
        Rarity.MYTHIC: 10.0
    }

    base_value = int((50 + level * 10) * rarity_multipliers[rarity])

    # Generate modifiers based on rarity
    modifiers = {}
    status_effects_on_use = []
    status_effects_on_hit = []
    sockets = 0

    if item_type == ItemType.WEAPON:
        if rarity == Rarity.COMMON:
            modifiers = {"attack": random.randint(1, 3)}
        elif rarity == Rarity.MAGIC:
            modifiers = {"attack": random.randint(3, 6), random.choice(["defense", "agility"]): random.randint(1, 3)}
        elif rarity == Rarity.RARE:
            modifiers = {
                "attack": random.randint(5, 10),
                "defense": random.randint(2, 5),
                "crit_chance": random.randint(2, 5)
            }
            sockets = 1
        elif rarity == Rarity.EPIC:
            modifiers = {
                "attack": random.randint(8, 15),
                "defense": random.randint(4, 8),
                "crit_chance": random.randint(3, 8),
                "crit_damage": random.randint(10, 20)
            }
            sockets = 2
            # Add on-hit effect
            effect_choices = [
                StatusEffect(StatusEffectType.BURN, 3, 5 + level),
                StatusEffect(StatusEffectType.BLEED, 4, 4 + level),
                StatusEffect(StatusEffectType.POISON, 3, 6 + level),
                StatusEffect(StatusEffectType.SHOCK, 2, 8 + level)
            ]
            status_effects_on_hit.append(random.choice(effect_choices))
        elif rarity == Rarity.LEGENDARY:
            modifiers = {
                "attack": random.randint(12, 20),
                "defense": random.randint(6, 12),
                "hp": random.randint(20, 40),
                "crit_chance": random.randint(5, 10),
                "crit_damage": random.randint(15, 30)
            }
            sockets = 3
            # Multiple on-hit effects
            status_effects_on_hit.append(StatusEffect(StatusEffectType.LIFESTEAL, 999, 15))
            status_effects_on_hit.append(random.choice([
                StatusEffect(StatusEffectType.BURN, 4, 8 + level),
                StatusEffect(StatusEffectType.MARKED, 3, 20)
            ]))
        elif rarity == Rarity.MYTHIC:
            modifiers = {
                "attack": random.randint(20, 30),
                "defense": random.randint(10, 20),
                "hp": random.randint(40, 60),
                "mana": random.randint(20, 40),
                "agility": random.randint(10, 15),
                "crit_chance": random.randint(8, 15),
                "crit_damage": random.randint(25, 50)
            }
            sockets = 4
            # Powerful effects
            status_effects_on_use.append(StatusEffect(StatusEffectType.EMPOWERED, 999, 20))
            status_effects_on_hit.append(StatusEffect(StatusEffectType.LIFESTEAL, 999, 25))
            status_effects_on_hit.append(StatusEffect(StatusEffectType.MARKED, 5, 30))

    elif item_type == ItemType.ARMOR:
        if rarity == Rarity.COMMON:
            modifiers = {"defense": random.randint(2, 4), "hp": random.randint(5, 10)}
        elif rarity == Rarity.MAGIC:
            modifiers = {
                "defense": random.randint(4, 8),
                "hp": random.randint(10, 20),
                random.choice(["mana", "agility"]): random.randint(3, 8)
            }
        elif rarity == Rarity.RARE:
            modifiers = {
                "defense": random.randint(8, 15),
                "hp": random.randint(20, 35),
                "agility": random.randint(3, 8)
            }
            sockets = 1
            status_effects_on_use.append(StatusEffect(StatusEffectType.FORTIFIED, 999, 5))
        elif rarity == Rarity.EPIC:
            modifiers = {
                "defense": random.randint(12, 20),
                "hp": random.randint(30, 50),
                "mana": random.randint(15, 30),
                "agility": random.randint(5, 10)
            }
            sockets = 2
            status_effects_on_use.append(StatusEffect(StatusEffectType.THORNS, 999, 10))
            status_effects_on_use.append(StatusEffect(StatusEffectType.REGENERATION, 999, 3))
        elif rarity == Rarity.LEGENDARY:
            modifiers = {
                "defense": random.randint(18, 30),
                "hp": random.randint(45, 70),
                "mana": random.randint(25, 45),
                "agility": random.randint(8, 15),
                "attack": random.randint(5, 10)
            }
            sockets = 3
            status_effects_on_use.append(StatusEffect(StatusEffectType.SHIELD, 999, 30))
            status_effects_on_use.append(StatusEffect(StatusEffectType.THORNS, 999, 15))
            status_effects_on_use.append(StatusEffect(StatusEffectType.REGENERATION, 999, 5))
        elif rarity == Rarity.MYTHIC:
            modifiers = {
                "defense": random.randint(25, 40),
                "hp": random.randint(60, 100),
                "mana": random.randint(40, 60),
                "agility": random.randint(12, 20),
                "attack": random.randint(8, 15),
                "crit_chance": random.randint(5, 10)
            }
            sockets = 4
            status_effects_on_use.append(StatusEffect(StatusEffectType.BLESSED, 999, 10))
            status_effects_on_use.append(StatusEffect(StatusEffectType.SHIELD, 999, 50))
            status_effects_on_use.append(StatusEffect(StatusEffectType.REGENERATION, 999, 8))

    else:  # Accessories
        if rarity in [Rarity.COMMON, Rarity.MAGIC]:
            stat = random.choice(["attack", "defense", "hp", "mana", "agility"])
            modifiers = {stat: random.randint(3, 8) if rarity == Rarity.MAGIC else random.randint(1, 4)}
        elif rarity == Rarity.RARE:
            modifiers = {
                random.choice(["attack", "defense"]): random.randint(5, 10),
                random.choice(["hp", "mana"]): random.randint(10, 25),
                "agility": random.randint(2, 6)
            }
            sockets = 1
        elif rarity == Rarity.EPIC:
            modifiers = {
                "attack": random.randint(6, 12),
                "defense": random.randint(6, 12),
                "hp": random.randint(15, 35),
                "mana": random.randint(15, 35),
                "crit_chance": random.randint(3, 7)
            }
            sockets = 1
            # Add unique effect
            effect_choices = [
                StatusEffect(StatusEffectType.SWIFT, 999, 10),
                StatusEffect(StatusEffectType.FOCUSED, 999, 15),
                StatusEffect(StatusEffectType.STRENGTH, 999, 8)
            ]
            status_effects_on_use.append(random.choice(effect_choices))
        elif rarity in [Rarity.LEGENDARY, Rarity.MYTHIC]:
            modifiers = {
                "attack": random.randint(10, 20),
                "defense": random.randint(10, 20),
                "hp": random.randint(25, 50),
                "mana": random.randint(25, 50),
                "agility": random.randint(5, 12),
                "crit_chance": random.randint(5, 10),
                "crit_damage": random.randint(10, 25)
            }
            sockets = 2 if rarity == Rarity.LEGENDARY else 3
            # Multiple effects
            status_effects_on_use.append(StatusEffect(StatusEffectType.BLESSED, 999, 5))
            if rarity == Rarity.MYTHIC:
                status_effects_on_use.append(StatusEffect(StatusEffectType.EMPOWERED, 999, 10))
                status_effects_on_use.append(StatusEffect(StatusEffectType.INVISIBLE, 999, 10))

    return Item(
        name=name,
        item_type=item_type,
        rarity=rarity,
        value=base_value,
        durability=100,
        max_durability=100,
        level_requirement=max(1, level - 5),
        modifiers=modifiers,
        status_effects_on_use=status_effects_on_use,
        status_effects_on_hit=status_effects_on_hit,
        sockets=sockets
    )


def generate_monster(level: int, rarity: Rarity, dungeon_theme: str, boss_tier: int = 0):
    monster_templates = {
        "Forest": {
            "names": ["Dire Wolf", "Giant Spider", "Forest Troll", "Corrupted Ent", "Shadow Bear"],
            "weaknesses": [StatusEffectType.BURN],
            "resistances": [StatusEffectType.POISON]
        },
        "Cave": {
            "names": ["Cave Bat", "Stone Golem", "Crystal Elemental", "Deep Dweller"],
            "weaknesses": [StatusEffectType.SHOCK],
            "resistances": [StatusEffectType.BLEED]
        },
        "Undead": {
            "names": ["Skeleton Warrior", "Zombie", "Wraith", "Lich", "Death Knight"],
            "weaknesses": [StatusEffectType.BURN, StatusEffectType.BLESSED],
            "resistances": [StatusEffectType.POISON, StatusEffectType.BLEED]
        },
        "Infernal": {
            "names": ["Fire Demon", "Hellhound", "Infernal Beast", "Pit Lord"],
            "weaknesses": [StatusEffectType.FREEZE],
            "resistances": [StatusEffectType.BURN]
        },
        "Void": {
            "names": ["Void Walker", "Shadow Fiend", "Chaos Spawn", "Null Entity"],
            "weaknesses": [StatusEffectType.BLESSED],
            "resistances": [StatusEffectType.CURSED, StatusEffectType.MANA_BURN]
        }
    }

    template = monster_templates.get(dungeon_theme, monster_templates["Forest"])
    name = random.choice(template["names"])

    # Add boss prefix if applicable
    boss_prefixes = ["", "Elite ", "Champion ", "Legendary "]
    name = boss_prefixes[boss_tier] + name

    # Base stats with boss scaling
    base_hp = 50 + (level * 10)
    base_attack = 10 + (level * 3)
    base_defense = 5 + (level * 2)
    base_agility = 8 + level

    # Rarity multipliers
    rarity_multipliers = {
        Rarity.COMMON: 1.0,
        Rarity.MAGIC: 1.3,
        Rarity.RARE: 1.6,
        Rarity.EPIC: 2.0,
        Rarity.LEGENDARY: 2.5,
        Rarity.MYTHIC: 3.0
    }

    # Boss tier multipliers
    boss_multipliers = [1.0, 1.5, 2.5, 4.0]

    multiplier = rarity_multipliers[rarity] * boss_multipliers[boss_tier]

    hp = int(base_hp * multiplier)
    attack = int(base_attack * multiplier)
    defense = int(base_defense * multiplier)
    agility = int(base_agility * multiplier * 0.8)  # Bosses are slightly slower
    mana = int((30 + level * 5) * multiplier)

    # Generate skills based on rarity and boss tier
    base_skills = ["Strike", "Defend"]
    theme_skills = {
        "Forest": ["Poison Bite", "Entangle", "Nature's Wrath", "Wild Growth"],
        "Cave": ["Stone Skin", "Crystal Shard", "Earthquake", "Petrify"],
        "Undead": ["Life Drain", "Curse", "Fear", "Death Touch"],
        "Infernal": ["Fire Blast", "Hellfire", "Infernal Rage", "Meteor"],
        "Void": ["Void Blast", "Phase Shift", "Reality Tear", "Nullify"]
    }

    available_skills = base_skills + theme_skills.get(dungeon_theme, [])
    skill_count = min(3 + boss_tier + (1 if rarity in [Rarity.EPIC, Rarity.LEGENDARY, Rarity.MYTHIC] else 0),
                      len(available_skills))
    skills = random.sample(available_skills, skill_count)

    # Natural status effects for bosses
    status_effects = {}
    if boss_tier >= 1:
        # Mini-bosses and above get natural resistances
        if dungeon_theme == "Infernal":
            status_effects[StatusEffectType.THORNS] = StatusEffect(StatusEffectType.THORNS, 999, 5 + level)
        elif dungeon_theme == "Undead":
            status_effects[StatusEffectType.REGENERATION] = StatusEffect(StatusEffectType.REGENERATION, 999,
                                                                         3 + level // 2)
        elif dungeon_theme == "Void":
            status_effects[StatusEffectType.SHIELD] = StatusEffect(StatusEffectType.SHIELD, 999, 20 + level * 2)

    if boss_tier >= 2:
        # Bosses get additional effects
        status_effects[StatusEffectType.FORTIFIED] = StatusEffect(StatusEffectType.FORTIFIED, 999, 10 + level)

    return Monster(
        name=f"{rarity.value} {name}",
        level=level,
        hp=hp,
        max_hp=hp,
        mana=mana,
        max_mana=mana,
        attack=attack,
        defense=defense,
        agility=agility,
        skills=skills,
        rarity=rarity,
        loot_table=[],
        status_effects=status_effects,
        weaknesses=template["weaknesses"],
        resistances=template["resistances"],
        boss_tier=boss_tier
    )


class RPGGame:
    def __init__(self):
        self.state = GameState()
        self.dungeons = {
            "Forest Depths": {"theme": "Forest", "description": "🌲 A dark forest filled with corrupted creatures",
                              "min_level": 1},
            "Crystal Caves": {"theme": "Cave", "description": "💎 Ancient caves with crystal formations",
                              "min_level": 5},
            "Cursed Catacombs": {"theme": "Undead", "description": "💀 Underground tombs with restless spirits",
                                 "min_level": 10},
            "Infernal Fortress": {"theme": "Infernal", "description": "🔥 A hellish stronghold of demons",
                                  "min_level": 15},
            "Void Sanctum": {"theme": "Void", "description": "🌌 Reality tears at the seams here", "min_level": 20}
        }
        self.current_room_content = None
        self.combat_state = None
        self.turn_counter = 0

    def start_game(self):
        print("=" * 60)
        print("🎮 EPIC RPG ADVENTURE - ENHANCED EDITION 🎮")
        print("=" * 60)
        print("\n📜 Welcome, brave adventurer!")
        print("A world of danger, mystery, and treasure awaits...")

        # Difficulty selection
        print("\n🎯 Select Difficulty:")
        difficulties = list(DifficultyMode)
        for i, diff in enumerate(difficulties, 1):
            bonuses = {
                DifficultyMode.EASY: "(-50% enemy stats, +50% rewards)",
                DifficultyMode.NORMAL: "(Standard experience)",
                DifficultyMode.HARD: "(+25% enemy stats, +25% rewards)",
                DifficultyMode.NIGHTMARE: "(+50% enemy stats, +50% rewards)",
                DifficultyMode.APOCALYPSE: "(+100% enemy stats, +100% rewards)"
            }
            print(f"{i}. {diff.value} {bonuses[diff]}")

        while True:
            try:
                diff_choice = int(input("\nChoose difficulty (1-5): ")) - 1
                if 0 <= diff_choice < len(difficulties):
                    self.state.difficulty = difficulties[diff_choice]
                    break
            except ValueError:
                pass
            print("Invalid choice. Please try again.")

        # Character creation
        print("\n📝 Character Creation")
        name = input("Enter your character name: ").strip()
        if not name:
            name = "Hero"

        print("\n🎭 Choose your class:")
        classes = list(PlayerClass)
        for i, cls in enumerate(classes, 1):
            print(f"{i:2}. {cls.value}")

        while True:
            try:
                choice = int(input("\nEnter class number: ")) - 1
                if 0 <= choice < len(classes):
                    player_class = classes[choice]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        self.state.player = Player(name, player_class)
        self.state.refresh_shops()

        print(f"\n🎉 Welcome, {name} the {player_class.value}!")
        print(f"⚔️  Difficulty: {self.state.difficulty.value}")
        print("\n📍 Your adventure begins in the town square...")
        input("\nPress Enter to continue...")

        self.main_game_loop()

    def main_game_loop(self):
        while True:
            if self.state.current_location == "town":
                self.town_menu()
            elif self.state.current_location == "dungeon":
                self.dungeon_menu()
            elif self.state.current_location == "combat":
                self.combat_loop()

    def town_menu(self):
        print("\n" + "=" * 50)
        print("🏘️  TOWN SQUARE")
        print("=" * 50)
        print(f"📅 Day {self.state.game_day} | 💰 Gold: {self.state.player.gold}")
        print(f"⭐ Level {self.state.player.level} {self.state.player.player_class.value}")

        # Show class resources
        if self.state.player.class_resources:
            resource_display = []
            for name, resource in self.state.player.class_resources.items():
                resource_display.append(f"{resource.name}: {resource.current}/{resource.maximum}")
            print(f"🔋 {' | '.join(resource_display)}")

        print()
        print("1. 🛍️  Visit Shops")
        print("2. 🏨 Visit Inn (Rest for 50 gold)")
        print("3. ⛪ Visit Shrine (Free blessing, 3-day cooldown)")
        print("4. 🔨 Visit Blacksmith")
        print("5. 🗡️  Manage Equipment")
        print("6. 📊 View Character Stats")
        print("7. 🎯 Enhanced Skill Management")
        print("8. 🌳 Skill Tree & Evolution")
        print("9. 🏰 Enter Dungeon")
        print("10. 💾 Save & Quit")

        choice = input("\nChoose action: ").strip()

        if choice == "1":
            self.shop_menu()
        elif choice == "2":
            self.visit_inn()
        elif choice == "3":
            self.visit_shrine()
        elif choice == "4":
            self.visit_blacksmith()
        elif choice == "5":
            self.equipment_menu()
        elif choice == "6":
            self.show_character_stats()
        elif choice == "7":
            self.enhanced_skill_menu()
        elif choice == "8":
            self.skill_tree_menu()
        elif choice == "9":
            self.dungeon_selection()
        elif choice == "10":
            print("\n👋 Thanks for playing! Your adventure awaits your return...")
            exit()
        else:
            print("❌ Invalid choice. Please try again.")

    def enhanced_skill_menu(self):
        player = self.state.player

        print(f"\n🎯 ENHANCED SKILLS - {player.player_class.value}")
        print("=" * 60)
        print(f"🎯 Skill Points: {player.skill_points}")

        # Group by tier with enhanced display
        tiers = {1: [], 2: [], 3: [], 4: [], 5: []}
        for name, skill in player.skills.items():
            tiers[skill.tier].append((name, skill))

        tier_names = ["Novice", "Adept", "Expert", "Master", "Grandmaster"]

        for tier in [1, 2, 3, 4, 5]:
            if not tiers.get(tier):
                continue

            print(f"\n🏆 Tier {tier} - {tier_names[tier - 1]}:")
            for name, skill in tiers.get(tier, []):
                status = "✅" if skill.unlocked else "🔒"

                # Enhanced skill display
                skill_level = f"Lv.{skill.progression.skill_level}"
                mastery = f"M:{skill.progression.mastery_points}" if skill.progression.mastery_points > 0 else ""
                evolution = "🧬" if skill.can_evolve and skill.check_evolution() else ""

                # Resource cost display
                resource_info = ""
                if skill.resource_type != "mana":
                    resource_info = f" | {skill.resource_type.title()}: {skill.resource_cost}"

                cd_info = f" (CD: {skill.current_cooldown}/{skill.cooldown})" if skill.cooldown > 0 else ""

                print(f"  {status} {name} {skill_level} {mastery} {evolution}{cd_info}")
                print(f"     💙 Mana: {skill.mana_cost}{resource_info}")
                print(f"     📖 {skill.description}")

                if skill.elemental_type:
                    print(f"     🔥 Element: {skill.elemental_type.title()}")

                if skill.progression.skill_level > 1:
                    exp_to_next = skill.progression.skill_level * 100 - skill.progression.skill_exp
                    print(
                        f"     ⭐ EXP: {skill.progression.skill_exp}/{skill.progression.skill_level * 100} (Need {exp_to_next})")

        print("\n📋 Actions:")
        print("1. 🔓 Unlock Skill")
        print("2. 🧬 Evolve Skill")
        print("3. 🎭 View Skill Details")
        print("4. ⬅️  Back")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            self.unlock_skill()
        elif choice == "2":
            self.evolve_skill()
        elif choice == "3":
            self.view_skill_details()
        elif choice == "4":
            return

    def skill_tree_menu(self):
        player = self.state.player

        print(f"\n🌳 SKILL TREE - {player.player_class.value}")
        print("=" * 60)

        if not player.skill_trees:
            print("🚫 No skill trees available for this class yet.")
            input("\nPress Enter to continue...")
            return

        for tree_name, nodes in player.skill_trees.items():
            print(f"\n🌿 {tree_name}:")
            for i, node in enumerate(nodes, 1):
                status = "✅" if node.unlocked else "🔒"
                prereq_info = ""
                if node.prerequisites and not node.unlocked:
                    prereq_info = f" (Needs: {', '.join(node.prerequisites)})"

                print(f"  {i}. {status} {node.name}{prereq_info}")
                print(f"     📖 {node.description}")

        print("\n📋 Actions:")
        print("1. 🔓 Unlock Tree Node")
        print("2. ⬅️  Back")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            self.unlock_tree_node()
        elif choice == "2":
            return

    def unlock_tree_node(self):
        player = self.state.player

        all_nodes = []
        for tree_name, nodes in player.skill_trees.items():
            for node in nodes:
                if not node.unlocked and self.can_unlock_node(node):
                    all_nodes.append((tree_name, node))

        if not all_nodes:
            print("🚫 No nodes available to unlock!")
            return

        print("\n🔓 AVAILABLE NODES:")
        for i, (tree_name, node) in enumerate(all_nodes, 1):
            print(f"{i}. {node.name} ({tree_name})")
            print(f"   📖 {node.description}")

        choice = input("\nChoose node (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(all_nodes):
                tree_name, node = all_nodes[choice_num - 1]
                if player.skill_points >= 1:
                    player.skill_points -= 1
                    node.unlocked = True
                    print(f"✅ Unlocked {node.name} in {tree_name}!")

                    # Apply node effect
                    self.apply_tree_node_effect(node)
                else:
                    print("🚫 Not enough skill points!")
        except ValueError:
            print("Invalid input.")

    def can_unlock_node(self, node):
        player = self.state.player

        # Check prerequisites
        for prereq in node.prerequisites:
            # Find the prerequisite node
            prereq_unlocked = False
            for tree_nodes in player.skill_trees.values():
                for tree_node in tree_nodes:
                    if tree_node.name == prereq and tree_node.unlocked:
                        prereq_unlocked = True
                        break
                if prereq_unlocked:
                    break

            if not prereq_unlocked:
                return False

        return True

    def apply_tree_node_effect(self, node):
        player = self.state.player

        # Apply various node effects
        if node.effect == "cooldown_reduction":
            for skill in player.skills.values():
                if "Shield" in skill.name:
                    skill.cooldown = max(0, skill.cooldown - 1)
        elif node.effect == "duration_boost":
            # Effects will be applied during skill usage
            pass
        elif node.effect == "cost_reduction":
            # Effects will be applied during skill usage
            pass
        elif node.effect == "healing_boost":
            # Applied when healing skills are used
            pass
        elif node.effect == "heal_shield":
            # Applied when healing skills are used
            pass
        elif node.effect == "heal_efficiency":
            # Applied when healing skills are used
            pass
        elif node.effect == "faith_on_damage":
            # Applied when dealing damage
            pass
        elif node.effect == "holy_power":
            # Applied to holy damage calculations
            pass
        elif node.effect == "battle_healing":
            # Applied when using attack abilities
            pass
        elif node.effect == "mark_crit":
            # Applied to marked targets
            pass
        elif node.effect == "guaranteed_hit":
            # Applied on first attack
            pass
        elif node.effect == "escalating_mark":
            # Applied to mark mechanics
            pass
        elif node.effect == "focus_regen":
            # Add regeneration to focus resource
            if "focus" in player.class_resources:
                player.class_resources["focus"].regen_rate += 3
        elif node.effect == "companion":
            # Summon mechanics
            pass
        elif node.effect == "hunt_mode":
            # Applied when companion is active
            pass
        elif node.effect == "energy_efficiency":
            # Applied to energy costs
            pass
        elif node.effect == "overcharge":
            # Allows energy abilities to exceed limits
            pass
        elif node.effect == "energy_perpetual":
            if "energy" in player.class_resources:
                player.class_resources["energy"].regen_rate += 10
        elif node.effect == "explosive_damage":
            # Applied to explosion abilities
            pass
        elif node.effect == "chain_explosions":
            # Applied to explosion mechanics
            pass
        elif node.effect == "burn_all":
            # All attacks apply burn
            pass
        elif node.effect == "holy_generation":
            # Generate holy power from damage
            pass
        elif node.effect == "holy_weapon":
            # Add holy damage to weapon attacks
            pass
        elif node.effect == "divine_protection":
            # Prevent death while blessed
            pass
        elif node.effect == "consecrate":
            # Create holy ground
            pass
        elif node.effect == "sanctuary_defense":
            # Defense bonus on holy ground
            pass
        elif node.effect == "holy_ground":
            # Instant kill undead on holy ground
            pass
        elif node.effect == "rage_from_damage":
            # Enhance rage generation from damage
            if self.player_class == PlayerClass.BARBARIAN:
                self.passive_abilities["rage_on_damage"] = self.passive_abilities.get("rage_on_damage", 5) + 5
            pass
        elif node.effect == "kill_streak":
            # Damage bonus on kills
            pass
        elif node.effect == "rage_sustain":
            if "rage" in player.class_resources:
                player.class_resources["rage"].decay_rate = 0
        elif node.effect == "damage_reduction":
            # Reduce all damage by 15%
            self.passive_abilities["damage_reduction"] = self.passive_abilities.get("damage_reduction", 0) + 15
            pass
        elif node.effect == "lifesteal_all":
            # All attacks lifesteal
            pass
        elif node.effect == "death_prevention":
            # Gain rage and heal when near death
            pass
        elif node.effect == "quick_start":
            # First ability has no cooldown
            pass
        elif node.effect == "extra_actions":
            # Chance for extra actions
            pass
        elif node.effect == "execute":
            # Instant kill low HP enemies
            pass
        elif node.effect == "double_tap":
            # Basic attacks hit twice
            pass
        elif node.effect == "ricochet":
            # Attacks bounce
            pass
        elif node.effect == "ultimate_barrage":
            # Ultimate ability
            pass
        elif node.effect == "crit_poison":
            # Crits apply poison
            pass
        elif node.effect == "stealth_crit":
            # Stealth attacks always crit
            pass
        elif node.effect == "assassinate":
            # Instant kill low HP
            pass
        elif node.effect == "escape_stealth":
            # Auto-stealth at low HP
            pass
        elif node.effect == "illusions":
            # Create decoys
            pass
        elif node.effect == "perma_stealth":
            # All abilities grant stealth
            pass
        elif node.effect == "nature_regen":
            # Permanent regeneration
            player.add_status_effect(StatusEffect(StatusEffectType.REGENERATION, 999, 5))
        elif node.effect == "group_heal":
            # Healing affects all allies
            pass
        elif node.effect == "summon_treants":
            # Summon treants
            pass
        elif node.effect == "form_bonus":
            # Stats based on form
            pass
        elif node.effect == "form_flexibility":
            # Change forms per turn
            pass
        elif node.effect == "all_forms":
            # All form benefits
            pass
        elif node.effect == "resource_gain":
            # Gain resource when taking damage
            pass
        elif node.effect == "immunity":
            # Immune to stun/slow
            pass
        elif node.effect == "spell_synergy":
            # Elemental combo damage
            pass
        elif node.effect == "mana_efficiency":
            # Chance to not consume mana
            pass
        elif node.effect == "area_mastery":
            # All spells gain area effect
            pass
        elif node.effect == "time_magic":
            # Gain time dilation on cast
            pass
        elif node.effect == "delayed_cast":
            # Delay spell effects
            pass
        elif node.effect == "extra_action":
            # Extra turn every 5 rounds
            pass
        # Add more effects as needed

    def evolve_skill(self):
        player = self.state.player

        evolvable = []
        for name, skill in player.skills.items():
            if skill.can_evolve and skill.check_evolution():
                evolvable.append((name, skill))

        if not evolvable:
            print("🚫 No skills ready for evolution!")
            return

        print("\n🧬 EVOLVABLE SKILLS:")
        for i, (name, skill) in enumerate(evolvable, 1):
            print(f"{i}. {name}")
            print(f"   📖 Current: {skill.description}")
            print(f"   🧬 Evolution requirements met!")

        choice = input("\nChoose skill to evolve (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(evolvable):
                name, skill = evolvable[choice_num - 1]
                self.perform_skill_evolution(name, skill)
        except ValueError:
            print("Invalid input.")

    def perform_skill_evolution(self, skill_name, skill):
        player = self.state.player

        # Define evolution paths
        evolution_map = {
            "Sword Strike": "Blade Mastery",
            "Whirlwind": "Hurricane Strike",
            "Power Strike": "Devastating Blow"
        }

        new_name = evolution_map.get(skill_name, f"Enhanced {skill_name}")

        # Enhance the skill
        skill.damage = int(skill.damage * 1.5)
        skill.mana_cost = int(skill.mana_cost * 1.2)
        skill.description = f"Evolved form of {skill_name} - much more powerful!"
        skill.evolved_form = new_name
        skill.can_evolve = False

        # Add new effects
        if "Strike" in skill_name:
            skill.status_effects.append(StatusEffect(StatusEffectType.EMPOWERED, 3, 15))
        elif "Whirlwind" in skill_name:
            skill.area_effect = True
            skill.status_effects.append(StatusEffect(StatusEffectType.STUNNED, 1))

        # Update in skills dictionary
        del player.skills[skill_name]
        player.skills[new_name] = skill
        skill.name = new_name

        print(f"🎉 {skill_name} evolved into {new_name}!")
        print(f"✨ Enhanced power and new abilities unlocked!")

        # Check achievement
        achievement = self.state.check_achievement("evolve_skill")
        if achievement:
            print(f"🏆 Achievement: {achievement.name}!")

    def view_skill_details(self):
        player = self.state.player

        skills_list = list(player.skills.items())

        print("\n📖 SKILL DETAILS:")
        for i, (name, skill) in enumerate(skills_list, 1):
            print(f"{i}. {name}")

        choice = input("\nChoose skill to examine (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(skills_list):
                name, skill = skills_list[choice_num - 1]
                self.display_detailed_skill_info(name, skill)
        except ValueError:
            print("Invalid input.")

    def display_detailed_skill_info(self, name, skill):
        print(f"\n📖 {name} - DETAILED INFO")
        print("=" * 50)
        print(f"🎯 Tier: {skill.tier} | Level: {skill.progression.skill_level}/10")
        print(f"💙 Mana Cost: {skill.mana_cost}")

        if skill.resource_type != "mana":
            print(f"🔋 {skill.resource_type.title()} Cost: {skill.resource_cost}")

        print(f"⚔️  Damage: {skill.damage}")
        print(f"💚 Healing: {skill.heal}")
        print(f"⏰ Cooldown: {skill.cooldown} turns")
        print(f"🎭 Type: {skill.skill_type}")

        if skill.elemental_type:
            print(f"🔥 Element: {skill.elemental_type}")

        if skill.area_effect:
            print("💥 Area Effect: Yes")

        if skill.casting_time > 0:
            print(f"⏳ Casting Time: {skill.casting_time} turns")

        print(f"📝 Description: {skill.description}")

        if skill.status_effects:
            print("\n🎭 Status Effects:")
            for effect in skill.status_effects:
                print(f"  • {effect.description}")

        if skill.combo_with:
            print(f"\n🔗 Combos with: {', '.join(skill.combo_with)}")

        # Progression info
        exp_to_next = skill.progression.skill_level * 100 - skill.progression.skill_exp
        print(f"\n⭐ Experience: {skill.progression.skill_exp}/{skill.progression.skill_level * 100}")
        print(f"🎯 Mastery Points: {skill.progression.mastery_points}")

        if skill.can_evolve:
            print(f"\n🧬 Can Evolve: {skill.check_evolution()}")
            if skill.evolution_requirements:
                print(f"Requirements: {skill.evolution_requirements}")

        input("\nPress Enter to continue...")

    def shop_menu(self):
        print("\n🛍️  SHOPPING DISTRICT")
        print("=" * 30)
        print("1. ⚔️  Weapon Shop")
        print("2. 🛡️  Armor Shop")
        print("3. 💍 Accessory Shop")
        print("4. 🧪 Potion Shop")
        print("5. 💎 Rune Shop")
        print("6. 🔄 Refresh All Shops (Advance Day)")
        print("7. ⬅️  Back to Town")

        choice = input("\nChoose shop: ").strip()

        if choice == "1":
            self.browse_shop("weapons")
        elif choice == "2":
            self.browse_shop("armor")
        elif choice == "3":
            self.browse_shop("accessories")
        elif choice == "4":
            self.browse_shop("potions")
        elif choice == "5":
            self.browse_shop("runes")
        elif choice == "6":
            self.state.advance_day()
            print("🌅 A new day dawns! All shops have refreshed their inventory.")
        elif choice == "7":
            return

    def browse_shop(self, shop_type):
        inventory = self.state.shop_inventory.get(shop_type, [])

        if not inventory:
            print(f"The {shop_type} shop is empty!")
            return

        rarity_colors = {
            "Common": "⚪", "Magic": "🔵", "Rare": "🟣",
            "Epic": "🟡", "Legendary": "🟠", "Mythic": "🔴"
        }

        print(f"\n{'=' * 50}")
        print(f"🏪 {shop_type.upper()} SHOP")
        print(f"{'=' * 50}")
        print(f"💰 Your Gold: {self.state.player.gold}")
        print()

        for i, item in enumerate(inventory, 1):
            print(f"{i}. {rarity_colors.get(item.rarity.value, '⚪')} {item.name}")
            print(f"   💰 Price: {item.value} | 🎯 Lvl Req: {item.level_requirement}")

            if item.modifiers:
                mods = ", ".join([f"{k}+{v}" for k, v in item.modifiers.items()])
                print(f"   ✨ Stats: {mods}")

            if hasattr(item, 'sockets') and item.sockets > 0:
                print(f"   💎 Sockets: {item.sockets}")

            if item.description:
                print(f"   📝 {item.description}")
            print()

        print(f"{len(inventory) + 1}. ⬅️  Back")

        choice = input("\nChoose item to buy: ").strip()

        try:
            choice_num = int(choice)
            if choice_num == len(inventory) + 1:
                return
            elif 1 <= choice_num <= len(inventory):
                self.buy_item(inventory[choice_num - 1], shop_type, choice_num - 1)
        except ValueError:
            print("Please enter a valid number.")

    def buy_item(self, item, shop_type, index):
        player = self.state.player

        if player.gold < item.value:
            print("💸 Not enough gold!")
            return

        if item.level_requirement > player.level:
            print(f"🚫 You need to be level {item.level_requirement}!")
            return

        player.gold -= item.value

        # Add to inventory
        if item.name in player.inventory:
            player.inventory[item.name] += 1
        else:
            player.inventory[item.name] = 1

        # Store item object
        if not hasattr(player, 'item_objects'):
            player.item_objects = {}
        player.item_objects[item.name] = item

        # Remove from shop
        self.state.shop_inventory[shop_type].pop(index)

        print(f"✅ Purchased {item.name} for {item.value} gold!")

    def visit_inn(self):
        player = self.state.player
        cost = 50

        if player.gold < cost:
            print("💸 Not enough gold! The inn costs 50 gold.")
            return

        player.gold -= cost
        player.hp = player.get_total_stats()["hp"]
        player.mana = player.get_total_stats()["mana"]

        # Restore class resources
        for resource in player.class_resources.values():
            resource.current = resource.maximum

        # Clear all negative status effects
        negative_effects = [
            StatusEffectType.POISON, StatusEffectType.BURN, StatusEffectType.BLEED,
            StatusEffectType.FREEZE, StatusEffectType.SHOCK, StatusEffectType.WEAKNESS,
            StatusEffectType.VULNERABLE, StatusEffectType.SLOWED, StatusEffectType.CONFUSED,
            StatusEffectType.STUNNED, StatusEffectType.SLEEPING, StatusEffectType.CURSED,
            StatusEffectType.MANA_BURN, StatusEffectType.MARKED, StatusEffectType.SOUL_BURN
        ]

        for effect_type in negative_effects:
            if effect_type in player.status_effects:
                player.remove_status_effect(effect_type)

        # Reset skill cooldowns
        for skill in player.skills.values():
            skill.current_cooldown = 0

        print("🏨 You rest at the inn and feel completely refreshed!")
        print(f"💖 HP: {player.hp}/{player.get_total_stats()['hp']}")
        print(f"💙 Mana: {player.mana}/{player.get_total_stats()['mana']}")
        print("🔋 All resources restored!")
        print("✨ All negative effects removed and cooldowns reset!")

    def visit_shrine(self):
        player = self.state.player

        if self.state.last_shrine_use and self.state.game_day - self.state.last_shrine_use < 3:
            days_left = 3 - (self.state.game_day - self.state.last_shrine_use)
            print(f"⛪ The shrine's power is recovering. Come back in {days_left} days.")
            return

        self.state.last_shrine_use = self.state.game_day
        player.hp = player.get_total_stats()["hp"]
        player.mana = player.get_total_stats()["mana"]

        # Grant powerful blessing
        blessing = StatusEffect(StatusEffectType.BLESSED, 20, 10)
        regen = StatusEffect(StatusEffectType.REGENERATION, 15, 5)
        shield = StatusEffect(StatusEffectType.SHIELD, 10, 30)

        player.add_status_effect(blessing)
        player.add_status_effect(regen)
        player.add_status_effect(shield)

        print("⛪ Divine light bathes you in holy power!")
        print("✨ You receive powerful blessings!")
        print("🛡️ A divine shield protects you!")
        print("💚 Regeneration flows through you!")

    def visit_blacksmith(self):
        print("\n🔨 BLACKSMITH FORGE")
        print("=" * 30)
        print("1. 🔧 Repair Equipment")
        print("2. ⬅️  Back")

        choice = input("\nChoose service: ").strip()

        if choice == "1":
            self.repair_equipment()
        elif choice == "2":
            return

    def repair_equipment(self):
        player = self.state.player
        damaged_items = []

        for slot, item in player.equipment.items():
            if item and item.durability < item.max_durability:
                damaged_items.append((slot, item))

        if not damaged_items:
            print("✨ All equipment is in perfect condition!")
            return

        print("\n🔧 EQUIPMENT REPAIR")
        for i, (slot, item) in enumerate(damaged_items, 1):
            repair_cost = int((item.max_durability - item.durability) * 2)
            print(f"{i}. {item.name} ({slot})")
            print(f"   Durability: {item.durability}/{item.max_durability}")
            print(f"   Cost: {repair_cost} gold")

        choice = input("\nChoose item to repair (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(damaged_items):
                slot, item = damaged_items[choice_num - 1]
                repair_cost = int((item.max_durability - item.durability) * 2)

                if player.gold >= repair_cost:
                    player.gold -= repair_cost
                    item.durability = item.max_durability
                    print(f"✅ {item.name} fully repaired!")
                else:
                    print("💸 Not enough gold!")
        except ValueError:
            print("Invalid input.")

    def equipment_menu(self):
        player = self.state.player

        print(f"\n🎒 {player.name}'s EQUIPMENT")
        print("=" * 40)

        print("📋 Currently Equipped:")
        for slot, item in player.equipment.items():
            if item:
                durability_icon = "🟢" if item.durability > 70 else "🟡" if item.durability > 30 else "🔴"
                print(f"  {slot}: {item.name} {durability_icon}")
            else:
                print(f"  {slot}: [Empty]")

        print(f"\n🎒 Inventory ({len(player.inventory)} items)")

        print("\n📋 Actions:")
        print("1. 🔄 Equip Item")
        print("2. 📤 Unequip Item")
        print("3. ⬅️  Back")

        choice = input("\nChoose action: ").strip()

        if choice == "1":
            self.equip_item()
        elif choice == "2":
            self.unequip_item()
        elif choice == "3":
            return

    def equip_item(self):
        player = self.state.player

        equippable = []
        for item_name in player.inventory:
            if hasattr(player, 'item_objects') and item_name in player.item_objects:
                item = player.item_objects[item_name]
                if item.item_type in [ItemType.WEAPON, ItemType.ARMOR, ItemType.RING,
                                      ItemType.AMULET, ItemType.TRINKET, ItemType.OFFHAND]:
                    equippable.append(item)

        if not equippable:
            print("🚫 No equippable items!")
            return

        print("\n🔄 EQUIPPABLE ITEMS:")
        for i, item in enumerate(equippable, 1):
            print(f"{i}. {item.name} ({item.item_type.value})")

        choice = input("\nChoose item (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(equippable):
                item = equippable[choice_num - 1]

                # Check requirements
                if item.level_requirement > player.level:
                    print(f"🚫 Requires level {item.level_requirement}!")
                    return

                # Determine slot
                slot_map = {
                    ItemType.WEAPON: "weapon",
                    ItemType.OFFHAND: "offhand",
                    ItemType.ARMOR: "armor",
                    ItemType.AMULET: "amulet",
                    ItemType.TRINKET: "trinket"
                }

                if item.item_type == ItemType.RING:
                    slot = "ring1" if not player.equipment["ring1"] else "ring2"
                else:
                    slot = slot_map.get(item.item_type)

                if slot:
                    # Unequip current item
                    if player.equipment[slot]:
                        old_item = player.equipment[slot]
                        if old_item.name in player.inventory:
                            player.inventory[old_item.name] += 1
                        else:
                            player.inventory[old_item.name] = 1

                    # Equip new item
                    player.equipment[slot] = item
                    player.inventory[item.name] -= 1
                    if player.inventory[item.name] <= 0:
                        del player.inventory[item.name]

                    # Apply passive effects
                    for effect in item.status_effects_on_use:
                        player.add_status_effect(effect)

                    print(f"✅ Equipped {item.name}!")
        except ValueError:
            print("Invalid input.")

    def unequip_item(self):
        player = self.state.player

        equipped = [(slot, item) for slot, item in player.equipment.items() if item]

        if not equipped:
            print("🚫 No items equipped!")
            return

        print("\n📤 EQUIPPED ITEMS:")
        for i, (slot, item) in enumerate(equipped, 1):
            print(f"{i}. {item.name} ({slot})")

        choice = input("\nChoose item to unequip (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(equipped):
                slot, item = equipped[choice_num - 1]

                player.equipment[slot] = None
                if item.name in player.inventory:
                    player.inventory[item.name] += 1
                else:
                    player.inventory[item.name] = 1

                print(f"✅ Unequipped {item.name}!")
        except ValueError:
            print("Invalid input.")

    def show_character_stats(self):
        player = self.state.player
        stats = player.get_total_stats()

        print(f"\n📊 {player.name} the {player.player_class.value}")
        print("=" * 50)
        print(f"🎖️  Level: {player.level}")
        print(f"⭐ Experience: {player.exp}/{player.exp_to_next}")
        print(f"🎯 Skill Points: {player.skill_points}")
        print(f"💰 Gold: {player.gold}")

        print("\n📈 CORE STATS:")
        print(f"  💖 HP: {player.hp}/{stats['hp']}")
        print(f"  💙 Mana: {player.mana}/{stats['mana']}")
        print(f"  ⚔️  Attack: {stats['attack']}")
        print(f"  🛡️  Defense: {stats['defense']}")
        print(f"  🏃 Agility: {stats['agility']}")
        print(f"  🎯 Crit Chance: {stats['crit_chance']}%")
        print(f"  💥 Crit Damage: {stats['crit_damage']}%")

        if player.class_resources:
            print("\n🔋 CLASS RESOURCES:")
            for name, resource in player.class_resources.items():
                print(f"  {resource.name}: {resource.current}/{resource.maximum}")

        if player.status_effects:
            print("\n🎭 STATUS EFFECTS:")
            for effect_type, effect in player.status_effects.items():
                duration_text = f" ({effect.duration} turns)" if effect.duration != 999 else " (Permanent)"
                print(f"  • {effect.description}{duration_text}")

        # Show combo info
        if player.combo_tracker.combo_count > 0:
            print(f"\n💥 Active Combo: {player.combo_tracker.combo_count} hits")
            print(f"    Damage Multiplier: {player.combo_tracker.combo_damage_multiplier:.1f}x")

        input("\nPress Enter to continue...")

    def unlock_skill(self):
        player = self.state.player

        unlockable = []
        for name, skill in player.skills.items():
            if not skill.unlocked and player.level >= skill.level_requirement:
                unlockable.append((name, skill))

        if not unlockable:
            print("🚫 No skills available to unlock!")
            return

        print("\n🔓 UNLOCKABLE SKILLS:")
        for i, (name, skill) in enumerate(unlockable, 1):
            print(f"{i}. {name} (Tier {skill.tier})")
            print(f"   {skill.description}")

        choice = input("\nChoose skill (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(unlockable):
                name, skill = unlockable[choice_num - 1]
                if player.skill_points >= 1:
                    player.skill_points -= 1
                    skill.unlocked = True
                    print(f"✅ Unlocked {name}!")
                else:
                    print("🚫 Not enough skill points!")
        except ValueError:
            print("Invalid input.")

    def dungeon_selection(self):
        print("\n🏰 DUNGEON SELECTION")
        print("=" * 40)

        player = self.state.player
        dungeons = list(self.dungeons.items())

        for i, (name, info) in enumerate(dungeons, 1):
            locked = "🔒" if player.level < info["min_level"] else "✅"
            print(f"{i}. {locked} {name} (Lvl {info['min_level']}+)")
            print(f"   {info['description']}")

        print(f"\n{len(dungeons) + 1}. ⬅️  Back")

        choice = input("\nChoose dungeon: ").strip()

        try:
            choice_num = int(choice)
            if choice_num == len(dungeons) + 1:
                return
            elif 1 <= choice_num <= len(dungeons):
                name, info = dungeons[choice_num - 1]
                if player.level >= info["min_level"]:
                    self.enter_dungeon(name)
                else:
                    print(f"🚫 Requires level {info['min_level']}!")
        except ValueError:
            print("Invalid input.")

    def enter_dungeon(self, dungeon_name):
        self.state.current_location = "dungeon"
        self.state.current_dungeon = dungeon_name
        self.state.current_level = 1
        self.state.current_room = 1
        self.current_room_content = None

        print(f"\n🚪 Entering {dungeon_name}...")
        print(f"⚔️  Difficulty: {self.state.difficulty.value}")
        input("Press Enter to continue...")

    def dungeon_menu(self):
        print(f"\n🏰 {self.state.current_dungeon}")
        print(f"📍 Floor {self.state.current_level}, Room {self.state.current_room}")
        print("=" * 50)

        player = self.state.player

        # Process status effects
        messages = player.process_status_effects()
        for msg in messages:
            print(msg)

        if player.hp <= 0:
            self.handle_player_death()
            return

        # Generate room if needed
        if not self.current_room_content:
            self.generate_room_content()

        # Auto-combat for monsters
        if (self.current_room_content and
                self.current_room_content["type"] == "monster" and
                not self.current_room_content["explored"]):
            print(f"⚔️  {self.current_room_content['content'].name} attacks!")
            self.current_room_content["explored"] = True
            self.start_combat(self.current_room_content["content"])
            return

        self.display_room_content()

        print("\n📋 ACTIONS:")
        if (self.current_room_content and
                self.current_room_content["type"] != "monster" and
                not self.current_room_content["explored"]):
            print("1. 🔍 Explore Room")
        print("2. 🚪 Next Room")
        print("3. 📊 View Stats")
        print("4. 🎒 Equipment")
        print("5. 🏃 Return to Town")

        choice = input("\nChoose: ").strip()

        if choice == "1" and self.current_room_content and not self.current_room_content["explored"]:
            self.explore_room()
        elif choice == "2":
            self.next_room()
        elif choice == "3":
            self.show_character_stats()
        elif choice == "4":
            self.equipment_menu()
        elif choice == "5":
            self.state.current_location = "town"
            self.current_room_content = None

    def generate_room_content(self):
        # Room type probabilities
        room_types = ["monster", "treasure", "trap", "empty"]

        # Boss rooms at specific intervals
        if self.state.current_room == 10:
            room_type = "boss"
        elif self.state.current_room == 25:
            room_type = "boss"
        else:
            weights = [50, 25, 15, 10]
            room_type = random.choices(room_types, weights=weights)[0]

        self.current_room_content = {
            "type": room_type,
            "explored": False,
            "content": None
        }

        if room_type == "monster":
            self.generate_monster_room()
        elif room_type == "boss":
            self.generate_boss_room()
        elif room_type == "treasure":
            self.generate_treasure_room()
        elif room_type == "trap":
            self.current_room_content["content"] = "trap"
        elif room_type == "empty":
            self.current_room_content["content"] = "empty"

    def generate_monster_room(self):
        player_level = self.state.player.level

        # Monster level based on dungeon depth
        level_variance = random.randint(-2, 3)
        monster_level = max(1, player_level + self.state.current_level + level_variance)

        # Rarity based on difficulty
        rarity_weights = {
            DifficultyMode.EASY: [70, 20, 8, 2, 0, 0],
            DifficultyMode.NORMAL: [50, 30, 15, 4, 1, 0],
            DifficultyMode.HARD: [30, 35, 20, 10, 4, 1],
            DifficultyMode.NIGHTMARE: [20, 30, 25, 15, 8, 2],
            DifficultyMode.APOCALYPSE: [10, 20, 30, 20, 15, 5]
        }

        rarities = list(Rarity)
        weights = rarity_weights[self.state.difficulty]
        rarity = random.choices(rarities, weights=weights)[0]

        theme = self.dungeons[self.state.current_dungeon]["theme"]
        monster = generate_monster(monster_level, rarity, theme, boss_tier=0)

        # Apply difficulty modifiers
        difficulty_mods = {
            DifficultyMode.EASY: 0.5,
            DifficultyMode.NORMAL: 1.0,
            DifficultyMode.HARD: 1.25,
            DifficultyMode.NIGHTMARE: 1.5,
            DifficultyMode.APOCALYPSE: 2.0
        }

        mod = difficulty_mods[self.state.difficulty]
        monster.hp = int(monster.hp * mod)
        monster.max_hp = monster.hp
        monster.attack = int(monster.attack * mod)
        monster.defense = int(monster.defense * mod)

        self.current_room_content["content"] = monster

    def generate_boss_room(self):
        player_level = self.state.player.level

        # Determine boss tier
        if self.state.current_room == 10:
            boss_tier = 1  # Mini-boss
        elif self.state.current_room == 25:
            boss_tier = 2  # Floor boss
        else:
            boss_tier = 1

        monster_level = player_level + self.state.current_level + 3

        # Bosses are always at least Rare
        rarities = [Rarity.RARE, Rarity.EPIC, Rarity.LEGENDARY, Rarity.MYTHIC]
        weights = [40, 35, 20, 5]
        rarity = random.choices(rarities, weights=weights)[0]

        theme = self.dungeons[self.state.current_dungeon]["theme"]
        boss = generate_monster(monster_level, rarity, theme, boss_tier=boss_tier)

        # Apply difficulty modifiers
        difficulty_mods = {
            DifficultyMode.EASY: 0.7,
            DifficultyMode.NORMAL: 1.0,
            DifficultyMode.HARD: 1.3,
            DifficultyMode.NIGHTMARE: 1.6,
            DifficultyMode.APOCALYPSE: 2.0
        }

        mod = difficulty_mods[self.state.difficulty]
        boss.hp = int(boss.hp * mod)
        boss.max_hp = boss.hp
        boss.attack = int(boss.attack * mod)
        boss.defense = int(boss.defense * mod)

        self.current_room_content["content"] = boss
        self.current_room_content["type"] = "monster"  # Treat boss as monster for combat

    def generate_treasure_room(self):
        items = []
        gold = random.randint(50, 200) * (self.state.current_level + 1)

        # Number of items based on room depth
        item_count = random.randint(1, 3) + (self.state.current_level // 5)

        for _ in range(item_count):
            item_type = random.choice([ItemType.WEAPON, ItemType.ARMOR,
                                       ItemType.RING, ItemType.AMULET, ItemType.TRINKET])

            # Better loot deeper in dungeon
            rarity_weights = [40, 30, 20, 8, 2, 0]
            if self.state.current_level >= 3:
                rarity_weights = [20, 30, 30, 15, 4, 1]

            rarities = list(Rarity)
            rarity = random.choices(rarities, weights=rarity_weights)[0]

            item = generate_item(item_type, rarity, self.state.player.level)
            items.append(item)

        self.current_room_content["content"] = {
            "items": items,
            "gold": gold
        }

    def display_room_content(self):
        if not self.current_room_content:
            return

        content = self.current_room_content

        if content["explored"]:
            print("✅ Room already explored")
            return

        if content["type"] == "monster":
            monster = content["content"]
            print(f"👹 {monster.name} lurks here!")
            print(f"   Level {monster.level} | HP: {monster.hp}/{monster.max_hp}")
        elif content["type"] == "treasure":
            print("💰 A treasure chest gleams in the corner!")
        elif content["type"] == "trap":
            print("⚠️  Something seems dangerous here...")
        elif content["type"] == "empty":
            print("🕸️  The room appears empty...")

    def explore_room(self):
        if not self.current_room_content or self.current_room_content["explored"]:
            print("🚫 Nothing to explore")
            return

        content = self.current_room_content
        content["explored"] = True

        if content["type"] == "treasure":
            self.handle_treasure(content["content"])
        elif content["type"] == "trap":
            self.handle_trap()
        elif content["type"] == "empty":
            self.handle_empty_room()

    def handle_treasure(self, treasure):
        player = self.state.player

        print("💰 You open the treasure chest!")
        print(f"💎 Found {treasure['gold']} gold!")
        player.gold += treasure['gold']
        self.state.total_gold_earned += treasure['gold']

        print("\n🎁 Items found:")
        for item in treasure['items']:
            rarity_colors = {
                "Common": "⚪", "Magic": "🔵", "Rare": "🟣",
                "Epic": "🟡", "Legendary": "🟠", "Mythic": "🔴"
            }
            print(f"  {rarity_colors.get(item.rarity.value, '⚪')} {item.name}")

            if item.name in player.inventory:
                player.inventory[item.name] += 1
            else:
                player.inventory[item.name] = 1

            if not hasattr(player, 'item_objects'):
                player.item_objects = {}
            player.item_objects[item.name] = item

        print("✅ All items added to inventory!")

    def handle_trap(self):
        player = self.state.player
        stats = player.get_total_stats()

        # Agility check
        check = random.randint(1, 20) + (stats["agility"] // 5)
        difficulty = 15

        if check >= difficulty:
            print("🎯 Your agility saves you!")
            gold = random.randint(20, 50)
            player.gold += gold
            print(f"💰 Found {gold} gold!")
        else:
            damage = random.randint(15, 40)
            player.hp = max(0, player.hp - damage)
            self.state.total_damage_taken += damage

            # Apply random debuff
            effects = [
                StatusEffect(StatusEffectType.POISON, 5, 8),
                StatusEffect(StatusEffectType.BLEED, 4, 10),
                StatusEffect(StatusEffectType.WEAKNESS, 6, 10)
            ]

            effect = random.choice(effects)
            player.add_status_effect(effect)

            print(f"💥 Trap triggered! {damage} damage!")
            print(f"🎭 {effect.effect_type.value} applied!")

            if player.hp <= 0:
                self.handle_player_death()

    def handle_empty_room(self):
        # Small chance to find something
        if random.randint(1, 100) <= 30:
            gold = random.randint(10, 30)
            self.state.player.gold += gold
            print(f"🔍 Found {gold} gold in the dust!")
        else:
            print("🕸️  Nothing of interest here.")

    def next_room(self):
        # Check if floor is complete
        if self.state.current_room >= 25:
            if self.state.current_level < 5:
                print("🎉 Floor completed!")
                self.state.current_level += 1
                self.state.current_room = 1

                # Floor completion bonus
                bonus_gold = 100 * self.state.current_level
                self.state.player.gold += bonus_gold
                print(f"💰 Floor bonus: {bonus_gold} gold!")
            else:
                print("🏆 DUNGEON CONQUERED!")

                # Dungeon completion rewards
                rewards = 1000 * (list(DifficultyMode).index(self.state.difficulty) + 1)
                self.state.player.gold += rewards
                self.state.player.exp += rewards

                print(f"💰 Reward: {rewards} gold and experience!")

                self.state.current_location = "town"
                return
        else:
            self.state.current_room += 1

        self.current_room_content = None
        print(f"🚪 Moving to room {self.state.current_room}...")

    def start_combat(self, monster):
        self.combat_state = {
            "monster": monster,
            "player_turn": True,
            "turn_count": 0
        }
        self.state.current_location = "combat"

    def combat_loop(self):
        if not self.combat_state:
            self.state.current_location = "dungeon"
            return

        monster = self.combat_state["monster"]
        player = self.state.player
        self.combat_state["turn_count"] += 1

        print(f"\n⚔️  COMBAT - Turn {self.combat_state['turn_count']}")
        print("=" * 50)

        # Display health bars
        player_hp_bar = self.create_health_bar(player.hp, player.get_total_stats()["hp"])
        monster_hp_bar = self.create_health_bar(monster.hp, monster.max_hp)

        print(f"👤 {player.name}: {player_hp_bar} {player.hp}/{player.get_total_stats()['hp']}")
        print(f"👹 {monster.name}: {monster_hp_bar} {monster.hp}/{monster.max_hp}")

        # Show status effects
        if player.status_effects:
            effects = []
            for effect_type, effect in player.status_effects.items():
                duration_text = f"({effect.duration})" if effect.duration != 999 else ""
                effects.append(f"{effect_type.value}{duration_text}")
            print(f"🎭 You: {', '.join(effects)}")

        if monster.status_effects:
            effects = []
            for effect_type, effect in monster.status_effects.items():
                duration_text = f"({effect.duration})" if effect.duration != 999 else ""
                effects.append(f"{effect_type.value}{duration_text}")
            print(f"🎭 Enemy: {', '.join(effects)}")

        # Show class resources
        if player.class_resources:
            resource_display = []
            for name, resource in player.class_resources.items():
                resource_display.append(f"{resource.name}: {resource.current}/{resource.maximum}")
            print(f"🔋 {' | '.join(resource_display)}")

        if self.combat_state["player_turn"]:
            # Process player status effects
            messages = player.process_status_effects()
            for msg in messages:
                print(msg)

            if player.hp <= 0:
                self.handle_player_death()
                return

            # Check if player can act (redundant with player_combat_turn but ensures consistency)
            if not player.can_act():
                print("😵 You cannot act this turn!")
                self.combat_state["player_turn"] = False
                return

            self.player_combat_turn()
        else:
            self.monster_combat_turn()

    def create_health_bar(self, current, maximum):
        percentage = current / maximum if maximum > 0 else 0
        bar_length = 20
        filled = int(bar_length * percentage)

        if percentage > 0.66:
            color = "🟩"
        elif percentage > 0.33:
            color = "🟨"
        else:
            color = "🟥"

        bar = color * filled + "⬜" * (bar_length - filled)
        return f"[{bar}]"

    def player_combat_turn(self):
        player = self.state.player

        # Check if player can act
        if StatusEffectType.STUNNED in player.status_effects:
            print("\n😵 You are STUNNED and cannot act this turn!")
            print(f"   Stun duration remaining: {player.status_effects[StatusEffectType.STUNNED].duration} turns")
            self.combat_state["player_turn"] = False
            return

        if StatusEffectType.SLEEPING in player.status_effects:
            print("\n😴 You are SLEEPING and cannot act this turn!")
            print(f"   Sleep duration remaining: {player.status_effects[StatusEffectType.SLEEPING].duration} turns")
            print("   ⚠️  Warning: You take double damage while sleeping!")
            self.combat_state["player_turn"] = False
            return

        if StatusEffectType.FREEZE in player.status_effects:
            # Freeze slows but doesn't prevent action
            print("🧊 You are frozen and move slowly...")

        print("\n📋 YOUR TURN:")
        print("1. ⚔️  Attack")
        print("2. 🎯 Use Skill")
        print("3. 🧪 Use Item")
        print("4. 🛡️  Defend")
        print("5. 🏃 Flee")

        choice = input("\nAction: ").strip()

        if choice == "1":
            self.basic_attack()
        elif choice == "2":
            self.use_skill()
        elif choice == "3":
            self.use_combat_item()
        elif choice == "4":
            self.defend()
        elif choice == "5":
            if self.flee_combat():
                return
        else:
            print("Invalid choice!")
            return

        self.combat_state["player_turn"] = False

        # Check victory
        if self.combat_state["monster"].hp <= 0:
            self.victory()

    def basic_attack(self):
        player = self.state.player
        monster = self.combat_state["monster"]
        stats = player.get_total_stats()

        # Check if monster is invisible
        if StatusEffectType.INVISIBLE in monster.status_effects:
            dodge_bonus = monster.status_effects[StatusEffectType.INVISIBLE].power
            if random.randint(1, 100) <= dodge_bonus:
                print(f"⚔️  Your attack misses! {monster.name} is invisible!")
                return

        # Check for confused effect on player
        if StatusEffectType.CONFUSED in player.status_effects:
            miss_chance = player.status_effects[StatusEffectType.CONFUSED].power
            if random.randint(1, 100) <= miss_chance:
                print("😵 You're confused and miss your attack!")
                return

        # Check if monster dodges (based on agility difference and swift status)
        dodge_chance = max(5, monster.agility - stats["agility"])
        if StatusEffectType.SWIFT in monster.status_effects:
            dodge_chance += monster.status_effects[StatusEffectType.SWIFT].power // 2
        if StatusEffectType.SLOWED in player.status_effects:
            dodge_chance += 10

        if random.randint(1, 100) <= dodge_chance:
            print(f"🏃 {monster.name} dodges your attack!")
            return

        # Calculate base damage
        base_damage = stats["attack"] + random.randint(-5, 5)
        damage = max(1, base_damage - monster.defense // 2)

        # Apply crit
        damage, crit = player.calculate_damage(damage)

        # Apply damage
        actual_damage = self.apply_damage_to_monster(damage)

        # Display
        crit_text = " CRITICAL!" if crit else ""
        print(f"⚔️  Attack deals {actual_damage} damage!{crit_text}")

        # Generate focus on crit for Pathfinder
        if crit and player.player_class == PlayerClass.PATHFINDER and "focus" in player.class_resources:
            focus_gain = player.passive_abilities.get("focus_on_crit", 0)
            if focus_gain > 0:
                player.class_resources["focus"].gain(focus_gain)
                print(f"🎯 Critical hit grants {focus_gain} focus!")

        # Update combo
        player.combo_tracker.combo_count += 1
        player.combo_tracker.combo_timer = 3
        player.combo_tracker.combo_damage_multiplier = min(2.0, 1.0 + (player.combo_tracker.combo_count * 0.1))

        # Track stats
        self.state.total_damage_dealt += actual_damage

        # Apply on-hit effects from weapon
        if player.equipment["weapon"] and hasattr(player.equipment["weapon"], 'status_effects_on_hit'):
            for effect in player.equipment["weapon"].status_effects_on_hit:
                # Check proc chance if applicable
                if hasattr(effect, 'proc_chance') and effect.proc_chance > 0:
                    if random.random() > effect.proc_chance:
                        continue
                self.apply_effect_to_monster(copy.deepcopy(effect))

        # Class-specific on-hit effects
        if player.player_class == PlayerClass.SHADOWBLADE:
            poison_chance = player.passive_abilities.get("poison_chance", 0)
            if random.randint(1, 100) <= poison_chance:
                poison = StatusEffect(StatusEffectType.POISON, 3, 5)
                self.apply_effect_to_monster(poison)

        # Check combo achievement
        if player.combo_tracker.combo_count >= 10:
            achievement = self.state.check_achievement("combo", player.combo_tracker.combo_count)
            if achievement:
                print(f"🏆 Achievement: {achievement.name}!")

    def use_skill(self):
        player = self.state.player
        monster = self.combat_state["monster"]

        # Get available skills
        available = []
        for name, skill in player.skills.items():
            if skill.unlocked and skill.is_ready():
                mana_cost = player.get_effective_resource_cost(
                    skill) if skill.resource_type == "mana" else skill.mana_cost
                resource_cost = player.get_effective_resource_cost(
                    skill) if skill.resource_type != "mana" else skill.resource_cost

                can_afford_mana = player.mana >= mana_cost if skill.mana_cost > 0 else True
                can_afford_resource = True

                if skill.resource_type != "mana" and skill.resource_cost > 0:
                    resource = player.class_resources.get(skill.resource_type)
                    can_afford_resource = resource and resource.current >= resource_cost

                if can_afford_mana and can_afford_resource:
                    available.append((name, skill, mana_cost, resource_cost))

        if not available:
            print("🚫 No skills available!")
            return

        print("\n🎯 AVAILABLE SKILLS:")
        for i, (name, skill, mana_cost, resource_cost) in enumerate(available, 1):
            cost_display = f"{mana_cost} MP"
            if skill.resource_type != "mana" and skill.resource_cost > 0:
                cost_display += f" + {resource_cost} {skill.resource_type.title()}"

            print(f"{i}. {name} ({cost_display})")
            print(f"   📖 {skill.description}")
            if skill.elemental_type:
                print(f"   🔥 Element: {skill.elemental_type.title()}")

        choice = input("\nChoose skill (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(available):
                name, skill, mana_cost, resource_cost = available[choice_num - 1]
                self.execute_skill(name, skill, mana_cost, resource_cost)
        except ValueError:
            print("Invalid input!")

    def execute_skill(self, name, skill, mana_cost, resource_cost):
        player = self.state.player
        monster = self.combat_state["monster"]

        # Pay costs
        if skill.mana_cost > 0:
            player.mana -= mana_cost

        if skill.resource_type != "mana" and skill.resource_cost > 0:
            resource = player.class_resources.get(skill.resource_type)
            if resource:
                resource.spend(resource_cost)

        skill.use()  # Set cooldown and gain experience

        # Check for skill level up
        if skill.progression.gain_exp(random.randint(15, 30)):
            print(f"🎉 {name} leveled up! Now level {skill.progression.skill_level}")

            # Check max level achievement
            if skill.progression.skill_level >= 10:
                achievement = self.state.check_achievement("max_skill")
                if achievement:
                    print(f"🏆 Achievement: {achievement.name}!")

        print(f"✨ {name}!")

        # Special handling for Purify skill
        if name == "Purify":
            negative_effects = [
                StatusEffectType.POISON, StatusEffectType.BURN, StatusEffectType.BLEED,
                StatusEffectType.FREEZE, StatusEffectType.SHOCK, StatusEffectType.WEAKNESS,
                StatusEffectType.VULNERABLE, StatusEffectType.SLOWED, StatusEffectType.CONFUSED,
                StatusEffectType.STUNNED, StatusEffectType.SLEEPING, StatusEffectType.CURSED,
                StatusEffectType.MANA_BURN, StatusEffectType.MARKED, StatusEffectType.SOUL_BURN
            ]
            removed = []
            for effect_type in negative_effects:
                if effect_type in player.status_effects:
                    player.remove_status_effect(effect_type)
                    removed.append(effect_type.value)
            if removed:
                print(f"✨ Purified: {', '.join(removed)}!")
            else:
                print("✨ You are already pure!")
            return

        # Check if skill hits (for offensive skills)
        if skill.target_type == "enemy" and skill.damage > 0:
            # Check if target is invisible
            if StatusEffectType.INVISIBLE in monster.status_effects:
                dodge_bonus = monster.status_effects[StatusEffectType.INVISIBLE].power
                if random.randint(1, 100) <= dodge_bonus:
                    print(f"✨ {name} misses! {monster.name} is invisible!")
                    return

            # Check for confused effect
            if StatusEffectType.CONFUSED in player.status_effects:
                miss_chance = player.status_effects[StatusEffectType.CONFUSED].power
                if random.randint(1, 100) <= miss_chance:
                    print(f"😵 You're confused and {name} misses!")
                    return

            # Precision effect guarantees hit
            if StatusEffectType.PRECISION not in player.status_effects:
                # Check dodge for non-precision attacks
                dodge_chance = max(5, monster.agility - player.get_total_stats()["agility"]) // 2
                if StatusEffectType.SWIFT in monster.status_effects:
                    dodge_chance += monster.status_effects[StatusEffectType.SWIFT].power // 3
                if StatusEffectType.SLOWED in player.status_effects:
                    dodge_chance += 10

                if random.randint(1, 100) <= dodge_chance:
                    print(f"🏃 {monster.name} dodges {name}!")
                    return

        # Apply damage
        if skill.damage > 0:
            base_damage = skill.damage + player.get_total_stats()["attack"] // 3
            damage, crit = player.calculate_damage(base_damage, is_skill=True, skill_name=name, skill=skill)

            actual_damage = self.apply_damage_to_monster(damage)

            crit_text = " CRITICAL!" if crit else ""
            print(f"💥 {actual_damage} damage!{crit_text}")

            self.state.total_damage_dealt += actual_damage

            # Generate focus on crit for Pathfinder
            if crit and player.player_class == PlayerClass.PATHFINDER and "focus" in player.class_resources:
                focus_gain = player.passive_abilities.get("focus_on_crit", 0)
                if focus_gain > 0:
                    player.class_resources["focus"].gain(focus_gain)
                    print(f"🎯 Critical hit grants {focus_gain} focus!")

        # Apply healing
        if skill.heal > 0:
            heal_amount = skill.get_effective_value(skill.heal, player.get_total_stats().get(skill.scaling_stat, 0))

            # Apply healing boost from skill tree
            for tree_nodes in player.skill_trees.values():
                for node in tree_nodes:
                    if node.effect == "healing_boost" and node.unlocked:
                        heal_amount = int(heal_amount * 1.2)

            heal = min(heal_amount, player.get_total_stats()["hp"] - player.hp)
            player.hp += heal
            print(f"💚 Healed {heal} HP!")

            # Generate faith for Priestess on heal
            if player.player_class == PlayerClass.PRIESTESS and "faith" in player.class_resources:
                faith_gain = player.passive_abilities.get("faith_on_heal", 0)
                player.class_resources["faith"].gain(faith_gain)

        # Apply buffs
        if skill.buff_type:
            player.buffs[skill.buff_type] = player.buffs.get(skill.buff_type, 0) + skill.buff_value
            print(f"✨ {skill.buff_type} +{skill.buff_value}!")

        # Apply status effects
        for effect in skill.status_effects:
            # Determine target
            negative_types = [
                StatusEffectType.POISON, StatusEffectType.BURN, StatusEffectType.BLEED,
                StatusEffectType.FREEZE, StatusEffectType.SHOCK, StatusEffectType.WEAKNESS,
                StatusEffectType.VULNERABLE, StatusEffectType.SLOWED, StatusEffectType.CONFUSED,
                StatusEffectType.STUNNED, StatusEffectType.SLEEPING, StatusEffectType.CURSED,
                StatusEffectType.MANA_BURN, StatusEffectType.MARKED, StatusEffectType.SOUL_BURN
            ]

            if effect.effect_type in negative_types:
                self.apply_effect_to_monster(copy.deepcopy(effect))
            else:
                player.add_status_effect(copy.deepcopy(effect))
                print(f"✨ {effect.effect_type.value} applied to you!")

        # Check for combo chains
        completed_chains = player.check_combo_chains(name)
        for chain in completed_chains:
            print(f"🔗 COMBO CHAIN COMPLETED!")
            print(f"💥 Bonus damage: {chain.bonus_damage}")

            # Apply bonus damage to last target (monster)
            if chain.bonus_damage > 0:
                bonus_damage = self.apply_damage_to_monster(chain.bonus_damage)
                print(f"💥 Chain deals {bonus_damage} bonus damage!")

            # Apply chain effects
            for effect in chain.bonus_effects:
                if effect.effect_type in [StatusEffectType.POISON, StatusEffectType.BURN,
                                          StatusEffectType.BLEED, StatusEffectType.STUNNED,
                                          StatusEffectType.VULNERABLE, StatusEffectType.MARKED]:
                    self.apply_effect_to_monster(copy.deepcopy(effect))
                else:
                    player.add_status_effect(copy.deepcopy(effect))

        # Update combo tracker
        player.combo_tracker.combo_count += 1
        player.combo_tracker.combo_timer = 3
        player.combo_tracker.combo_damage_multiplier = min(2.0, 1.0 + (player.combo_tracker.combo_count * 0.15))

        # Class-specific resource generation
        if player.player_class == PlayerClass.WIZARD and "arcane_power" in player.class_resources:
            arcane_gain = player.passive_abilities.get("arcane_power_on_cast", 0)
            player.class_resources["arcane_power"].gain(arcane_gain)

        # Rage generation for damage
        if player.player_class == PlayerClass.BARBARIAN and skill.damage > 0 and "rage" in player.class_resources:
            player.class_resources["rage"].gain(10)

    def apply_damage_to_monster(self, damage):
        monster = self.combat_state["monster"]

        # Apply damage modifiers based on monster's status effects
        if StatusEffectType.SLEEPING in monster.status_effects:
            damage = damage * 2
            print("💤 Double damage to sleeping target!")
            # Wake up the target
            del monster.status_effects[StatusEffectType.SLEEPING]
            print("⏰ Target wakes up!")

        if StatusEffectType.MARKED in monster.status_effects:
            mark_bonus = monster.status_effects[StatusEffectType.MARKED].power
            damage = int(damage * (1 + mark_bonus / 100))
            print(f"🎯 Marked target takes {mark_bonus}% extra damage!")

        if StatusEffectType.VULNERABLE in monster.status_effects:
            vuln_bonus = monster.status_effects[StatusEffectType.VULNERABLE].power
            damage = int(damage * (1 + vuln_bonus / 100))

        if StatusEffectType.FORTIFIED in monster.status_effects:
            fort_reduction = monster.status_effects[StatusEffectType.FORTIFIED].power
            damage = max(1, damage - fort_reduction)

        # Check for shield
        if StatusEffectType.SHIELD in monster.status_effects:
            shield = monster.status_effects[StatusEffectType.SHIELD]
            absorbed = min(damage, shield.power)
            damage -= absorbed
            shield.power -= absorbed

            if shield.power <= 0:
                del monster.status_effects[StatusEffectType.SHIELD]
                print("🔮 Shield broken!")
            else:
                print(f"🔮 Shield absorbs {absorbed}!")

        actual_damage = min(monster.hp, damage)
        monster.hp -= actual_damage

        # Apply thorns damage to attacker if applicable
        if StatusEffectType.THORNS in monster.status_effects:
            thorns_damage = monster.status_effects[StatusEffectType.THORNS].power
            self.state.player.hp -= min(thorns_damage, self.state.player.hp)
            print(f"🌹 Thorns reflect {thorns_damage} damage to you!")
            self.state.total_damage_taken += thorns_damage

        return actual_damage

    def apply_effect_to_monster(self, effect):
        monster = self.combat_state["monster"]

        # Check weakness - double effectiveness
        if effect.effect_type in monster.weaknesses:
            print(f"💥 {monster.name} is weak to {effect.effect_type.value}!")
            effect.power = int(effect.power * 1.5)
            effect.duration = int(effect.duration * 1.5)

        # Check resistance
        if effect.effect_type in monster.resistances:
            if random.random() < 0.5:
                print(f"🛡️  {monster.name} resists {effect.effect_type.value}!")
                return
            else:
                print(f"⚠️  {monster.name} partially resists {effect.effect_type.value}!")
                effect.power = int(effect.power * 0.5)
                effect.duration = int(effect.duration * 0.5)

        # Apply effect
        if effect.effect_type not in monster.status_effects:
            monster.status_effects[effect.effect_type] = effect
        else:
            existing = monster.status_effects[effect.effect_type]
            # Refresh duration and stack if applicable
            existing.duration = max(existing.duration, effect.duration)

            # Handle stacking for certain effects
            if effect.effect_type in [StatusEffectType.POISON, StatusEffectType.BURN,
                                      StatusEffectType.BLEED, StatusEffectType.FREEZE]:
                if existing.stacks < existing.max_stacks:
                    existing.stacks += 1
                    existing.power = int(existing.power * 1.2)

        print(f"🎭 {effect.effect_type.value} applied to {monster.name}!")

    def use_combat_item(self):
        player = self.state.player

        # Find consumables
        consumables = []
        for name, qty in player.inventory.items():
            if hasattr(player, 'item_objects') and name in player.item_objects:
                item = player.item_objects[name]
                if item.item_type == ItemType.CONSUMABLE:
                    consumables.append((name, item, qty))

        if not consumables:
            print("🚫 No consumables!")
            return

        print("\n🧪 ITEMS:")
        for i, (name, item, qty) in enumerate(consumables, 1):
            print(f"{i}. {name} x{qty}")
            print(f"   {item.description}")

        choice = input("\nUse item (0 to cancel): ").strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(consumables):
                name, item, _ = consumables[choice_num - 1]
                self.use_consumable(name, item)
        except ValueError:
            print("Invalid input!")

    def use_consumable(self, name, item):
        player = self.state.player

        # Remove from inventory
        player.inventory[name] -= 1
        if player.inventory[name] <= 0:
            del player.inventory[name]

        print(f"🧪 Used {name}!")

        # Apply effects
        if "Health" in name:
            amount = 50 if "Greater" not in name else 150
            heal = min(amount, player.get_total_stats()["hp"] - player.hp)
            player.hp += heal
            print(f"💚 Healed {heal} HP!")

        elif "Mana" in name:
            amount = 50 if "Greater" not in name else 150
            restore = min(amount, player.get_total_stats()["mana"] - player.mana)
            player.mana += restore
            print(f"💙 Restored {restore} MP!")

        # Apply status effects
        for effect in item.status_effects_on_use:
            player.add_status_effect(effect)
            print(f"✨ {effect.effect_type.value} applied!")

    def defend(self):
        player = self.state.player

        # Defensive bonus
        defense = StatusEffect(StatusEffectType.FORTIFIED, 2, 20)
        player.add_status_effect(defense)

        # Small heal
        heal = int(player.get_total_stats()["hp"] * 0.05)
        player.hp = min(player.get_total_stats()["hp"], player.hp + heal)

        # Restore some class resource
        for resource in player.class_resources.values():
            resource.gain(10)

        # Special reload for Gunslinger
        if player.player_class == PlayerClass.GUNSLINGER and "ammo" in player.class_resources:
            reload_amount = player.passive_abilities.get("reload_speed", 2)
            player.class_resources["ammo"].gain(reload_amount)
            print(f"🔫 Reloaded {reload_amount} ammo!")

        print("🛡️  Defensive stance!")
        print(f"💚 Recovered {heal} HP!")

        # 30% chance to cleanse a random debuff
        if random.random() < 0.3:
            negative_effects = [
                StatusEffectType.POISON, StatusEffectType.BURN, StatusEffectType.BLEED,
                StatusEffectType.FREEZE, StatusEffectType.WEAKNESS, StatusEffectType.VULNERABLE,
                StatusEffectType.SLOWED, StatusEffectType.CONFUSED, StatusEffectType.CURSED,
                StatusEffectType.MANA_BURN, StatusEffectType.MARKED, StatusEffectType.SOUL_BURN
            ]

            current_debuffs = []
            for effect_type in negative_effects:
                if effect_type in player.status_effects:
                    current_debuffs.append(effect_type)

            if current_debuffs:
                removed = random.choice(current_debuffs)
                player.remove_status_effect(removed)
                print(f"✨ Defensive focus cleanses {removed.value}!")

    def flee_combat(self):
        player = self.state.player
        monster = self.combat_state["monster"]

        # Can't flee if stunned, sleeping, or frozen
        if StatusEffectType.STUNNED in player.status_effects:
            print("🚫 You can't flee while stunned!")
            return False

        if StatusEffectType.SLEEPING in player.status_effects:
            print("🚫 You can't flee while sleeping!")
            return False

        if StatusEffectType.FREEZE in player.status_effects:
            print("🚫 You're frozen solid and can't flee!")
            return False

        # Flee chance based on agility
        flee_chance = 30 + (player.get_total_stats()["agility"] - monster.agility) * 2

        # Modifiers
        if StatusEffectType.SLOWED in player.status_effects:
            flee_chance -= 20
        if StatusEffectType.SWIFT in player.status_effects:
            flee_chance += player.status_effects[StatusEffectType.SWIFT].power

        flee_chance = max(10, min(90, flee_chance))

        if random.randint(1, 100) <= flee_chance:
            print("🏃 Escaped successfully!")
            self.combat_state = None
            self.state.current_location = "dungeon"
            return True
        else:
            print("🚫 Can't escape!")
            return False

    def monster_combat_turn(self):
        monster = self.combat_state["monster"]
        player = self.state.player

        print(f"\n👹 {monster.name}'s turn!")

        # Process monster status effects
        self.process_monster_effects(monster)

        if monster.hp <= 0:
            self.victory()
            return

        # Check if stunned
        if StatusEffectType.STUNNED in monster.status_effects:
            print(f"😵 {monster.name} is STUNNED and cannot act!")
            self.combat_state["player_turn"] = True
            return

        if StatusEffectType.SLEEPING in monster.status_effects:
            print(f"😴 {monster.name} is SLEEPING and cannot act!")
            self.combat_state["player_turn"] = True
            return

        # Enhanced Monster AI
        hp_percent = monster.hp / monster.max_hp * 100
        player_hp_percent = player.hp / player.get_total_stats()["hp"] * 100

        # Smart skill selection based on situation
        available_skills = []

        # Prioritize healing if low HP
        if hp_percent < 30 and "Heal" in monster.skills and monster.mana >= 10:
            available_skills.append("Heal")

        # Use debuffs if player is strong
        if player_hp_percent > 70:
            debuff_skills = ["Curse", "Poison Bite", "Entangle", "Fear", "Petrify"]
            for skill in monster.skills:
                if skill in debuff_skills and monster.mana >= 10:
                    available_skills.append(skill)

        # Use powerful attacks if player is low
        if player_hp_percent < 40:
            power_skills = ["Death Touch", "Fire Blast", "Hellfire", "Meteor", "Soul Drain"]
            for skill in monster.skills:
                if skill in power_skills and monster.mana >= 10:
                    available_skills.append(skill)

        # Add other available skills
        for skill in monster.skills:
            if skill not in available_skills and monster.mana >= 10:
                available_skills.append(skill)

        # Decide action
        if available_skills and random.random() < 0.7:  # 70% chance to use skill if available
            skill = random.choice(available_skills)
            self.monster_use_skill(skill)
        else:
            # Basic attack
            self.monster_attack()

        self.combat_state["player_turn"] = True

        if player.hp <= 0:
            self.handle_player_death()

    def process_monster_effects(self, monster):
        effects_to_remove = []

        for effect_type, effect in monster.status_effects.items():
            if effect.duration == 999:  # Permanent effect
                continue

            # Process damage effects
            if effect_type == StatusEffectType.POISON:
                damage = effect.power * effect.stacks
                monster.hp -= min(damage, monster.hp)
                print(f"🤢 Poison: {damage} damage (x{effect.stacks})")

            elif effect_type == StatusEffectType.BURN:
                damage = effect.power
                monster.hp -= min(damage, monster.hp)
                print(f"🔥 Burn: {damage} damage")

            elif effect_type == StatusEffectType.BLEED:
                damage = effect.power
                monster.hp -= min(damage, monster.hp)
                print(f"🩸 Bleed: {damage} damage")

            elif effect_type == StatusEffectType.FREEZE:
                damage = effect.power
                monster.hp -= min(damage, monster.hp)
                print(f"🧊 Freeze: {damage} damage and slows!")

            elif effect_type == StatusEffectType.SHOCK:
                damage = effect.power
                monster.hp -= min(damage, monster.hp)
                print(f"⚡ Shock: {damage} damage")

            elif effect_type == StatusEffectType.SOUL_BURN:
                damage = effect.power
                mana_loss = min(effect.power, monster.mana)
                monster.hp -= min(damage, monster.hp)
                monster.mana -= mana_loss
                print(f"👻 Soul burn: {damage} HP and {mana_loss} MP lost!")

            elif effect_type == StatusEffectType.REGENERATION:
                heal = min(effect.power, monster.max_hp - monster.hp)
                monster.hp += heal
                if heal > 0:
                    print(f"💚 {monster.name} regenerates {heal} HP!")

            elif effect_type == StatusEffectType.STUNNED:
                print(f"😵 {monster.name} is stunned!")

            elif effect_type == StatusEffectType.SLEEPING:
                print(f"😴 {monster.name} is sleeping!")

            # Reduce duration
            effect.duration -= 1
            if effect.duration <= 0:
                effects_to_remove.append(effect_type)

        # Remove expired
        for effect_type in effects_to_remove:
            del monster.status_effects[effect_type]
            print(f"✨ {monster.name}'s {effect_type.value} effect wore off!")

    def monster_attack(self):
        monster = self.combat_state["monster"]
        player = self.state.player
        stats = player.get_total_stats()

        # Check if player is invisible
        if StatusEffectType.INVISIBLE in player.status_effects:
            dodge_bonus = player.status_effects[StatusEffectType.INVISIBLE].power
            if random.randint(1, 100) <= dodge_bonus:
                print(f"👻 {monster.name}'s attack misses! You're invisible!")
                return

        # Check for confused effect on monster
        if StatusEffectType.CONFUSED in monster.status_effects:
            miss_chance = monster.status_effects[StatusEffectType.CONFUSED].power
            if random.randint(1, 100) <= miss_chance:
                print(f"😵 {monster.name} is confused and misses!")
                return

        # Calculate damage
        base_damage = monster.attack + random.randint(-3, 3)

        # Apply berserker vulnerability
        if StatusEffectType.BERSERKER in player.status_effects:
            vuln_bonus = player.status_effects[StatusEffectType.BERSERKER].power // 2
            base_damage = int(base_damage * (1 + vuln_bonus / 100))

        # Apply marked vulnerability
        if StatusEffectType.MARKED in player.status_effects:
            mark_bonus = player.status_effects[StatusEffectType.MARKED].power
            base_damage = int(base_damage * (1 + mark_bonus / 100))

        # Apply vulnerable status
        if StatusEffectType.VULNERABLE in player.status_effects:
            vuln_bonus = player.status_effects[StatusEffectType.VULNERABLE].power
            base_damage = int(base_damage * (1 + vuln_bonus / 100))

        damage = max(1, base_damage - stats["defense"] // 2)

        # Apply damage reduction passive (like from Barbarian's Thick Skin)
        damage_reduction = player.passive_abilities.get("damage_reduction", 0)
        if damage_reduction > 0:
            damage = int(damage * (100 - damage_reduction) / 100)

        # Double damage if player is sleeping
        if StatusEffectType.SLEEPING in player.status_effects:
            damage = damage * 2
            print("💤 You take double damage while sleeping!")
            # Wake up
            player.remove_status_effect(StatusEffectType.SLEEPING)
            print("⏰ You wake up!")

        # Apply player shield
        if StatusEffectType.SHIELD in player.status_effects:
            shield = player.status_effects[StatusEffectType.SHIELD]
            absorbed = min(damage, shield.power)
            damage -= absorbed
            shield.power -= absorbed

            if shield.power <= 0:
                player.remove_status_effect(StatusEffectType.SHIELD)
                print("🔮 Your shield breaks!")
            else:
                print(f"🔮 Shield absorbs {absorbed}!")

        # Apply thorns damage
        if StatusEffectType.THORNS in player.status_effects:
            thorns_damage = player.status_effects[StatusEffectType.THORNS].power
            monster.hp -= min(thorns_damage, monster.hp)
            print(f"🌹 Thorns reflect {thorns_damage} damage!")

        # Apply damage
        actual_damage = min(player.hp, damage)
        player.hp -= actual_damage
        self.state.total_damage_taken += actual_damage

        # Generate rage when taking damage for Barbarian
        if player.player_class == PlayerClass.BARBARIAN and "rage" in player.class_resources:
            rage_gain = player.passive_abilities.get("rage_on_damage", 0)
            if rage_gain > 0:
                player.class_resources["rage"].gain(rage_gain + actual_damage // 10)

        # Apply lifesteal
        if StatusEffectType.LIFESTEAL in player.status_effects:
            lifesteal_percent = player.status_effects[StatusEffectType.LIFESTEAL].power
            steal_amount = int(actual_damage * lifesteal_percent / 100)
            player.hp = min(player.get_total_stats()["hp"], player.hp + steal_amount)
            print(f"🧛 Lifesteal: {steal_amount} HP restored!")

        print(f"👹 {monster.name} attacks: {actual_damage} damage!")

    def monster_use_skill(self, skill_name):
        monster = self.combat_state["monster"]
        player = self.state.player

        monster.mana = max(0, monster.mana - 10)
        print(f"💀 {monster.name} uses {skill_name}!")

        # Enhanced monster skills
        damage_reduction = player.passive_abilities.get("damage_reduction", 0)

        if skill_name in ["Strike", "Bite", "Claw"]:
            damage = monster.attack + random.randint(10, 20)
            damage = max(1, damage - player.get_total_stats()["defense"] // 3)
            if damage_reduction > 0:
                damage = int(damage * (100 - damage_reduction) / 100)
            player.hp = max(0, player.hp - damage)
            print(f"💥 {damage} damage!")
            self.state.total_damage_taken += damage

        elif skill_name == "Entangle":
            damage = monster.attack // 2
            player.hp = max(0, player.hp - damage)
            root = StatusEffect(StatusEffectType.STUNNED, 2)
            player.add_status_effect(root)
            print(f"🌿 {damage} damage and you're entangled (stunned)!")
            self.state.total_damage_taken += damage

        elif skill_name == "Poison Bite" or skill_name == "Poison":
            damage = monster.attack // 2
            player.hp = max(0, player.hp - damage)
            poison = StatusEffect(StatusEffectType.POISON, 5, 8 + monster.level // 2)
            player.add_status_effect(poison)
            print(f"💥 {damage} damage and poisoned!")
            self.state.total_damage_taken += damage

        elif skill_name in ["Fire Blast", "Burn", "Hellfire"]:
            damage = monster.attack + random.randint(15, 30)
            player.hp = max(0, player.hp - damage)
            burn = StatusEffect(StatusEffectType.BURN, 4, 10 + monster.level // 2)
            player.add_status_effect(burn)
            print(f"🔥 {damage} fire damage and burning!")
            self.state.total_damage_taken += damage

        elif skill_name == "Freeze" or skill_name == "Crystal Shard":
            damage = monster.attack + random.randint(10, 25)
            player.hp = max(0, player.hp - damage)
            freeze = StatusEffect(StatusEffectType.FREEZE, 3, 8)
            slow = StatusEffect(StatusEffectType.SLOWED, 4, 15)
            player.add_status_effect(freeze)
            player.add_status_effect(slow)
            print(f"🧊 {damage} ice damage! You're frozen and slowed!")
            self.state.total_damage_taken += damage

        elif skill_name == "Stone Skin":
            fortify = StatusEffect(StatusEffectType.FORTIFIED, 5, 20)
            shield = StatusEffect(StatusEffectType.SHIELD, 4, 30)
            if StatusEffectType.FORTIFIED not in monster.status_effects:
                monster.status_effects[StatusEffectType.FORTIFIED] = fortify
            if StatusEffectType.SHIELD not in monster.status_effects:
                monster.status_effects[StatusEffectType.SHIELD] = shield
            print(f"🪨 {monster.name} hardens its skin! Defense and shield increased!")

        elif skill_name == "Curse":
            curse = StatusEffect(StatusEffectType.CURSED, 6, 15)
            weak = StatusEffect(StatusEffectType.WEAKNESS, 5, 10)
            player.add_status_effect(curse)
            player.add_status_effect(weak)
            print("💀 You are cursed! All stats reduced!")

        elif skill_name == "Fear":
            stun = StatusEffect(StatusEffectType.STUNNED, 2)
            confuse = StatusEffect(StatusEffectType.CONFUSED, 4, 25)
            player.add_status_effect(stun)
            player.add_status_effect(confuse)
            print("😱 You are terrified! Stunned and confused!")

        elif skill_name == "Petrify":
            stun = StatusEffect(StatusEffectType.STUNNED, 3)
            slow = StatusEffect(StatusEffectType.SLOWED, 6, 20)
            player.add_status_effect(stun)
            player.add_status_effect(slow)
            print("🗿 You are petrified! Stunned and slowed!")

        elif skill_name == "Life Drain":
            damage = monster.attack + random.randint(15, 30)
            player.hp = max(0, player.hp - damage)
            heal = damage // 2
            monster.hp = min(monster.max_hp, monster.hp + heal)
            print(f"🧛 {damage} damage drained! {monster.name} heals {heal} HP!")
            self.state.total_damage_taken += damage

        elif skill_name == "Heal":
            heal = 30 + monster.level * 2
            monster.hp = min(monster.max_hp, monster.hp + heal)
            print(f"💚 {monster.name} heals {heal} HP!")

        elif skill_name in ["Death Touch", "Soul Drain"]:
            damage = monster.attack + random.randint(20, 40)
            player.hp = max(0, player.hp - damage)
            soul_burn = StatusEffect(StatusEffectType.SOUL_BURN, 3, 10)
            player.add_status_effect(soul_burn)
            print(f"👻 {damage} necrotic damage! Soul burning applied!")
            self.state.total_damage_taken += damage

        elif skill_name == "Meteor":
            damage = monster.attack + random.randint(30, 50)
            player.hp = max(0, player.hp - damage)
            burn = StatusEffect(StatusEffectType.BURN, 6, 15)
            stun = StatusEffect(StatusEffectType.STUNNED, 1)
            player.add_status_effect(burn)
            player.add_status_effect(stun)
            print(f"☄️ {damage} meteor damage! Burned and stunned!")
            self.state.total_damage_taken += damage

        elif skill_name == "Phase Shift":
            invis = StatusEffect(StatusEffectType.INVISIBLE, 3, 75)
            swift = StatusEffect(StatusEffectType.SWIFT, 4, 20)
            if StatusEffectType.INVISIBLE not in monster.status_effects:
                monster.status_effects[StatusEffectType.INVISIBLE] = invis
            if StatusEffectType.SWIFT not in monster.status_effects:
                monster.status_effects[StatusEffectType.SWIFT] = swift
            print(f"👻 {monster.name} phases out of reality! Invisible and swift!")

        elif skill_name == "Infernal Rage":
            berserk = StatusEffect(StatusEffectType.BERSERKER, 5, 30)
            empower = StatusEffect(StatusEffectType.EMPOWERED, 4, 25)
            if StatusEffectType.BERSERKER not in monster.status_effects:
                monster.status_effects[StatusEffectType.BERSERKER] = berserk
            if StatusEffectType.EMPOWERED not in monster.status_effects:
                monster.status_effects[StatusEffectType.EMPOWERED] = empower
            print(f"🔥 {monster.name} enters an infernal rage! Attack greatly increased!")

        else:
            # Generic skill
            damage = monster.attack + random.randint(5, 15)
            player.hp = max(0, player.hp - damage)
            print(f"✨ {damage} damage!")
            self.state.total_damage_taken += damage

    def victory(self):
        monster = self.combat_state["monster"]
        player = self.state.player

        print("\n" + "=" * 50)
        print("🎉 VICTORY!")
        print("=" * 50)

        # Calculate rewards based on difficulty
        difficulty_bonus = {
            DifficultyMode.EASY: 0.5,
            DifficultyMode.NORMAL: 1.0,
            DifficultyMode.HARD: 1.25,
            DifficultyMode.NIGHTMARE: 1.5,
            DifficultyMode.APOCALYPSE: 2.0
        }

        bonus = difficulty_bonus[self.state.difficulty]

        # Base rewards
        exp_reward = int((monster.level * 20 + random.randint(10, 30)) * bonus)
        gold_reward = int((monster.level * 15 + random.randint(20, 50)) * bonus)

        # Rarity bonus
        rarity_multipliers = {
            Rarity.COMMON: 1.0,
            Rarity.MAGIC: 1.5,
            Rarity.RARE: 2.0,
            Rarity.EPIC: 3.0,
            Rarity.LEGENDARY: 5.0,
            Rarity.MYTHIC: 10.0
        }

        rarity_mult = rarity_multipliers[monster.rarity]
        exp_reward = int(exp_reward * rarity_mult)
        gold_reward = int(gold_reward * rarity_mult)

        # Combo bonus
        if player.combo_tracker.combo_count >= 5:
            combo_bonus = int((exp_reward + gold_reward) * 0.2)
            exp_reward += combo_bonus
            gold_reward += combo_bonus
            print(f"🔗 Combo Bonus ({player.combo_tracker.combo_count} hits): +{combo_bonus} rewards!")

        player.exp += exp_reward
        player.gold += gold_reward
        self.state.total_gold_earned += gold_reward
        self.state.total_monsters_killed += 1

        # Grant class resource bonuses
        for resource in player.class_resources.values():
            if resource.name.lower() == "rage" and player.player_class == PlayerClass.BARBARIAN:
                rage_bonus = player.passive_abilities.get("rage_on_kill", 0)
                resource.gain(rage_bonus)
            elif resource.name.lower() == "holy_power" and player.player_class == PlayerClass.CRUSADER:
                holy_bonus = player.passive_abilities.get("holy_power_on_kill", 0)
                resource.gain(holy_bonus)
            elif resource.name.lower() == "faith" and player.player_class == PlayerClass.PRIESTESS:
                # Faith generation might be triggered by healing instead
                pass

        print(f"⭐ +{exp_reward} EXP")
        print(f"💰 +{gold_reward} Gold")

        # Check highest combo achievement
        if player.combo_tracker.combo_count > self.state.highest_combo:
            self.state.highest_combo = player.combo_tracker.combo_count
            achievement = self.state.check_achievement("combo", player.combo_tracker.combo_count)
            if achievement:
                print(f"🏆 Achievement: {achievement.name}!")

        # Level up check
        if player.level_up():
            print("\n🎊 LEVEL UP!")
            print(f"You are now level {player.level}!")

        # Loot drops
        loot_chance = 30 + (monster.rarity.value.__hash__() % 4) * 10
        if monster.boss_tier > 0:
            loot_chance = 100

        if random.randint(1, 100) <= loot_chance:
            loot = self.generate_loot(monster)
            if loot:
                print(f"\n🎁 {monster.name} dropped:")
                print(f"   {loot.name}")

                if loot.name in player.inventory:
                    player.inventory[loot.name] += 1
                else:
                    player.inventory[loot.name] = 1

                if not hasattr(player, 'item_objects'):
                    player.item_objects = {}
                player.item_objects[loot.name] = loot

        # Boss kill timing
        if monster.boss_tier >= 2:
            if self.combat_state["turn_count"] < self.state.fastest_boss_kill:
                self.state.fastest_boss_kill = self.combat_state["turn_count"]
                if self.combat_state["turn_count"] <= 5:
                    achievement = self.state.check_achievement("fast_boss")
                    if achievement:
                        print(f"🏆 Achievement: {achievement.name}!")

        # Clear combat
        self.combat_state = None
        self.state.current_location = "dungeon"

        input("\nPress Enter to continue...")

    def generate_loot(self, monster):
        # Determine loot type and quality based on monster

        if monster.boss_tier >= 2:
            # Bosses always drop good stuff
            item_type = random.choice([ItemType.WEAPON, ItemType.ARMOR,
                                       ItemType.RING, ItemType.AMULET])
            rarities = [Rarity.RARE, Rarity.EPIC, Rarity.LEGENDARY, Rarity.MYTHIC]
            weights = [20, 40, 30, 10]
        else:
            # Regular monsters
            item_type = random.choice([ItemType.WEAPON, ItemType.ARMOR,
                                       ItemType.RING, ItemType.AMULET,
                                       ItemType.TRINKET, ItemType.CONSUMABLE])

            rarities = list(Rarity)
            base_weights = [40, 30, 20, 8, 2, 0]

            # Better loot from rarer monsters
            if monster.rarity in [Rarity.LEGENDARY, Rarity.MYTHIC]:
                base_weights = [10, 20, 30, 25, 10, 5]
            elif monster.rarity in [Rarity.RARE, Rarity.EPIC]:
                base_weights = [20, 30, 30, 15, 5, 0]

            weights = base_weights

        rarity = random.choices(rarities, weights=weights)[0]

        return generate_item(item_type, rarity, monster.level)

    def handle_player_death(self):
        player = self.state.player

        print("\n" + "=" * 50)
        print("💀 YOU HAVE DIED")
        print("=" * 50)

        # Death penalty
        gold_loss = player.gold // 4
        exp_loss = player.exp // 10

        player.gold = max(0, player.gold - gold_loss)
        player.exp = max(0, player.exp - exp_loss)

        print(f"💸 Lost {gold_loss} gold")
        print(f"⭐ Lost {exp_loss} experience")

        # Check for Phoenix Feather
        if "Phoenix Feather" in player.inventory:
            print("\n🔥 PHOENIX FEATHER ACTIVATES!")
            player.inventory["Phoenix Feather"] -= 1
            if player.inventory["Phoenix Feather"] <= 0:
                del player.inventory["Phoenix Feather"]

            # Revive with full HP
            player.hp = player.get_total_stats()["hp"]
            player.mana = player.get_total_stats()["mana"]

            # Restore class resources
            for resource in player.class_resources.values():
                resource.current = resource.maximum

            print("🔥 You rise from the ashes!")
            print("💖 Full HP and Mana restored!")

            # Continue combat if in combat
            if self.combat_state:
                self.combat_state["player_turn"] = True
            return

        # Normal death - return to town
        player.hp = player.get_total_stats()["hp"] // 4
        player.mana = 0

        # Restore some class resources
        for resource in player.class_resources.values():
            resource.current = resource.maximum // 4

        # Clear all status effects
        player.status_effects.clear()
        player.buffs.clear()
        player.debuffs.clear()

        print("\n🏥 You wake up in the town temple...")
        print("💤 You feel weak but alive...")

        # Return to town
        self.combat_state = None
        self.current_room_content = None
        self.state.current_location = "town"

        input("\nPress Enter to continue...")


def main():
    print("=" * 60)
    print("🎮 EPIC RPG ADVENTURE - ENHANCED EDITION 🎮")
    print("=" * 60)
    print("\nPreparing your adventure...")
    print("🔥 New Features: Dynamic Skill System, Skill Trees, Evolution!")
    print("🎯 Class Resources, Enhanced Combos, and Much More!")
    print()

    game = RPGGame()

    try:
        game.start_game()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing!")
        print("Your adventure will be waiting for your return...")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please restart the game.")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()