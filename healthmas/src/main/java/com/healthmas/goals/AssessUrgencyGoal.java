package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Patient;
public class AssessUrgencyGoal implements Goal {
    private final Patient patient;
    private final String replyToAID;
    public AssessUrgencyGoal(Patient patient, String replyToAID) { this.patient = patient; this.replyToAID = replyToAID; }
    public Patient getPatient() { return patient; }
    public String getReplyToAID() { return replyToAID; }
    @Override public String getName() { return "AssessUrgencyGoal[" + patient.getName() + "]"; }
}
