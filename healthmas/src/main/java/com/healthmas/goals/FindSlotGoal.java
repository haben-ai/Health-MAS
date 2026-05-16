package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Patient;
public class FindSlotGoal implements Goal {
    private final Patient patient;
    private final String replyToAgentAID;
    public FindSlotGoal(Patient patient, String replyToAgentAID) { this.patient = patient; this.replyToAgentAID = replyToAgentAID; }
    public Patient getPatient() { return patient; }
    public String getReplyToAgentAID() { return replyToAgentAID; }
    @Override public String getName() { return "FindSlotGoal[" + patient.getName() + "]"; }
}
