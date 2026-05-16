package com.healthmas.model;

public class Patient {
    private final String patientId;
    private final String name;
    private final String symptoms;
    private final String requiredSpecialty;
    private int urgencyScore;
    private UrgencyLevel urgencyLevel;

    public Patient(String patientId, String name, String symptoms, String requiredSpecialty) {
        this.patientId = patientId;
        this.name = name;
        this.symptoms = symptoms;
        this.requiredSpecialty = requiredSpecialty;
    }

    public String getPatientId() { return patientId; }
    public String getName() { return name; }
    public String getSymptoms() { return symptoms; }
    public String getRequiredSpecialty() { return requiredSpecialty; }
    public int getUrgencyScore() { return urgencyScore; }
    public UrgencyLevel getUrgencyLevel() { return urgencyLevel; }

    public void setUrgencyScore(int score) { this.urgencyScore = score; }
    public void setUrgencyLevel(UrgencyLevel level) { this.urgencyLevel = level; }

    public String toAclString() {
        return patientId + "|" + name + "|" + symptoms + "|" + requiredSpecialty + "|" + urgencyScore + "|" + (urgencyLevel != null ? urgencyLevel.name() : "null");
    }

    public static Patient fromAclString(String s) {
        String[] p = s.split("\\|", -1);
        Patient patient = new Patient(p[0], p[1], p[2], p[3]);
        patient.setUrgencyScore(Integer.parseInt(p[4]));
        if (!p[5].equals("null")) patient.setUrgencyLevel(UrgencyLevel.valueOf(p[5]));
        return patient;
    }

    @Override public String toString() {
        return "Patient{id=" + patientId + ", name=" + name + ", urgency=" + urgencyLevel + "(" + urgencyScore + ")}";
    }
}
