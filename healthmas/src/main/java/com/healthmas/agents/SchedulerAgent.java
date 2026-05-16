package com.healthmas.agents;

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
                String[] parts = msg.getContent().split("\\|\\|", 2);
                addGoal(new FindSlotGoal(Patient.fromAclString(parts[0]), parts[1]));
            } else block();
        }
    }

    private class NegotiateResultReceiverBehaviour extends CyclicBehaviour {
        private final MessageTemplate MT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM), MessageTemplate.MatchOntology(MsgOntology.NEGOTIATE_RESULT));
        @Override public void action() {
            ACLMessage msg = myAgent.receive(MT);
            if (msg != null) {
                String[] parts = msg.getContent().split("\\|\\|", 2);
                String patAID = (String) beliefBase.getOrDefault("pendingPatientAgentAID", "PatientAgent");
                ScheduleDB.getInstance().getSlot(parts[1]).ifPresent(slot -> addGoal(new BookAppointmentGoal(Patient.fromAclString(parts[0]), slot, patAID)));
            } else block();
        }
    }
}
