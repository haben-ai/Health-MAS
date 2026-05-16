package com.healthmas.bdi;

public abstract class Plan {
    public abstract String getName();
    public abstract boolean isApplicable(Goal goal);
    public abstract void execute(Goal goal, BeliefBase beliefs);
}
