package com.healthmas.util;

public final class MsgOntology {
    private MsgOntology() {}
    public static final String TRIAGE_REQUEST = "TRIAGE-REQUEST";
    public static final String TRIAGE_RESULT = "TRIAGE-RESULT";
    public static final String NEGOTIATE_REQUEST = "NEGOTIATE-REQUEST";
    public static final String NEGOTIATE_RESULT = "NEGOTIATE-RESULT";
    public static final String APPOINTMENT_CONFIRM = "APPOINTMENT-CONFIRM";
    public static final String RESCHEDULE_NOTIFY = "RESCHEDULE-NOTIFY";

    public static final String TRIAGE_AGENT = "TriageAgent";
    public static final String SCHEDULER_AGENT = "SchedulerAgent";
    public static final String NEGOTIATOR_AGENT = "NegotiatorAgent";
}
