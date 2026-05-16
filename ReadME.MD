# HealthMAS — Minimal Project Configuration Guide

A decentralized **Multi-Agent System (MAS)** engineered in Java using the **JADE framework** that implements a custom manual **Belief-Desire-Intention (BDI)** reasoning engine to optimize patient triage scheduling.

## 📂 Project Architecture Quick Look

```text
healthmas/
├── pom.xml                 # Maven dependency tracking and compiler settings
├── lib/
│   └── jade.jar            # JADE 4.6 Runtime Core Binary
└── src/main/java/com/healthmas/
    ├── bdi/                # Manual BDI Layer (BDIAgent, BeliefBase, Goal, Plan)
    ├── model/              # Entities (Patient, DoctorSlot, Appointment)
    ├── util/               # Backend Core (ScheduleDB, UrgencyEvaluator)
    ├── goals/              # BDI System Motivations
    ├── agents/             # JADE Lifecycle Threads (Patient, Triage, Scheduler, Negotiator)
    └── scenario/           # Executable Validation Scenarios (Scenario 1 & 2 Launcher)