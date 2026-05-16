package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Patient;
public class EscalateGoal implements Goal {
    private final Patient patient;
    private final String patientAgentAID;
    public EscalateGoal(Patient patient, String patientAgentAID) { this.patient = patient; this.patientAgentAID = patientAgentAID; }
    public Patient getPatient() { return patient; }
    public String getPatientAgentAID() { return patientAgentAID; }
    @Override public String getName() { return "EscalateGoal[" + patient.getName() + "]"; }
}
