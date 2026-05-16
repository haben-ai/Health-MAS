package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.DoctorSlot;
import com.healthmas.model.Patient;
public class BookAppointmentGoal implements Goal {
    private final Patient patient;
    private final DoctorSlot slot;
    private final String patientAgentAID;
    public BookAppointmentGoal(Patient patient, DoctorSlot slot, String patientAgentAID) { this.patient = patient; this.slot = slot; this.patientAgentAID = patientAgentAID; }
    public Patient getPatient() { return patient; }
    public DoctorSlot getSlot() { return slot; }
    public String getPatientAgentAID() { return patientAgentAID; }
    @Override public String getName() { return "BookAppointmentGoal[" + patient.getName() + "]"; }
}
