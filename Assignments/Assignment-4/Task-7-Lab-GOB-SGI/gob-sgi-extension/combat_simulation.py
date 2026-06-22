"""
Combat Simulation using Goal Oriented Behaviour (SGI)

Two AI-controlled NPCs fight each other in turn-based combat.
Each NPC uses Simple Goal Insistence (SGI) to choose actions:
- Attack: Want to damage opponent
- Survive: Want to heal when damaged

This demonstrates SGI's decision-making in a game context.

Created for COS30002 AI for Games, Lab
"""

from gob_oo import Goal, Action, Agent

VERBOSE = True


class CombatAction(Action):
    """
    Combat action with effects on self and combat effects (damage/heal).

    Effects: goal changes for self (SGI as usual)
    Damage: HP removed from opponent
    Heal: HP restored to self
    """

    def __init__(self, name: str, effects: dict, damage: int = 0, heal: int = 0):
        """
        Args:
            name: Action name (e.g., 'Sword Slash')
            effects: Goal changes for self (e.g., {'Attack': -5})
            damage: HP damage dealt to opponent (default 0)
            heal: HP restored to self (default 0)
        """
        super().__init__(name, effects)
        self.damage = damage
        self.heal = heal

    def __repr__(self):
        return f"CombatAction('{self.name}', effects={self.effects}, damage={self.damage}, heal={self.heal})"


class CombatAgent(Agent):
    """
    An agent with HP and combat capabilities.

    Extends Agent with:
    - HP (current and max)
    - Combat methods (take_damage, heal_hp)
    - Dynamic goal updates (Survive goal based on HP)
    """

    def __init__(self, name: str, hp: int, goals: list, actions: list):
        """
        Args:
            name: Agent identifier
            hp: Initial HP (also max HP)
            goals: List of Goal objects
            actions: List of CombatAction objects
        """
        super().__init__(name, goals, actions)
        self.hp = hp
        self.max_hp = hp

    def is_alive(self) -> bool:
        """Check if agent is still alive."""
        return self.hp > 0

    def take_damage(self, amount: int):
        """Reduce HP by amount, minimum 0."""
        self.hp = max(self.hp - amount, 0)

    def heal_hp(self, amount: int):
        """Restore HP by amount, maximum max_hp."""
        self.hp = min(self.hp + amount, self.max_hp)

    def update_goals(self):
        """
        Refresh goals based on current combat state.

        - Survive goal = max_hp - hp (more damage = more urgent to heal)
        - Attack goal increases by 2 (keeps agent wanting to attack)
        """
        for goal in self.goals:
            if goal.name == 'Survive':
                # More damage taken = higher Survive insistence
                goal.value = self.max_hp - self.hp
            elif goal.name == 'Attack':
                # Gradually increase attack urge each turn
                goal.value += 2

    def get_status(self) -> str:
        """Return formatted HP status."""
        return f"{self.name} HP: {self.hp}/{self.max_hp}"


class Combat:
    """
    Manages turn-based combat between two CombatAgents using SGI.
    """

    def __init__(self, agent_a: CombatAgent, agent_b: CombatAgent):
        """
        Args:
            agent_a: First combatant
            agent_b: Second combatant
        """
        self.agents = [agent_a, agent_b]  # [0] = attacker, [1] = defender per turn
        self.turn = 0

    def print_header(self):
        """Print combat setup."""
        print("\n" + "=" * 50)
        print("COMBAT START: SGI-Based Turn-Based Battle")
        print("=" * 50)
        for agent in self.agents:
            print(f"\n{agent.name} (HP: {agent.max_hp})")
            print(f"  Goals: {', '.join(f'{g.name}' for g in agent.goals)}")
            print(f"  Actions:")
            for action in agent.actions:
                action_str = f"    - {action.name}: effects={action.effects}"
                if action.damage > 0:
                    action_str += f", damage={action.damage}"
                if action.heal > 0:
                    action_str += f", heal={action.heal}"
                print(action_str)
        print("\n" + "-" * 50)

    def apply_combat_action(self, attacker: CombatAgent, defender: CombatAgent, action: CombatAction):
        """
        Execute a combat action.

        Args:
            attacker: Agent taking the action
            defender: Agent receiving the effects
            action: CombatAction to apply
        """
        # Apply goal effects to attacker
        attacker.apply_action(action)

        # Apply combat effects
        if action.damage > 0:
            defender.take_damage(action.damage)

        if action.heal > 0:
            attacker.heal_hp(action.heal)

        # Print action result
        result = f"[{attacker.name}] chooses {action.name}"
        if action.damage > 0:
            result += f" -> deals {action.damage} damage to {defender.name}"
        if action.heal > 0:
            result += f" -> heals {action.heal} HP"
        print(result)

    def print_status(self):
        """Print current status of both agents."""
        status = " | ".join(agent.get_status() for agent in self.agents)
        print(f"Status: {status}")

    def run(self):
        """Run combat simulation until one agent dies."""
        self.print_header()

        while all(agent.is_alive() for agent in self.agents):
            self.turn += 1
            print(f"\n--- Turn {self.turn} ---")

            for agent in self.agents:
                # Update goals based on current HP
                agent.update_goals()

                # Print agent's state
                goals_str = ', '.join(f"{g.name}={g.value}" for g in agent.goals)
                print(f"[{agent.name}] Goals: {goals_str}")

                # Use SGI to choose action
                action = agent.choose_action()

                # Determine opponent
                opponent = self.agents[1] if agent == self.agents[0] else self.agents[0]

                # Apply action
                self.apply_combat_action(agent, opponent, action)

            # Print turn summary
            self.print_status()

        # Determine and announce winner
        print("\n" + "=" * 50)
        winner = next(agent for agent in self.agents if agent.is_alive())
        loser = next(agent for agent in self.agents if not agent.is_alive())
        print(f"COMBAT END: {winner.name} WINS after {self.turn} turns!")
        print(f"{winner.name}: {winner.hp}/{winner.max_hp} HP")
        print(f"{loser.name}: {loser.hp}/{loser.max_hp} HP (Defeated)")
        print("=" * 50 + "\n")


def main():
    """Set up and run the combat simulation."""

    # Create Hero
    hero_goals = [
        Goal('Attack', 8),
        Goal('Survive', 0),
    ]
    hero_actions = [
        CombatAction('Sword Slash', {'Attack': -5}, damage=6, heal=0),
        CombatAction('Power Strike', {'Attack': -9}, damage=10, heal=0),
        CombatAction('Heal Potion', {'Survive': -6}, damage=0, heal=8),
    ]
    hero = CombatAgent('Hero', hp=30, goals=hero_goals, actions=hero_actions)

    # Create Villain
    villain_goals = [
        Goal('Attack', 8),
        Goal('Survive', 0),
    ]
    villain_actions = [
        CombatAction('Dark Strike', {'Attack': -5}, damage=7, heal=0),
        CombatAction('Drain Life', {'Attack': -3}, damage=4, heal=3),
        CombatAction('Shadow Heal', {'Survive': -6}, damage=0, heal=7),
    ]
    villain = CombatAgent('Villain', hp=25, goals=villain_goals, actions=villain_actions)

    # Run combat
    combat = Combat(hero, villain)
    combat.run()


if __name__ == '__main__':
    main()
