"""
werr.py
Root forwarder module for WERR Decision Engine.
Allows direct import of werr from the root workspace directory.
"""
import os
import sys

_WERRENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "werrengine"))
if _WERRENGINE_DIR not in sys.path:
    sys.path.insert(0, _WERRENGINE_DIR)

from werrengine.werr import (
    WerrEngine,
    WevvEngine,
    JevWireAdapter,
    DynamicCalibration,
    AutoSeedRouter,
    DomainGate,
    DOMAIN_GATES,
    APISecurityGate,
    FinancialRiskGate,
    IoTSafetyGate,
    EcommerceFraudGate,
    GameCombatGate,
    NoulQuestion,
    ChoiceQuestion,
    ScoreQuestion,
    NoulAnswer,
    ChoiceAnswer,
    ScoreAnswer,
    WerrResponse,
    WevvResponse,
    create_security_guard,
    create_smart_router,
    create_risk_evaluator,
)

__version__ = "0.5.0"
