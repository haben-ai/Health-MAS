package com.healthmas.util;

import com.healthmas.model.Patient;
import com.healthmas.model.UrgencyLevel;

public final class UrgencyEvaluator {
    private UrgencyEvaluator() {}

    public static int evaluate(Patient patient) {
        String symptoms = patient.getSymptoms().toLowerCase();
        int score = 1;

        if (symptoms.contains("chest pain") || symptoms.contains("heart attack") || symptoms.contains("stroke") || symptoms.contains("unconscious") || symptoms.contains("severe bleeding") || symptoms.contains("not breathing")) {
            score = 9;
        } else if (symptoms.contains("high fever") || symptoms.contains("fracture") || symptoms.contains("broken bone") || symptoms.contains("severe pain") || symptoms.contains("difficulty breathing") || symptoms.contains("allergic reaction")) {
            score = 7;
        } else if (symptoms.contains("moderate pain") || symptoms.contains("infection") || symptoms.contains("nausea") || symptoms.contains("headache") || symptoms.contains("dizziness") || symptoms.contains("sprain")) {
            score = 5;
        } else {
            score = 2;
        }

        patient.setUrgencyScore(score);
        patient.setUrgencyLevel(scoreToLevel(score));
        return score;
    }

    private static UrgencyLevel scoreToLevel(int score) {
        if (score >= 8) return UrgencyLevel.CRITICAL;
        if (score >= 6) return UrgencyLevel.HIGH;
        if (score >= 4) return UrgencyLevel.MEDIUM;
        return UrgencyLevel.LOW;
    }
}
