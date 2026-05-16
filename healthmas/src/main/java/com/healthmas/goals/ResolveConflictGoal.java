package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Patient;
public class ResolveConflictGoal implements Goal {
    private final Patient urgentPatient;
    private final String schedulerAID;
    public ResolveConflictGoal(Patient urgentPatient, String schedulerAID) { this.urgentPatient = urgentPatient; this.schedulerAID = schedulerAID; }
    public Patient getUrgentPatient() { return urgentPatient; }
    public String getSchedulerAID() { return schedulerAID; }
    @Override public String getName() { return "ResolveConflictGoal[" + urgentPatient.getName() + "]"; }
}
