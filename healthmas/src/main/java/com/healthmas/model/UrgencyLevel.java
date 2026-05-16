package com.healthmas.model;

public enum UrgencyLevel {
    CRITICAL(4), HIGH(3), MEDIUM(2), LOW(1);

    private final int priority;
    UrgencyLevel(int priority) { this.priority = priority; }
    public int getPriority() { return priority; }
    public boolean isMoreUrgentThan(UrgencyLevel other) { return this.priority > other.priority; }
}
