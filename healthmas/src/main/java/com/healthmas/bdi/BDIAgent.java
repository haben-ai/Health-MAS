package com.healthmas.bdi;

import jade.core.Agent;
import jade.core.behaviours.OneShotBehaviour;
import java.util.ArrayList;
import java.util.List;

public abstract class BDIAgent extends Agent {
    protected final BeliefBase beliefBase = new BeliefBase();
    protected final List<Plan> planLibrary = new ArrayList<>();
    protected final List<Goal> activeGoals = new ArrayList<>();

    @Override
    protected void setup() {
        initBeliefs();
        initPlans();
    }

    protected abstract void initBeliefs();
    protected abstract void initPlans();

    public void addGoal(Goal goal) {
        activeGoals.add(goal);
        System.out.println("[" + getLocalName() + "] Goal added: " + goal.getName());
        for (Plan plan : planLibrary) {
            if (plan.isApplicable(goal)) {
                System.out.println("[" + getLocalName() + "] Executing plan: " + plan.getName());
                addBehaviour(new OneShotBehaviour() {
                    @Override public void action() {
                        plan.execute(goal, beliefBase);
                        activeGoals.remove(goal);
                    }
                });
                return;
            }
        }
        System.out.println("[" + getLocalName() + "] WARNING: No plan found for goal: " + goal.getName());
    }
}
