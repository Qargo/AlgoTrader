#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 12:24:48 2021

@author: srdjan
agent module: contains the Agent class.
"""

# add FinRL-Library path
import sys

sys.path.append("./FinRL-Library")

from finrl.model.models import DRLAgent, MODELS

class Agent(DRLAgent):
    """Agent class (extends DRLAgent)"""
    def __init__(self, env):
        """Create an Agent with the given environment"""
        super().__init__(env)

    @staticmethod
    def load_model(model_name, path):
        """Static method to load a saved model"""
        if model_name not in MODELS:
            raise NotImplementedError()
        model = MODELS[model_name].load(path)
        return model

    def save_model(self, model, path):
        """Save a model with the given path"""
        model.save(path)

