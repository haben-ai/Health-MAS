package com.healthmas.util;

import com.healthmas.model.DoctorSlot;
import com.healthmas.model.Patient;
import com.healthmas.model.UrgencyLevel;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class ScheduleDB {
    private static ScheduleDB instance;
    private final Map<String, DoctorSlot> slots = new ConcurrentHashMap<>();

    private ScheduleDB() {}

    public static synchronized ScheduleDB getInstance() {
        if (instance == null) instance = new ScheduleDB();
        return instance;
    }

    public void seedNormalSchedule() {
        slots.clear();
        addSlot(new DoctorSlot("GP-001", "Dr. Smith", "GP", "Mon 09:00"));
        addSlot(new DoctorSlot("GP-002", "Dr. Smith", "GP", "Mon 10:00"));
        addSlot(new DoctorSlot("GP-003", "Dr. Patel", "GP", "Mon 11:00"));
        addSlot(new DoctorSlot("CARD-001", "Dr. Jones", "Cardiology", "Mon 14:00"));
        addSlot(new DoctorSlot("CARD-002", "Dr. Jones", "Cardiology", "Mon 15:00"));
    }

    public void seedFullyBookedCardiologist() {
        slots.clear();
        addSlot(new DoctorSlot("GP-001", "Dr. Smith", "GP", "Mon 09:00"));
        DoctorSlot card1 = new DoctorSlot("CARD-001", "Dr. Jones", "Cardiology", "Mon 14:00");
        DoctorSlot card2 = new DoctorSlot("CARD-002", "Dr. Jones", "Cardiology", "Mon 15:00");

        Patient low1 = new Patient("P-LOW1", "Alice Brown", "mild fatigue", "Cardiology");
        Patient low2 = new Patient("P-LOW2", "Bob Wilson", "routine check", "Cardiology");
        low1.setUrgencyScore(2); low1.setUrgencyLevel(UrgencyLevel.LOW);
        low2.setUrgencyScore(2); low2.setUrgencyLevel(UrgencyLevel.LOW);
        card1.book(low1); card2.book(low2);

        slots.put(card1.getSlotId(), card1);
        slots.put(card2.getSlotId(), card2);
    }

    private void addSlot(DoctorSlot slot) { slots.put(slot.getSlotId(), slot); }

    public Optional<DoctorSlot> findAvailableSlot(String specialty) {
        return slots.values().stream().filter(s -> s.getSpecialty().equalsIgnoreCase(specialty) && s.isAvailable()).findFirst();
    }

    public List<DoctorSlot> findReschedulableSlotsForSpecialty(String specialty) {
        List<DoctorSlot> result = new ArrayList<>();
        for (DoctorSlot s : slots.values()) {
            if (s.getSpecialty().equalsIgnoreCase(specialty) && !s.isAvailable()) result.add(s);
        }
        return result;
    }

    public boolean bookSlot(String slotId, Patient patient) {
        DoctorSlot slot = slots.get(slotId);
        if (slot != null && slot.isAvailable()) { slot.book(patient); return true; }
        return false;
    }

    public boolean freeSlot(String slotId) {
        DoctorSlot slot = slots.get(slotId);
        if (slot != null) { slot.free(); return true; }
        return false;
    }

    public Optional<DoctorSlot> getSlot(String slotId) { return Optional.ofNullable(slots.get(slotId)); }
}
