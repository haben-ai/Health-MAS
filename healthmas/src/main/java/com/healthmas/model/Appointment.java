package com.healthmas.model;

public class Appointment {
    private final String appointmentId;
    private final Patient patient;
    private final DoctorSlot slot;

    public Appointment(String appointmentId, Patient patient, DoctorSlot slot) {
        this.appointmentId = appointmentId;
        this.patient = patient;
        this.slot = slot;
    }

    public String getAppointmentId() { return appointmentId; }
    public Patient getPatient() { return patient; }
    public DoctorSlot getSlot() { return slot; }

    public String toAclString() {
        return appointmentId + "|" + patient.toAclString() + "|" + slot.getSlotId() + "|" + slot.getDoctorName() + "|" + slot.getDateTime();
    }

    public static Appointment fromAclString(String s, DoctorSlot slot) {
        String[] p = s.split("\\|", 2);
        String appointmentId = p[0];
        String[] rest = p[1].split("\\|", -1);
        StringBuilder patientAcl = new StringBuilder();
        for (int i = 0; i < 6; i++) {
            if (i > 0) patientAcl.append("|");
            patientAcl.append(rest[i]);
        }
        Patient patient = Patient.fromAclString(patientAcl.toString());
        return new Appointment(appointmentId, patient, slot);
    }

    @Override public String toString() {
        return "Appointment{id=" + appointmentId + ", patient=" + patient.getName() + ", slot=" + slot.getSlotId() + ", doctor=" + slot.getDoctorName() + ", time=" + slot.getDateTime() + "}";
    }
}
