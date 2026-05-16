package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Appointment;
public class ConfirmAppointmentGoal implements Goal {
    private final Appointment appointment;
    public ConfirmAppointmentGoal(Appointment appointment) { this.appointment = appointment; }
    public Appointment getAppointment() { return appointment; }
    @Override public String getName() { return "ConfirmAppointmentGoal[" + appointment.getAppointmentId() + "]"; }
}
