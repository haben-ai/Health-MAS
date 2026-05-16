package com.healthmas.model;

public class DoctorSlot {
    private final String slotId;
    private final String doctorName;
    private final String specialty;
    private final String dateTime;
    private boolean available;
    private Patient bookedPatient;

    public DoctorSlot(String slotId, String doctorName, String specialty, String dateTime) {
        this.slotId = slotId;
        this.doctorName = doctorName;
        this.specialty = specialty;
        this.dateTime = dateTime;
        this.available = true;
    }

    public String getSlotId() { return slotId; }
    public String getDoctorName() { return doctorName; }
    public String getSpecialty() { return specialty; }
    public String getDateTime() { return dateTime; }
    public boolean isAvailable() { return available; }
    public Patient getBookedPatient() { return bookedPatient; }

    public void book(Patient patient) { this.available = false; this.bookedPatient = patient; }
    public void free() { this.available = true; this.bookedPatient = null; }

    @Override public String toString() {
        return "DoctorSlot{id=" + slotId + ", doctor=" + doctorName + ", specialty=" + specialty + ", time=" + dateTime + ", available=" + available + "}";
    }
}
