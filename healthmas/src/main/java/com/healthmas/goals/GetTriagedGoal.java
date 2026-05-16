package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Patient;
public class GetTriagedGoal implements Goal {
    private final Patient patient;
    public GetTriagedGoal(Patient patient) { this.patient = patient; }
    public Patient getPatient() { return patient; }
    @Override public String getName() { return "GetTriagedGoal[" + patient.getName() + "]"; }
}
