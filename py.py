import os

# Define the project structure and contents based on the HealthMAS specifications
project_files = {
    # Maven Project Object Model
    "healthmas/pom.xml": """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.healthmas</groupId>
    <artifactId>healthmas</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    <name>HealthMAS - Intelligent Healthcare Appointment Scheduling</name>

    <properties>
        <maven.compiler.release>17</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.tilab.jade</groupId>
            <artifactId>jade</artifactId>
            <version>4.6.0</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <release>17</release>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.5.0</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals><goal>shade</goal></goals>
                        <configuration>
                            <transformers>
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <mainClass>com.healthmas.scenario.Scenario1Launcher</mainClass>
                                </transformer>
                            </transformers>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
""",

    # Manual BDI Framework Core Architecture
    "healthmas/src/main/java/com/healthmas/bdi/Goal.java": """package com.healthmas.bdi;

public interface Goal {
    String getName();
}
""",

    "healthmas/src/main/java/com/healthmas/bdi/BeliefBase.java": """package com.healthmas.bdi;

import java.util.LinkedHashMap;
import java.util.Map;

public class BeliefBase {
    private final Map<String, Object> beliefs = new LinkedHashMap<>();

    public void set(String name, Object value) { beliefs.put(name, value); }
    public Object get(String name) { return beliefs.get(name); }
    public Object getOrDefault(String name, Object def) { return beliefs.getOrDefault(name, def); }
    public boolean has(String name) { return beliefs.containsKey(name); }
    public void remove(String name) { beliefs.remove(name); }

    public void print(String agentName) {
        System.out.println("[" + agentName + "] BeliefBase:");
        beliefs.forEach((k, v) -> System.out.println("  " + k + " = " + v));
    }
}
""",

    "healthmas/src/main/java/com/healthmas/bdi/Plan.java": """package com.healthmas.bdi;

public abstract class Plan {
    public abstract String getName();
    public abstract boolean isApplicable(Goal goal);
    public abstract void execute(Goal goal, BeliefBase beliefs);
}
""",

    "healthmas/src/main/java/com/healthmas/bdi/BDIAgent.java": """package com.healthmas.bdi;

import jade.core.Agent;
import jade.core.behaviours.OneShotBehaviour;
import java.util.ArrayList;
import java.util.List;

public abstract class BDIAgent extends Agent {
    protected final BeliefBase beliefBase = new BeliefBase();
    protected final List<Plan> planLibrary = new ArrayList<>();
    protected final List<Goal> activeGoals = new ArrayList<>();

    @Override
    protected void setup() {
        initBeliefs();
        initPlans();
    }

    protected abstract void initBeliefs();
    protected abstract void initPlans();

    public void addGoal(Goal goal) {
        activeGoals.add(goal);
        System.out.println("[" + getLocalName() + "] Goal added: " + goal.getName());
        for (Plan plan : planLibrary) {
            if (plan.isApplicable(goal)) {
                System.out.println("[" + getLocalName() + "] Executing plan: " + plan.getName());
                addBehaviour(new OneShotBehaviour() {
                    @Override public void action() {
                        plan.execute(goal, beliefBase);
                        activeGoals.remove(goal);
                    }
                });
                return;
            }
        }
        System.out.println("[" + getLocalName() + "] WARNING: No plan found for goal: " + goal.getName());
    }
}
""",

    # Domain Models Layer
    "healthmas/src/main/java/com/healthmas/model/UrgencyLevel.java": """package com.healthmas.model;

public enum UrgencyLevel {
    CRITICAL(4), HIGH(3), MEDIUM(2), LOW(1);

    private final int priority;
    UrgencyLevel(int priority) { this.priority = priority; }
    public int getPriority() { return priority; }
    public boolean isMoreUrgentThan(UrgencyLevel other) { return this.priority > other.priority; }
}
""",

    "healthmas/src/main/java/com/healthmas/model/Patient.java": """package com.healthmas.model;

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
        String[] p = s.split("\\\|", -1);
        Patient patient = new Patient(p[0], p[1], p[2], p[3]);
        patient.setUrgencyScore(Integer.parseInt(p[4]));
        if (!p[5].equals("null")) patient.setUrgencyLevel(UrgencyLevel.valueOf(p[5]));
        return patient;
    }

    @Override public String toString() {
        return "Patient{id=" + patientId + ", name=" + name + ", urgency=" + urgencyLevel + "(" + urgencyScore + ")}";
    }
}
""",

    "healthmas/src/main/java/com/healthmas/model/DoctorSlot.java": """package com.healthmas.model;

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
""",

    "healthmas/src/main/java/com/healthmas/model/Appointment.java": """package com.healthmas.model;

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
        String[] p = s.split("\\\|", 2);
        String appointmentId = p[0];
        String[] rest = p[1].split("\\\|", -1);
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
""",

    # Utilities Layers
    "healthmas/src/main/java/com/healthmas/util/MsgOntology.java": """package com.healthmas.util;

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
""",

    "healthmas/src/main/java/com/healthmas/util/UrgencyEvaluator.java": """package com.healthmas.util;

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
""",

    "healthmas/src/main/java/com/healthmas/util/ScheduleDB.java": """package com.healthmas.util;

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
""",

    # BDI Goals
    "healthmas/src/main/java/com/healthmas/goals/GetTriagedGoal.java": """package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Patient;
public class GetTriagedGoal implements Goal {
    private final Patient patient;
    public GetTriagedGoal(Patient patient) { this.patient = patient; }
    public Patient getPatient() { return patient; }
    @Override public String getName() { return "GetTriagedGoal[" + patient.getName() + "]"; }
}
""",

    "healthmas/src/main/java/com/healthmas/goals/AssessUrgencyGoal.java": """package com.healthmas.goals;
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
""",

    "healthmas/src/main/java/com/healthmas/goals/FindSlotGoal.java": """package com.healthmas.goals;
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
""",

    "healthmas/src/main/java/com/healthmas/goals/BookAppointmentGoal.java": """package com.healthmas.goals;
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
""",

    "healthmas/src/main/java/com/healthmas/goals/EscalateGoal.java": """package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Patient;
public class EscalateGoal implements Goal {
    private final Patient patient;
    private final String patientAgentAID;
    public EscalateGoal(Patient patient, String patientAgentAID) { this.patient = patient; this.patientAgentAID = patientAgentAID; }
    public Patient getPatient() { return patient; }
    public String getPatientAgentAID() { return patientAgentAID; }
    @Override public String getName() { return "EscalateGoal[" + patient.getName() + "]"; }
}
""",

    "healthmas/src/main/java/com/healthmas/goals/ResolveConflictGoal.java": """package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Patient;
public class ResolveConflictGoal implements Goal {
    private final Patient urgentPatient;
    private final String schedulerAID;
    public ResolveConflictGoal(Patient urgentPatient, String schedulerAID) { this.urgentPatient = urgentPatient; this.schedulerAID = schedulerAID; }
    public Patient getUrgentPatient() { return urgentPatient; }
    public String getSchedulerAID() { return schedulerAID; }
    @Override public String getName() { return "ResolveConflictGoal[" + urgentPatient.getName() + "]"; }
}
""",

    "healthmas/src/main/java/com/healthmas/goals/ConfirmAppointmentGoal.java": """package com.healthmas.goals;
import com.healthmas.bdi.Goal;
import com.healthmas.model.Appointment;
public class ConfirmAppointmentGoal implements Goal {
    private final Appointment appointment;
    public ConfirmAppointmentGoal(Appointment appointment) { this.appointment = appointment; }
    public Appointment getAppointment() { return appointment; }
    @Override public String getName() { return "ConfirmAppointmentGoal[" + appointment.getAppointmentId() + "]"; }
}
""",

    # Multi-Agent System Core Interfaces
    "healthmas/src/main/java/com/healthmas/agents/PatientAgent.java": """package com.healthmas.agents;

import com.healthmas.bdi.*;
import com.healthmas.goals.*;
import com.healthmas.model.*;
import com.healthmas.util.MsgOntology;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class PatientAgent extends BDIAgent {
    private Patient patient;

    @Override
    protected void setup() {
        Object[] args = getArguments();
        if (args != null && args.length > 0) {
            patient = (Patient) args[0];
        } else {
            patient = new Patient("P000", "Default Patient", "headache", "GP");
        }
        super.setup();

        beliefBase.set("patient", patient);
        beliefBase.set("status", "waiting");

        addBehaviour(new ConfirmationReceiverBehaviour());
        addBehaviour(new RescheduleNotifyReceiverBehaviour());

        if (patient.getUrgencyScore() == 0) {
            addGoal(new GetTriagedGoal(patient));
        }
        System.out.println("[" + getLocalName() + "] Started for patient: " + patient);
    }

    @Override protected void initBeliefs() {}

    @Override
    protected void initPlans() {
        planLibrary.add(new Plan() {
            @Override public String getName() { return "SendToTriagePlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof GetTriagedGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                Patient p = ((GetTriagedGoal) goal).getPatient();
                ACLMessage msg = new ACLMessage(ACLMessage.REQUEST);
                msg.addReceiver(new jade.core.AID(MsgOntology.TRIAGE_AGENT, jade.core.AID.ISLOCALNAME));
                msg.setOntology(MsgOntology.TRIAGE_REQUEST);
                msg.setContent(p.toAclString());
                send(msg);
            }
        });

        planLibrary.add(new Plan() {
            @Override public String getName() { return "HandleConfirmationPlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof ConfirmAppointmentGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                Appointment appt = ((ConfirmAppointmentGoal) goal).getAppointment();
                beliefs.set("appointment", appt);
                beliefs.set("status", "confirmed");
                System.out.println("[" + getLocalName() + "] * APPOINTMENT CONFIRMED: " + appt);
            }
        });
    }

    private class ConfirmationReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.CONFIRM), MessageTemplate.MatchOntology(MsgOntology.APPOINTMENT_CONFIRM));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                String content = msg.getContent();
                String[] parts = content.split("\\\|", -1);
                DoctorSlot slot = new DoctorSlot(parts[7], parts[8], "?", parts[9]);
                Appointment appt = Appointment.fromAclString(content, slot);
                addGoal(new ConfirmAppointmentGoal(appt));
            } else block();
        }
    }

    private class RescheduleNotifyReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.MatchOntology(MsgOntology.RESCHEDULE_NOTIFY);
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                System.out.println("[" + myAgent.getLocalName() + "] ! RESCHEDULE NOTICE: " + msg.getContent());
                beliefBase.set("status", "rescheduled");
            } else block();
        }
    }
}
""",

    "healthmas/src/main/java/com/healthmas/agents/TriageAgent.java": """package com.healthmas.agents;

import com.healthmas.bdi.*;
import com.healthmas.goals.*;
import com.healthmas.model.Patient;
import com.healthmas.util.*;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class TriageAgent extends BDIAgent {
    @Override
    protected void setup() {
        super.setup();
        addBehaviour(new TriageRequestReceiverBehaviour());
        System.out.println("[" + getLocalName() + "] Triage agent ready.");
    }

    @Override protected void initBeliefs() { beliefBase.set("triageCount", 0); }

    @Override
    protected void initPlans() {
        planLibrary.add(new Plan() {
            @Override public String getName() { return "EvaluateAndForwardPlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof AssessUrgencyGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                AssessUrgencyGoal g = (AssessUrgencyGoal) goal;
                Patient patient = g.getPatient();
                int score = UrgencyEvaluator.evaluate(patient);
                beliefs.set("triageCount", (int) beliefs.get("triageCount") + 1);

                System.out.println("[" + getLocalName() + "] Triaged " + patient.getName() + " -> level=" + patient.getUrgencyLevel());
                ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
                reply.addReceiver(new AID(MsgOntology.SCHEDULER_AGENT, AID.ISLOCALNAME));
                reply.setOntology(MsgOntology.TRIAGE_RESULT);
                reply.setContent(patient.toAclString() + "||" + g.getReplyToAID());
                send(reply);
            }
        });
    }

    private class TriageRequestReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.REQUEST), MessageTemplate.MatchOntology(MsgOntology.TRIAGE_REQUEST));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                addGoal(new AssessUrgencyGoal(Patient.fromAclString(msg.getContent()), msg.getSender().getLocalName()));
            } else block();
        }
    }
}
""",

    "healthmas/src/main/java/com/healthmas/agents/SchedulerAgent.java": """package com.healthmas.agents;

import com.healthmas.bdi.*;
import com.healthmas.goals.*;
import com.healthmas.model.*;
import com.healthmas.util.*;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;

public class SchedulerAgent extends BDIAgent {
    private final AtomicInteger apptCounter = new AtomicInteger(1000);

    @Override
    protected void setup() {
        super.setup();
        addBehaviour(new TriageResultReceiverBehaviour());
        addBehaviour(new NegotiateResultReceiverBehaviour());
        System.out.println("[" + getLocalName() + "] Scheduler agent ready.");
    }

    @Override protected void initBeliefs() { beliefBase.set("appointmentsBooked", 0); }

    @Override
    protected void initPlans() {
        planLibrary.add(new Plan() {
            @Override public String getName() { return "FindSlotPlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof FindSlotGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                FindSlotGoal g = (FindSlotGoal) goal; Patient p = g.getPatient();
                Optional<DoctorSlot> slotOpt = ScheduleDB.getInstance().findAvailableSlot(p.getRequiredSpecialty());
                if (slotOpt.isPresent()) {
                    addGoal(new BookAppointmentGoal(p, slotOpt.get(), g.getReplyToAgentAID()));
                } else {
                    addGoal(new EscalateGoal(p, g.getReplyToAgentAID()));
                }
            }
        });

        planLibrary.add(new Plan() {
            @Override public String getName() { return "DirectBookPlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof BookAppointmentGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                BookAppointmentGoal g = (BookAppointmentGoal) goal;
                boolean booked = ScheduleDB.getInstance().bookSlot(g.getSlot().getSlotId(), g.getPatient());
                if (!booked) return;

                Appointment appt = new Appointment("APPT-" + apptCounter.getAndIncrement(), g.getPatient(), g.getSlot());
                ACLMessage confirm = new ACLMessage(ACLMessage.CONFIRM);
                confirm.addReceiver(new AID(g.getPatientAgentAID(), AID.ISLOCALNAME));
                confirm.setOntology(MsgOntology.APPOINTMENT_CONFIRM);
                confirm.setContent(appt.toAclString());
                send(confirm);
            }
        });

        planLibrary.add(new Plan() {
            @Override public String getName() { return "EscalatePlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof EscalateGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                EscalateGoal g = (EscalateGoal) goal;
                beliefs.set("pendingPatientAgentAID", g.getPatientAgentAID());
                ACLMessage negotiate = new ACLMessage(ACLMessage.REQUEST);
                negotiate.addReceiver(new AID(MsgOntology.NEGOTIATOR_AGENT, AID.ISLOCALNAME));
                negotiate.setOntology(MsgOntology.NEGOTIATE_REQUEST);
                negotiate.setContent(g.getPatient().toAclString() + "||" + getLocalName());
                send(negotiate);
            }
        });
    }

    private class TriageResultReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM), MessageTemplate.MatchOntology(MsgOntology.TRIAGE_RESULT));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                String[] parts = msg.getContent().split("\\\\|\\\\|", 2);
                addGoal(new FindSlotGoal(Patient.fromAclString(parts[0]), parts[1]));
            } else block();
        }
    }

    private class NegotiateResultReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM), MessageTemplate.MatchOntology(MsgOntology.NEGOTIATE_RESULT));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                String[] parts = msg.getContent().split("\\\\|\\\\|", 2);
                String patAID = (String) beliefBase.getOrDefault("pendingPatientAgentAID", "PatientAgent");
                ScheduleDB.getInstance().getSlot(parts[1]).ifPresent(slot -> addGoal(new BookAppointmentGoal(Patient.fromAclString(parts[0]), slot, patAID)));
            } else block();
        }
    }
}
""",

    "healthmas/src/main/java/com/healthmas/agents/NegotiatorAgent.java": """package com.healthmas.agents;

import com.healthmas.bdi.*;
import com.healthmas.goals.*;
import com.healthmas.model.*;
import com.healthmas.util.*;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;

public class NegotiatorAgent extends BDIAgent {
    @Override
    protected void setup() {
        super.setup();
        addBehaviour(new NegotiateRequestReceiverBehaviour());
        System.out.println("[" + getLocalName() + "] Negotiator agent ready.");
    }

    @Override protected void initBeliefs() {}

    @Override
    protected void initPlans() {
        planLibrary.add(new Plan() {
            @Override public String getName() { return "RankAndReschedulePlan"; }
            @Override public boolean isApplicable(Goal goal) { return goal instanceof ResolveConflictGoal; }
            @Override public void execute(Goal goal, BeliefBase beliefs) {
                ResolveConflictGoal g = (ResolveConflictGoal) goal;
                Patient urgent = g.getUrgentPatient();

                List<DoctorSlot> booked = ScheduleDB.getInstance().findReschedulableSlotsForSpecialty(urgent.getRequiredSpecialty());
                Optional<DoctorSlot> targetSlotOpt = booked.stream().filter(s -> s.getBookedPatient() != null).min(Comparator.comparingInt(s -> s.getBookedPatient().getUrgencyScore()));

                if (targetSlotOpt.isEmpty()) return;
                DoctorSlot targetSlot = targetSlotOpt.get();
                Patient displaced = targetSlot.getBookedPatient();

                if (!urgent.getUrgencyLevel().isMoreUrgentThan(displaced.getUrgencyLevel())) return;

                System.out.println("[" + getLocalName() + "] Preempting booking! Displacing: " + displaced.getName() + " for Urgent Intake: " + urgent.getName());
                ScheduleDB.getInstance().freeSlot(targetSlot.getSlotId());

                ACLMessage notice = new ACLMessage(ACLMessage.INFORM);
                notice.addReceiver(new AID(displaced.getPatientId(), AID.ISLOCALNAME));
                notice.setOntology(MsgOntology.RESCHEDULE_NOTIFY);
                notice.setContent("Your booking has been bumped down due to an emergency. Alternate allocations will follow.");
                send(notice);

                ACLMessage result = new ACLMessage(ACLMessage.INFORM);
                result.addReceiver(new AID(g.getSchedulerAID(), AID.ISLOCALNAME));
                result.setOntology(MsgOntology.NEGOTIATE_RESULT);
                result.setContent(urgent.toAclString() + "||" + targetSlot.getSlotId());
                send(result);
            }
        });
    }

    private class NegotiateRequestReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.REQUEST), MessageTemplate.MatchOntology(MsgOntology.NEGOTIATE_REQUEST));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                String[] parts = msg.getContent().split("\\\\|\\\\|", 2);
                addGoal(new ResolveConflictGoal(Patient.fromAclString(parts[0]), parts[1]));
            } else block();
        }
    }
}
""",

    # Execution Scenario Launchers
    "healthmas/src/main/java/com/healthmas/scenario/Scenario1Launcher.java": """package com.healthmas.scenario;

import com.healthmas.agents.*;
import com.healthmas.model.Patient;
import com.healthmas.util.ScheduleDB;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.AgentContainer;

public class Scenario1Launcher {
    public static void main(String[] args) throws Exception {
        System.out.println("=== Running HealthMAS Scenario 1 ===");
        ScheduleDB.getInstance().seedNormalSchedule();

        Runtime rt = Runtime.instance();
        Profile p = new ProfileImpl();
        p.setParameter(Profile.MAIN_HOST, "localhost");
        p.setParameter(Profile.GUI, "true");
        AgentContainer container = rt.createMainContainer(p);

        container.createNewAgent("TriageAgent", TriageAgent.class.getName(), null).start();
        container.createNewAgent("SchedulerAgent", SchedulerAgent.class.getName(), null).start();
        container.createNewAgent("NegotiatorAgent", NegotiatorAgent.class.getName(), null).start();

        Thread.sleep(300);
        Patient john = new Patient("P001", "John Doe", "headache and dizziness", "GP");
        container.createNewAgent("PatientAgent-P001", PatientAgent.class.getName(), new Object[]{john}).start();
    }
}
""",

    "healthmas/src/main/java/com/healthmas/scenario/Scenario2Launcher.java": """package com.healthmas.scenario;

import com.healthmas.agents.*;
import com.healthmas.model.*;
import com.healthmas.util.ScheduleDB;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.AgentContainer;

public class Scenario2Launcher {
    public static void main(String[] args) throws Exception {
        System.out.println("=== Running HealthMAS Scenario 2 ===");
        ScheduleDB.getInstance().seedFullyBookedCardiologist();

        Runtime rt = Runtime.instance();
        Profile p = new ProfileImpl();
        p.setParameter(Profile.MAIN_HOST, "localhost");
        p.setParameter(Profile.GUI, "true");
        AgentContainer container = rt.createMainContainer(p);

        container.createNewAgent("TriageAgent", TriageAgent.class.getName(), null).start();
        container.createNewAgent("SchedulerAgent", SchedulerAgent.class.getName(), null).start();
        container.createNewAgent("NegotiatorAgent", NegotiatorAgent.class.getName(), null).start();

        Thread.sleep(300);
        Patient alice = new Patient("P-LOW1", "Alice Brown", "mild fatigue", "Cardiology");
        alice.setUrgencyScore(2); alice.setUrgencyLevel(UrgencyLevel.LOW);
        container.createNewAgent("P-LOW1", PatientAgent.class.getName(), new Object[]{alice}).start();

        Patient bob = new Patient("P-LOW2", "Bob Wilson", "routine check", "Cardiology");
        bob.setUrgencyScore(2); bob.setUrgencyLevel(UrgencyLevel.LOW);
        container.createNewAgent("P-LOW2", PatientAgent.class.getName(), new Object[]{bob}).start();

        Thread.sleep(300);
        Patient fatima = new Patient("P002", "Fatima Al-Hassan", "chest pain and difficulty breathing", "Cardiology");
        container.createNewAgent("PatientAgent-P002", PatientAgent.class.getName(), new Object[]{fatima}).start();
    }
}
"""
}

# Generate directories and write individual source files to system disk
print("Initializing Local Project Generator for HealthMAS...")
for path, content in project_files.items():
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Created: {path}")

# Explicitly build an empty lib directory for the user's manual framework inclusion
lib_dir = "healthmas/lib"
if not os.path.exists(lib_dir):
    os.makedirs(lib_dir)

print("\\n[SUCCESS] Project structures built entirely inside the 'healthmas/' folder!")
print("Drop your 'jade.jar' dependency directly into 'healthmas/lib/' to run.")