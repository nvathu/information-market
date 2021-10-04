import copy
from abc import ABC, abstractmethod

from navigation import Target


class InformationStrategy(ABC):
    @abstractmethod
    def should_combine(self, my_target: Target, other_target: Target):
        """Whether a robot's target information should be replaced/combined with another"""

    @abstractmethod
    def combine(self, my_target: Target, other_target: Target, bots_distance) -> Target:
        """Combine a robot's target information with other information"""


class BetterAgeStrategy(InformationStrategy):
    def should_combine(self, my_target: Target, other_target: Target):
        """Whether a robot's target information should be replaced/combined with another"""
        if other_target.is_known() and my_target.age > other_target.age:
            return True
        return False

    def combine(self, my_target: Target, other_target: Target, bots_distance) -> Target:
        """Combine a robot's target information with other information"""
        new_target = copy.deepcopy(other_target)
        new_target.set_distance(new_target.get_distance() + bots_distance)
        return new_target


class WeightedAverageAgeStrategy(InformationStrategy):
    def should_combine(self, my_target: Target, other_target: Target):
        """Whether a robot's target information should be replaced/combined with another"""
        if other_target.known and my_target.age > other_target.age:
            return True
        return False

    def combine(self, my_target: Target, other_target: Target, bots_distance) -> Target:
        """Combine a robot's target information with other information"""
        new_target = copy.deepcopy(other_target)
        ages_sum = my_target.age + other_target.age
        new_distance = (my_target.age / ages_sum) * other_target.get_distance() + (
                new_target.age / ages_sum) * my_target.get_distance() + bots_distance  # older = lower weight
        if not my_target.is_known():
            new_distance = other_target.get_distance() + bots_distance
        new_target.set_distance(new_distance)
        return new_target


class QualityStrategy(InformationStrategy):
    def __init__(self, initial_quality):
        self.initial_quality = initial_quality

    def should_combine(self, my_target: Target, other_target: Target):
        """Whether a robot's target information should be replaced/combined with another"""
        if other_target.is_known() and (my_target.quality < other_target.quality):
            return True
        return False

    def combine(self, my_target: Target, other_target: Target, bots_distance) -> Target:
        """Combine a robot's target information with other information"""
        new_target = copy.deepcopy(other_target)
        new_target.set_distance(new_target.get_distance() + bots_distance)
        new_target.quality = self.initial_quality
        return new_target


class DecayingQualityStrategy(InformationStrategy):

    def should_combine(self, my_target: Target, other_target: Target):
        """Whether a robot's target information should be replaced/combined with another"""
        if other_target.is_known() and other_target.decaying_quality > my_target.decaying_quality:
            return True
        return False

    def combine(self, my_target: Target, other_target: Target, bots_distance) -> Target:
        """Combine a robot's target information with other information"""
        new_target = copy.deepcopy(other_target)
        new_target.set_distance(new_target.get_distance() + bots_distance)
        return new_target
